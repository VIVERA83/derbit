"""Модуль по работе с данными из базы данных."""
from datetime import datetime

from base.base_accessor import BaseAccessor
from derbit.data_classes import Currency
from derbit.models import CurrencyModel


class DerbitAccessor(BaseAccessor):
    """Класс описывает методы взаимодействия с БД."""

    async def add_currency_index(
        self, ticker: str, value: float, date: datetime
    ) -> Currency:
        """Добавить новую запись о валюте."""

        async with self.app.database.session.begin().session as session:
            currency = CurrencyModel(
                title=ticker,
                price=value,
                create_date=date,
            )
            session.add(currency)
            await session.commit()
            await session.refresh(currency)
        return currency.as_dataclass
