"""Сервис отвечает за работу с внешними источниками данных."""
import typing

from store.database.postgres import Database
from store.derbit.accessor import DerbitAccessor
from store.scheduler.accessor import SchedulerAccessor
from store.scheduler.manager import ScheduleManager

if typing.TYPE_CHECKING:
    from core.app import Application


class Store:  # pylint: disable=R0903 # noqa
    """Собирательный класс, в котором происходит инициализация внешних источников данных."""

    def __init__(self, app: "Application"):
        """Инициализация обработчиков данных"""
        from store.ws.ws_accessor import WSAccessor  # pylint: disable=C0415 # noqa

        self.ws_accessor = WSAccessor(app)
        self.derbit = DerbitAccessor(app)
        self.scheduler = SchedulerAccessor(app)
        self.schedule_manager = ScheduleManager(app)


def setup_store(app: "Application"):
    """Настройка Store, подключение к основному приложению."""
    app.postgres = Database(app)
    app.store = Store(app)
