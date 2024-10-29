"""Periodic tasks module."""
import contextlib
import random
from logging import getLogger

from telegram.constants import ParseMode

from rgb_ln_telegram_bot.exceptions import AllocationsAlreadyAvailable
from rgb_ln_telegram_bot.ln import (
    asset_balance,
    btc_balance,
    create_utxos,
    get_invoice_status,
)

from . import msgs
from . import settings as sett
from .database import Purchase, PurchaseStatus

LOGGER = getLogger(__name__)


async def node_checks(context):
    """Perform node checks.

    Notify the developers if the node is finishing the assets.
    Try to create more UTXOs.
    """
    balance = asset_balance()
    if balance["future"] < sett.MIN_ASSET_BALANCE:
        msg = "Asset balance under minimum acceptable"
        LOGGER.warning(msg)
        if sett.DEVELOPER_CHAT_ID:
            await context.bot.send_message(chat_id=sett.DEVELOPER_CHAT_ID, text=msg)
    with contextlib.suppress(AllocationsAlreadyAvailable):
        create_utxos()
        LOGGER.info("Created UTXOs")
    sat_balance = btc_balance()
    if sat_balance["vanilla"]["future"] < sett.MIN_BTC_BALANCE:
        msg = "BTC balance under minimum acceptable"
        LOGGER.warning(msg)
        if sett.DEVELOPER_CHAT_ID:
            await context.bot.send_message(chat_id=sett.DEVELOPER_CHAT_ID, text=msg)


async def get_invoice_check_task(context):
    """Handle pending purchases that changed status.

    If the invoice is paid or expired notify the user, otherwise notify the
    developers.
    """
    LOGGER.debug("Checking invoice status updates...")
    with sett.Session() as session:
        purchases = (
            session.query(Purchase).filter_by(status=PurchaseStatus.PENDING).all()
        )
        LOGGER.debug("Found %d pending purchases", len(purchases))

        for purchase in purchases:
            invoice = purchase.invoice
            LOGGER.info("Getting status for invoice %s", invoice)
            status = get_invoice_status(invoice).lower()
            if status == "pending":
                continue
            if status == "succeeded":
                LOGGER.debug("Invoice %s has been paid", purchase.invoice)
                await context.bot.send_message(
                    chat_id=purchase.chat_id,
                    text=msgs.INVOICE_PAID,
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
                sticker = random.choice(sett.STICKERS)
                await context.bot.send_sticker(purchase.chat_id, sticker)
                purchase.status = PurchaseStatus.DELIVERED
                session.commit()
            elif status == "expired":
                await context.bot.send_message(
                    chat_id=purchase.chat_id,
                    text=msgs.INVOICE_EXPIRED,
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
                purchase.status = PurchaseStatus.EXPIRED
                session.commit()
            else:
                msg = f"Invoice in unexpected status: {status}"
                LOGGER.error(msg)
                if sett.DEVELOPER_CHAT_ID:
                    await context.bot.send_message(
                        chat_id=sett.DEVELOPER_CHAT_ID, text=msg
                    )
                purchase.status = PurchaseStatus.FAILED
                session.commit()
