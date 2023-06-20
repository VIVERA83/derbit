"""Логирование."""
import logging
import sys
import typing

from loguru import logger

if typing.TYPE_CHECKING:
    from core.components import Application


def setup_logging(app: "Application") -> None:
    """Настройка логирования в приложении.

    В данном случае есть вариант использовать loguru.
    https://github.com/Delgan/loguru
    """
    if app.settings.logging.guru:
        logger.configure(
            **{
                "handlers": [
                    {
                        "sink": sys.stderr,
                        "level": app.settings.logging.level,
                        "backtrace": app.settings.logging.traceback,
                    },
                ],
            }
        )
        app.logger = logger
    else:
        logging.basicConfig(level=app.settings.logging.level)
        app.logger = logging
    app.logger.info("Starting logging")
