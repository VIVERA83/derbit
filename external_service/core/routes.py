""""Routes приложения """
import typing

if typing.TYPE_CHECKING:
    from core.components import Application


def setup_routes(app: "Application"):
    """Настройка подключаемых route к приложению."""
    from currency.views import currency_route

    app.include_router(currency_route)
