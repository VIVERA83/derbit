import json
import os

import pytest
from aiohttp import ClientSession, web
from aiohttp.pytest_plugin import aiohttp_server
from aiohttp.test_utils import TestClient, TestServer

from core.app import make_app
from store.ws.ws_accessor import WSAccessor
from tests.fixtures import FIXTURE_PATH

ETH = {
    "jsonrpc": "2.0",
    "method": "public/get_index",
    "params": {"currency": "ETH"},
}
BTC = {
    "jsonrpc": "2.0",
    "method": "public/get_index",
    "params": {"currency": "BTC"},
}


@pytest.fixture(scope='session')
def clone_server():
    return make_app()


@pytest.fixture()
async def clone_cli(aiohttp_client, clone_server) -> TestClient:
    return await aiohttp_client(clone_server)


@pytest.fixture()
async def server(clone_server) -> TestServer:
    return aiohttp_server(clone_server)



def get_eth_original_response():
    with open(os.path.join(FIXTURE_PATH, "mocks", "derbit", "get_index_eth.json")) as f:
        data = json.load(f)
    return data


def get_bth_original_response():
    with open(os.path.join(FIXTURE_PATH, "mocks", "derbit", "get_index_btc.json")) as f:
        data = json.load(f)
    return data


@pytest.fixture(autouse=True)
def clone_mocker():
    async def call(message: dict) -> dict:
        if message == ETH:
            return get_eth_original_response()
        elif message == BTC:
            return get_bth_original_response()
        else:
            raise NotImplementedError

    WSAccessor.send = call


def derbit_api_call(mock_func):
    WSAccessor.call = mock_func
