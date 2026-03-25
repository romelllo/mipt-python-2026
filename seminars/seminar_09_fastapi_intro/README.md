# Семинар 9: Введение в FastAPI

**Модуль:** 3 — Создание Web-сервисов на Python
**Дата:** 30.03.2026
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1BWHiVhAJsG8uyufTNJYQF4bxIDjEgYiwCekrFPMvyD0/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:

- **Называть** HTTP-методы, соответствующие CRUD-операциям, и правильные статус-коды
- **Объяснять** ключевые отличия FastAPI от Django и когда выбирать каждый из них
- **Организовывать** FastAPI-проект с разделением на `main.py`, роутеры и модели
- **Настраивать** приложение FastAPI и читать его документацию через Swagger UI
- **Реализовывать** задокументированные эндпоинты с Pydantic-моделями, `response_model` и правильными статус-кодами

---

## Подготовка

```bash
# Активируйте виртуальное окружение
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# FastAPI и uvicorn уже установлены в проекте (см. pyproject.toml)
# Убедитесь, что всё установлено:
uv sync
python -c "import fastapi; print(fastapi.__version__)"

# Запустите примеры для ознакомления:
python seminars/seminar_09_fastapi_intro/examples/01_http_rest_recap.py
python seminars/seminar_09_fastapi_intro/examples/02_fastapi_hello.py
python seminars/seminar_09_fastapi_intro/examples/04_app_config.py
python seminars/seminar_09_fastapi_intro/examples/05_pydantic_docs.py

# Запустить сервер из примера (и открыть http://127.0.0.1:8000/docs):
uvicorn seminars.seminar_09_fastapi_intro.examples.02_fastapi_hello:app --reload
```

---

## План семинара

Семинар построен по принципу **«теория → практика»**: после каждого блока теории переходите к соответствующим упражнениям в файле [`exercises/fastapi_intro_practice.md`](exercises/fastapi_intro_practice.md).

| Время | Тема | Практика |
|-------|------|----------|
| 15 мин | Блок 1: REST + CRUD + HTTP — повторение | → Упражнения: Часть 1 |
| 15 мин | Блок 2: FastAPI — введение и сравнение с Django | → Упражнения: Часть 2 |
| 20 мин | Блок 3: Структура FastAPI-проекта | → Упражнения: Часть 3 |
| 10 мин | Блок 4: Конфигурация приложения и Swagger UI | → Упражнения: Часть 4 |
| 25 мин | Блок 5: Pydantic-модели + документация эндпоинтов | → Упражнения: Часть 5 |
| 5 мин | Подведение итогов | — |

**Итого:** ~90 минут

---

## Блок 1: REST + CRUD + HTTP — повторение (15 мин)

**REST** (Representational State Transfer) — архитектурный стиль API. Главная идея: URL — это **существительное** (ресурс), HTTP-метод — это **глагол** (действие).

### CRUD ↔ HTTP-методы

| CRUD | HTTP-метод | URL | Статус-код ответа |
|------|-----------|-----|-------------------|
| **C**reate | `POST` | `/tasks` | 201 Created |
| **R**ead (список) | `GET` | `/tasks` | 200 OK |
| **R**ead (один) | `GET` | `/tasks/{id}` | 200 OK |
| **U**pdate (полный) | `PUT` | `/tasks/{id}` | 200 OK |
| **U**pdate (частичный) | `PATCH` | `/tasks/{id}` | 200 OK |
| **D**elete | `DELETE` | `/tasks/{id}` | 204 No Content |

### Структура HTTP-запроса и ответа

```
POST /tasks HTTP/1.1
Host: api.example.com
Content-Type: application/json        ← заголовок

{"title": "Купить продукты"}          ← тело запроса (body)
```

```
HTTP/1.1 201 Created
Content-Type: application/json        ← заголовок

{"id": 42, "title": "Купить продукты", "done": false}   ← тело ответа
```

### Важные статус-коды

| Код | Название | Когда |
|-----|---------|-------|
| 200 | OK | GET, PUT, PATCH — успешно |
| 201 | Created | POST — ресурс создан |
| 204 | No Content | DELETE — успешно, но тело пустое |
| 400 | Bad Request | Ошибка в данных запроса |
| 404 | Not Found | Ресурс не существует |
| 422 | Unprocessable Entity | Данные не прошли валидацию (FastAPI) |
| 500 | Internal Server Error | Ошибка на стороне сервера |

**Ключевое правило REST:** URL — это существительные (`/tasks`, `/users`), не глаголы (`/getTasks`, `/createUser`).

> **Подробнее:** см. файл [`examples/01_http_rest_recap.py`](examples/01_http_rest_recap.py) — таблица CRUD↔HTTP, структура запроса/ответа, симуляция REST API для задач.

### Практика

Перейдите к файлу [`exercises/fastapi_intro_practice.md`](exercises/fastapi_intro_practice.md) и выполните **Часть 1: REST + CRUD + HTTP** (задания 1.1–1.2).

---

## Блок 2: FastAPI — введение и сравнение с Django (15 мин)

FastAPI — современный Python-фреймворк для создания API. Его главные преимущества:

1. **Автоматическая документация** — Swagger UI и ReDoc генерируются из кода
2. **Автоматическая валидация** — Pydantic проверяет данные запроса; при ошибке → 422
3. **Нативный async** — `async def` работает «из коробки»
4. **Типизация** — type hints используются для валидации и генерации схемы

### Минимальное приложение

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root() -> dict:
    """FastAPI использует docstring как описание в Swagger UI."""
    return {"message": "Привет!"}
```

**Три строки — и у вас**: работающий API, Swagger UI на `/docs`, ReDoc на `/redoc`, JSON-схема на `/openapi.json`.

### Sync vs Async

```python
# Синхронный: для вычислений без I/O
@app.get("/sync")
def compute() -> dict:
    result = sum(range(1_000_000))
    return {"result": result}

# Асинхронный: для I/O — запросы к БД, HTTP, файлы
@app.get("/async")
async def fetch_data() -> dict:
    # await не блокирует event loop — другие запросы обрабатываются параллельно
    data = await some_async_db_query()
    return {"data": data}
```

**Правило:** используйте `async def`, если вызываете `await` внутри. В остальных случаях — обычный `def` (FastAPI запустит его в thread pool).

### FastAPI vs Django: ключевые отличия

| Критерий | Django | FastAPI |
|---------|--------|---------|
| Маршрутизация | `urls.py` + `views.py` | Декоратор `@app.get(...)` |
| Валидация | Forms / Serializers (DRF) | Pydantic (автоматически) |
| Документация API | DRF browsable API / расширения | Swagger UI (встроено) |
| Async | Частичная (Django 4.1+) | Нативная |
| ORM | Встроенный | Нет (SQLAlchemy, Tortoise) |
| Шаблоны HTML | Встроенные (DTL / Jinja2) | Не предназначен |
| Назначение | Полный сайт + API | API-сервисы / микросервисы |

**Когда использовать FastAPI:** нужен чистый API (для фронтенда, мобильного приложения, микросервиса), нужна автоматическая документация, важна производительность async.

> **Подробнее:** см. файл [`examples/02_fastapi_hello.py`](examples/02_fastapi_hello.py) — минимальное приложение, sync/async эндпоинты, path/query параметры, сравнительная таблица.

### Практика

Перейдите к файлу [`exercises/fastapi_intro_practice.md`](exercises/fastapi_intro_practice.md) и выполните **Часть 2: FastAPI — первые шаги** (задания 2.1–2.2).

---

## Блок 3: Структура FastAPI-проекта (20 мин)

Маленький проект можно держать в одном файле `main.py`. Когда проект растёт — нужна структура.

### Рекомендуемая структура

```
todo_api/
├── main.py                # Создание приложения, подключение роутеров
├── models.py              # Pydantic-модели (запрос / ответ)
└── routers/
    ├── __init__.py
    ├── tasks.py           # Эндпоинты для /tasks
    └── users.py           # Эндпоинты для /users (когда понадобится)
```

### `APIRouter` — модульная маршрутизация

**Проблема:** все маршруты в одном файле → код трудно читать и поддерживать.
**Решение:** `APIRouter` — как «мини-приложение» для одного ресурса.

```python
# routers/tasks.py
from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")            # → GET /tasks
def list_tasks() -> list[dict]:
    return []

@router.post("/")           # → POST /tasks
def create_task() -> dict:
    return {}
```

```python
# main.py
from fastapi import FastAPI
from .routers import tasks

app = FastAPI()
app.include_router(tasks.router)   # подключить роутер

# Добавить новый ресурс = одна строка:
# app.include_router(users.router)
```

**Преимущества роутеров:**
- Каждый файл отвечает за один ресурс
- Легко добавлять новые ресурсы
- Можно задать `prefix` и `tags` один раз для всего роутера

### In-memory хранилище vs база данных

В учебных примерах используем словарь. В реальном проекте — SQLAlchemy + PostgreSQL:

```python
# Учебный in-memory (не для production!)
_tasks_db: dict[int, dict] = {}
_next_id = 1

# Реальный проект: получать сессию БД через Depends()
# def create_task(task: TaskCreate, db: Session = Depends(get_db)):
#     ...
```

> **Подробнее:** см. директорию [`examples/03_project_structure/`](examples/03_project_structure/) — полный пример с `main.py`, `models.py`, `routers/tasks.py`. Запуск:
> ```bash
> uvicorn seminars.seminar_09_fastapi_intro.examples.03_project_structure.main:app --reload
> ```

### Практика

Перейдите к файлу [`exercises/fastapi_intro_practice.md`](exercises/fastapi_intro_practice.md) и выполните **Часть 3: Структура проекта** (задания 3.1–3.2).

---

## Блок 4: Конфигурация приложения и Swagger UI (10 мин)

### Параметры конструктора `FastAPI()`

```python
app = FastAPI(
    title="TODO API",
    description="""
## TODO API
Управление задачами. Поддерживает **Markdown** в описании.
""",
    version="1.0.0",
    contact={"name": "Команда", "email": "dev@example.com"},
    license_info={"name": "MIT"},
    openapi_tags=[
        {"name": "tasks", "description": "Операции с задачами"},
        {"name": "health", "description": "Статус сервиса"},
    ],
    # Отключить документацию в production:
    # docs_url=None, redoc_url=None
)
```

### Swagger UI и ReDoc

После запуска сервера документация доступна сразу:

| URL | Что открывается |
|-----|----------------|
| `/docs` | Swagger UI — интерактивная документация |
| `/redoc` | ReDoc — красивый статичный вид |
| `/openapi.json` | Машиночитаемая OpenAPI-схема |

**Swagger UI позволяет:**
- Видеть все эндпоинты, сгруппированные по тегам
- Нажать «Try it out» и отправить реальный запрос прямо из браузера
- Видеть схемы запросов и ответов (из Pydantic-моделей)

**Правило:** не забудьте отключить документацию (`docs_url=None`) в production, если API не должен быть публичным.

> **Подробнее:** см. файл [`examples/04_app_config.py`](examples/04_app_config.py) — все параметры `FastAPI()`, метаданные тегов, кастомная OpenAPI-схема.

### Практика

Перейдите к файлу [`exercises/fastapi_intro_practice.md`](exercises/fastapi_intro_practice.md) и выполните **Часть 4: Конфигурация и Swagger** (задание 4.1).

---

## Блок 5: Pydantic-модели + документация эндпоинтов (25 мин)

Pydantic — сердце FastAPI. Он обеспечивает валидацию входных данных и генерирует JSON-схему для Swagger UI автоматически — из ваших type hints.

### Разделение моделей: Create / Update / Response

**Проблема:** одна модель для всего — клиент сможет задать `id` при создании, или `done` при первоначальном запросе.
**Решение:** три роли — три модели.

```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    """Что клиент ОТПРАВЛЯЕТ при создании."""
    title: str = Field(..., min_length=1, description="Заголовок задачи",
                       examples=["Купить продукты"])
    description: str = Field(default="", description="Описание")

class TaskUpdate(BaseModel):
    """Что клиент ОТПРАВЛЯЕТ при обновлении (все поля необязательны)."""
    title: str | None = Field(default=None, min_length=1)
    done: bool | None = Field(default=None)

class TaskResponse(BaseModel):
    """Что сервер ВОЗВРАЩАЕТ клиенту."""
    id: int
    title: str
    description: str
    done: bool
```

### `Field` — документирование полей

```python
title: str = Field(
    ...,                          # ... = обязательное поле
    min_length=1,                 # валидация
    max_length=200,
    description="Заголовок задачи",   # показывается в Swagger UI
    examples=["Купить продукты"],     # пример в Swagger UI
)
```

### `response_model` и `status_code` на эндпоинтах

```python
@app.post(
    "/tasks",
    response_model=TaskResponse,   # → схема ответа в Swagger UI + авто-фильтрация полей
    status_code=201,               # → правильный HTTP-код при успехе
    summary="Создать задачу",      # → краткое название в Swagger UI
    tags=["tasks"],                # → группа в Swagger UI
)
def create_task(task: TaskCreate) -> dict:
    ...
```

**Зачем `response_model`:**
- Swagger UI показывает схему ответа
- FastAPI автоматически **фильтрует** поля ответа (не вернёт лишних полей)
- Документирует контракт API

### `model_dump(exclude_unset=True)` — паттерн для PATCH

```python
@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate) -> dict:
    task = _db[task_id]
    # exclude_unset=True → берём только явно переданные поля
    # Иначе None перезапишет существующие значения!
    updates = task_update.model_dump(exclude_unset=True)
    task.update(updates)
    return task
```

**Использование:**

```python
update = TaskUpdate(done=True)
update.model_dump()                     # {'title': None, 'done': True}
update.model_dump(exclude_unset=True)   # {'done': True}  ← только явно переданное
```

> **Подробнее:** см. файл [`examples/05_pydantic_docs.py`](examples/05_pydantic_docs.py) — полный пример с `TaskCreate/Update/Response`, `field_validator`, `Query()`, документацией эндпоинтов.

### Практика

Перейдите к файлу [`exercises/fastapi_intro_practice.md`](exercises/fastapi_intro_practice.md) и выполните **Часть 5: Pydantic + документация** (задания 5.1–5.2).

---

## Подведение итогов

### Шпаргалка

| Концепция | Ключевое |
|-----------|---------|
| `POST /tasks` | Создать → 201 Created |
| `GET /tasks` | Список → 200 OK |
| `GET /tasks/{id}` | Один → 200 OK или 404 |
| `PATCH /tasks/{id}` | Частичное обновление → 200 OK |
| `DELETE /tasks/{id}` | Удалить → 204 No Content |
| `app = FastAPI(title=...)` | Конфигурация приложения |
| `/docs` | Swagger UI (интерактивная документация) |
| `/redoc` | ReDoc |
| `APIRouter(prefix=..., tags=...)` | Модульная маршрутизация |
| `app.include_router(router)` | Подключить роутер к приложению |
| `BaseModel` | Объявить Pydantic-модель |
| `Field(..., description=..., examples=...)` | Документировать поле |
| `response_model=TaskResponse` | Тип ответа → схема в Swagger |
| `status_code=201` | HTTP-код при успехе |
| `model_dump(exclude_unset=True)` | Паттерн PATCH: только изменённые поля |
| `HTTPException(status_code=404)` | Вернуть HTTP-ошибку |

### Ключевые выводы

1. **FastAPI строит документацию из вашего кода.** Type hints, docstrings, `Field(description=...)`, `summary=...` на эндпоинтах — всё это появляется в Swagger UI без дополнительных усилий.

2. **Три модели вместо одной.** `TaskCreate` (что клиент отправляет), `TaskUpdate` (частичное обновление), `TaskResponse` (что сервер возвращает) — явно описывают контракт API и предотвращают ошибки.

3. **Роутеры держат код структурированным.** Один файл — один ресурс. `app.include_router()` — одна строка для подключения.

---

## Файлы семинара

```
seminar_09_fastapi_intro/
├── README.md                                   # Этот файл
├── examples/
│   ├── 01_http_rest_recap.py                  # HTTP/REST/CRUD: таблицы, статус-коды, симуляция API
│   ├── 02_fastapi_hello.py                    # Минимальное FastAPI-приложение, sync/async, сравнение с Django
│   ├── 03_project_structure/                  # Полный пример структуры проекта
│   │   ├── main.py                            # Точка входа, include_router()
│   │   ├── models.py                          # Pydantic-модели TaskCreate/Update/Response
│   │   └── routers/
│   │       └── tasks.py                       # APIRouter для /tasks, все CRUD-эндпоинты
│   ├── 04_app_config.py                       # Параметры FastAPI(), теги, Swagger UI
│   └── 05_pydantic_docs.py                    # Pydantic: Field, validators, response_model, status_code
└── exercises/
    └── fastapi_intro_practice.md                           # Практические задания по всем блокам
```

---

## Дополнительные материалы

- [FastAPI — официальная документация](https://fastapi.tiangolo.com/) — туториал, path/query параметры, dependency injection
- [Pydantic — документация](https://docs.pydantic.dev/latest/) — validators, Field, типы данных, config
- [Real Python — FastAPI Tutorial](https://realpython.com/fastapi-python-web-apis/) — подробный туториал с примерами
- [HTTP Status Codes](https://developer.mozilla.org/ru/docs/Web/HTTP/Status) — MDN: полный справочник статус-кодов
- [REST API Design Best Practices](https://restfulapi.net/) — соглашения об именовании, версионирование, пагинация
