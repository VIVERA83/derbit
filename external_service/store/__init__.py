""""Модуль описывающий сервисы по работе с данными."""
from typing import TYPE_CHECKING

from store.currency.accessor import CurrencyAccessor
from store.database.database import Database

if TYPE_CHECKING:
    from external_service.core.app import Application


class Store:
    """Store, сервис данных и работы с ним.

    Инициализация источников данных."""

    def __init__(self, app: "Application"):
        self.currency = CurrencyAccessor(app)


def setup_store(app: "Application"):
    """Настраивая подключение и отключение хранилищ.

    Здесь мы сообщаем приложению, о базах базы данных и других источнгиков данных
    которые мы запускаем при запуске приложения, и как их отключить..
    """
    app.database = Database(app)
    app.store = Store(app)
