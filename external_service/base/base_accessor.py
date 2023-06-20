"""Базовый класс, отвечающий за связь логики с базовым приложением."""
import typing

if typing.TYPE_CHECKING:
    from core.app import Application


class BaseAccessor:
    def __init__(self, app: "Application", *args: list, **kwargs: dict):
        """Инициализация, потключаемого сервиса в основном приложении Fast-Api."""
        self.app = app
        self.logger = app.logger
        app.on_event("startup")(self.connect)
        app.on_event("shutdown")(self.disconnect)
        self._init_(app, *args, **kwargs)

    def _init_(self, app: "Application", *_: list, **__: dict):
        """Описание дополнительных действий для инициализации"""
        pass

    async def connect(self, *_: "Application"):
        """Логика отвечающая за подключение и настройку модуля к контексту приложения
        как пример настройка подключения к стороннему API
        """
        pass

    async def disconnect(self, *_: "Application"):
        """Настройка корректного закрытия всех соединений"""
        pass
