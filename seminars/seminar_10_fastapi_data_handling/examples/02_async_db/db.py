"""
Семинар 10, Блок 2: Асинхронный движок и сессии базы данных.

Содержит:
- async engine (asyncpg)
- async_sessionmaker → AsyncSession
- lifespan: create_all при старте приложения
- get_session: dependency injection через Depends()

DATABASE_URL задаётся через переменную окружения.
По умолчанию: postgresql+asyncpg://postgres:postgres@localhost:5432/notes_db
"""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

# ============================================================
# 1. URL базы данных
# ============================================================
# Берём из переменной окружения или используем дефолт для локальной разработки.
# asyncpg — асинхронный драйвер PostgreSQL.
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/notes_db",
)

# ============================================================
# 2. Async Engine
# ============================================================
# create_async_engine — асинхронный аналог create_engine.
# echo=True выводит SQL — удобно при разработке, отключите в production.
async_engine = create_async_engine(DATABASE_URL, echo=True)

# ============================================================
# 3. AsyncSession factory
# ============================================================
# async_sessionmaker создаёт сессии с нужными параметрами.
# expire_on_commit=False — объекты остаются доступны после commit().
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ============================================================
# 4. Lifespan: создание таблиц при старте
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan-контекст FastAPI приложения.

    Startup: создаём таблицы (если не существуют).
    Shutdown: закрываем соединения с БД.

    В production используйте Alembic вместо create_all!
    """
    async with async_engine.begin() as conn:
        # create_all создаёт таблицы по метаданным SQLModel.
        # Аналог: CREATE TABLE IF NOT EXISTS ...
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✓ База данных готова")
    yield
    # Shutdown
    await async_engine.dispose()
    print("✓ Соединения с БД закрыты")


# ============================================================
# 5. Dependency: get_session
# ============================================================
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость FastAPI для получения сессии БД.

    Используется через Depends(get_session) в эндпоинтах.
    Автоматически закрывает сессию после запроса.

    Пример:
        @router.get("/notes")
        async def list_notes(session: AsyncSession = Depends(get_session)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session


# ============================================================
# 6. Аннотированный тип для удобного использования в роутерах
# ============================================================
# SessionDep — сокращение для повторного использования в сигнатурах функций.
# Вместо: session: AsyncSession = Depends(get_session)
# Пишем:  session: SessionDep
SessionDep = Annotated[AsyncSession, Depends(get_session)]
