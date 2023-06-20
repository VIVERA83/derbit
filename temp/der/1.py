import asyncio
import json

import websockets

clientId = "h6X80xUjU"
clientSecret = "gtVfADuHLcAZknJ_kgtnEWkfT-Y4RUHmVe4giC23e5s"
msg = {
    "jsonrpc": "2.0",
    "id": 9929,
    "method": "public/auth",
    "params": {
        "grant_type": "client_credentials",
        "client_id": clientId,
        "client_secret": clientSecret,
    },
}


async def call_api(msg):
    async with websockets.connect("wss://test.deribit.com/ws/api/v2") as websocket:
        await websocket.send(msg)
        while websocket.open:
            response = await websocket.recv()
            # do something with the response...
            print(response)


asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
