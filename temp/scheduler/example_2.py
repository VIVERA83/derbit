import asyncio
from asyncio import sleep

from apscheduler.schedulers.asyncio import AsyncIOScheduler

# функция - задание
counter = 0


async def prompt():
    global counter
    counter += 1
    print("Executing Task...{}".format(counter))


async def main():
    # Создает ФОНОВЫЙ планировщик
    scheduler = AsyncIOScheduler()
    # планирование задания
    scheduler.add_job(prompt, "interval", seconds=5)
    # Запуск запланированных заданий
    scheduler.start()
    try:
        while True:
            await sleep(1)
    except asyncio.CancelledError:
        print("Stop")
        pass
    scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
