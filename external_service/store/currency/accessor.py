"""Модуль по работе с данными из базы данных."""
from datetime import datetime, time

from base.base_accessor import BaseAccessor
from currency.data_classes import Currency
from currency.models import CurrencyModel
from icecream import ic
from sqlalchemy import and_, select


class CurrencyAccessor(BaseAccessor):
    """Класс описывает методы взаимодействия с БД."""

    async def get_all_currency_index(self, ticker: str) -> list[CurrencyModel]:
        """Получить все записи о валюте."""

        async with self.app.database.session.begin().session as session:
            smtp = select(CurrencyModel).where(CurrencyModel.title == ticker)
            currency = await session.execute(smtp)
            return [i[0] for i in currency.all()]

    async def get_last_index(self, ticker: str) -> float:
        """Получить последнею запись."""

        async with self.app.database.session.begin().session as session:
            smtp = select(CurrencyModel) \
                .where(CurrencyModel.title == ticker) \
                .order_by(CurrencyModel.create_date.desc()) \
                .limit(1)
            currency = await session.execute(smtp)
            return currency.first()[0].price

    async def get_prices_period(self, ticker: str, start: datetime, end: datetime) -> list[CurrencyModel]:
        """Получить данные по валюте за период."""

        async with self.app.database.session.begin().session as session:
            smtp = select(CurrencyModel) \
                .where(CurrencyModel.title == ticker) \
                .filter(and_(CurrencyModel.create_date >= start,
                             CurrencyModel.create_date <= end))
            currency = await session.execute(smtp)
            return [i[0] for i in currency.all()]
