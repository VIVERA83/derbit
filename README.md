# Derbit

___


<span id="0"></span>

### <span id="1">1. </span><span style="color:purple">Описание</span>

Сервис для криптобиржи [Deribit](https://www.deribit.com/ru/). Раз в минуту сервис делает запрос к api биржи за данными
по текущей цене [BTC (БИТКОИН)](https://ru.wikipedia.org/wiki/%D0%91%D0%B8%D1%82%D0%BA%D0%BE%D0%B9%D0%BD) и
[ETH (Эфириум)](https://en.wikipedia.org/wiki/Ethereum) полученные данные сохраняются в базу данных.
Для работы с сохраненными данными есть Api:

* </span><span style="color:orange">__/all__ получить все данные по криптовалюте</span>
* </span><span style="color:orange">__/last__ получить последний запись по криптовалюте</span>
* </span><span style="color:orange">__/get_between__ получить данные по криптовалюте за период</span>

__Подробная информация по Api:__

- Swagger документация http://127.0.0.1:8000/docs
- Swagger(альтернатива) http://127.0.0.1:8000/redoc

  Точная ссылка к документации выводится в логах при запуске сервиса.

___

### <span id="2">2. </span><span style="color:purple">Запуск сервиса</span>

* </span><span style="color:orange">__Клонируем репозиторий:__</span>

```bash
git clone git@github.com:VIVERA83/derbit.git
```

* </span><span style="color:orange">__Переходи в папку с проектом:__</span>

```bash
cd derbit
```

* </span><span style="color:orange">__Создаем файл .env (с переменными окружения) на основе
  примера [.env_example](.env_example)*:__</span>

```bash
echo "COMPOSE_PROJECT_NAME="derbit"
# Настройка приложения
LOGGING_LEVEL="DEBUG"
LOGGING_GURU="1"
HOST="0.0.0.0"
PORT=8004
TRACEBACK="False"

# Настройка Postgres
POSTGRES__DB=test_db
POSTGRES__USER=test_user
POSTGRES__PASSWORD=password
POSTGRES__HOST=postgres_derbit
POSTGRES__PORT=5432
POSTGRES__DB_SCHEMA=derbit

POSTGRES_DB="${POSTGRES__DB}"
POSTGRES_USER="${POSTGRES__USER}"
POSTGRES_PASSWORD="${POSTGRES__PASSWORD}"
POSTGRES_HOST="${POSTGRES__HOST}"
POSTGRES_PORT="${POSTGRES__PORT}"

#app
LOGGING__GURU=True
LOGGING__TRACEBACK=True
" >>.env
```

В ОС windows можно скопировать фаил [.env_example](.env_example) в `.env` командой `copy`, это будет равнозначно команде
выше

```shell
copy /Y ".env_example" ".env"
```

* </span><span style="color:orange">__Запускаем приложение в контейнере:__</span>

```bash
docker-compose up --build
```


### <span id="3">3. </span><span style="color:purple">Техническое описание реализации сервиса </span>
__Стек__:
1. asyncio
2. aiohttp
3. apscheduler
4. sqlalchemy 2.0+ (async)
5. postgresql
6. fastapi
7. dataclasses
8. pytest-asyncio/pytest

Физически сервис состоит из трех компонентов
1. [Внутренний сервис](internal_service)
2. [Внешний сервис](external_service)
3. База данных PostgresSQL
* </span><span style="color:orange">__Внутренний сервис:__</span>
   - __Задача:__ внутреннего сервиса обращаться с периодичностью в 1 минуту за данными по крипте и записывать 
полученные данные в БД. 
   - __Реализация:__ Сервис при старте поднимает соединение с БД и [биржей](internal_service%2Fstore%2Fws%2Fws_accessor.py) 
по web socket`у, далее поднимается [планировщик](internal_service%2Fstore%2Fscheduler%2Faccessor.py) и формируется 
[задание](internal_service%2Fstore%2Fscheduler%2Fmanager.py) на получение данных по валютам и запись в БД. 
Так как, данные по обеим валютам приходили практически мгновенно возникала конкуренция за соединение с БД в
результате чего, терялась информация по одной из валют. Для решения данной проблемы используется синхронизатор Lock
из asyncio. К сожалению подключиться к websocket``у биржи не всегда удается с первого раза, для решения данной проблемы 
используется [декоратор before_execution](internal_service%2Fbase%2Futils.py) который в течение минуты делает попытки выполнения метода отвечающего за соединение с биржей.   
За основу взят aiohttp, apscheduler, asyncio, sqlalchemy 2.0+ (async), dataclasses
   - __Возможный альтернативный вариант реализации:__ Можно пученные данные от планировщика класть в очередь которую 
слушает Worker. Задача Worker класть данные в БД.
* </span><span style="color:orange">__Внешний сервис:__</span>
  - __Задача:__ Отработка запросов к api на полученные данные из БД.
  - __Реализация:__ Сервис при старте поднимает соединение с [БД](external_service%2Fstore%2Fdatabase%2Fdatabase.py)
При получении данных от клиента проводится валидация полученных данных и в случае если данные корректны выполняется 
запрос к БД с последующим возвратом клиенту. В случае получения некорректных данных клиент получает сообщение об 
ошибке с указанием причины ошибки.
За основу взят fastapi, asyncio, sqlalchemy 2.0+ (async), dataclasses
