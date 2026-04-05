"""
Семинар 10, Блок 2 + 3: Модели SQLModel для Notes API.

Содержит:
- Note    — таблица в PostgreSQL (table=True)
- NoteCreate / NoteUpdate / NoteResponse — Pydantic-схемы
"""

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class NoteBase(SQLModel):
    """Общие поля: используются в таблице и Pydantic-схемах."""

    title: str = Field(min_length=1, max_length=200, description="Заголовок заметки")
    content: str = Field(default="", description="Содержимое заметки")


class Note(NoteBase, table=True):
    """Таблица notes в PostgreSQL.

    Поля id и created_at генерируются базой данных автоматически.
    table=True → SQLModel создаёт реальную таблицу через SQLAlchemy.
    """

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class NoteCreate(NoteBase):
    """Тело запроса при создании заметки.

    Клиент передаёт title (обязательно) и content (опционально).
    id и created_at сервер генерирует сам.
    """

    model_config = {  # type: ignore[assignment]
        "json_schema_extra": {
            "examples": [{"title": "Список покупок", "content": "Молоко, хлеб, яйца"}]
        }
    }


class NoteUpdate(SQLModel):
    """Тело запроса при частичном обновлении (PATCH).

    Все поля Optional: клиент передаёт только изменяемые поля.
    """

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Новый заголовок",
    )
    content: str | None = Field(
        default=None,
        description="Новое содержимое",
    )


class NoteResponse(NoteBase):
    """Ответ сервера: включает серверные поля id и created_at."""

    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
