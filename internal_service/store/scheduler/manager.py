"""Менеджер."""
from asyncio import Lock
from datetime import datetime
from typing import Optional

from base.base_accessor import BaseAccessor


class ScheduleManager(BaseAccessor):
    """Менеджер, отвечает за стыковку и обработку бизнес задач."""

    lock: Optional[Lock] = None

    def _init_(self):
        self.lock = Lock()

    async def handler(self, ticker: str):
        """Добавить данные с Derbit в БД.

        1. Получает данные из внешнего сервиса Berbit
        2. Записывает полученные данные в БД.

        """
        msg = {
            "jsonrpc": "2.0",
            "method": "public/get_index",
            "params": {"currency": ticker},
        }
        async with self.lock:
            result = await self.app.store.ws_accessor.send(msg)
            price = result["result"].get(ticker)
            date = datetime.fromtimestamp(result["usOut"] / 1_000_000)
            await self.app.store.derbit.add_currency_index(
                ticker=ticker, value=price, date=date
            )
        self.logger.info(f"Added currency index for ticker {ticker} new value {price}")
