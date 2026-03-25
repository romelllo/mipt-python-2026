# Практические задания: Введение в FastAPI

## Подготовка

```bash
# Активируйте виртуальное окружение
source .venv/bin/activate  # Linux/Mac

# Запустите примеры для ознакомления перед выполнением заданий
python seminars/seminar_09_fastapi_intro/examples/01_http_rest_recap.py
python seminars/seminar_09_fastapi_intro/examples/02_fastapi_hello.py
python seminars/seminar_09_fastapi_intro/examples/05_pydantic_docs.py

# Для заданий с сервером — запустите в отдельном терминале:
uvicorn seminars.seminar_09_fastapi_intro.examples.02_fastapi_hello:app --reload
# → Swagger UI: http://127.0.0.1:8000/docs
```

> **Как работать с заданиями:** прочитайте условие, попробуйте ответить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: REST + CRUD + HTTP

> **Теория:** [README.md — Блок 1](../README.md#блок-1-rest--crud--http--повторение-10-мин) | **Примеры:** [`examples/01_http_rest_recap.py`](../examples/01_http_rest_recap.py)

### Задание 1.1

Для каждого действия ниже укажите: **HTTP-метод**, **URL** и **ожидаемый статус-код ответа**.

Ресурс: пользователи (`users`) с полями `id`, `name`, `email`.

| Действие | HTTP-метод | URL | Статус-код |
|---------|-----------|-----|-----------|
| Получить список всех пользователей | ? | ? | ? |
| Получить пользователя с id=5 | ? | ? | ? |
| Зарегистрировать нового пользователя | ? | ? | ? |
| Обновить email пользователя с id=5 | ? | ? | ? |
| Удалить пользователя с id=5 | ? | ? | ? |
| Получить пользователя с id=999 (не существует) | ? | ? | ? |

<details>
<summary>Подсказка</summary>

Используйте таблицу CRUD↔HTTP из теории:
- Список ресурсов → `GET /ресурсы`
- Один ресурс → `GET /ресурсы/{id}`
- Создать → `POST /ресурсы` → 201
- Обновить (частично) → `PATCH /ресурсы/{id}` → 200
- Удалить → `DELETE /ресурсы/{id}` → 204 (тело пустое)
- Не найдено → 404

</details>

<details>
<summary>Решение</summary>

| Действие | HTTP-метод | URL | Статус-код |
|---------|-----------|-----|-----------|
| Список всех пользователей | `GET` | `/users` | 200 |
| Пользователь id=5 | `GET` | `/users/5` | 200 |
| Зарегистрировать | `POST` | `/users` | 201 |
| Обновить email id=5 | `PATCH` | `/users/5` | 200 |
| Удалить id=5 | `DELETE` | `/users/5` | 204 |
| Пользователь id=999 | `GET` | `/users/999` | 404 |

**Пояснения:**
- `PATCH` вместо `PUT` — мы меняем только один атрибут (email), а не весь объект целиком. `PUT` подразумевает полную замену ресурса.
- `DELETE` → 204 No Content: ресурс удалён, тело ответа пустое.
- 404 возвращается сервером, когда ресурс с таким ID не существует.

</details>

---

### Задание 1.2

Найдите ошибки в следующих URL-маршрутах REST API. Для каждого объясните, что не так, и предложите исправление:

```
A)  GET  /getAllProducts
B)  POST /products/create
C)  DELETE /products/delete/15
D)  GET  /products?id=15
E)  PUT  /users/7/changeEmail
```

<details>
<summary>Подсказка</summary>

В REST URL — это **существительное** (ресурс), а HTTP-метод — **глагол** (действие). Все глаголы в URL — нарушение REST.

ID ресурса должен быть **частью пути** (`/products/15`), а не query-параметром, если речь идёт об одном конкретном ресурсе.

</details>

<details>
<summary>Решение</summary>

**A) `GET /getAllProducts`**
- ❌ Проблема: глагол `get` в URL, `All` — избыточно.
- ✅ Исправление: `GET /products` — метод GET уже означает «получить».

**B) `POST /products/create`**
- ❌ Проблема: глагол `create` в URL.
- ✅ Исправление: `POST /products` — метод POST уже означает «создать».

**C) `DELETE /products/delete/15`**
- ❌ Проблема: глагол `delete` дублирует смысл HTTP-метода DELETE.
- ✅ Исправление: `DELETE /products/15`.

**D) `GET /products?id=15`**
- ❌ Проблема: ID конкретного ресурса должен быть в path, не в query-параметре.
- ✅ Исправление: `GET /products/15`. Query-параметры (`?...`) — для фильтрации списков, не для идентификации одного ресурса.

**E) `PUT /users/7/changeEmail`**
- ❌ Проблема: `changeEmail` — глагол, описывающий действие.
- ✅ Исправление: `PATCH /users/7` с телом `{"email": "new@example.com"}` — partial update через PATCH.

</details>

---

## Часть 2: FastAPI — первые шаги

> **Теория:** [README.md — Блок 2](../README.md#блок-2-fastapi--введение-и-сравнение-с-django-10-мин) | **Примеры:** [`examples/02_fastapi_hello.py`](../examples/02_fastapi_hello.py)

### Задание 2.1

Запустите минимальное FastAPI-приложение и откройте Swagger UI.

1. Запустите сервер:
   ```bash
   uvicorn seminars.seminar_09_fastapi_intro.examples.02_fastapi_hello:app --reload
   ```
2. Откройте http://127.0.0.1:8000/docs
3. Найдите эндпоинт `GET /items/{item_id}` и нажмите «Try it out»
4. Отправьте запрос с `item_id=42` и `verbose=true`
5. Запишите: какой статус-код вернул ответ? Что в теле ответа?

Затем попробуйте передать `item_id=abc` (не число). Что происходит?

<details>
<summary>Подсказка</summary>

Swagger UI — это интерактивный клиент для вашего API. Нажмите на эндпоинт, затем «Try it out», заполните параметры, нажмите «Execute».

При передаче нечислового `item_id` FastAPI вернёт ответ с кодом 422 — Unprocessable Entity. Это автоматическая валидация типов.

</details>

<details>
<summary>Решение</summary>

**Запрос `GET /items/42?verbose=true`:**
```json
// Ответ 200 OK:
{
  "id": 42,
  "description": "Подробная информация о товаре 42"
}
```

**Запрос `GET /items/abc`:**
```json
// Ответ 422 Unprocessable Entity:
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "item_id"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "abc"
    }
  ]
}
```

**Что происходит:** FastAPI автоматически проверяет, что `item_id` — целое число (из аннотации `item_id: int`). Если преобразование невозможно — возвращает 422 с подробным описанием ошибки. Никакого кода валидации писать не нужно.

</details>

---

### Задание 2.2

Напишите FastAPI-приложение с одним эндпоинтом `GET /greet/{name}`, который возвращает приветствие:

```json
{"message": "Привет, Alice!"}
```

Дополнительно: добавьте опциональный query-параметр `formal` (bool, по умолчанию `False`). При `formal=true` возвращайте:
```json
{"message": "Добрый день, уважаемый(ая) Alice!"}
```

<details>
<summary>Подсказка</summary>

- Path-параметр: `{name}` в URL и `name: str` в параметрах функции.
- Query-параметр: просто добавьте `formal: bool = False` в параметры функции.
- FastAPI автоматически поймёт, что `name` — path-параметр (есть в URL), а `formal` — query-параметр (нет в URL).

</details>

<details>
<summary>Решение</summary>

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/greet/{name}")
def greet(name: str, formal: bool = False) -> dict:
    """Приветствовать пользователя по имени.

    - `name` — path-параметр (часть URL)
    - `formal` — query-параметр (?formal=true), по умолчанию False
    """
    if formal:
        message = f"Добрый день, уважаемый(ая) {name}!"
    else:
        message = f"Привет, {name}!"
    return {"message": message}
```

**Проверка:**
```
GET /greet/Alice          → {"message": "Привет, Alice!"}
GET /greet/Alice?formal=true → {"message": "Добрый день, уважаемый(ая) Alice!"}
```

FastAPI автоматически:
- Преобразует строку `"true"` / `"1"` / `"yes"` в `True` для bool-параметров
- Документирует оба параметра в Swagger UI

</details>

---

## Часть 3: Структура проекта

> **Теория:** [README.md — Блок 3](../README.md#блок-3-структура-fastapi-проекта-10-мин) | **Примеры:** [`examples/03_project_structure/`](../examples/03_project_structure/)

### Задание 3.1

Изучите структуру примера в `examples/03_project_structure/`.

1. Откройте `main.py`, `models.py` и `routers/tasks.py`
2. Запустите сервер:
   ```bash
   uvicorn seminars.seminar_09_fastapi_intro.examples.03_project_structure.main:app --reload
   ```
3. Откройте Swagger UI (`/docs`) и проверьте, что все эндпоинты `/tasks` присутствуют
4. Ответьте на вопросы:
   - Как `main.py` узнаёт о маршрутах из `routers/tasks.py`?
   - Почему `APIRouter` создаётся с `prefix="/tasks"`?
   - Что происходит при `PATCH /tasks/999`?

<details>
<summary>Подсказка</summary>

Обратите внимание на строку `app.include_router(tasks.router)` в `main.py`. Также посмотрите на обработку отсутствующего ID в `routers/tasks.py` — там используется `HTTPException`.

</details>

<details>
<summary>Решение</summary>

**Как `main.py` узнаёт о маршрутах:**

```python
# main.py
from .routers import tasks
app.include_router(tasks.router)   # ← регистрирует все маршруты роутера
```

`include_router()` берёт все `@router.get/post/patch/delete` из `tasks.py` и добавляет их к приложению с учётом `prefix="/tasks"`.

**Почему `prefix="/tasks"`:**

Без `prefix` нужно писать `@router.get("/tasks")` в каждом декораторе. С `prefix="/tasks"` — достаточно `@router.get("/")`, `@router.get("/{task_id}")`. Префикс применяется один раз ко всем маршрутам роутера.

**Что происходит при `PATCH /tasks/999`:**

```python
# routers/tasks.py
if task_id not in _tasks_db:
    raise HTTPException(status_code=404, detail="Задача 999 не найдена")
```

FastAPI перехватывает `HTTPException` и возвращает:
```
HTTP/1.1 404 Not Found
{"detail": "Задача 999 не найдена"}
```

</details>

---

### Задание 3.2

Расширьте структуру проекта из `examples/03_project_structure/`: добавьте роутер для нового ресурса — **метки** (tags/labels) для задач.

Структура нового роутера (`routers/labels.py`):

- `GET /labels` — список меток
- `POST /labels` — создать метку
- Метка имеет поля: `id: int`, `name: str`, `color: str` (например, `"red"`, `"blue"`)

Создайте отдельный файл. Не забудьте подключить роутер в `main.py`.

<details>
<summary>Подсказка</summary>

Скопируйте структуру из `routers/tasks.py` и адаптируйте:
1. Создайте `routers/labels.py` с `router = APIRouter(prefix="/labels", tags=["labels"])`
2. Добавьте in-memory хранилище `_labels_db`
3. Реализуйте `GET /` и `POST /`
4. В `main.py`: `from .routers import labels` + `app.include_router(labels.router)`

</details>

<details>
<summary>Решение</summary>

```python
# routers/labels.py
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/labels", tags=["labels"])

_labels_db: dict[int, dict] = {}
_next_id = 1


class LabelCreate(BaseModel):
    """Тело запроса при создании метки."""
    name: str = Field(..., min_length=1, max_length=50, description="Название метки")
    color: str = Field(
        default="blue",
        pattern=r"^(red|green|blue|yellow|purple)$",
        description="Цвет метки",
    )


class LabelResponse(BaseModel):
    """Ответ с данными метки."""
    id: int
    name: str
    color: str


@router.get("/", response_model=list[LabelResponse])
def list_labels() -> list[dict]:
    """Получить список всех меток."""
    return list(_labels_db.values())


@router.post("/", response_model=LabelResponse, status_code=201)
def create_label(label: LabelCreate) -> dict:
    """Создать новую метку."""
    global _next_id
    new_label = {"id": _next_id, "name": label.name, "color": label.color}
    _labels_db[_next_id] = new_label
    _next_id += 1
    return new_label
```

```python
# main.py — добавить строки:
from .routers import labels  # type: ignore[import]
app.include_router(labels.router)
```

После этого в Swagger UI появятся эндпоинты `GET /labels` и `POST /labels`, сгруппированные в тег «labels».

</details>

---

## Часть 4: Конфигурация и Swagger

> **Теория:** [README.md — Блок 4](../README.md#блок-4-конфигурация-приложения-и-swagger-ui-5-мин) | **Примеры:** [`examples/04_app_config.py`](../examples/04_app_config.py)

### Задание 4.1

Создайте FastAPI-приложение с полной конфигурацией для учебного TODO API:

1. Установите `title`, `description` (с Markdown-форматированием), `version="0.1.0"`
2. Добавьте контактную информацию (ваше имя и email)
3. Настройте теги для двух групп: `"tasks"` и `"health"`, каждый с описанием
4. Добавьте эндпоинт `GET /health` с тегом `"health"`, который возвращает `{"status": "ok"}`
5. Запустите и проверьте в Swagger UI: отображаются ли метаданные?

<details>
<summary>Подсказка</summary>

Параметр `openapi_tags` принимает список словарей вида:
```python
[{"name": "tasks", "description": "Операции с задачами"}]
```

Описание (`description`) поддерживает Markdown: используйте `##`, `**bold**`, списки.

</details>

<details>
<summary>Решение</summary>

```python
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "tasks",
        "description": "CRUD-операции с задачами: создание, чтение, обновление, удаление.",
    },
    {
        "name": "health",
        "description": "Проверка работоспособности сервиса.",
    },
]

app = FastAPI(
    title="TODO API",
    description="""
## TODO API — учебный проект

Простой API для управления задачами.

### Возможности
- Создавать, читать, обновлять и удалять задачи
- Фильтровать по статусу выполнения
""",
    version="0.1.0",
    contact={
        "name": "Иван Иванов",
        "email": "ivan@mipt.ru",
    },
    openapi_tags=tags_metadata,
)


@app.get("/health", tags=["health"], summary="Проверка работоспособности")
def health() -> dict:
    """Возвращает статус сервиса."""
    return {"status": "ok"}
```

Запустите и откройте http://127.0.0.1:8000/docs:
- Вверху страницы — название, версия, описание с Markdown-форматированием
- Эндпоинты сгруппированы по тегам (tasks, health)
- Секция «health» выделена в отдельную группу

</details>

---

## Часть 5: Pydantic + документация эндпоинтов

> **Теория:** [README.md — Блок 5](../README.md#блок-5-pydantic-модели--документация-эндпоинтов-10-мин) | **Примеры:** [`examples/05_pydantic_docs.py`](../examples/05_pydantic_docs.py)

### Задание 5.1

Изучите поведение `model_dump(exclude_unset=True)` на практике:

```python
from pydantic import BaseModel

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    done: bool | None = None

# Случай A: клиент передал только done=True
update_a = TaskUpdate(done=True)

# Случай B: клиент передал title и done
update_b = TaskUpdate(title="Новый заголовок", done=False)

# Случай C: клиент передал пустой объект {}
update_c = TaskUpdate()
```

Для каждого случая предскажите вывод:
- `model.model_dump()`
- `model.model_dump(exclude_unset=True)`

Объясните, почему `exclude_unset=True` критически важен для реализации PATCH-эндпоинта.

<details>
<summary>Подсказка</summary>

`exclude_unset=True` включает только поля, которые были **явно переданы** при создании объекта, даже если их значение `None`. Без него все поля с `default=None` тоже попадут в словарь.

Подумайте: если PATCH-запрос содержит только `{"done": true}`, и мы применим `model_dump()` (без `exclude_unset`), что случится с полем `title` существующей задачи?

</details>

<details>
<summary>Решение</summary>

```python
from pydantic import BaseModel

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    done: bool | None = None

# Случай A: только done=True
update_a = TaskUpdate(done=True)
print(update_a.model_dump())
# {'title': None, 'description': None, 'done': True}
print(update_a.model_dump(exclude_unset=True))
# {'done': True}   ← только явно переданное

# Случай B: title и done
update_b = TaskUpdate(title="Новый заголовок", done=False)
print(update_b.model_dump())
# {'title': 'Новый заголовок', 'description': None, 'done': False}
print(update_b.model_dump(exclude_unset=True))
# {'title': 'Новый заголовок', 'done': False}

# Случай C: пустой объект
update_c = TaskUpdate()
print(update_c.model_dump())
# {'title': None, 'description': None, 'done': None}
print(update_c.model_dump(exclude_unset=True))
# {}   ← ничего не установлено явно
```

**Почему `exclude_unset=True` критически важен для PATCH:**

Допустим, в БД хранится задача:
```python
task = {"id": 1, "title": "Купить продукты", "description": "Молоко", "done": False}
```

Клиент отправляет PATCH только с `{"done": true}` (хочет отметить как выполненную).

```python
# БЕЗ exclude_unset — ПЛОХО:
update = TaskUpdate(done=True)
task.update(update.model_dump())
# task = {"id": 1, "title": None, "description": None, "done": True}
# title и description перезаписались в None! ❌

# С exclude_unset=True — ПРАВИЛЬНО:
task.update(update.model_dump(exclude_unset=True))
# task = {"id": 1, "title": "Купить продукты", "description": "Молоко", "done": True}
# Изменился только done ✅
```

</details>

---

### Задание 5.2

Добавьте Pydantic-валидатор к модели `TaskCreate` из примера. Валидатор должен:

1. Автоматически удалять пробелы в начале и конце `title` (`.strip()`)
2. Запрещать `title`, состоящий только из пробелов (поднимать `ValueError`)
3. Проверьте валидатор: что происходит при `TaskCreate(title="   ")`?

<details>
<summary>Подсказка</summary>

Используйте `@field_validator("title")` из Pydantic v2. Декоратор `@classmethod` обязателен. Метод принимает `cls` и значение `v: str`, возвращает обработанное значение (или поднимает `ValueError`).

```python
from pydantic import BaseModel, field_validator

class MyModel(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        # обработайте v и верните результат
        ...
```

</details>

<details>
<summary>Решение</summary>

```python
from pydantic import BaseModel, Field, field_validator

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок задачи")
    description: str = Field(default="", description="Описание задачи")

    @field_validator("title")
    @classmethod
    def title_strip_and_validate(cls, v: str) -> str:
        """Обрезать пробелы и запретить пустой заголовок."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Заголовок не может состоять только из пробелов")
        return stripped  # возвращаем обрезанное значение


# Проверка:
from pydantic import ValidationError

# Корректный вариант с пробелами:
task = TaskCreate(title="  Купить продукты  ")
print(task.title)  # "Купить продукты" — пробелы убраны ✅

# Только пробелы → ошибка:
try:
    TaskCreate(title="   ")
except ValidationError as e:
    print(e)
    # 1 validation error for TaskCreate
    # title
    #   Value error, Заголовок не может состоять только из пробелов
```

**Как это работает:** `@field_validator` вызывается до создания объекта. Если функция поднимает `ValueError` — Pydantic преобразует его в `ValidationError`. FastAPI перехватывает `ValidationError` и возвращает 422 с описанием ошибки.

</details>

---

## Бонусные задания

### Бонус 1: Статистика задач

Добавьте эндпоинт `GET /tasks/stats`, который возвращает статистику:

```json
{
  "total": 5,
  "done": 2,
  "active": 3,
  "completion_rate": 0.4
}
```

Требования:
- Создайте Pydantic-модель `TaskStats` для ответа
- Используйте `response_model=TaskStats`
- `completion_rate` — доля выполненных задач (0.0–1.0), округлённая до 2 знаков

> **Внимание:** маршрут `/tasks/stats` нужно зарегистрировать **до** `/tasks/{task_id}`, иначе FastAPI попытается интерпретировать `"stats"` как `task_id` (целое число) и вернёт 422.

<details>
<summary>Подсказка</summary>

Порядок регистрации маршрутов важен. Статичный маршрут (`/tasks/stats`) должен идти раньше параметрического (`/tasks/{task_id}`).

Для `completion_rate` используйте: `done_count / total` если `total > 0`, иначе `0.0`.

</details>

<details>
<summary>Решение</summary>

```python
from pydantic import BaseModel

class TaskStats(BaseModel):
    total: int = Field(..., description="Всего задач")
    done: int = Field(..., description="Выполненных задач")
    active: int = Field(..., description="Активных задач")
    completion_rate: float = Field(..., description="Доля выполненных (0.0–1.0)")


# ВАЖНО: этот маршрут должен быть зарегистрирован ДО @app.get("/tasks/{task_id}")
@app.get("/tasks/stats", response_model=TaskStats,
         summary="Статистика задач", tags=["tasks"])
def get_task_stats() -> dict:
    """Получить статистику по задачам."""
    tasks = list(_db.values())
    total = len(tasks)
    done_count = sum(1 for t in tasks if t["done"])
    active = total - done_count
    rate = round(done_count / total, 2) if total > 0 else 0.0
    return {
        "total": total,
        "done": done_count,
        "active": active,
        "completion_rate": rate,
    }
```

**Почему порядок важен:** FastAPI проверяет маршруты в порядке регистрации. Если `/tasks/{task_id}` зарегистрирован первым, запрос `GET /tasks/stats` совпадёт с ним (с `task_id="stats"`), FastAPI попытается преобразовать `"stats"` в `int` и вернёт 422.

</details>

---

### Бонус 2: Полный **TODO API**

Реализуйте полный **TODO API** с Pydantic-моделями и документацией. Требования:

- Три модели: `TaskCreate`, `TaskUpdate`, `TaskResponse`
- Все поля с `description=` и хотя бы один `examples=`
- Эндпоинты: `POST /tasks`, `GET /tasks`, `GET /tasks/{id}`, `PATCH /tasks/{id}`, `DELETE /tasks/{id}`
- Каждый эндпоинт с `response_model`, `status_code`, `summary`, `tags`
- `HTTPException` с 404 для несуществующих задач
- Фильтрация по `done` в `GET /tasks`

После реализации запустите сервер и проверьте в Swagger UI:
1. Создайте 3 задачи через `POST /tasks`
2. Отметьте одну как выполненную через `PATCH /tasks/{id}`
3. Проверьте `GET /tasks?done=true` — должна вернуться только выполненная
4. Удалите одну задачу и убедитесь, что `GET /tasks/{id}` вернёт 404

<details>
<summary>Подсказка</summary>

Используйте `examples/05_pydantic_docs.py` как отправную точку — там уже реализована большая часть. Ваша задача — убедиться, что:
- `GET /tasks?done=true` фильтрует правильно
- PATCH использует `model_dump(exclude_unset=True)`
- DELETE возвращает `None` (FastAPI сам вернёт 204)

</details>

<details>
<summary>Решение</summary>

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="TODO API", version="1.0.0")

_db: dict[int, dict] = {}
_next_id = 1


class TaskCreate(BaseModel):
    title: str = Field(
        ..., min_length=1, max_length=200,
        description="Заголовок задачи", examples=["Купить продукты"]
    )
    description: str = Field(default="", description="Описание")

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Заголовок не может быть пустым")
        return stripped


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = None
    done: bool | None = None


class TaskResponse(BaseModel):
    id: int = Field(..., description="ID задачи", examples=[1])
    title: str = Field(..., description="Заголовок", examples=["Купить продукты"])
    description: str = Field(default="")
    done: bool = Field(default=False, description="Выполнена?")


@app.post("/tasks", response_model=TaskResponse, status_code=201,
          summary="Создать задачу", tags=["tasks"])
def create_task(task: TaskCreate) -> dict:
    """Создать новую задачу. Поле done всегда False для новой задачи."""
    global _next_id
    new = {"id": _next_id, "title": task.title,
           "description": task.description, "done": False}
    _db[_next_id] = new
    _next_id += 1
    return new


@app.get("/tasks", response_model=list[TaskResponse],
         summary="Список задач", tags=["tasks"])
def list_tasks(done: bool | None = None,
               limit: int = Query(default=100, ge=1, le=1000)) -> list[dict]:
    """Получить задачи. Фильтр ?done=true/false. Лимит до 1000."""
    tasks = list(_db.values())
    if done is not None:
        tasks = [t for t in tasks if t["done"] == done]
    return tasks[:limit]


@app.get("/tasks/{task_id}", response_model=TaskResponse,
         summary="Получить задачу", tags=["tasks"],
         responses={404: {"description": "Задача не найдена"}})
def get_task(task_id: int) -> dict:
    """Получить задачу по ID."""
    if task_id not in _db:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")
    return _db[task_id]


@app.patch("/tasks/{task_id}", response_model=TaskResponse,
           summary="Обновить задачу", tags=["tasks"],
           responses={404: {"description": "Задача не найдена"}})
def update_task(task_id: int, task_update: TaskUpdate) -> dict:
    """Частично обновить задачу. Передайте только изменяемые поля."""
    if task_id not in _db:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")
    _db[task_id].update(task_update.model_dump(exclude_unset=True))
    return _db[task_id]


@app.delete("/tasks/{task_id}", status_code=204,
            summary="Удалить задачу", tags=["tasks"],
            responses={404: {"description": "Задача не найдена"}})
def delete_task(task_id: int) -> None:
    """Удалить задачу. Возвращает 204 No Content при успехе."""
    if task_id not in _db:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")
    del _db[task_id]
```

**Проверка в Swagger UI (`/docs`):**
1. `POST /tasks` с `{"title": "Первая"}` → 201, получаем `{"id": 1, ..., "done": false}`
2. `POST /tasks` × 2 ещё задачи
3. `PATCH /tasks/1` с `{"done": true}` → 200
4. `GET /tasks?done=true` → список из 1 задачи ✅
5. `DELETE /tasks/2` → 204
6. `GET /tasks/2` → 404 ✅

</details>

---

### Бонус 3: Полная структура проекта

Организуйте TODO API из Бонус 2 в виде полноценной структуры проекта:

```
todo_api/
├── main.py         # FastAPI() + include_router
├── models.py       # TaskCreate, TaskUpdate, TaskResponse, TaskStats
└── routers/
    ├── __init__.py
    └── tasks.py    # Все эндпоинты + in-memory хранилище
```

Дополнительно:
- Вынесите in-memory хранилище в отдельную переменную модуля `routers/tasks.py`
- Добавьте эндпоинт `DELETE /tasks` (без ID) — удалить все задачи (полезно для тестов), возвращает `{"deleted": N}`
- Напишите конфигурацию приложения в `main.py` с `title`, `description` и метаданными тегов

<details>
<summary>Подсказка</summary>

Структура аналогична `examples/03_project_structure/`. Обратите внимание на импорты: в `routers/tasks.py` используйте `from ..models import ...` для импорта моделей из родительского пакета.

Для `DELETE /tasks` (без ID): `@router.delete("/", status_code=200)` — здесь уместен 200 с телом ответа (не 204, т.к. возвращаем количество удалённых).

</details>

<details>
<summary>Решение</summary>

```python
# models.py
from pydantic import BaseModel, Field, field_validator

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200,
                       examples=["Купить продукты"])
    description: str = Field(default="")

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Заголовок не может быть пустым")
        return s

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    done: bool | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    done: bool

class TaskStats(BaseModel):
    total: int
    done: int
    active: int
    completion_rate: float
```

```python
# routers/tasks.py
from fastapi import APIRouter, HTTPException
from ..models import TaskCreate, TaskResponse, TaskStats, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

_db: dict[int, dict] = {}
_next_id = 1


@router.get("/stats", response_model=TaskStats, summary="Статистика")
def get_stats() -> dict:
    tasks = list(_db.values())
    total = len(tasks)
    done_n = sum(1 for t in tasks if t["done"])
    return {"total": total, "done": done_n, "active": total - done_n,
            "completion_rate": round(done_n / total, 2) if total else 0.0}


@router.post("/", response_model=TaskResponse, status_code=201,
             summary="Создать задачу")
def create_task(task: TaskCreate) -> dict:
    global _next_id
    new = {"id": _next_id, "title": task.title,
           "description": task.description, "done": False}
    _db[_next_id] = new
    _next_id += 1
    return new


@router.get("/", response_model=list[TaskResponse], summary="Список задач")
def list_tasks(done: bool | None = None) -> list[dict]:
    tasks = list(_db.values())
    if done is not None:
        tasks = [t for t in tasks if t["done"] == done]
    return tasks


@router.get("/{task_id}", response_model=TaskResponse, summary="Получить задачу")
def get_task(task_id: int) -> dict:
    if task_id not in _db:
        raise HTTPException(404, detail=f"Задача {task_id} не найдена")
    return _db[task_id]


@router.patch("/{task_id}", response_model=TaskResponse, summary="Обновить задачу")
def update_task(task_id: int, upd: TaskUpdate) -> dict:
    if task_id not in _db:
        raise HTTPException(404, detail=f"Задача {task_id} не найдена")
    _db[task_id].update(upd.model_dump(exclude_unset=True))
    return _db[task_id]


@router.delete("/{task_id}", status_code=204, summary="Удалить задачу")
def delete_task(task_id: int) -> None:
    if task_id not in _db:
        raise HTTPException(404, detail=f"Задача {task_id} не найдена")
    del _db[task_id]


@router.delete("/", status_code=200, summary="Удалить все задачи")
def delete_all_tasks() -> dict:
    global _db, _next_id
    count = len(_db)
    _db = {}
    _next_id = 1
    return {"deleted": count}
```

```python
# main.py
from fastapi import FastAPI
from .routers import tasks

app = FastAPI(
    title="TODO API",
    description="Полный учебный пример структуры FastAPI-проекта.",
    version="1.0.0",
    openapi_tags=[
        {"name": "tasks", "description": "Управление задачами"},
    ],
)

app.include_router(tasks.router)


@app.get("/", tags=["root"])
def root() -> dict:
    return {"message": "TODO API", "docs": "/docs"}
```

</details>

---

## Полезные ресурсы

- [FastAPI — First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) — официальный туториал, начало
- [FastAPI — Path/Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/) — path и query параметры
- [Pydantic — Fields](https://docs.pydantic.dev/latest/concepts/fields/) — Field, validators, constraints
- [HTTPie](https://httpie.io/) — удобный CLI-клиент для тестирования API из терминала
- [HTTP Status Codes (MDN)](https://developer.mozilla.org/ru/docs/Web/HTTP/Status) — полный справочник статус-кодов
