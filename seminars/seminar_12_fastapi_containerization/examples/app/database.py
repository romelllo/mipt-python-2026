"""Настройка подключения к базе данных через SQLAlchemy."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# ============================================================
# Строка подключения к БД из переменной окружения
# ============================================================
# В Docker Compose DATABASE_URL задаётся в блоке environment:
#   DATABASE_URL=postgresql://user:password@db:5432/tasks_db
#
# Для локальной разработки без Docker можно задать в .env:
#   DATABASE_URL=postgresql://user:password@localhost:5432/tasks_db
#
# Fallback на SQLite — только для быстрого локального запуска.
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "sqlite:///./tasks.db",
)

# ============================================================
# Движок SQLAlchemy
# ============================================================
# connect_args={"check_same_thread": False} — только для SQLite,
# чтобы несколько потоков могли использовать одно соединение.
# Для PostgreSQL этот аргумент не нужен.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(DATABASE_URL)

# ============================================================
# Фабрика сессий
# ============================================================
# autocommit=False — транзакции подтверждаются явно через session.commit()
# autoflush=False  — изменения не сбрасываются в БД до commit()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ============================================================
# Базовый класс для ORM-моделей
# ============================================================
class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей."""

    pass


# ============================================================
# Dependency для FastAPI — получение сессии БД
# ============================================================
def get_db() -> Session:  # type: ignore[return]
    """Dependency: создать сессию БД и закрыть её после запроса.

    Используется через Depends(get_db) в роутерах FastAPI.
    Гарантирует закрытие сессии даже при исключении.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
