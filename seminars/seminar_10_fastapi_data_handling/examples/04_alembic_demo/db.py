"""
Семинар 10, Блок 4: db.py для Alembic-проекта.

Содержит async engine для использования в приложении и Alembic env.py.
"""

import os

from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/notes_db",
)

async_engine = create_async_engine(DATABASE_URL, echo=True)
