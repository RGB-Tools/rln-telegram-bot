"""Messages to users module."""

from . import settings as sett

# pylint: disable=unnecessary-lambda-assignment

USE_HELP = rf"Use /{sett.HELP_CMD} for info on what you can do with this bot\."

START = (
    r"""
⚡️ Welcome to the RGB LN test bot\! ⚡️

"""
    + USE_HELP
)

TOO_MANY_ASSET_REQUESTS = (
    r"You requested assets too many times in the past 24 hours\. You can try again "
    r"{next_request_time}\."
)

TOO_MANY_BTC_REQUESTS = (
    r"You requested BTC too many times in the past 24 hours\. You can try again "
    r"{next_request_time}\."
)

INVALID_INPUT = r"""
This is neither a valid RGB invoice nor a valid bitcoin address\.
"""

INVALID_ADDRESS = r"This is not a valid bitcoin address\."

INVALID_RGB_INVOICE = r"This is not a valid RGB invoice\."

INVALID_RGB_TRANSPORT_ENDPOINTS = (
    INVALID_RGB_INVOICE + r" The embedded transport endpoints are invalid or not supported\."
)

ASK_RGB_INVOICE = r"""
Please give me an RGB invoice to send some assets\.
"""

ASK_BTC_ADDRESS = r"""
Please give me an address where to send some bitcoins\.
"""

RGB_INVOICE_ALREADY_USED = r"""
This RGB invoice has already been used, please send another one\.
"""

RGB_INVOICE_INVALID_NETWORK = r"""
This RGB invoice is for a different bitcoin network, please send another one\.
"""

RGB_INVOICE_INVALID_TYPE = (
    r"This RGB invoice is requesting to receive in witness but the bot supports "
    r"only the blind mode, please send another one\."
)

ASSET_SENT = (
    lambda: rf"""
I have sent you {sett.ASSET_AMOUNT_TO_SEND} {sett.ASSET_TICKER} with """
    rf"""TXID:
`{{txid}}`

Don't forget to refresh your wallet's transfers to complete the asset """
    rf"""receiving process \(multiple refreshes may be needed for the transfer to get """
    rf"""to the settled status\)\.

Once the tranfer has settled you can open a channel with
`{sett.NODE_URI}`
using
`{sett.ASSET_TICKER}` \(`{sett.ASSET_ID}`\)
as the RGB asset
"""
)

BTC_SENT = (
    lambda: f"""
I have sent you {sett.SAT_AMOUNT_TO_SEND} sats with TXID:
`{{txid}}`
"""
)

MESSAGE_TOO_LONG = """
Tried to send a message over the text length limit
"""

SENDING_ASSET = (
    lambda: rf"""
I'm now sending {sett.ASSET_AMOUNT_TO_SEND} {sett.ASSET_TICKER}\.

This may take a while\.
"""
)

SENDING_BTC = (
    lambda: rf"""
I'm now sending {sett.SAT_AMOUNT_TO_SEND} sats\.
"""
)

SOMETHING_WENT_WRONG = r"""
Oops\! Something went wrong\.

The issue has been reported\. Try again later\.
"""

UNKNOWN_COMMAND = (
    r"""
Sorry, I don't understand this command 😕

"""
    + USE_HELP
)

HELP = (
    lambda: rf"""
This bot helps testing RGB on LN\.
This can be done using Iris Wallet desktop which you can find in its """
    rf"""[GitHub releases page](https://github.com/RGB-Tools/iris-wallet-desktop/releases)\.

Under the hood """
    rf"""[RLN \(rgb\-lightning\-node\)](https://github.com/RGB-Tools/rgb-lightning-node) """
    rf"""is used to provide LN functionality on a shared regtest\.

Features:
1\. get on\-chain bitcoins
2\. get on\-chain RGB assets
3\. pay an RGB LN invoice to simulate the purchase of a virtual item

How to test an RGB LN payment:
1\. request on\-chain bitcoins with the /{sett.GETBTC_CMD} command
2\. request on\-chain assets with the /{sett.GETASSET_CMD} command
3\. open an RGB LN channel with the received asset towards the bot's LN """
    rf"""node\. Use /{sett.GETNODEINFO_CMD} to get the necessary info
4\. request an RGB LN invoice with the /{sett.GETINVOICE_CMD} command
5\. pay the invoice and wait for feedback from the bot
"""
)

GET_NODE_INFO = (
    lambda: f"""
Node URI:
`{sett.NODE_URI}`

RGB asset ID:
`{sett.ASSET_ID}`

RGB asset ticker:
`{sett.ASSET_TICKER}`
"""
)

INVOICE_PENDING = (
    r"There's already a pending invoice:"
    r"""
`{invoice}`

If you haven't paid it yet, please do it, otherwise please wait for the """
    r"payment to be detected\."
)

INVOICE_SEND = (
    r"""Here's your invoice:
`{invoice}`

Once the payment will be detected I will send you a nice sticker\.

Make sure the channel is usable \(by checking the channel management page\) """
    r"before attempting the payment\."
)

INVOICE_PAID = r"""
LN payment received\. Here's your sticker, congrats\!
"""

INVOICE_EXPIRED = rf"""
Invoice has expired\. Use /{sett.GETINVOICE_CMD} to request a new one\.
"""
