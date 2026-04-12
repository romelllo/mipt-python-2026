"""Модели данных для auth-приложения."""

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Схема для регистрации нового пользователя."""

    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)


class UserResponse(BaseModel):
    """Схема для ответа — без пароля!"""

    username: str
    is_active: bool


class UserInDB(BaseModel):
    """Внутренняя модель пользователя — хранит хеш пароля."""

    username: str
    hashed_password: str
    is_active: bool = True


class Token(BaseModel):
    """Ответ на успешный логин."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Данные из декодированного токена."""

    username: str | None = None


class ItemResponse(BaseModel):
    """Схема элемента (защищённый ресурс)."""

    id: int
    title: str
    owner: str
