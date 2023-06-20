"""Полезные утилиты используемые в приложении."""
import logging
from asyncio import Event, create_task, sleep, wait_for
from functools import wraps
from random import randint
from typing import Any, Callable


async def timeout(event: Event, time_out: int) -> True:
    """Вспомогательная функция которая по истечению time_out снимает блокировку с события event."""
    await sleep(time_out)
    event.set()
    return True


def delta_time() -> float:
    """Возвращает случайное число в миллисекундах.

    Применяется для того что бы минимизировать вероятность одномоментного
    обращение к одному сервису большого количества обращений.
    """
    return randint(100, 1000) / 1000


def before_execution(
    total_timeout=10,
    request_timeout: int = 3,
    logger: logging.Logger = logging.getLogger(),
    raise_exception: bool = False,
) -> Any:
    """Декоратор, который пытается выполнить входящий вызываемый объект.

    В течении определенного времянки которое указано в параметре `total_timeout`,
    пытается выполнить функцию или другой вызываемый объект.
    В случае неудачной попытки, засыпает на время указанное в `request_timeout` + delta_time(),
    и делает следующею попытку до тех пор, пока не наступит одно из событий:
        1. Общее время выполнения превысило `total_timeout`, и тогда возвращается None
        2. Вызываемый объект `func` выполнился, и тогда возвращается результат выполнения `func`.
    `raise_exception` - True: в конце выполнения функции при не удачной попытки
    инициализируется исключение.
                      - False: в конце выполнения функции при не удачной попытки вернется None

    Неудачная попытка выводится в лог. В качестве люггера по умолчанию можно использовать loguru
    https://pypi.org/project/loguru/
    """

    def func_wrapper(func: Callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            # по сути засекаем время которое будет работать цикл
            event = Event()  # event блокирует выход из цикла
            create_task(timeout(event, total_timeout))
            error = None
            while not event.is_set():
                try:
                    task = create_task(func(*args, **kwargs))
                    result = await wait_for(task, request_timeout)
                    # отменяем запущенный таймаут если он еще не кончился
                    if not task.done():
                        task.cancel()
                    return result
                except Exception as ex:  # pylint: disable=W0718
                    error = ex
                    sec = randint(0, 1) + delta_time()
                    logger.error(
                        f"Error during execution of the called object"
                        f" '{func.__name__}': : {str(ex)}"
                    )

                await sleep(sec)
            logger.warning(f" Failed to execute: {func.__name__}")
            if raise_exception:
                raise error
            return None

        return inner

    return func_wrapper
