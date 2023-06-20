"""Дата Классы."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Currency:
    """Дата класс Валюта."""

    title: str
    price: float
    create_date: datetime
    id: UUID = None
