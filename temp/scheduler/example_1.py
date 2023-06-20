from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler

# Создает ФОНОВЫЙ планировщик
scheduler = BackgroundScheduler()


# функция - задание
def prompt():
    print("Executing Task...")


# планирование задания
scheduler.add_job(prompt, "interval", seconds="5")

# Запуск запланированных заданий
scheduler.start()

# Запускает бесконечный цикл
while True:
    sleep(1)
