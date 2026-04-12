"""Роутер аутентификации: регистрация и логин."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import (  # type: ignore[import]
    create_access_token,
    hash_password,
    verify_password,
)
from ..dependencies import fake_users_db  # type: ignore[import]
from ..models import Token, UserCreate, UserInDB, UserResponse  # type: ignore[import]

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user_data: UserCreate) -> UserResponse:
    """Зарегистрировать нового пользователя.

    - Проверяет, что username не занят
    - Хеширует пароль (НИКОГДА не сохраняем plain text!)
    - Сохраняет UserInDB в "базу данных"
    """
    # Проверяем уникальность username
    if user_data.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Хешируем пароль перед сохранением
    hashed = hash_password(user_data.password)

    # Сохраняем в "БД"
    new_user = UserInDB(
        username=user_data.username,
        hashed_password=hashed,
        is_active=True,
    )
    fake_users_db[user_data.username] = new_user

    return UserResponse(username=new_user.username, is_active=new_user.is_active)


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Выдать JWT access token при успешном логине.

    OAuth2PasswordRequestForm ожидает form-encoded тело:
        username=alice&password=secret

    Swagger UI автоматически создаёт форму для этого эндпоинта
    (потому что он указан в OAuth2PasswordBearer(tokenUrl=...)).
    """
    # Ищем пользователя
    user = fake_users_db.get(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем пароль против хеша из "БД"
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаём JWT токен
    # "sub" (subject) — стандартный claim для идентификатора пользователя
    access_token = create_access_token(data={"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")
