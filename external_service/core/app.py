"""Место окончательной сборки приложения."""
from core.components import Application
from core.exceptions import setup_exception
from core.logger import setup_logging
from core.middelware import setup_middleware
from core.routes import setup_routes
from core.settings import Settings
from store import setup_store

app = Application()


def setup_app() -> "Application":
    """Место сборки приложения, подключения бд, роутов, и т.д"""
    app.settings = Settings()
    setup_logging(app)
    setup_middleware(app)
    setup_exception(app)
    setup_routes(app)
    setup_store(app)
    app.logger.info(f"Swagger link: {app.settings.base_url}{app.docs_url}")  # noqa
    return app
