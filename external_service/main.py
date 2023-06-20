"""Модуль запуска приложения."""
import uvicorn
from core.app import setup_app

app = setup_app()

if __name__ == "__main__":
    uvicorn.run(app=app, host=app.settings.host, port=app.settings.port, use_colors=True)
