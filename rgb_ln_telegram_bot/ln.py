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


def _check_if_err(res):
    if "error" in res:
        err = res["error"]
        if "Allocations already available" in err:
            raise AllocationsAlreadyAvailable
        if "Invalid transport endpoints" in err:
            raise InvalidTransportEndpoints
        if "Recipient ID already used" in err:
            raise RecipientIDAlreadyUsed
        raise APIException(err)


def asset_balance():
    """Call the /assetbalance API."""
    payload = {
        "asset_id": sett.ASSET_ID,
    }
    res = requests.post(
        f"{sett.LN_NODE_URL}/assetbalance", json=payload, timeout=sett.REQUESTS_TIMEOUT
    ).json()
    _check_if_err(res)
    return res


def btc_balance():
    """Call the /btcbalance API."""
    payload = {
        "skip_sync": False,
    }
    res = requests.post(
        f"{sett.LN_NODE_URL}/btcbalance", json=payload, timeout=sett.REQUESTS_TIMEOUT
    ).json()
    _check_if_err(res)
    return res


def create_utxos():
    """Call the /createutxos API."""
    payload = {
        "up_to": True,
        "num": sett.UTXOS_TO_CREATE,
        "size": None,
        "fee_rate": sett.FEE_RATE,
        "skip_sync": False,
    }
    res = requests.post(
        f"{sett.LN_NODE_URL}/createutxos", json=payload, timeout=sett.REQUESTS_TIMEOUT
    ).json()
    _check_if_err(res)
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
    _check_if_err(res)
    return res["invoice"]


def get_invoice_status(invoice):
    """Call the /invoicestatus API."""
    payload = {"invoice": invoice}
    res = requests.post(
        f"{sett.LN_NODE_URL}/invoicestatus", json=payload, timeout=sett.REQUESTS_TIMEOUT
    ).json()
    _check_if_err(res)
    return res["status"]


def get_network_info():
    """Call the /networkinfo API."""
    res = requests.get(f"{sett.LN_NODE_URL}/networkinfo", timeout=sett.REQUESTS_TIMEOUT).json()
    _check_if_err(res)
    return res


def get_node_info():
    """Call the /nodeinfo API."""
    res = requests.get(f"{sett.LN_NODE_URL}/nodeinfo", timeout=sett.REQUESTS_TIMEOUT).json()
    _check_if_err(res)
    return res


def list_assets():
    """Call the /listassets API."""
    payload = {
        "filter_asset_schemas": [],
    }
    res = requests.post(
        f"{sett.LN_NODE_URL}/listassets", json=payload, timeout=sett.REQUESTS_TIMEOUT
    ).json()
    _check_if_err(res)
    return res


def refresh_transfers():
    """Call the /refreshtransfers API."""
    payload = {
        "skip_sync": False,
    }
    res = requests.post(
        f"{sett.LN_NODE_URL}/refreshtransfers",
        json=payload,
        timeout=sett.REQUESTS_TIMEOUT,
    ).json()
    _check_if_err(res)
    return res


def send_asset(blinded_utxo, transport_endpoints):
    """Call the /sendasset API."""
    payload = {
        "asset_id": sett.ASSET_ID,
        "assignment": {
            "type": "Fungible",
            "value": sett.ASSET_AMOUNT_TO_SEND,
        },
        "recipient_id": blinded_utxo,
        "donation": True,
        "fee_rate": sett.FEE_RATE,
        "min_confirmations": 0,
        "transport_endpoints": transport_endpoints,
        "skip_sync": False,
    }
    res = requests.post(
        f"{sett.LN_NODE_URL}/sendasset", json=payload, timeout=sett.REQUESTS_TIMEOUT
    ).json()
    _check_if_err(res)
    return res["txid"]


def send_btc(address):
    """Call the /sendbtc API."""
    payload = {
        "amount": sett.SAT_AMOUNT_TO_SEND,
        "address": address,
        "fee_rate": sett.FEE_RATE,
        "skip_sync": False,
    }
    res = requests.post(
        f"{sett.LN_NODE_URL}/sendbtc", json=payload, timeout=sett.REQUESTS_TIMEOUT
    ).json()
    _check_if_err(res)
    return res["txid"]
