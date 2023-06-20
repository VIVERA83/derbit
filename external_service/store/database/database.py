"""Database..."""
from typing import Optional, Type
from uuid import uuid4

from base.base_accessor import BaseAccessor
from core.settings import Settings
from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Настройка мета данных.

    В частности указываем схему для хранения таблиц."""

    metadata = MetaData(schema=Settings().postgres.db_schema)
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    __str__ = __repr__


class Database(BaseAccessor):
    """Описание правил подключения PostgresQL к приложению Fast-Api"""

    _engine: Optional[AsyncEngine] = None
    _db: Optional[Type[DeclarativeBase]] = None
    session: Optional[AsyncSession] = None

    async def connect(self, *_: list, **__: dict):
        """Настройка соединения с БД."""
        self._db = Base
        self._engine = create_async_engine(
            self.app.settings.postgres.dsn, echo=False, future=True
        )
        self.session = AsyncSession(self._engine, expire_on_commit=False)
        self.logger.info("Connected to Postgres")

    async def disconnect(self, *_: list, **__: dict):
        """Закрытие соединение с БД."""
        if self._engine:
            await self._engine.dispose()
        self.logger.info("Disconnected from Postgres")
