"""Переназначенные компоненты Fast-Api."""
import logging
from typing import Optional

from core.settings import Settings
from fastapi import FastAPI, Request as FastAPIRequest
from store import Store
from store.database.database import Database


class Application(FastAPI):
    """Application главный класс.

    Описываем сервисы, которые будут использоваться в приложении.
    Так же это нужно для корректной подсказки IDE.
    """

    settings: Optional["Settings"] = None
    database: Optional["Database"] = None
    store: Optional["Store"] = None
    logger: Optional[logging.Logger] = None


class Request(FastAPIRequest):
    """Переопределения Request.

    Для корректной подсказки IDE по методам `Application`."""

    app: Optional["Application"] = None
    user_id: Optional[str] = None
    token: Optional[str] = None
