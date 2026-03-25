"""
Семинар 9: Структура FastAPI-проекта — модели данных.

Здесь хранятся Pydantic-модели, используемые в разных роутерах.
Разделение моделей и маршрутов позволяет избежать циклических импортов
и делает код чище.
"""

from pydantic import BaseModel, Field

# ============================================================
# Модели для ресурса «Задача» (Task)
# ============================================================


class TaskBase(BaseModel):
    """Базовые поля задачи, общие для создания и обновления."""

    title: str = Field(
        ..., min_length=1, max_length=200, description="Заголовок задачи"
    )
    description: str = Field(default="", max_length=1000, description="Описание задачи")


class TaskCreate(TaskBase):
    """Тело запроса при создании задачи (POST /tasks)."""

    # При создании поле done всегда False — клиент не задаёт его
    pass


class TaskUpdate(BaseModel):
    """Тело запроса при обновлении задачи (PATCH /tasks/{id}).

    Все поля необязательны: клиент передаёт только то, что хочет изменить.
    """

    title: str | None = Field(
        default=None, min_length=1, max_length=200, description="Новый заголовок"
    )
    description: str | None = Field(default=None, description="Новое описание")
    done: bool | None = Field(default=None, description="Статус выполнения")


class TaskResponse(TaskBase):
    """Ответ сервера с данными задачи (включает поля, генерируемые сервером)."""

    id: int = Field(..., description="Уникальный идентификатор задачи")
    done: bool = Field(default=False, description="Выполнена ли задача")

    model_config = {"from_attributes": True}
