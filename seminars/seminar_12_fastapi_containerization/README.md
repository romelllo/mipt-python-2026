# Семинар 12: Контейнеризация FastAPI-приложения

**Модуль:** 3 — Создание Web-сервисов на Python  
**Дата:** 20.04.2026  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1tjzCpI_ahr2ihYmoC2zn-QdwYaXezlpTLMSTutAst10/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:

- **Писать** Dockerfile для FastAPI-приложения и объяснять отличия от Django Dockerfile
- **Настраивать** двухконтейнерный стек (FastAPI + PostgreSQL) через `docker-compose.yml`
- **Запускать** Alembic-миграции как часть `docker compose up` с корректным порядком зависимостей
- **Управлять** конфигурацией через переменные окружения и `.env`-файлы, не допуская утечки секретов

---

## Подготовка

```bash
# Убедитесь, что Docker установлен
docker --version          # Docker version 24+
docker compose version    # Docker Compose version v2+

# Перейдите в директорию с примерами
cd seminars/seminar_12_fastapi_containerization/examples

# Скопируйте .env.example в .env и при необходимости отредактируйте
cp .env.example .env

# Соберите образ и запустите все сервисы
docker compose up --build

# В другом терминале: проверьте работу API
curl http://localhost:8000/health
# → {"status":"ok"}

# Swagger UI: http://localhost:8000/docs
```

---

## План семинара

Семинар построен по принципу **«теория → практика»**: после каждого блока теории переходите к соответствующим упражнениям в файле [`exercises/exercises.md`](exercises/exercises.md).

| Время | Тема | Практика |
|-------|------|----------|
| 20 мин | Блок 1: Dockerfile для FastAPI | → Упражнения: Часть 1 |
| 20 мин | Блок 2: Двухконтейнерный стек (db + web) | → Упражнения: Часть 2 |
| 20 мин | Блок 3: Alembic-миграции в Docker Compose | → Упражнения: Часть 3 |
| 15 мин | Блок 4: Переменные окружения и секреты | → Упражнения: Часть 4 |
| 5 мин | Интерактив: ситуационные задачи (Chat Polls) | → Упражнения: Часть 5 |
| 10 мин | Подведение итогов | — |

**Итого:** ~80 мин теории + практика + 10 мин итоги = ~90 минут

---

## Блок 1: Dockerfile для FastAPI (20 мин)

> **Контекст:** в семинаре 08 вы уже написали Dockerfile для Django. Здесь мы разберём, что меняется для FastAPI, и почему.

Dockerfile — это пошаговая инструкция для сборки Docker-образа. Каждая инструкция создаёт новый **слой** (layer). Docker кеширует слои: если слой не изменился, он берётся из кеша — это ускоряет повторные сборки.

### Ключевые отличия FastAPI Dockerfile от Django

| Аспект | Django (семинар 08) | FastAPI (этот семинар) |
|--------|---------------------|------------------------|
| Сервер | `gunicorn` (WSGI) | `uvicorn` (ASGI) |
| Статика | `collectstatic` | Не нужно |
| Миграции | `manage.py migrate` | `alembic upgrade head` |
| Системные зависимости | `gcc` | `gcc` + `libpq-dev` |

### Структура Dockerfile

**Проблема:** если копировать весь код перед установкой зависимостей, Docker будет переустанавливать все пакеты при каждом изменении кода.
**Решение:** сначала копируем `requirements.txt`, устанавливаем зависимости, потом копируем код.

```dockerfile
FROM python:3.11-slim

# Отключаем .pyc файлы и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Системные зависимости для psycopg2 (PostgreSQL драйвер)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала зависимости (кеш слоёв!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Потом код
COPY . .

# Непривилегированный пользователь (безопасность)
RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser \
    && chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

# Healthcheck — Docker проверяет /health каждые 30 секунд
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c \
    "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" \
    || exit 1

# uvicorn вместо gunicorn — FastAPI использует ASGI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### Почему `PYTHONUNBUFFERED=1`?

Без этой переменной Python буферизует вывод `print()` и `logging`. В контейнере это означает, что логи появляются в `docker logs` с задержкой или не появляются вовсе при аварийном завершении. `PYTHONUNBUFFERED=1` отключает буферизацию — логи видны сразу.

### Healthcheck — зачем он нужен?

`HEALTHCHECK` позволяет Docker знать, что приложение не просто запущено, но и **отвечает на запросы**. Это критично для `depends_on` с `condition: service_healthy` в docker-compose (Блок 2).

> **Подробнее:** см. файл [`examples/Dockerfile`](examples/Dockerfile) — полный Dockerfile с подробными комментариями к каждой инструкции.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 1: Dockerfile для FastAPI** (задания 1.1–1.2).

---

## Блок 2: Двухконтейнерный стек (db + web) (20 мин)

> **Контекст:** в семинаре 08 вы видели базовый `docker-compose.yml` с Django + SQLite. Здесь мы добавляем PostgreSQL как отдельный сервис и настраиваем правильный порядок запуска.

В реальных проектах FastAPI никогда не работает в одиночку — ему нужна база данных. `docker-compose.yml` описывает **все сервисы** и их связи.

### Архитектура двухконтейнерного стека

```
┌─────────────────────────────────────────┐
│           Docker Network: app_network    │
│                                         │
│  ┌──────────────┐    ┌───────────────┐  │
│  │   web        │    │   db          │  │
│  │  (FastAPI)   │───▶│  (PostgreSQL) │  │
│  │  port: 8000  │    │  port: 5432   │  │
│  └──────────────┘    └───────────────┘  │
│         │                    │          │
└─────────┼────────────────────┼──────────┘
          │                    │
     localhost:8000      (не доступен
     (браузер/curl)       снаружи сети)
```

Ключевой момент: **PostgreSQL не пробрасывает порт наружу**. Он доступен только внутри сети `app_network`. Это правильная практика безопасности.

### Имя сервиса как хост

В Docker Compose контейнеры в одной сети видят друг друга **по имени сервиса**. Поэтому в `DATABASE_URL` хост — это `db`, а не `localhost`:

```
DATABASE_URL=postgresql://user:pass@db:5432/tasks_db
#                                    ^^
#                          имя сервиса в docker-compose.yml
```

### `depends_on` с `condition: service_healthy`

**Проблема:** `web` стартует раньше, чем `db` готов принимать соединения → `alembic upgrade head` падает.
**Решение:** `depends_on` с `condition: service_healthy` — `web` ждёт, пока `db` пройдёт healthcheck.

```yaml
services:
  db:
    image: postgres:15-alpine
    env_file: .env
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 10s
    networks:
      - app_network

  web:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    command: >
      sh -c "alembic upgrade head &&
             uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2"
    depends_on:
      db:
        condition: service_healthy   # ← ждём healthcheck db
    networks:
      - app_network

volumes:
  postgres_data:

networks:
  app_network:
    driver: bridge
```

### Volumes — постоянное хранилище

Без `volumes` данные PostgreSQL **теряются** при `docker compose down`. Именованный volume `postgres_data` сохраняет данные между перезапусками.

```bash
docker volume ls                          # список volumes
docker volume inspect seminar_12_postgres_data  # детали
docker compose down -v                    # удалить контейнеры И volumes (ДАННЫЕ УДАЛЯТСЯ!)
```

> **Подробнее:** см. файл [`examples/docker-compose.yml`](examples/docker-compose.yml) — полный compose-файл с комментариями к каждой секции.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 2: Двухконтейнерный стек** (задания 2.1–2.3).

---

## Блок 3: Alembic-миграции в Docker Compose (20 мин)

> **Контекст:** в семинаре 08 Django-миграции запускались через `manage.py migrate`. В FastAPI-стеке мы используем Alembic — более гибкий инструмент, но требующий явной настройки.

### Почему Alembic, а не `Base.metadata.create_all()`?

`Base.metadata.create_all(engine)` создаёт таблицы, но **не умеет их изменять**. Если вы добавили поле в модель — `create_all` не добавит колонку в существующую таблицу. Alembic решает эту проблему: он хранит историю изменений схемы и применяет их инкрементально.

| | `create_all` | Alembic |
|--|--|--|
| Создание таблиц | ✓ | ✓ |
| Изменение схемы | ✗ | ✓ |
| История миграций | ✗ | ✓ |
| Откат изменений | ✗ | ✓ (`downgrade`) |

### Как Alembic читает DATABASE_URL в Docker

`env.py` — ключевой файл Alembic. Он читает `DATABASE_URL` из переменной окружения и передаёт в SQLAlchemy:

```python
# app/alembic/env.py
import os
from app.database import Base
from app.models import Task  # noqa: F401 — импорт нужен для автогенерации

config = context.config

# Читаем DATABASE_URL из окружения (задаётся в docker-compose.yml)
database_url = os.environ.get("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata  # Alembic знает о всех таблицах
```

**Важно:** все модели должны быть импортированы в `env.py` — иначе Alembic не увидит их при автогенерации (`--autogenerate`).

### Запуск миграций в docker-compose

Миграции запускаются в `command` сервиса `web`, **после** того как `db` прошёл healthcheck:

```yaml
web:
  command: >
    sh -c "alembic upgrade head &&
           uvicorn app.main:app --host 0.0.0.0 --port 8000"
  depends_on:
    db:
      condition: service_healthy
```

### Основные команды Alembic

```bash
# Внутри контейнера (docker compose exec web <команда>):

# Создать новую миграцию автоматически (сравнивает модели с БД)
alembic revision --autogenerate -m "add priority field to tasks"

# Применить все pending миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1

# Посмотреть текущую ревизию БД
alembic current

# История всех миграций
alembic history --verbose
```

### Workflow разработки с Alembic в Docker

```
1. Изменили модель (models.py)
         ↓
2. docker compose exec web alembic revision --autogenerate -m "описание"
         ↓
3. Проверили сгенерированный файл миграции (app/alembic/versions/)
         ↓
4. docker compose exec web alembic upgrade head
         ↓
5. Проверили изменения в БД
```

> **Подробнее:** см. файл [`examples/app/alembic/env.py`](examples/app/alembic/env.py) — полный `env.py` с комментариями. [`examples/alembic.ini`](examples/alembic.ini) — конфигурация Alembic.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 3: Alembic-миграции** (задания 3.1–3.2).

---

## Блок 4: Переменные окружения и секреты (15 мин)

> **Контекст:** в семинаре 08 переменные окружения задавались прямо в `docker-compose.yml` через `environment:`. Это удобно, но небезопасно для секретов. Разберём правильный подход.

### Три способа передать переменные в контейнер

```yaml
# Способ 1: inline в docker-compose.yml (НЕ для секретов!)
environment:
  - DEBUG=0
  - POSTGRES_USER=taskuser
  - SECRET_KEY=my_secret  # ← ПЛОХО: секрет в git!

# Способ 2: env_file — читать из файла (добавьте .env в .gitignore)
env_file:
  - .env                  # ← ХОРОШО для разработки

# Способ 3: передать конкретную переменную из окружения хоста
environment:
  - SECRET_KEY             # ← без значения: берётся из окружения хоста
```

### Структура `.env` файла

```bash
# .env (НЕ коммитить в git!)
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=super_secret_password_123
POSTGRES_DB=tasks_db
DATABASE_URL=postgresql://taskuser:super_secret_password_123@db:5432/tasks_db
SECRET_KEY=a3f8b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
DEBUG=0
```

### `.env.example` — безопасный шаблон для команды

Коммитьте в git только `.env.example` с примерами значений (без реальных секретов):

```bash
# .env.example (безопасно коммитить)
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=changeme_use_strong_password_here
POSTGRES_DB=tasks_db
DATABASE_URL=postgresql://taskuser:changeme@db:5432/tasks_db
SECRET_KEY=replace_with_random_64_char_hex_string
DEBUG=0
```

### Чтение переменных в FastAPI-приложении

```python
# app/database.py
import os

# os.getenv возвращает None если переменная не задана
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "sqlite:///./tasks.db",  # fallback для локальной разработки
)
```

### Правила безопасности

| Правило | Почему |
|---------|--------|
| `.env` в `.gitignore` | Секреты не попадают в git-историю |
| `.env.example` в git | Команда знает, какие переменные нужны |
| Не хардкодить секреты в `docker-compose.yml` | Compose-файл часто коммитится |
| Генерировать `SECRET_KEY` случайно | `python -c "import secrets; print(secrets.token_hex(32))"` |
| В production — использовать Vault/AWS Secrets Manager | `.env` файлы не масштабируются |

> **Подробнее:** см. файл [`examples/.env.example`](examples/.env.example) — шаблон с комментариями к каждой переменной.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 4: Переменные окружения** (задания 4.1–4.2).

---

## Подведение итогов

### Шпаргалка

| Концепция | Ключевое |
|-----------|----------|
| `FROM python:3.11-slim` | Минимальный базовый образ |
| `COPY requirements.txt .` перед `COPY . .` | Кеш слоёв Docker |
| `PYTHONUNBUFFERED=1` | Логи видны сразу в `docker logs` |
| `HEALTHCHECK` | Docker знает, что приложение отвечает |
| `USER appuser` | Не запускать от root |
| `uvicorn` вместо `gunicorn` | FastAPI — ASGI, не WSGI |
| `image: postgres:15-alpine` | Лёгкий образ PostgreSQL |
| `pg_isready` в healthcheck | Проверка готовности PostgreSQL |
| `depends_on: condition: service_healthy` | Web ждёт готовности db |
| Имя сервиса как хост | `@db:5432` вместо `@localhost:5432` |
| `volumes:` | Данные PostgreSQL не теряются при перезапуске |
| `networks:` | Изоляция: db не доступен снаружи |
| `alembic upgrade head` в `command:` | Миграции при каждом старте |
| `env.py` читает `DATABASE_URL` из env | Один alembic.ini для всех окружений |
| `env_file: .env` | Секреты не в docker-compose.yml |
| `.env` в `.gitignore` | Секреты не в git |
| `.env.example` в git | Документация нужных переменных |

### Ключевые выводы

1. **FastAPI Dockerfile отличается от Django Dockerfile** в трёх местах: `uvicorn` вместо `gunicorn`, `libpq-dev` для PostgreSQL, нет `collectstatic`. Всё остальное — те же принципы.

2. **`depends_on: condition: service_healthy` — обязательно** при использовании Alembic в compose. Без него миграции упадут, потому что PostgreSQL ещё не готов.

3. **Секреты — в `.env`, не в `docker-compose.yml`.** Compose-файл коммитится в git. `.env` — нет. Это единственное правило, которое нельзя нарушать.

---

## Файлы семинара

```
seminar_12_fastapi_containerization/
├── README.md                          # Этот файл
├── examples/
│   ├── Dockerfile                     # Dockerfile для FastAPI
│   ├── docker-compose.yml             # Стек: db (PostgreSQL) + web (FastAPI)
│   ├── .env.example                   # Шаблон переменных окружения
│   ├── .dockerignore                  # Исключения из контекста сборки
│   ├── requirements.txt               # Зависимости Python
│   ├── alembic.ini                    # Конфигурация Alembic
│   └── app/
│       ├── __init__.py
│       ├── main.py                    # FastAPI-приложение (Tasks API)
│       ├── models.py                  # SQLAlchemy ORM-модели
│       ├── database.py                # Подключение к БД, get_db dependency
│       └── alembic/
│           ├── __init__.py
│           ├── env.py                 # Конфигурация Alembic (читает DATABASE_URL)
│           └── versions/
│               └── README.md          # Пример сгенерированной миграции
└── exercises/
    └── exercises.md                   # Практические задания
```

---

## Дополнительные материалы

- [FastAPI — Deployment with Docker](https://fastapi.tiangolo.com/deployment/docker/) — официальное руководство FastAPI по Docker, включая multi-stage builds
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) — официальный туториал: создание миграций, autogenerate, downgrade
- [Docker Compose — depends_on](https://docs.docker.com/compose/how-tos/startup-order/) — официальная документация по порядку запуска сервисов
- [12 Factor App — Config](https://12factor.net/config) — методология хранения конфигурации в переменных окружения
- [Real Python — Docker for Python](https://realpython.com/docker-in-action-fitter-happier-more-productive/) — практическое руководство по Docker для Python-разработчиков
