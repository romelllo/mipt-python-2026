"""Главный модуль FastAPI-приложения Tasks API."""

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task

# ============================================================
# Инициализация приложения
# ============================================================
app = FastAPI(
    title="Tasks API",
    description="Простое API для управления задачами. Семинар 12 — контейнеризация.",
    version="1.0.0",
)


# ============================================================
# Pydantic-схемы (входные и выходные данные)
# ============================================================
class TaskCreate(BaseModel):
    """Схема для создания задачи (входные данные)."""

    title: str = Field(
        ..., min_length=1, max_length=200, description="Заголовок задачи"
    )
    description: str | None = Field(None, description="Описание задачи")


class TaskUpdate(BaseModel):
    """Схема для обновления задачи (все поля опциональны)."""

    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    is_done: bool | None = None


class TaskResponse(BaseModel):
    """Схема ответа — данные задачи, возвращаемые клиенту."""

    id: int
    title: str
    description: str | None
    is_done: bool

    model_config = {"from_attributes": True}


# ============================================================
# Эндпоинты
# ============================================================


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Проверка работоспособности сервиса.

    Используется Docker healthcheck и оркестраторами (k8s liveness probe).
    """
    return {"status": "ok"}


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),  # noqa: B008
) -> list[Task]:
    """Получить список всех задач с пагинацией."""
    return db.query(Task).offset(skip).limit(limit).all()


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)) -> Task:  # noqa: B008
    """Создать новую задачу."""
    task = Task(title=task_in.title, description=task_in.description)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)) -> Task:  # noqa: B008
    """Получить задачу по ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с id={task_id} не найдена",
        )
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),  # noqa: B008
) -> Task:
    """Частично обновить задачу."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с id={task_id} не найдена",
        )
    # Обновляем только переданные поля
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:  # noqa: B008
    """Удалить задачу по ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с id={task_id} не найдена",
        )
    db.delete(task)
    db.commit()
