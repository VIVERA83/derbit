"""Модуль сборки приложения."""

from core.componets import Application
from core.logger import setup_logging
from core.settings import Settings
from store import setup_store
from store.scheduler.accessor import setup_scheduler

app = Application()


def make_app() -> "Application":
    """Место сборки приложения, подключения бд, роутов, и т.д"""
    app.settings = Settings()
    setup_logging(app)
    setup_store(app)
    setup_scheduler(app)
    return app
