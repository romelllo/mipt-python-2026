"""
Семинар 10, Блок 2–3: Notes API — основной файл приложения.

Запуск (из корня репозитория):
    # Предварительно: docker compose up -d (PostgreSQL)
    uvicorn seminars.seminar_10_fastapi_data_handling.examples.02_async_db.main:app --reload

    # Swagger UI: http://127.0.0.1:8000/docs
    # Задать DATABASE_URL через переменную окружения:
    # DATABASE_URL=postgresql+asyncpg://user:pass@host/db uvicorn ...
"""

from fastapi import FastAPI

from .db import lifespan  # type: ignore[import]
from .routers.notes import router as notes_router  # type: ignore[import]

# ============================================================
# Создание приложения FastAPI с lifespan
# ============================================================
app = FastAPI(
    title="Notes API",
    description="""
## Notes API

REST API для управления заметками с хранением в **PostgreSQL**.

### Стек
- **FastAPI** — фреймворк
- **SQLModel** — ORM + Pydantic (модели и таблицы)
- **asyncpg** — асинхронный драйвер PostgreSQL
- **SQLAlchemy** — async engine и сессии
""",
    version="1.0.0",
    lifespan=lifespan,  # создаёт таблицы при старте
)

# ============================================================
# Подключение роутеров
# ============================================================
app.include_router(notes_router)
