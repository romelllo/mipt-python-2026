"""Зависимости FastAPI — получение текущего пользователя.

Паттерн Dependency Injection:
    get_current_user — зависимость, которая проверяет Bearer токен
    и возвращает текущего пользователя (или 401 если токен невалиден).
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .auth import decode_access_token  # type: ignore[import]
from .models import UserInDB  # type: ignore[import]

# ============================================================
# OAuth2PasswordBearer — схема безопасности
# ============================================================

# OAuth2PasswordBearer говорит FastAPI:
# "Токен приходит в заголовке Authorization: Bearer <token>"
# tokenUrl — URL для получения токена (используется Swagger UI)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ============================================================
# "База данных" пользователей (in-memory для демонстрации)
# ============================================================

# В production: заменить на реальную БД (PostgreSQL + SQLModel/SQLAlchemy)
# Структура: {username: UserInDB}
fake_users_db: dict[str, UserInDB] = {}


# ============================================================
# Dependency: get_current_user
# ============================================================


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserInDB:
    """Зависимость: извлечь и валидировать текущего пользователя из токена.

    FastAPI автоматически:
    1. Читает заголовок Authorization: Bearer <token>
    2. Передаёт токен в эту функцию
    3. Если функция выбрасывает HTTPException — возвращает 401

    Args:
        token: JWT токен из Authorization заголовка

    Returns:
        UserInDB — аутентифицированный пользователь

    Raises:
        HTTPException 401: токен отсутствует, истёк или невалиден
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Декодируем токен → получаем username
    username = decode_access_token(token)
    if username is None:
        raise credentials_exception

    # Ищем пользователя в "БД"
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception

    return user


# Удобный тип-алиас для использования в эндпоинтах
CurrentUser = Annotated[UserInDB, Depends(get_current_user)]
