"""
Семинар 9: Pydantic-модели и документирование эндпоинтов.

Демонстрирует:
- Базовые Pydantic-модели: BaseModel, Field
- Разделение моделей: Create / Update / Response
- Параметры Field: description, example, min_length, ge, le
- response_model — типизация ответа и документация схемы
- status_code — правильные HTTP-коды для каждой операции
- summary, description на эндпоинтах — документация в Swagger UI
- HTTPException с кастомными деталями

Запуск (из корня репозитория):
    python seminars/seminar_09_fastapi_intro/examples/05_pydantic_docs.py

Или через uvicorn:
    uvicorn seminars.seminar_09_fastapi_intro.examples.05_pydantic_docs:app --reload
    → Swagger UI: http://127.0.0.1:8000/docs
"""

import json

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, field_validator

# ============================================================
# 1. Pydantic-модели: разделение по назначению
# ============================================================
# Хорошая практика — иметь отдельные модели для:
#   TaskCreate   — тело запроса при создании (без id, без done)
#   TaskUpdate   — тело запроса при обновлении (все поля Optional)
#   TaskResponse — ответ сервера (включает id, done)
#
# Это явно разграничивает: что клиент отправляет → что сервер возвращает.


class TaskCreate(BaseModel):
    """Тело запроса при создании задачи.

    Клиент обязан указать title. description — необязательное.
    Поле `done` клиент не задаёт: новая задача всегда не выполнена.
    """

    title: str = Field(
        ...,  # обязательное поле (без default)
        min_length=1,
        max_length=200,
        description="Заголовок задачи",
        examples=["Купить продукты"],
    )
    description: str = Field(
        default="",
        max_length=1000,
        description="Подробное описание задачи",
        examples=["Молоко, хлеб, яйца"],
    )

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str) -> str:
        """Заголовок не должен состоять только из пробелов."""
        if not v.strip():
            raise ValueError("Заголовок не может быть пустым")
        return v.strip()


class TaskUpdate(BaseModel):
    """Тело запроса при частичном обновлении задачи (PATCH).

    Все поля Optional: клиент передаёт только то, что хочет изменить.
    """

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Новый заголовок задачи",
        examples=["Обновлённый заголовок"],
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Новое описание",
    )
    done: bool | None = Field(
        default=None,
        description="Статус выполнения: true — выполнена, false — активна",
        examples=[True],
    )


class TaskResponse(BaseModel):
    """Ответ сервера с данными задачи.

    Включает поля, генерируемые сервером: id.
    """

    id: int = Field(..., description="Уникальный идентификатор", examples=[1])
    title: str = Field(
        ..., description="Заголовок задачи", examples=["Купить продукты"]
    )
    description: str = Field(default="", description="Описание задачи")
    done: bool = Field(default=False, description="Выполнена ли задача")

    model_config = {"from_attributes": True}


# ============================================================
# 2. Приложение FastAPI
# ============================================================

app = FastAPI(
    title="TODO API — полная документация",
    description="Пример полностью документированного FastAPI-приложения.",
    version="1.0.0",
)

# In-memory хранилище для примера
_db: dict[int, dict] = {}
_next_id = 1


# ============================================================
# 3. Документированные эндпоинты
# ============================================================


@app.post(
    "/tasks",
    response_model=TaskResponse,  # тип ответа → схема в Swagger UI
    status_code=201,  # 201 Created для успешного создания
    summary="Создать задачу",  # краткое название в Swagger UI
    description="""
Создаёт новую задачу и возвращает её с присвоенным `id`.

**Правила:**
- `title` обязателен и не может быть пустым
- `done` всегда `false` для новой задачи (клиент не управляет этим полем)
""",
    tags=["tasks"],
)
def create_task(task: TaskCreate) -> dict:
    """Создать новую задачу."""
    global _next_id
    new_task = {
        "id": _next_id,
        "title": task.title,
        "description": task.description,
        "done": False,
    }
    _db[_next_id] = new_task
    _next_id += 1
    return new_task


@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    status_code=200,
    summary="Получить список задач",
    tags=["tasks"],
)
def list_tasks(
    done: bool | None = None,
    limit: int = Query(
        default=100, ge=1, le=1000, description="Максимальное количество задач"
    ),
) -> list[dict]:
    """Получить все задачи.

    - `done=true` → только выполненные
    - `done=false` → только активные
    - `limit` — максимальное количество задач в ответе (1–1000)
    """
    tasks = list(_db.values())
    if done is not None:
        tasks = [t for t in tasks if t["done"] == done]
    return tasks[:limit]


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=200,
    summary="Получить задачу по ID",
    responses={
        404: {"description": "Задача не найдена"},
    },
    tags=["tasks"],
)
def get_task(task_id: int) -> dict:
    """Получить одну задачу по её ID.

    Возвращает 404, если задача с таким ID не существует.
    """
    if task_id not in _db:
        raise HTTPException(
            status_code=404,
            detail=f"Задача с id={task_id} не найдена",
        )
    return _db[task_id]


@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=200,
    summary="Обновить задачу",
    responses={
        404: {"description": "Задача не найдена"},
    },
    tags=["tasks"],
)
def update_task(task_id: int, task_update: TaskUpdate) -> dict:
    """Частично обновить задачу (PATCH).

    Передайте только те поля, которые нужно изменить.
    Непереданные поля останутся без изменений.
    """
    if task_id not in _db:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")
    task = _db[task_id]
    # exclude_unset=True → обновляем только явно переданные поля
    updates = task_update.model_dump(exclude_unset=True)
    task.update(updates)
    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=204,  # 204 No Content — тело ответа пустое
    summary="Удалить задачу",
    responses={
        404: {"description": "Задача не найдена"},
    },
    tags=["tasks"],
)
def delete_task(task_id: int) -> None:
    """Удалить задачу по ID.

    Возвращает 204 No Content при успехе (тело ответа отсутствует).
    """
    if task_id not in _db:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")
    del _db[task_id]


# ============================================================
# 4. Демонстрация валидации Pydantic без сервера
# ============================================================


def demo_pydantic_validation() -> None:
    """Показать работу валидации Pydantic напрямую."""
    print("=" * 60)
    print("СЕМИНАР 9: PYDANTIC-МОДЕЛИ + ДОКУМЕНТАЦИЯ ЭНДПОИНТОВ")
    print("=" * 60)
    print()

    # Корректные данные
    print("1. Корректное создание задачи:")
    task = TaskCreate(title="Купить продукты", description="Молоко, хлеб")
    print(f"   {task.model_dump()}")
    print()

    # Автоматическое приведение типов
    print("2. Автоматическое приведение типов:")
    task2 = TaskCreate(title="  Задача с пробелами  ")  # validator уберёт пробелы
    print(f"   title после валидатора: {task2.title!r}")
    print()

    # Ошибка валидации
    print("3. Ошибка валидации (пустой title):")
    try:
        TaskCreate(title="   ")
    except Exception as e:
        # Показываем первую ошибку
        errors = e.errors()  # type: ignore[union-attr]
        print(f"   Ошибка: {errors[0]['msg']}")
    print()

    # PATCH-модель: только обновляемые поля
    print("4. TaskUpdate — только переданные поля:")
    update = TaskUpdate(done=True)
    # exclude_unset=True — ключевой паттерн для PATCH
    print(f"   model_dump():               {update.model_dump()}")
    print(f"   model_dump(exclude_unset=True): {update.model_dump(exclude_unset=True)}")
    print()

    # JSON-схема (то, что видит Swagger UI)
    print("5. JSON-схема TaskCreate (для Swagger UI):")
    schema = TaskCreate.model_json_schema()
    print(f"   {json.dumps(schema, ensure_ascii=False, indent=2)}")
    print()

    print("Запустите сервер для просмотра документации:")
    print(
        "  uvicorn seminars.seminar_09_fastapi_intro.examples.05_pydantic_docs:app --reload"
    )
    print("  → http://127.0.0.1:8000/docs")


def main() -> None:
    """Точка входа."""
    demo_pydantic_validation()


if __name__ == "__main__":
    main()
