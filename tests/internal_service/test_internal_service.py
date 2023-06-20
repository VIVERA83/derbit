import pytest
from aiohttp.pytest_plugin import aiohttp_client
from icecream import ic

from tests.fixtures.internal_service import (
    BTC,
    ETH,
    derbit_api_call,
    get_bth_original_response,
    get_eth_original_response,
)


class TestInternalService:
    @pytest.mark.parametrize(
        "message,original_data",
        [
            (ETH, get_eth_original_response()),
            (BTC, get_bth_original_response()),
        ],
    )
    async def test_list_schema_including(
        self, server, clone_server, message, original_data
    ):
        url = "/ws/api/v2"
        resp = clone_server.get("/")

        # assert resp.status == 200, f'Получен неуспешный ({resp.status}) статус ответа. ' \
        #                            f'Скорее всего не все поля в querystring_schema помечены как необязательные'
        # data = await resp.json()
        # assert data == original_data, f'Данные, полученные от стороннего API и данные полученные от нашего API' \
        #                               f' не совпадают. Скорее всего схема для {message} написана неверно'
