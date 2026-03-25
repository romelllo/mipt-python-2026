"""
Семинар 9: Структура FastAPI-проекта — роутер задач.

Роутер (APIRouter) — способ разбить большое приложение на модули.
Каждый роутер отвечает за свой ресурс (tasks, users, orders и т.д.)
и подключается к главному приложению в main.py через app.include_router().
"""

from fastapi import APIRouter, HTTPException

from ..models import TaskCreate, TaskResponse, TaskUpdate  # type: ignore[import]

# ============================================================
# Создание роутера с общим префиксом и тегом
# ============================================================
# prefix="/tasks"  → все маршруты этого роутера начинаются с /tasks
# tags=["tasks"]   → группировка в Swagger UI

router = APIRouter(prefix="/tasks", tags=["tasks"])

# ============================================================
# In-memory хранилище (имитация базы данных)
# ============================================================
# В реальном проекте здесь будет SQLAlchemy Session или другая БД.
# Для учебного примера используем словарь.

_tasks_db: dict[int, dict] = {}
_next_id = 1


# ============================================================
# CRUD-эндпоинты
# ============================================================


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate) -> dict:
    """Создать новую задачу.

    Принимает title и description, возвращает созданный объект с id.
    """
    global _next_id
    new_task = {
        "id": _next_id,
        "title": task.title,
        "description": task.description,
        "done": False,
    }
    _tasks_db[_next_id] = new_task
    _next_id += 1
    return new_task


@router.get("/", response_model=list[TaskResponse])
def list_tasks(done: bool | None = None) -> list[dict]:
    """Получить список всех задач.

    Опциональный query-параметр `done` фильтрует по статусу:
    - `?done=true`  → только выполненные
    - `?done=false` → только активные
    - (без параметра) → все задачи
    """
    tasks = list(_tasks_db.values())
    if done is not None:
        tasks = [t for t in tasks if t["done"] == done]
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int) -> dict:
    """Получить задачу по ID.

    Возвращает 404, если задача не найдена.
    """
    if task_id not in _tasks_db:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")
    return _tasks_db[task_id]


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate) -> dict:
    """Частично обновить задачу.

    Обновляет только переданные поля (PATCH, не PUT).
    """
    if task_id not in _tasks_db:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")
    task = _tasks_db[task_id]
    # Обновляем только те поля, которые клиент явно передал
    update_data = task_update.model_dump(exclude_unset=True)
    task.update(update_data)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    """Удалить задачу по ID.

    Возвращает 204 No Content при успехе, 404 если не найдена.
    """
    if task_id not in _tasks_db:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")
    del _tasks_db[task_id]
