"""Модуль начальных настроек приложения."""
import os

from pydantic import BaseModel, BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class Postgres(BaseModel):
    """Параметры потключения к PostgresQL"""

    db: str
    user: str
    password: str
    host: str
    port: int
    db_schema: str = "public"

    @property
    def dsn(self) -> str:
        """Возвращает link настройки."""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Log(BaseModel):
    """Параметры логирования."""

    level: str = "INFO"
    guru: bool = False
    traceback: bool = False


class Settings(BaseSettings):
    """Объединяющий класс, в котором собраны настройки приложения."""

    postgres: Postgres
    logging: Log
    host: str
    port: int

    class Config:
        """Настройки для чтения переменных окружения из файла."""

        env_nested_delimiter = "__"
        env_file = BASE_DIR + "/.env"
        enf_file_encoding = "utf-8"

    @property
    def base_url(self) -> str:
        """Начальный url адрес приложения."""
        return f"http://{self.host}:{self.port}"
