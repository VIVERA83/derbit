from unittest.mock import AsyncMock

import pytest

from aiohttp.test_utils import TestClient, loop_context

from internal_service.core.app import make_app
from internal_service.store import Store


@pytest.fixture(scope="session")
def event_loop():
    with loop_context() as _loop:
        yield _loop


@pytest.fixture(scope="session")
def server():
    app = make_app()
    app.store.ws_accessor.send = AsyncMock(return_value={
        "jsonrpc": "2.0",
        "result": {
            "BTC": 26322.94,
            "ETH": 1714.56,
        },
        "testnet": "False",
        "usDiff": 123,
        "usIn": 1686943920159443,
        "usOut": 1686943920159566
    })
    app.store.scheduler = AsyncMock()
    return app


@pytest.fixture
def store(server) -> Store:
    return server.store


@pytest.fixture(autouse=True)
def cli(aiohttp_client, event_loop, server) -> TestClient:
    return event_loop.run_until_complete(aiohttp_client(server))
