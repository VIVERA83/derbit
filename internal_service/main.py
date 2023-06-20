"""Модуль запуска приложения"""

from aiohttp.web import run_app
from core.app import make_app

app = make_app()

if __name__ == "__main__":
    run_app(app)
