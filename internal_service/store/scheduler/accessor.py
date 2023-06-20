"""Планировщик задач."""
from typing import TYPE_CHECKING, Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from base.base_accessor import BaseAccessor

if TYPE_CHECKING:
    from core.componets import Application


class SchedulerAccessor(BaseAccessor):
    """Планировщик задач."""

    scheduler: Optional[AsyncIOScheduler] = None

    def _init_(self):
        """Инициализация."""
        self.scheduler = AsyncIOScheduler()

    async def connect(self, app: "Application"):
        """Запуск."""
        self.scheduler.start()
        self.logger.info("Scheduler running")

    async def disconnect(self, app: "Application"):
        """Остановка."""
        self.scheduler.shutdown()
        self.logger.info("Scheduler stopped")


def setup_scheduler(app: "Application"):
    """Настройка заданий для планировщика."""

    app.store.scheduler.scheduler.add_job(
        func=app.store.schedule_manager.handler,
        trigger="cron",
        minute="*",
        kwargs={"ticker": "BTC"},
        name="BTC",
    )
    app.store.scheduler.scheduler.add_job(
        func=app.store.schedule_manager.handler,
        trigger="cron",
        minute="*",
        kwargs={"ticker": "ETH"},
        name="ETH",
    )
