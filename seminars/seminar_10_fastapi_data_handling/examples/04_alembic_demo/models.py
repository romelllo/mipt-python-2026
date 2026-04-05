"""
Семинар 10, Блок 4: Notes API с поддержкой Alembic.

Модели. Этот файл импортируется в alembic/env.py для autogenerate.
"""

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Note(SQLModel, table=True):
    """Таблица notes. Alembic отслеживает изменения в этой модели."""

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(default="")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
