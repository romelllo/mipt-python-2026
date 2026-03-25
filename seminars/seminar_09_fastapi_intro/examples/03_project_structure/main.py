"""
Семинар 9: Структура FastAPI-проекта — точка входа.

main.py — корневой файл FastAPI-приложения.
Отвечает за:
- Создание экземпляра FastAPI
- Подключение роутеров через include_router()
- Корневой эндпоинт и health check

Запуск (из корня репозитория):
    uvicorn seminars.seminar_09_fastapi_intro.examples.03_project_structure.main:app --reload
    → Swagger UI: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI

from .routers import tasks  # type: ignore[import]

# ============================================================
# Создание приложения
# ============================================================

app = FastAPI(
    title="TODO API",
    description="Простой API для управления задачами — учебный пример.",
    version="1.0.0",
)

# ============================================================
# Подключение роутеров
# ============================================================
# Каждый роутер отвечает за свой ресурс.
# Добавить новый ресурс = создать новый файл в routers/ + одна строка здесь.

app.include_router(tasks.router)

# Пример расширения:
# from .routers import users, projects
# app.include_router(users.router)
# app.include_router(projects.router)


# ============================================================
# Корневые эндпоинты
# ============================================================


@app.get("/", tags=["root"])
def root() -> dict:
    """Корневой эндпоинт — подтверждает, что API работает."""
    return {"message": "TODO API работает", "docs": "/docs"}


@app.get("/health", tags=["root"])
def health_check() -> dict:
    """Health check — для систем мониторинга."""
    return {"status": "ok"}
