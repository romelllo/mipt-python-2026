"""ORM-модели SQLAlchemy для приложения задач (Tasks API)."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Task(Base):
    """Модель задачи."""

    __tablename__ = "tasks"

    # Первичный ключ — автоинкремент
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Заголовок задачи — обязательное поле
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    # Описание — необязательное поле
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Статус выполнения
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Временные метки — заполняются автоматически на уровне БД
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """Строковое представление для отладки."""
        status = "✓" if self.is_done else "○"
        return f"<Task [{status}] id={self.id} title={self.title!r}>"
