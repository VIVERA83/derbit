"""Компоненты приложения."""
from typing import Optional

from aiohttp import web
from core.settings import Settings
from store import Store
from store.database.postgres import Database


class Application(web.Application):
    """Основной класс приложения, описываем дополнительные атрибуты"""

    #  настройки приложения
    settings: Optional["Settings"] = None
    #  ассессоры
    store: Optional["Store"] = None
    # подключенные БД
    database: Optional["Database"] = None
