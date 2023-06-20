# Derbit

___

### [Список полезных команд](docs%2Fcommand.md)

<span id="0"></span>

### <span id="1">1. </span><span style="color:purple">Описание</span>

Описание API Сервиса

__При запуске локально:__

- Swagger документация http://127.0.0.1:8000/docs
- Swagger(альтернатива) http://127.0.0.1:8000/redoc

  Точная ссылка к документации выводится в логах при запуске сервиса.

___

### <span id="2">2. </span><span style="color:purple">Запуск сервиса</span>

* </span><span style="color:orange">__Клонируем репозиторий:__</span>

```bash

```

* </span><span style="color:orange">__Переходи в папку с проектом:__</span>

```bash
cd derbit
```

* </span><span style="color:orange">__Создаем файл .env (с переменными окружения) на основе
  примера [.env_example](.env_example)*:__</span>

```bash
echo "COMPOSE_PROJECT_NAME="renovation_api"
# Настройка приложения
SECRET_KEY="hello world"
HOST="0.0.0.0"
PORT=8000
LOGGING__LEVEL="INFO"
LOGGING__TRACEBACK="True"

POSTGRES__DB="test_db"
POSTGRES__USER="test_user"
POSTGRES__PASSWORD="pass"
POSTGRES__HOST="postgres_renovation_api"
POSTGRES__PORT=5432
POSTGRES__DB_SCHEMA="renovation"

# Настройка Postgres
POSTGRES_DB="test_db"
POSTGRES_USER="test_user"
POSTGRES_PASSWORD="pass"

# Настройка Uvicorn
UVICORN_WORKERS=3
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

* </span><span style="color:orange">__Запускаем приложение локально:__</span>

Обратите внимание, что требуется подключение к PostgresSQL

```bash
python internal_service/main.py
python external_service/main.py
```
