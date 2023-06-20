"""Web Socket."""
from typing import Optional

from aiohttp import ClientSession
from aiohttp.client_ws import ClientWebSocketResponse
from base.base_accessor import BaseAccessor
from base.utils import before_execution
from core.componets import Application


class WSAccessor(BaseAccessor):
    """Web Socket приложения."""

    session: Optional[ClientSession] = None
    ws_session: Optional[ClientWebSocketResponse] = None
    url = "wss://www.deribit.com/ws/api/v2"

    async def connect(self, app: "Application"):
        """Подключение к Web Socket www.deribit."""

        self.session = ClientSession()
        # Не всегда проходит подключение, поэтому используем декоратор
        # который пытается подключиться
        self.ws_session = await before_execution(total_timeout=60)(
            self.session.ws_connect
        )(self.url)
        if not self.ws_session:
            await self.session.close()
            raise RuntimeError(f"Could not connect to {self.url}")
        self.logger.info(f"Connected to {self.url}")

    async def disconnect(self, app: "Application"):
        """Закрытие соединения."""

        await self.ws_session.close()
        await self.session.close()
        self.logger.info(f"Disconnect {self.url}")

    async def send(self, message: dict) -> dict:
        """Оправить сообщение на www.deribit."""

        await self.ws_session.send_json(message)
        return await self.ws_session.receive_json()
