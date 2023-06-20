import asyncio
import json

import websockets
from aiohttp import ClientSession
from icecream import ic

msg = {
    "jsonrpc": "2.0",
    "id": 8066,
    "method": "public/ticker",
    "params": {"instrument": "BTC-24AUG18-6500-P"},
}


async def call_api(msq):
    session = ClientSession()
    url = "https://test.deribit.com/api/v2/"
    method = "public/get_book_summary_by_currency?"
    # method = "public/ticker?"
    params = "currency=BTC&kind=future"
    # params = "instrument=BTC-24AUG18-6500-P"
    url += method + params
    ic(url)
    async with session.get(url) as resp:
        ic(resp.status)
        ic(await resp.json())
    await session.close()


# async def call_api(msg):
#     async with websockets.connect('wss://test.deribit.com/den/ws') as websocket:
#         await websocket.send(msg)
#         while websocket.open:
#             response = await websocket.recv()
#             # do something with the response...
#             print(response)


asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
