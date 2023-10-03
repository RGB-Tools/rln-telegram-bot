"""Bot handlers module."""
import datetime
import time
from functools import wraps
from logging import getLogger

import rgb_lib
import sqlalchemy as sa
from telegram.constants import ParseMode

from rgb_ln_telegram_bot.exceptions import (
    InvalidTransportEndpoints,
    RecipientIDAlreadyUsed,
)
from rgb_ln_telegram_bot.ln import get_invoice, refresh_transfers, send_asset

from . import msgs
from . import settings as sett
from .database import Purchase, PurchaseStatus, SendRequest, SendRequestStatus, User

LOGGER = getLogger(__name__)


def _track_time(func):
    """Log the time spent on a handler."""

    @wraps(func)
    async def _wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        LOGGER.debug("%s ran in %0.3fs", func.__name__, round(end - start, 3))
        return result

    return _wrapper


def _reply(update, msg):
    """Send a telegram message in markdown, disabling web page previews."""
    return update.message.reply_text(
        msg, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True
    )


def _get_user(update, session):
    """Return the user from the DB, adding it if it isn't already there."""
    user_id = update.effective_user.id
    user = session.query(User).filter_by(user_id=user_id).first()
    if user is None:
        user = User(user_id=user_id)
        session.add(user)
        session.commit()
    return user


async def help_handler(update, _context):
    """Handle the /help command."""
    await _reply(update, msgs.HELP())


async def unknown_command_handler(update, _context):
    """Handle an unknown command."""
    await _reply(update, msgs.UNKNOWN_COMMAND)


async def node_command_help_handler(update, _context):
    """Handle the /nodecommandhelp command."""
    await _reply(update, msgs.NODECOMMANDHELP())


async def get_node_info_handler(update, _context):
    """Handle the /getnodeinfo command."""
    await _reply(update, msgs.GET_NODE_INFO())


async def start_handler(update, _context):
    """Handle the /start command."""
    with sett.Session() as session:
        _get_user(update, session)
    await _reply(update, msgs.START)


@_track_time
async def get_asset_handler(update, _context):
    """Handle the /getasset command."""
    now = datetime.datetime.now()
    time_24hours_ago = now - datetime.timedelta(days=1)
    with sett.Session() as session:
        user = _get_user(update, session)
        successful_interactions = (
            session.query(SendRequest)
            .where(
                sa.and_(
                    SendRequest.user_idx == user.idx,
                    SendRequest.timestamp > time_24hours_ago,
                    SendRequest.status == SendRequestStatus.SUCCESS,
                )
            )
            .order_by(SendRequest.timestamp)
        )
        if successful_interactions.count() >= sett.MAX_SUCCESSFUL_INTERACTIONS_PER_DAY:
            next_request_time = (
                successful_interactions.first().timestamp + datetime.timedelta(days=1)
            )
            when = "today"
            if now.weekday() != next_request_time.weekday():
                when = "tomorrow"
            nrt = f"{when} after {next_request_time.strftime('%H:%M:%S')}"
            return await _reply(
                update,
                msgs.TOO_MANY_ASSET_REQUESTS.format(next_request_time=nrt),
            )

        pending_request = (
            session.query(SendRequest)
            .filter_by(
                user_idx=user.idx,
                status=SendRequestStatus.PENDING,
            )
            .count()
        )
        if not pending_request:
            session.add(SendRequest(user_idx=user.idx))
            session.commit()
        await _reply(update, msgs.ASK_RGB_INVOICE)


@_track_time
async def msg_handler(update, _context):
    """Handle messages that are not commands.

    If the user has a pending SendRequest check if the message is a valid RGB
    invoice and, if so, try to send assets to it.
    """
    with sett.Session() as session:
        user = _get_user(update, session)

        pending_request = (
            session.query(SendRequest)
            .where(
                sa.and_(
                    SendRequest.user_idx == user.idx,
                    sa.or_(
                        SendRequest.status == SendRequestStatus.PENDING,
                        SendRequest.status
                        == SendRequestStatus.RGB_INVOICE_ALREADY_USED,
                    ),
                )
            )
            .order_by(sa.desc(SendRequest.timestamp))
            .first()
        )
        if not pending_request:
            return

        if not update.message.text:
            return
        rgb_invoice = update.message.text.strip()

        rgb_invoice_already_used = (
            session.query(SendRequest)
            .where(
                sa.and_(
                    SendRequest.rgb_invoice == rgb_invoice,
                    sa.or_(
                        SendRequest.status == SendRequestStatus.SUCCESS,
                        SendRequest.status
                        == SendRequestStatus.RGB_INVOICE_ALREADY_USED,
                    ),
                )
            )
            .count()
        )
        if rgb_invoice_already_used:
            return await _reply(update, msgs.RGB_INVOICE_ALREADY_USED)

        if pending_request.status == SendRequestStatus.RGB_INVOICE_ALREADY_USED:
            pending_request = SendRequest(user_idx=user.idx)
            session.add(pending_request)
            session.commit()

        try:
            invoice_data = rgb_lib.Invoice(rgb_invoice).invoice_data()
            blinded_utxo = invoice_data.recipient_id
            transport_endpoints = invoice_data.transport_endpoints
        except rgb_lib.RgbLibError.InvalidInvoice:
            return await _reply(update, msgs.INVALID_RGB_INVOICE)

        pending_request.rgb_invoice = rgb_invoice
        await _reply(update, msgs.SENDING_ASSET())

        LOGGER.info("Sending to %s for user %s", rgb_invoice, user.user_id)
        try:
            txid = send_asset(blinded_utxo, transport_endpoints)
            pending_request.status = SendRequestStatus.SUCCESS
            pending_request.txid = txid
            session.commit()
            await _reply(update, msgs.ASSET_SENT().format(txid=txid))
            refresh_transfers()
        except InvalidTransportEndpoints:
            LOGGER.warning(
                "Send failed because RGB invoice has invalid transport endpoints"
            )
            await _reply(update, msgs.INVALID_RGB_TRANSPORT_ENDPOINTS)
        except RecipientIDAlreadyUsed:
            LOGGER.warning("Send failed because RGB invoice has already been used")
            pending_request.status = SendRequestStatus.RGB_INVOICE_ALREADY_USED
            session.commit()
            await _reply(update, msgs.RGB_INVOICE_ALREADY_USED)


@_track_time
async def get_invoice_handler(update, _context):
    """Handle the /getinvoice command."""
    with sett.Session() as session:
        ongoing_purchase = (
            session.query(Purchase)
            .filter_by(chat_id=update.effective_chat.id, status=PurchaseStatus.PENDING)
            .first()
        )
        if ongoing_purchase:
            return await _reply(
                update,
                msgs.INVOICE_PENDING.format(invoice=ongoing_purchase.invoice),
            )

        LOGGER.info("Getting invoice for chat %s", update.effective_chat.id)
        invoice = get_invoice()
        purchase = Purchase(invoice=invoice, chat_id=update.effective_chat.id)
        session.add(purchase)
        session.commit()
        await _reply(update, msgs.INVOICE_SEND.format(invoice=invoice))