from datetime import datetime
from unittest.mock import AsyncMock
from uuid import UUID

from derbit.data_classes import Currency

msg = {
    "jsonrpc": "2.0",
    "method": "public/get_index",
    "params": {"currency": "BTC"},
}


class TestHandler:
    async def test_new_record_btc(self, store):
        """Проверям работу schedule_manager.handler."""
        # мокаем метод добавления в БД
        store.derbit.add_currency_index = AsyncMock(
            return_value=Currency("792d1482-34f9-417a-8b4e-ae972565cf76", "BTC", 26322.94, 1686943920159566))
        # Вызываем метод который ходит в сторонний сервис за данными по валюте
        await store.schedule_manager.handler("BTC")
        # Проверка передаваемых параметров в функцию которая добавляет запись в БД
        assert store.derbit.add_currency_index.mock_calls[0].kwargs["ticker"] == "BTC"
        assert store.derbit.add_currency_index.mock_calls[0].kwargs["value"] == 26322.94
        assert store.derbit.add_currency_index.mock_calls[0].kwargs["date"].year == 2023
        assert store.derbit.add_currency_index.mock_calls[0].kwargs["date"].month == 6

    async def test_new_record_eth(self, store):
        """Проверям работу schedule_manager.handler."""
        # мокаем метод добавления в БД+
        store.derbit.add_currency_index = AsyncMock(
            return_value=Currency(id=UUID("792d1482-34f9-417a-8b4e-ae972565cf72"),
                                  title="ETH",
                                  price=1714.56,
                                  create_date=datetime.fromtimestamp(1686943440)))
        # Вызываем метод который ходит в сторонний сервис за данными по валюте
        await store.schedule_manager.handler("ETH")
        # Проверка передаваемых параметров в функцию которая добавляет запись в БД
        assert store.derbit.add_currency_index.mock_calls[0].kwargs["ticker"] == "ETH"
        assert store.derbit.add_currency_index.mock_calls[0].kwargs["value"] == 1714.56
        assert store.derbit.add_currency_index.mock_calls[0].kwargs["date"].year == 2023
        assert store.derbit.add_currency_index.mock_calls[0].kwargs["date"].month == 6
