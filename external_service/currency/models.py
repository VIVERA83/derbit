"""Модели Currency."""

from datetime import datetime

from currency.data_classes import Currency
from sqlalchemy import TIMESTAMP, Float
from sqlalchemy.orm import Mapped, mapped_column
from store.database.database import Base


class CurrencyModel(Base):
    """Model Currency."""

    __tablename__ = "currencies"

    title: Mapped[str]
    price: Mapped[Float] = mapped_column(Float)
    create_date: Mapped[datetime] = mapped_column(TIMESTAMP)

    @property
    def as_dataclass(self) -> Currency:
        """Получить dataclass."""
        return Currency(self.id, self.title, self.price, self.create_date)


#
