import asyncio
import hashlib
import hmac
import json
from datetime import datetime

import aiohttp
import websockets
from icecream import ic

clientId = "6X80xUjU"
clientSecret = "gtVfADuHLcAZknJ_kgtnEWkfT-Y4RUHmVe4giC23e5s"
timestamp = round(datetime.now().timestamp() * 1000)
nonce = "abcd"
data = ""
signature = (
    hmac.new(
        bytes(clientSecret, "latin-1"),
        msg=bytes("{}\n{}\n{}".format(timestamp, nonce, data), "latin-1"),
        digestmod=hashlib.sha256,
    )
    .hexdigest()
    .lower()
)

msg = {
    "jsonrpc": "2.0",
    "method": "public/auth",
    "params": {
        "grant_type": "client_signature",
        "client_id": clientId,
        "timestamp": timestamp,
        "signature": signature,
    },
}


async def call_api(msg):
    session = aiohttp.ClientSession()
    # url = f"https://deribit.com/api/v2/public/auth?client_id={clientId}&client_secret={clientSecret}&grant_type=client_credentials"
    # async with session.get(url, ) as response:
    #     ic(await response.json())

    msg = {
        "jsonrpc": "2.0",
        "method": "public/get_book_summary_by_currency",
        "params": {"currency": "BTC", "kind": "future"},
    }
    msg = {
        "jsonrpc": "2.0",
        "method": "public/get_index",
        "id": 42,
        "params": {"currency": "ETH"},
    }
    async with session.ws_connect(url="wss://www.deribit.com/ws/api/v2") as ws:
        ic(await ws.send_json(msg))
        ic(await ws.receive_json())

    await session.close()


asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
