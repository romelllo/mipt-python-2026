# Практические задания: Работа с данными в FastAPI

## Подготовка

```bash
# 1. Активируйте виртуальное окружение
source .venv/bin/activate  # Linux/Mac

# 2. Запустите PostgreSQL через Docker
cd seminars/seminar_10_fastapi_data_handling
docker compose up -d

# 3. Проверьте, что PostgreSQL доступен
docker compose ps   # должен быть статус "healthy" или "running"

# 4. Задайте DATABASE_URL (по умолчанию уже совпадает с docker-compose.yml)
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/notes_db"

# 5. Убедитесь, что зависимости установлены
cd ../..   # вернитесь в корень репозитория
uv sync

# 6. Запустите примеры, которые не требуют Docker:
python seminars/seminar_10_fastapi_data_handling/examples/01_sqlmodel_intro.py
python seminars/seminar_10_fastapi_data_handling/examples/03_external_service.py
```

> **Как работать с заданиями:** прочитайте условие, попробуйте ответить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: SQLModel + PostgreSQL в Docker

> **Теория:** [README.md — Блок 1](../README.md#блок-1-sqlmodel--postgresql-в-docker-20-мин) | **Примеры:** [`examples/01_sqlmodel_intro.py`](../examples/01_sqlmodel_intro.py)

### Задание 1.1

Запустите демо-скрипт и объясните вывод:

```bash
python seminars/seminar_10_fastapi_data_handling/examples/01_sqlmodel_intro.py
```

Ответьте на вопросы:
1. Чем `Note(table=True)` отличается от `NoteCreate`?
2. Почему после `session.commit()` вызывается `session.refresh(note)`?
3. Что вернёт `get_note_by_id(999)` и почему?

<details>
<summary>Подсказка</summary>

- `table=True` → SQLModel регистрирует класс как ORM-модель (таблица в БД).
- После `commit()` атрибуты объекта могут быть «expired» — `refresh()` перечитывает их из БД.
- `session.get(Note, 999)` возвращает `None` если строки нет.

</details>

<details>
<summary>Решение</summary>

1. **`Note(table=True)`** — это ORM-модель, отображённая на таблицу `note` в БД. SQLAlchemy знает, как делать INSERT/SELECT/UPDATE/DELETE для неё. `NoteCreate` — это чистая Pydantic-схема для валидации входных данных клиента; она не привязана к БД.

2. После `commit()` SQLAlchemy помечает атрибуты объекта как «устаревшие» (expired). При следующем обращении они будут перечитаны из БД. `session.refresh(note)` принудительно делает SELECT и подгружает `id` и `created_at`, сгенерированные БД.

3. `get_note_by_id(999)` вернёт `None`, потому что `session.get(Note, 999)` возвращает `None` если строки с `id=999` нет в таблице.

</details>

---

### Задание 1.2

Используя модели из `01_sqlmodel_intro.py`, реализуйте функцию поиска заметок по подстроке в заголовке:

```python
def search_notes(query: str) -> list[Note]:
    """Найти заметки, у которых title содержит query (регистронезависимо)."""
    ...
```

Добавьте вызов в `if __name__ == "__main__"` и проверьте результат.

<details>
<summary>Подсказка</summary>

SQLModel использует SQLAlchemy под капотом. Для LIKE-запроса:
```python
from sqlmodel import col
statement = select(Note).where(col(Note.title).icontains(query))
```
`icontains` генерирует `WHERE title ILIKE '%query%'` (регистронезависимо).

</details>

<details>
<summary>Решение</summary>

```python
from sqlmodel import Session, col, select

def search_notes(query: str) -> list[Note]:
    """Найти заметки по подстроке в заголовке (регистронезависимо)."""
    with Session(ENGINE) as session:
        statement = select(Note).where(
            col(Note.title).icontains(query)
        )
        return list(session.exec(statement).all())

# Проверка:
# create_tables()
# create_note(NoteCreate(title="Купить продукты"))
# create_note(NoteCreate(title="Список покупок"))
# create_note(NoteCreate(title="Встреча с командой"))
# results = search_notes("покуп")
# print([n.title for n in results])  # ['Купить продукты', 'Список покупок']
```

</details>

---

## Часть 2: `db.py` — асинхронная сессия и DI

> **Теория:** [README.md — Блок 2](../README.md#блок-2-appdbpy--асинхронная-сессия-20-мин) | **Примеры:** [`examples/02_async_db/db.py`](../examples/02_async_db/db.py)

### Задание 2.1

Изучите файл `examples/02_async_db/db.py` и ответьте на вопросы:

1. Почему используется `postgresql+asyncpg://...` вместо `postgresql://...`?
2. Что делает `expire_on_commit=False` в `async_sessionmaker`?
3. Зачем использовать `lifespan` вместо обычного события `@app.on_event("startup")`?

<details>
<summary>Подсказка</summary>

- `asyncpg` — асинхронный DBAPI-драйвер для PostgreSQL. Обычный `psycopg2` блокирует event loop.
- `expire_on_commit=False` влияет на поведение объектов после коммита в асинхронном контексте.
- `lifespan` — современный (FastAPI 0.95+) способ, заменяющий устаревший `@app.on_event`.

</details>

<details>
<summary>Решение</summary>

1. **`postgresql+asyncpg://`** — указывает SQLAlchemy использовать асинхронный драйвер `asyncpg` вместо синхронного `psycopg2`. Без `asyncpg` операции с БД заблокируют event loop и уничтожат всю пользу от `async def`.

2. **`expire_on_commit=False`** — по умолчанию SQLAlchemy помечает все атрибуты объекта как «expired» после `commit()`. В синхронном коде это не проблема — следующий доступ сделает SELECT автоматически. В асинхронном коде такой «ленивый» SELECT невозможен (нет активной сессии). Поэтому мы отключаем expiration: объекты остаются доступны после `commit()` без повторного запроса.

3. **`lifespan`** — это современный стандарт ASGI. `@app.on_event` помечен как deprecated с FastAPI 0.95. `lifespan` использует `asynccontextmanager`, что более Pythonic, и чётко разделяет startup и shutdown логику в одном месте.

</details>

---

### Задание 2.2

Запустите Notes API с реальной PostgreSQL (если Docker доступен):

```bash
cd seminars/seminar_10_fastapi_data_handling
docker compose up -d
cd ../..
uvicorn seminars.seminar_10_fastapi_data_handling.examples.02_async_db.main:app --reload
```

Откройте `http://127.0.0.1:8000/docs` и выполните:
1. `POST /notes/` — создайте 2–3 заметки
2. `GET /notes/` — получите список всех заметок
3. `PATCH /notes/1` — обновите только `content` (поле `title` не передавайте)
4. `DELETE /notes/2` — удалите вторую заметку, убедитесь, что вернулся статус 204

<details>
<summary>Подсказка</summary>

В Swagger UI нажмите «Try it out» на нужном эндпоинте, введите данные в форму и нажмите «Execute». Для PATCH передайте только поле `content` — поле `title` пропустите (не `null`, а просто не указывайте).

</details>

<details>
<summary>Решение</summary>

Пример запросов через curl (или аналогично через Swagger UI):

```bash
# 1. Создать заметку
curl -X POST http://localhost:8000/notes/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Первая заметка", "content": "Привет из PostgreSQL!"}'
# → {"id": 1, "title": "...", "content": "...", "created_at": "..."}

# 2. Список заметок
curl http://localhost:8000/notes/
# → [{"id": 1, ...}, ...]

# 3. Частичное обновление (только content)
curl -X PATCH http://localhost:8000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"content": "Обновлённое содержимое"}'
# title не изменился — exclude_unset=True сработал

# 4. Удаление
curl -X DELETE http://localhost:8000/notes/2
# → HTTP 204 No Content
```

</details>

---

## Часть 3: Async CRUD + внешние сервисы

> **Теория:** [README.md — Блок 3](../README.md#блок-3-async-crud-с-бд--внешние-сервисы-20-мин) | **Примеры:** [`examples/02_async_db/routers/notes.py`](../examples/02_async_db/routers/notes.py), [`examples/03_external_service.py`](../examples/03_external_service.py)

### Задание 3.1

Запустите пример с внешним сервисом:

```bash
python seminars/seminar_10_fastapi_data_handling/examples/03_external_service.py
```

Добавьте в скрипт функцию `fetch_user_todos(user_id: int) -> list[dict]`, которая получает все задачи конкретного пользователя с `https://jsonplaceholder.typicode.com/todos?userId={user_id}`.

<details>
<summary>Подсказка</summary>

Используйте query-параметр: `GET /todos?userId=1`. В httpx это:
```python
response = await client.get(f"{BASE_URL}/todos", params={"userId": user_id})
```

</details>

<details>
<summary>Решение</summary>

```python
import asyncio
import httpx

BASE_URL = "https://jsonplaceholder.typicode.com"

async def fetch_user_todos(user_id: int) -> list[dict]:
    """Получить все задачи пользователя.

    Args:
        user_id: идентификатор пользователя (1–10)

    Returns:
        список задач пользователя
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/todos",
            params={"userId": user_id},
        )
        response.raise_for_status()
        return list(response.json())


async def main() -> None:
    todos = await fetch_user_todos(1)
    print(f"Пользователь 1 имеет {len(todos)} задач")
    for t in todos[:3]:
        print(f"  [{t['id']}] {t['title'][:40]} — completed={t['completed']}")


asyncio.run(main())
# Пользователь 1 имеет 20 задач
# [1] delectus aut autem — completed=False
# ...
```

</details>

---

## Часть 4: Миграции с Alembic

> **Теория:** [README.md — Блок 4](../README.md#блок-4-миграции-с-alembic-20-мин) | **Примеры:** [`examples/04_alembic_demo/`](../examples/04_alembic_demo/)

### Задание 4.1

Инициализируйте и запустите первую миграцию для `04_alembic_demo`:

```bash
# 1. Убедитесь, что PostgreSQL запущен
cd seminars/seminar_10_fastapi_data_handling
docker compose up -d

# 2. Перейдите в директорию с alembic.ini
cd examples/04_alembic_demo

# 3. Сгенерируйте первую миграцию
alembic revision --autogenerate -m "create notes table"

# 4. Посмотрите на сгенерированный файл
cat alembic/versions/*.py

# 5. Примените миграцию
alembic upgrade head

# 6. Проверьте статус
alembic current
```

Ответьте на вопросы:
1. Что оказалось в сгенерированном файле миграции (`upgrade()` и `downgrade()`)?
2. Что вернула команда `alembic current`?

<details>
<summary>Подсказка</summary>

Alembic сравнивает текущее состояние БД (пустая) с метаданными моделей (`SQLModel.metadata`) и генерирует операции `op.create_table(...)` в `upgrade()` и `op.drop_table(...)` в `downgrade()`.

`alembic current` показывает текущую применённую ревизию. После `upgrade head` это будет хеш свежей миграции.

</details>

<details>
<summary>Решение</summary>

Сгенерированный файл будет похож на:

```python
"""create notes table

Revision ID: abc123def456
Revises:
Create Date: 2026-04-06 10:00:00
"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.create_table(
        'note',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

def downgrade() -> None:
    op.drop_table('note')
```

После `alembic upgrade head`:
```
INFO  [alembic.runtime.migration] Running upgrade  -> abc123def456, create notes table

$ alembic current
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
abc123def456 (head)
```

</details>

---

### Задание 4.2

Добавьте к модели `Note` в `04_alembic_demo/models.py` новое поле `is_pinned: bool` со значением по умолчанию `False`, и создайте миграцию для этого изменения.

```bash
alembic revision --autogenerate -m "add is_pinned to note"
alembic upgrade head
```

Затем откатите последнюю миграцию командой `alembic downgrade -1` и убедитесь, что поле пропало.

<details>
<summary>Подсказка</summary>

В `models.py` добавьте:
```python
is_pinned: bool = Field(default=False)
```

Для отката: `alembic downgrade -1` (откатить одну миграцию назад).

</details>

<details>
<summary>Решение</summary>

**models.py после изменения:**

```python
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_pinned: bool = Field(default=False)  # ← новое поле
```

**Сгенерированная миграция:**

```python
def upgrade() -> None:
    op.add_column(
        'note',
        sa.Column('is_pinned', sa.Boolean(), nullable=False, server_default='false')
    )

def downgrade() -> None:
    op.drop_column('note', 'is_pinned')
```

**Команды:**
```bash
alembic revision --autogenerate -m "add is_pinned to note"
alembic upgrade head      # применить
alembic current           # посмотреть текущую ревизию
alembic downgrade -1      # откатить последнюю миграцию → поле исчезнет
alembic upgrade head      # снова применить
```

</details>

---

## Бонусное задание

### Бонус: Notes API с тегами и миграцией

Расширьте проект `04_alembic_demo`, объединив знания всех блоков:

1. Добавьте модель `Tag(SQLModel, table=True)` с полями `id`, `name`
2. Добавьте промежуточную таблицу `NoteTag` для связи многие-ко-многим
3. Создайте и примените миграцию: `alembic revision --autogenerate -m "add tags"`
4. Добавьте async-эндпоинт `POST /notes/{note_id}/tags/{tag_name}` для привязки тега к заметке

<details>
<summary>Подсказка</summary>

Для связи многие-ко-многим в SQLModel:
```python
class NoteTag(SQLModel, table=True):
    note_id: Optional[int] = Field(default=None, foreign_key="note.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
```

В эндпоинте используйте `select(Tag).where(Tag.name == tag_name)` для поиска или создания тега.

</details>

<details>
<summary>Решение</summary>

```python
# models.py — расширенная версия
from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class NoteTag(SQLModel, table=True):
    """Промежуточная таблица для связи Note ↔ Tag."""
    note_id: Optional[int] = Field(
        default=None, foreign_key="note.id", primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )


class Tag(SQLModel, table=True):
    """Тег для заметки."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=50)
    notes: list["Note"] = Relationship(back_populates="tags", link_model=NoteTag)


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_pinned: bool = Field(default=False)
    tags: list[Tag] = Relationship(back_populates="notes", link_model=NoteTag)
```

```python
# routers/notes.py — эндпоинт добавления тега
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from ..db import SessionDep
from ..models import Note, NoteTag, Tag

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/{note_id}/tags/{tag_name}", status_code=201)
async def add_tag_to_note(note_id: int, tag_name: str, session: SessionDep) -> dict:
    """Привязать тег к заметке (создать тег если не существует)."""
    note = await session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    # Найти или создать тег
    result = await session.exec(select(Tag).where(Tag.name == tag_name))  # type: ignore[call-overload]
    tag = result.first()
    if not tag:
        tag = Tag(name=tag_name)
        session.add(tag)
        await session.commit()
        await session.refresh(tag)

    # Создать связь
    link = NoteTag(note_id=note.id, tag_id=tag.id)
    session.add(link)
    await session.commit()
    return {"note_id": note.id, "tag": tag.name}
```

После изменения моделей:
```bash
alembic revision --autogenerate -m "add tags"
alembic upgrade head
```

</details>

---

## Полезные ресурсы

- [SQLModel — документация](https://sqlmodel.tiangolo.com/) — официальный туториал от автора FastAPI
- [SQLAlchemy 2.0 — Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) — async engine, AsyncSession
- [Alembic — документация](https://alembic.sqlalchemy.org/en/latest/) — миграции, autogenerate, cookbook
- [httpx — документация](https://www.python-httpx.org/) — async HTTP клиент
- [asyncpg — документация](https://magicstack.github.io/asyncpg/current/) — высокопроизводительный драйвер PostgreSQL
