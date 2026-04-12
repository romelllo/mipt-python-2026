"""FastAPI приложение с JWT аутентификацией.

Запуск:
    uvicorn seminars.seminar_11_fastapi_security_testing.examples.03_auth_app.main:app --reload

Swagger UI: http://127.0.0.1:8000/docs
    1. POST /auth/register — зарегистрироваться
    2. Нажать кнопку "Authorize" → ввести username и password
       (Swagger сделает POST /auth/login и сохранит токен)
    3. GET /me — получить свой профиль
    4. GET /items — получить свои элементы

Эндпоинты:
    POST /auth/register  — регистрация (публичный)
    POST /auth/login     — логин, возвращает JWT (публичный)
    GET  /me             — профиль текущего пользователя (защищённый)
    GET  /items          — элементы текущего пользователя (защищённый)
"""

from fastapi import FastAPI

from .routers.protected import router as protected_router  # type: ignore[import]
from .routers.users import router as auth_router  # type: ignore[import]

app = FastAPI(
    title="Auth Demo API",
    description="Демонстрация JWT аутентификации в FastAPI",
    version="1.0.0",
)

# Регистрируем роутеры
app.include_router(auth_router)  # /auth/register, /auth/login
app.include_router(protected_router)  # /me, /items


@app.get("/")
def root() -> dict:
    """Корневой эндпоинт — проверка что сервер работает."""
    return {
        "message": "Auth Demo API",
        "docs": "/docs",
        "endpoints": {
            "register": "POST /auth/register",
            "login": "POST /auth/login",
            "profile": "GET /me (требует токен)",
            "items": "GET /items (требует токен)",
        },
    }
