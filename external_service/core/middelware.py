"""Middleware приложения."""
import traceback
from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

if TYPE_CHECKING:
    from core.components import Application, Request


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Обработка внутренних ошибок при выпоолнение обработсиков запроса."""

    async def dispatch(
            self, request: "Request", call_next: RequestResponseEndpoint
    ) -> Response:
        """Обрапботка ошибок при мполнении handlers (views)."""
        try:
            response = await call_next(request)
            # response.headers["Custom"] = "Example"
            return response
        except Exception as error:
            if isinstance(error, IntegrityError):
                content = {
                    "detail": "UnProcessable Entity",
                    "message": "Perhaps one of the parameters does not meet the uniqueness rules",
                }
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            else:
                content = {
                    "detail": "Internal server error",
                    "message": "The server is temporarily unavailable try contacting later",
                }
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            if request.app.settings.logging.traceback:
                request.app.logger.error(traceback.format_exc())
            else:
                request.app.logger.error(f"{request.url=}, {error=}")
        return JSONResponse(content=content, status_code=status_code)


def setup_middleware(app: "Application"):
    """Настройка подключаемый Middleware."""
    app.add_middleware(ErrorHandlingMiddleware)
