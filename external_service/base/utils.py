"""Полезные утилиты используемые в приложении."""
import logging
from asyncio import Event, create_task, get_event_loop, sleep, wait_for
from concurrent import futures
from functools import wraps
from inspect import iscoroutinefunction
from random import randint
from typing import Any, Callable

__all__ = ["before_execution"]


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
    fix_error: Callable = None,
) -> Any:
    """Декоратор, который пытается выполнить входящий вызываемый объект.

    В течении определенного времянки которое указано в параметре `total_timeout`,
    пытается выполнить функцию или другой вызываемый объект.
    В случае неудачной попытки, засыпает на время указанное в `request_timeout` + delta_time(),
    и делает следующею попытку до тех пор, пока не наступит одно из событий:
        1. Общее время выполнения превысило `total_timeout`, и тогда возвращается None
        2. Вызываемый объект `func` выполнился, и тогда возвращается результат выполнения `func`.
    `raise_exception` - True: в конце выполнения функции при не удачной попытки инициализируется исключение.
                      - False: в конце выполнения функции при не удачной попытки вернется None
    `fix_error`: вызываемый объект, задача которого попробовать исправить ошибку, возникшую в результате выполнения.

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
                    if error and fix_error:
                        fix_task = create_task(run_method(fix_error, *args, **kwargs))
                        await wait_for(fix_task, request_timeout)
                    task = create_task(run_method(func, *args, **kwargs))
                    result = await wait_for(task, request_timeout)
                    # отменяем запущенный таймаут если он еще не кончился
                    if not task.done():
                        task.cancel()

                    return result
                except Exception as ex:
                    error = ex
                    sec = randint(0, 1) + delta_time()
                    logger.error(
                        f"Error during execution of the called object '{func.__name__}': : {str(ex)}"
                    )

                await sleep(sec)

            logger.warning(f" Failed to execute: {func.__name__}")
            if raise_exception:
                raise error
            return None

        return inner

    return func_wrapper


def backoff(
    request_timeout: int = 3,
    logger: logging.Logger = logging.getLogger(),
) -> Any:
    """Декоратор, который пытается выполнить входящий вызываемый объект.

    Вечно пытается выполнить функцию или другой вызываемый объект.
    В случае неудачной попытки, засыпает на время указанное в `request_timeout` + delta_time(),
    и делает следующею попытку до тех пор, пока не наступит событие:
        1. Вызываемый объект `func` выполнился, и тогда возвращается результат выполнения `func`.

    Неудачная попытка выводится в лог. В качестве люггера по умолчанию можно использовать loguru
    https://pypi.org/project/loguru/
    """

    def func_wrapper(func: Callable):
        @wraps(func)
        async def inner(*args, **kwargs):
            while True:
                try:
                    task = create_task(run_method(func, *args, **kwargs))
                    return await wait_for(task, request_timeout)
                except Exception as ex:
                    sec = randint(0, 1) + delta_time()
                    logger.error(
                        f"Error during execution of the called object '{func.__name__}': : {str(ex)}"
                    )
                await sleep(sec)

        return inner

    return func_wrapper


async def run_method(func: Callable, *args, **kwargs) -> Any:
    """
    Запускает переданный вызываемый объект.

    В соответствии от типа, если объект не поддерживает асинхронный запуск
    он запускается в отдельном пуле. В случае возникновения ошибки в процессе исполнения объекта будет
    возвращено исключение.
    :param func: Любой объект который можно вызвать. Пример: foo()
    :param kwargs: именованные атрибуты для запуска. Пример: foo(**kwargs)
    :return: какой-то результат
    """
    try:
        if iscoroutinefunction(func):
            if args or kwargs:
                return await func(*args, **kwargs)
            else:
                return await func()
        elif kwargs:
            with futures.ProcessPoolExecutor() as pool:
                return await get_event_loop().run_in_executor(
                    pool, func, *args, *kwargs.values()
                )
        else:
            with futures.ProcessPoolExecutor() as pool:
                return await get_event_loop().run_in_executor(pool, func)
    except Exception as e:
        # конкретную ошибку не отследить так как она зависит от вызываемого метода,
        # который может быть чем угодно
        logging.error(
            f"Error during execution of the called object '{func.__name__}': : {str(e)}"
        )
        raise Exception(str(e))
