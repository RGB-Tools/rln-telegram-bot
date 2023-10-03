"""Messages to users module."""
from . import settings as sett

# pylint: disable=anomalous-backslash-in-string,unnecessary-lambda-assignment
# pylama:ignore=W605

USE_HELP = f"Use /{sett.HELP_CMD} for info on what you can do with this bot\."

START = (
    """
⚡️ Welcome to the RGB LN testnet bot\! ⚡️

"""
    + USE_HELP
)

TOO_MANY_ASSET_REQUESTS = """
You requested assets too many times in the past 24 hours\. You can try again \
{next_request_time}\.
"""

INVALID_RGB_INVOICE = "This is not a valid RGB invoice\."

INVALID_RGB_TRANSPORT_ENDPOINTS = (
    INVALID_RGB_INVOICE
    + """\
 The embedded transport endpoints are invalid or not supported\.
"""
)

ASK_RGB_INVOICE = """
Please give me an RGB invoice to send some assets\.

For a faster experience the invoice can be created with `min_confirmations` \
set to 0\.
"""

RGB_INVOICE_ALREADY_USED = """
This RGB invoice has already been used, please send another one\.
"""

ASSET_SENT = (
    lambda: f"""
I have sent you {sett.ASSET_AMOUNT_TO_SEND} {sett.ASSET_TICKER} with \
TXID:
`{{txid}}`

Don't forget to refresh your wallet's transfers to complete the asset \
receiving process \(multiple refreshes may be needed for the transfer to get \
to the _settled_ status\)\.

Once the tranfer has settled you can open a channel with
`{sett.NODE_URI}`
using
`{sett.ASSET_ID}`
as the RGB asset ID
"""
)

SENDING_ASSET = (
    lambda: f"""
I'm now sending {sett.ASSET_AMOUNT_TO_SEND} {sett.ASSET_TICKER}\.

This may take a while\.
"""
)

SOMETHING_WENT_WRONG = """
Oops! Something went wrong.

The issue has been reported. Try again later.
"""

UNKNOWN_COMMAND = (
    """
Sorry, I don't understand this command 😕

"""
    + USE_HELP
)

HELP = (
    lambda: f"""
This bot helps testing RGB on LN\.
This can be done using \
[RLN \(rgb\-lightning\-node\)](https://github.com/RGB-Tools/rgb-lightning-node) \
on testnet\.

Features:
1\. get RGB assets on\-chain
2\. pay an RGB LN invoice to simulate the purchase of a virtual item

How to test an RGB LN payment:
1\. request on\-chain assets with the /{sett.GETASSET_CMD} command
2\. open an RGB LN channel with the received asset towards the bot's LN \
node\. Use /{sett.GETNODEINFO_CMD} to get the necessary info
3\. request an RGB LN invoice with the /{sett.GETINVOICE_CMD} command
4\. pay the invoice and wait for feedback from the bot

If you need help operating RLN you can use the /{sett.NODECOMMANDHELP_CMD} \
command\.
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

INVOICE_PENDING = """
There's already a pending invoice:
`{invoice}`

If you haven't paid it yet, please do it, otherwise please wait for the \
payment to be detected\.
"""

INVOICE_SEND = """
Here's your invoice:
`{invoice}`

Once the payment will be detected I will send you a nice sticker\.

Make sure the channel is usable \(by calling the `/listchannels` API\) before \
attempting the payment\.
"""

INVOICE_PAID = """
Here's your sticker\! Congrats\!
"""

INVOICE_EXPIRED = f"""
Invoice has expired\. Use /{sett.GETINVOICE_CMD} to request a new one\.
"""

NODECOMMANDHELP = (
    lambda: f"""
You can operate \
[RLN \(rgb\-lightning\-node\)](https://github.com/RGB-Tools/rgb-lightning-node) \
by calling its APIs\.

You can do that by using `curl` or the \
[swagger interface](https://rgb-tools.github.io/rgb-lightning-node/)\. \
When using swagger, you can use the same request body from `curl` \
\(the `\-d` option value\)\.

To create an RGB invoice:
```
curl -X 'POST' \\\\
  'http://localhost:3001/rgbinvoice' \\\\
  -H 'Content-Type: application/json' \\\\
  -d '{{ "min_confirmations": 0 }}'
```
To open an RGB LN channel:
```
curl -X 'POST' \\\\
  'http://localhost:3001/openchannel' \\\\
  -H 'Content-Type: application/json' \\\\
  -d '{{
      "peer_pubkey_and_addr": "{sett.NODE_URI}",
      "capacity_sat": 30010,
      "push_msat": 2130000,
      "asset_amount": 10,
      "asset_id": "{sett.ASSET_ID}",
      "public": true
    }}'
```
To list the node's channels:
```
curl -X 'GET' 'http://localhost:3001/listchannels'
```
To pay an RGB LN invoice:
```
curl -X 'POST' \\\\
  'http://localhost:3001/sendpayment' \\\\
  -H 'Content-Type: application/json' \\\\
  -d '{{
      "invoice": "lntb30u1pj3g49vdqud3jxktt5w46x7unfv9kz6mn0v3jsnp4qvahn2d6nh\
ryhrk2y0w60dhg2pe2gwrqc5u2v65ev7tdt72qgs8zjpp5sheq45ehztuhzln57qgww7fmd\
9je0yjn39xrkwrkvs59s5vy2m5ssp5s068nrkgzy868luyz676fggkyrq9pm9zl4x04xv6h\
fvj4hs70msq9qyysgqcqpcxqzuylzlwfnkyw3jw4fkx4j9ggkh5u2wwae8qcjs2yknv7330\
pj9wst8xykkxmtwwe55ucn525kng6tttfs55s6gfvknxknhd9fkjjq7qp23szchlavdnfgq\
axsq2w3453g687sssaundfl0yajp0jmt7d736tqd54r38k94dgjakqekcjxfhkuetca4yff\
9qgsfn9kurg390455fqpcc20rz"
    }}'
```
If your node is exposed on a different host or port update \
`localhost:3001` to the correct endpoint\.
"""
)
