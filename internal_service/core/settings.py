"""Подключение переменных окружения."""
import os

from pydantic import BaseModel, BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class Postgres(BaseModel):
    """Параметры подключения к Postgres."""

    db: str
    host: str = "127.0.0.1"
    port: int = 5432
    password: str
    user: str
    db_schema: str = "derbit"

    @property
    def dsn(self) -> str:
        """Получить ссылку подключения к БД."""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    """Основной класс с настройками."""

    postgres: Postgres
    logging_level: str = "INFO"
    logging_guru: bool = True
    host: str = "localhost"

    class Config:
        """Параметры загрузки переменных окружения из файла."""

        env_nested_delimiter = "__"
        env_file = BASE_DIR + "/.env"
        enf_file_encoding = "utf-8"
