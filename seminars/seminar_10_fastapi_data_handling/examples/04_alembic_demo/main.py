"""
Семинар 10, Блок 4: Notes API с Alembic — основной файл.

Запуск:
    # 1. Запустить PostgreSQL:
    #    docker compose up -d
    #
    # 2. Сгенерировать первую миграцию:
    #    cd seminars/seminar_10_fastapi_data_handling/examples/04_alembic_demo
    #    alembic revision --autogenerate -m "create notes table"
    #
    # 3. Применить миграцию:
    #    alembic upgrade head
    #
    # 4. Запустить сервер:
    #    cd <корень репозитория>
    #    uvicorn seminars.seminar_10_fastapi_data_handling.examples.04_alembic_demo.main:app --reload
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlmodel import select

from .db import async_engine  # type: ignore[import]
from .models import Note  # type: ignore[import]

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan: только инициализация — таблицы создаёт Alembic."""
    print("✓ Приложение запущено (таблицы управляются через Alembic)")
    yield
    await async_engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость FastAPI для получения сессии."""
    async with AsyncSessionLocal() as session:
        yield session


app = FastAPI(
    title="Notes API (Alembic)",
    description="Notes API с миграциями через Alembic.",
    version="2.0.0",
    lifespan=lifespan,
)


@app.get("/notes", response_model=list[dict])
async def list_notes() -> list[dict]:
    """Получить все заметки."""
    async with AsyncSessionLocal() as session:
        result = await session.exec(select(Note))  # type: ignore[call-overload]
        return [
            {"id": n.id, "title": n.title, "content": n.content} for n in result.all()
        ]


@app.get("/notes/{note_id}", response_model=dict)
async def get_note(note_id: int) -> dict:
    """Получить заметку по ID."""
    async with AsyncSessionLocal() as session:
        note = await session.get(Note, note_id)
        if note is None:
            raise HTTPException(status_code=404, detail="Заметка не найдена")
        return {"id": note.id, "title": note.title, "content": note.content}
