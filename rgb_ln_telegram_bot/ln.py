"""Module to perform API calls to RLN."""
from logging import getLogger

import requests

from rgb_ln_telegram_bot.exceptions import (
    AllocationsAlreadyAvailable,
    APIException,
    InvalidTransportEndpoints,
    RecipientIDAlreadyUsed,
)

from . import settings as sett

LOGGER = getLogger(__name__)


def asset_balance():
    """Call the /assetbalance API."""
    payload = {
        "asset_id": sett.ASSET_ID,
    }
    res = requests.post(
        f"{sett.LN_NODE_URL}/assetbalance", json=payload, timeout=sett.REQUESTS_TIMEOUT
    ).json()
    if "error" in res:
        raise APIException(res["error"])
    return res


def create_utxos():
    """Call the /createutxos API."""
    payload = {"up_to": True, "num": sett.UTXOS_TO_CREATE}
    res = requests.post(
        f"{sett.LN_NODE_URL}/createutxos", json=payload, timeout=sett.REQUESTS_TIMEOUT
    ).json()
    if "error" in res:
        err = res["error"]
        if "Allocacations already available" in err:
            raise AllocationsAlreadyAvailable
        raise APIException(err)
    return res


def get_invoice():
    """Call the /lninvoice API."""
    payload = {
        "amt_msat": sett.HTLC_MIN_MSAT,
        "expiry_sec": sett.INVOICE_EXPIRATION_SEC,
        "asset_id": sett.ASSET_ID,
        "asset_amount": sett.INVOICE_PRICE,
    }
    res = requests.post(
        f"{sett.LN_NODE_URL}/lninvoice", json=payload, timeout=sett.REQUESTS_TIMEOUT
    ).json()
    if "error" in res:
        raise APIException(res["error"])
    return res["invoice"]


def get_invoice_status(invoice):
    """Call the /invoicestatus API."""
    payload = {"invoice": invoice}
    res = requests.post(
        f"{sett.LN_NODE_URL}/invoicestatus", json=payload, timeout=sett.REQUESTS_TIMEOUT
    ).json()
    if "error" in res:
        raise APIException(res["error"])
    return res["status"]


def get_node_info():
    """Call the /nodeinfo API."""
    res = requests.get(
        f"{sett.LN_NODE_URL}/nodeinfo", timeout=sett.REQUESTS_TIMEOUT
    ).json()
    if "error" in res:
        raise APIException(res["error"])
    return res


def list_assets():
    """Call the /listassets API."""
    res = requests.get(
        f"{sett.LN_NODE_URL}/listassets", timeout=sett.REQUESTS_TIMEOUT
    ).json()
    if "error" in res:
        raise APIException(res["error"])
    return res["assets"]


def refresh_transfers():
    """Call the /refreshtransfers API."""
    res = requests.post(
        f"{sett.LN_NODE_URL}/refreshtransfers", timeout=sett.REQUESTS_TIMEOUT
    ).json()
    if "error" in res:
        raise APIException(res["error"])
    return res


def send_asset(blinded_utxo, transport_endpoints):
    """Call the /sendasset API."""
    payload = {
        "asset_id": sett.ASSET_ID,
        "amount": sett.ASSET_AMOUNT_TO_SEND,
        "blinded_utxo": blinded_utxo,
        "donation": True,
        "min_confirmations": 0,
        "transport_endpoints": transport_endpoints,
    }
    res = requests.post(
        f"{sett.LN_NODE_URL}/sendasset", json=payload, timeout=sett.REQUESTS_TIMEOUT
    ).json()
    if "error" in res:
        err = res["error"]
        if "Invalid transport endpoints" in err:
            raise InvalidTransportEndpoints
        if "Recipient ID already used" in err:
            raise RecipientIDAlreadyUsed
        raise APIException(err)
    return res["txid"]
