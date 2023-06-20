"""Schemas сервиса Convertor."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel


class CurrencyEnum(str, Enum):
    BTC = "BTC"
    ETH = "ETH"

    @classmethod
    def get_all_options(cls) -> str:
        return ", ".join([f"`{value}`" for value in cls._member_names_])


query_ticket: CurrencyEnum = Query(
    title="Аббревиатура валюты",
    description=f"Аббревиатура валюты, Возможное значение: {CurrencyEnum.get_all_options()} ",
    example="BTH",
)
query_start_date: datetime = Query(
    title="Начальная дата",
    description="Начало периода",
    example="2023-06-16 11:23:00",
)
query_end_date: datetime = Query(
    title="Конечная дата",
    description="Окончание периода",
    example="2023-06-16 11:30:00",
)


class CurrencySchema(BaseModel):
    id: UUID
    title: str
    price: float
    create_date: datetime

    class Config:
        orm_mode = True
