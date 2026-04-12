"""Логика аутентификации: хеширование паролей + JWT токены.

Этот модуль — "сердце" системы безопасности:
- hash_password / verify_password — работа с bcrypt
- create_access_token / decode_access_token — работа с JWT
"""

import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

# ============================================================
# Конфигурация
# ============================================================

# В production: SECRET_KEY берётся из переменной окружения!
# Генерация: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ============================================================
# Хеширование паролей (passlib + bcrypt)
# ============================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Захешировать пароль с bcrypt.

    Args:
        plain_password: пароль в открытом виде

    Returns:
        bcrypt хеш (каждый раз разный из-за соли)
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить пароль против bcrypt хеша.

    Args:
        plain_password: введённый пользователем пароль
        hashed_password: хеш из "базы данных"

    Returns:
        True если пароль совпадает
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================
# JWT токены (python-jose)
# ============================================================


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """Создать подписанный JWT access token.

    Args:
        data: payload данные (обычно {"sub": username})
        expires_delta: время жизни; по умолчанию ACCESS_TOKEN_EXPIRE_MINUTES

    Returns:
        JWT токен в виде строки
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
    """Декодировать JWT и извлечь username (sub claim).

    Args:
        token: JWT-строка из заголовка Authorization: Bearer <token>

    Returns:
        username из токена, или None если токен невалиден
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        return username
    except JWTError:
        # Включает ExpiredSignatureError — истёкший токен тоже невалиден
        return None
