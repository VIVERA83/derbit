"""End points for currency."""
from datetime import date, datetime
from typing import Any

from core.components import Request
from currency.schemes import CurrencyEnum, CurrencySchema, query_ticket
from fastapi import APIRouter
from icecream import ic

from external_service.currency.schemes import query_end_date, query_start_date

currency_route = APIRouter()


@currency_route.get(
    "/all",
    summary="Все записи валюте",
    description="Получить все записи по валюте`",
    response_description="Список записей",
    tags=["currency"],
    response_model=list[CurrencySchema],
)
async def get_currency(request: "Request", ticker: CurrencyEnum = query_ticket) -> Any:
    """Все записи валюты."""
    return await request.app.store.currency.get_all_currency_index(ticker.value)


@currency_route.get(
    "/last",
    summary="Последнее значение",
    description="Получить последний цену на валюту",
    response_description="Цена",
    tags=["currency"],
    response_model=float,
)
async def get_last(request: "Request", ticker: CurrencyEnum = query_ticket) -> Any:
    """Получить последний цену на валюту."""
    return await request.app.store.currency.get_last_index(ticker.value)


@currency_route.get(
    "/get_between",
    summary="Последнее значение",
    description="Получить последний цену на валюту",
    response_description="Цена",
    tags=["currency"],
    response_model=list[CurrencySchema],
)
async def et_between(request: "Request",
                     ticker: CurrencyEnum = query_ticket,
                     start: datetime = query_start_date,
                     end: datetime = query_end_date) -> Any:
    """Получить валюту за период времянки."""
    return await request.app.store.currency.get_prices_period(ticker.value, start, end)

