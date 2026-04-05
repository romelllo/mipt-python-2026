# Семинар 10: Работа с данными в FastAPI

**Модуль:** 3 — Создание Web-сервисов на Python  
**Дата:** 06.04.2026  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1WF0hyQvlxm1CfT_u6_l7UBDejTPrtdnlNZqQxy8MguE/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:

- **Называть** компоненты SQLModel и объяснять, как он объединяет SQLAlchemy и Pydantic
- **Настраивать** PostgreSQL в Docker и подключать FastAPI-приложение через `DATABASE_URL`
- **Реализовывать** асинхронный `db.py` с async engine, `async_sessionmaker` и dependency injection через `Depends(get_session)`
- **Писать** полный async CRUD (SELECT, INSERT, UPDATE, DELETE) с SQLModel и вызывать внешние HTTP-сервисы через `httpx.AsyncClient`
- **Создавать** и применять Alembic-миграции для управления схемой базы данных

> **Важно:** Понимание async/await — необходимое условие. Без него работа с базой данных в FastAPI превращается в магию. Прежде чем читать дальше — убедитесь, что вы понимаете, чем `async def` отличается от `def` и почему `await` не блокирует event loop.

---

## Подготовка

```bash
# 1. Активируйте виртуальное окружение
source .venv/bin/activate  # Linux/Mac

# 2. Новые зависимости уже добавлены в pyproject.toml
#    (sqlmodel, asyncpg, alembic, psycopg2-binary)
uv sync

# 3. Проверьте установку
python -c "import sqlmodel; print('sqlmodel:', sqlmodel.__version__)"
python -c "import alembic; print('alembic:', alembic.__version__)"
python -c "import asyncpg; print('asyncpg OK')"

# 4. Запустите PostgreSQL через Docker
cd seminars/seminar_10_fastapi_data_handling
docker compose up -d

# Проверьте, что PostgreSQL доступен:
docker compose ps
# или:
docker exec -it $(docker ps -qf "name=db") psql -U postgres -c "\l"

# 5. Запустите примеры, не требующие Docker:
cd ../..   # вернитесь в корень репозитория
python seminars/seminar_10_fastapi_data_handling/examples/01_sqlmodel_intro.py
python seminars/seminar_10_fastapi_data_handling/examples/03_external_service.py

# 6. Запустите полное API (нужен Docker):
uvicorn seminars.seminar_10_fastapi_data_handling.examples.02_async_db.main:app --reload
# → Swagger UI: http://127.0.0.1:8000/docs
```

---

## План семинара

Семинар построен по принципу **«теория → практика»**: после каждого блока теории сразу переходите к соответствующим упражнениям в файле [`exercises/exercises.md`](exercises/exercises.md).

| Время | Тема | Практика |
|-------|------|----------|
| 20 мин | Блок 1: SQLModel + PostgreSQL в Docker | → Упражнения: Часть 1 |
| 20 мин | Блок 2: `app/db.py` — асинхронная сессия | → Упражнения: Часть 2 |
| 20 мин | Блок 3: Async CRUD с БД + внешние сервисы | → Упражнения: Часть 3 |
| 20 мин | Блок 4: Миграции с Alembic | → Упражнения: Часть 4 |
| 10 мин | Подведение итогов | — |

**Итого:** ~90 минут

---

## Блок 1: SQLModel + PostgreSQL в Docker (20 мин)

**SQLModel** — библиотека от автора FastAPI (Sebastián Ramírez), которая объединяет две вещи:
- **SQLAlchemy ORM** — работа с базой данных, таблицами, транзакциями
- **Pydantic** — валидация данных, сериализация, JSON-схема

Результат: один класс вместо двух. `Note(table=True)` — это одновременно таблица в PostgreSQL **и** Pydantic-модель.

### Три вида классов SQLModel

| Класс | `table=` | Назначение |
|-------|----------|-----------|
| `Note(SQLModel, table=True)` | `True` | Таблица в БД (ORM-модель) |
| `NoteCreate(SQLModel)` | нет | Pydantic-схема для входных данных |
| `NoteResponse(SQLModel)` | нет | Pydantic-схема для ответа API |

```python
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class NoteBase(SQLModel):
    """Общие поля — без id и created_at."""
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(default="")

class Note(NoteBase, table=True):
    """Таблица notes в PostgreSQL."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class NoteCreate(NoteBase):
    """Что клиент отправляет — только title и content."""

class NoteResponse(NoteBase):
    """Что сервер возвращает — включает id и created_at."""
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}
```

### PostgreSQL в Docker

Файл `docker-compose.yml` в директории семинара запускает PostgreSQL 16:

```bash
cd seminars/seminar_10_fastapi_data_handling
docker compose up -d     # запустить в фоне
docker compose ps        # проверить статус
docker compose down      # остановить
docker compose down -v   # остановить и удалить данные (volume)
```

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: notes_db
    ports:
      - "5432:5432"
```

**`DATABASE_URL`** — строка подключения для async драйвера:

```
postgresql+asyncpg://postgres:postgres@localhost:5432/notes_db
│              │         │        │         │         │
protocol    async      user    password   host      db name
           driver
```

### CRUD с синхронным Session (для понимания основ)

```python
from sqlmodel import Session, create_engine, select

engine = create_engine("sqlite:///:memory:")
SQLModel.metadata.create_all(engine)

# INSERT
with Session(engine) as session:
    note = Note(title="Привет", content="SQLModel!")
    session.add(note)
    session.commit()
    session.refresh(note)  # получить id из БД
    print(note.id)  # → 1

# SELECT
with Session(engine) as session:
    notes = session.exec(select(Note)).all()

# SELECT по ID
with Session(engine) as session:
    note = session.get(Note, 1)  # None если нет
```

**Когда использовать:** `Session` (синхронный) — для скриптов и задач без async. В FastAPI используйте `AsyncSession`.

> **Подробнее:** см. файл [`examples/01_sqlmodel_intro.py`](examples/01_sqlmodel_intro.py) — полный рабочий пример с SQLite in-memory: CREATE, INSERT, SELECT, UPDATE, DELETE. Запускается без Docker.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 1: SQLModel + PostgreSQL в Docker** (задания 1.1–1.2).

---

## Блок 2: `app/db.py` — асинхронная сессия (20 мин)

В FastAPI с PostgreSQL все операции с БД должны быть **асинхронными** — иначе они заблокируют event loop и сервер перестанет отвечать на другие запросы.

### Три компонента async БД

**1. Async Engine** — точка входа для всех соединений:

```python
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/notes_db"

async_engine = create_async_engine(DATABASE_URL, echo=True)
# echo=True — выводить SQL в консоль (удобно при разработке)
```

**2. `async_sessionmaker`** — фабрика сессий:

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # объекты доступны после commit() без re-select
)
```

**3. Lifespan** — создание таблиц при старте:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: создать таблицы (в production — Alembic!)
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Shutdown: освободить соединения
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)
```

### Dependency Injection: `get_session`

**Проблема:** каждый запрос должен получать свежую сессию и закрывать её после обработки.
**Решение:** `Depends(get_session)` — FastAPI вызывает функцию перед каждым запросом.

```python
from collections.abc import AsyncGenerator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость: открыть сессию → обработать запрос → закрыть."""
    async with AsyncSessionLocal() as session:
        yield session  # сессия передаётся в эндпоинт

# Удобный тип-алиас:
SessionDep = Annotated[AsyncSession, Depends(get_session)]

# Использование в эндпоинте:
@router.get("/notes")
async def list_notes(session: SessionDep) -> list[Note]:
    result = await session.exec(select(Note))
    return list(result.all())
```

**Как работает `yield` в dependency:**
1. FastAPI вызывает `get_session()`
2. Код до `yield` — инициализация (открытие сессии)
3. `yield session` — сессия передаётся в эндпоинт
4. Эндпоинт отрабатывает
5. Код после `yield` — cleanup (сессия закрывается)

> **Подробнее:** см. файл [`examples/02_async_db/db.py`](examples/02_async_db/db.py) — полный рабочий `db.py` с комментариями.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 2: `db.py` — асинхронная сессия** (задания 2.1–2.2).

---

## Блок 3: Async CRUD с БД + внешние сервисы (20 мин)

### Async CRUD с SQLModel

Все операции в `AsyncSession` — это корутины с `await`:

```python
from sqlmodel import select

# CREATE
note = Note(**note_in.model_dump())
session.add(note)
await session.commit()
await session.refresh(note)  # подгрузить id и created_at

# READ ALL (с пагинацией)
result = await session.exec(select(Note).offset(0).limit(100))
notes = list(result.all())

# READ ONE
note = await session.get(Note, note_id)  # None если нет

# UPDATE (паттерн PATCH)
note = await session.get(Note, note_id)
update_data = note_update.model_dump(exclude_unset=True)
for field, value in update_data.items():
    setattr(note, field, value)
session.add(note)
await session.commit()
await session.refresh(note)

# DELETE
note = await session.get(Note, note_id)
await session.delete(note)
await session.commit()
```

**Ключевое:** `session.exec()` в async-режиме нужен `await`. `session.get()` тоже асинхронный.

### Вызов внешних HTTP-сервисов: `httpx.AsyncClient`

**Проблема:** синхронный `requests.get()` блокирует event loop.
**Решение:** `httpx.AsyncClient` — асинхронный HTTP-клиент.

```python
import httpx

async def fetch_external_data(url: str) -> dict:
    """Асинхронный GET-запрос к внешнему API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # HTTPStatusError при 4xx/5xx
        return dict(response.json())
```

### Параллельные запросы: `asyncio.gather()`

```python
import asyncio

# Последовательно: total_time = t1 + t2
note = await session.get(Note, note_id)
external = await fetch_external_data(url)

# Параллельно: total_time = max(t1, t2)
note, external = await asyncio.gather(
    session.get(Note, note_id),
    fetch_external_data(url),
)
```

**Когда использовать `gather()`:** когда несколько async-операций не зависят друг от друга — запускайте их параллельно.

### Типичный паттерн в FastAPI-эндпоинте

```python
@router.get("/{note_id}/enriched")
async def get_enriched_note(note_id: int, session: SessionDep) -> dict:
    """Заметка + данные из внешнего API (параллельно)."""
    note, extra = await asyncio.gather(
        session.get(Note, note_id),
        fetch_external_data("https://api.example.com/data"),
    )
    if note is None:
        raise HTTPException(status_code=404, detail="Не найдено")
    return {"note": note, "extra": extra}
```

> **Подробнее:** см. [`examples/02_async_db/routers/notes.py`](examples/02_async_db/routers/notes.py) — полный async CRUD роутер. И [`examples/03_external_service.py`](examples/03_external_service.py) — демо httpx с параллельными запросами (запускается без Docker).

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 3: Async CRUD + внешние сервисы** (задание 3.1).

---

## Блок 4: Миграции с Alembic (20 мин)

### Зачем миграции?

`SQLModel.metadata.create_all()` — создаёт таблицы **только если их нет**. Если таблица уже существует — ничего не делает. Это значит:
- Добавить колонку в production → вручную или через `ALTER TABLE`
- Откатить изменение схемы → вручную

**Alembic** решает эту проблему: отслеживает историю изменений схемы и применяет/откатывает их воспроизводимо.

| `create_all` | Alembic |
|--------------|---------|
| Создаёт таблицы с нуля | Отслеживает историю изменений |
| Не обновляет существующие | `upgrade` — применить, `downgrade` — откатить |
| Только для разработки | Для production |

### Структура Alembic-проекта

```
04_alembic_demo/
├── alembic.ini          # конфиг (путь к env.py, DATABASE_URL)
├── alembic/
│   ├── env.py           # логика запуска миграций (async!)
│   └── versions/        # файлы миграций (генерируются автоматически)
│       └── 20260406_0001_abc123_create_notes_table.py
├── models.py            # SQLModel-модели (Alembic читает их метаданные)
└── db.py                # async engine
```

### Быстрый старт

```bash
# Перейти в директорию с alembic.ini
cd seminars/seminar_10_fastapi_data_handling/examples/04_alembic_demo

# Сгенерировать миграцию (autogenerate сравнивает модели с текущей схемой БД)
alembic revision --autogenerate -m "create notes table"

# Применить все ожидающие миграции
alembic upgrade head

# Проверить текущую ревизию
alembic current

# История миграций
alembic history

# Откатить последнюю миграцию
alembic downgrade -1

# Откатить до конкретной ревизии
alembic downgrade abc123
```

### Async `env.py` — ключевые части

Alembic — синхронный инструмент, но с async engine нужен специальный `env.py`:

```python
# alembic/env.py (упрощённо)
import asyncio, os
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel
import models  # регистрирует таблицы в метаданных

target_metadata = SQLModel.metadata  # Alembic смотрит сюда при autogenerate

async def run_async_migrations():
    engine = async_engine_from_config(
        config.get_section(config.config_ini_section),
        poolclass=pool.NullPool,  # без пула для миграций
    )
    async with engine.connect() as conn:
        await conn.run_sync(do_run_migrations)
    await engine.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())  # запускаем async из sync контекста
```

### Типичный файл миграции

```python
# alembic/versions/20260406_..._create_notes_table.py
def upgrade() -> None:
    """Применить изменение: создать таблицу."""
    op.create_table(
        "note",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

def downgrade() -> None:
    """Откатить изменение: удалить таблицу."""
    op.drop_table("note")
```

> **Подробнее:** см. директорию [`examples/04_alembic_demo/`](examples/04_alembic_demo/) — рабочий alembic-проект с async `env.py` и `alembic.ini`. Студенты сами генерируют первую миграцию через `alembic revision --autogenerate`.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 4: Миграции с Alembic** (задания 4.1–4.2).

---

## Подведение итогов

### Шпаргалка

| Концепция | Ключевое |
|-----------|---------|
| `SQLModel(table=True)` | ORM-модель = таблица в БД |
| `SQLModel()` (без table) | Pydantic-схема (Create/Update/Response) |
| `create_async_engine(url)` | Async движок для PostgreSQL |
| `async_sessionmaker(...)` | Фабрика AsyncSession |
| `AsyncSession` | Async транзакция с БД |
| `expire_on_commit=False` | Объекты доступны после commit() |
| `lifespan(app)` | Startup/shutdown логика (create_all) |
| `Depends(get_session)` | DI: FastAPI даёт сессию каждому запросу |
| `await session.exec(select(M))` | SELECT * FROM table |
| `await session.get(Model, id)` | SELECT WHERE id = ? |
| `session.add(obj); await session.commit()` | INSERT / UPDATE |
| `await session.refresh(obj)` | Перечитать объект из БД |
| `await session.delete(obj)` | DELETE |
| `model_dump(exclude_unset=True)` | PATCH: только изменённые поля |
| `httpx.AsyncClient` | Async HTTP-клиент (не блокирует event loop) |
| `response.raise_for_status()` | Исключение при 4xx/5xx |
| `asyncio.gather(coro1, coro2)` | Параллельные async-операции |
| `alembic revision --autogenerate` | Сгенерировать миграцию из моделей |
| `alembic upgrade head` | Применить все миграции |
| `alembic downgrade -1` | Откатить последнюю миграцию |
| `pool.NullPool` | Без пула соединений (для миграций) |

### Ключевые выводы

1. **SQLModel = одна модель вместо двух.** Не нужно писать отдельно SQLAlchemy ORM и Pydantic — `table=True` делает класс таблицей, без него — Pydantic-схемой.

2. **`async def` + `await` везде.** В FastAPI с PostgreSQL все операции с БД асинхронные. `Session` → `AsyncSession`, `create_engine` → `create_async_engine`. Синхронный `requests` → `httpx.AsyncClient`. Запускайте независимые запросы параллельно через `asyncio.gather()`.

3. **Alembic вместо `create_all` в production.** `create_all` только создаёт таблицы с нуля — он не поможет добавить колонку в существующую таблицу. Alembic отслеживает историю изменений и воспроизводимо применяет их в любой среде.

---

## Файлы семинара

```
seminar_10_fastapi_data_handling/
├── README.md                              # Этот файл
├── docker-compose.yml                     # PostgreSQL 16 для локальной разработки
├── examples/
│   ├── 01_sqlmodel_intro.py               # SQLModel + SQLite in-memory (без Docker)
│   ├── 02_async_db/                       # Полный async Notes API
│   │   ├── main.py                        # FastAPI app с lifespan
│   │   ├── db.py                          # async engine, SessionDep, get_session
│   │   ├── models.py                      # Note, NoteCreate, NoteUpdate, NoteResponse
│   │   └── routers/
│   │       └── notes.py                   # Async CRUD эндпоинты
│   ├── 03_external_service.py             # httpx.AsyncClient (без Docker)
│   └── 04_alembic_demo/                   # Notes API с Alembic
│       ├── main.py                        # FastAPI app (без create_all — Alembic)
│       ├── db.py                          # async engine
│       ├── models.py                      # Note модель
│       ├── alembic.ini                    # Конфиг Alembic
│       └── alembic/
│           ├── env.py                     # Async-compatible env.py
│           └── versions/                  # Здесь появятся файлы миграций
└── exercises/
    └── exercises.md                       # Практические задания (4 части + бонус)
```

---

## Дополнительные материалы

- [SQLModel — официальная документация](https://sqlmodel.tiangolo.com/) — туториал от автора FastAPI, включая async
- [SQLAlchemy 2.0 — Async I/O](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) — async engine, AsyncSession, паттерны
- [Alembic — документация и cookbook](https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic) — миграции, autogenerate, async
- [httpx — AsyncClient](https://www.python-httpx.org/async/) — async HTTP-клиент, timeout, error handling
- [FastAPI — SQL Databases (SQLModel)](https://fastapi.tiangolo.com/tutorial/sql-databases/) — официальный туториал по интеграции
