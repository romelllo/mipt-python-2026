"""Демонстрация JWT токенов с python-jose.

Запуск:
    python seminars/seminar_11_fastapi_security_testing/examples/02_jwt_tokens.py

Зависимости:
    uv add python-jose[cryptography]
"""

# ============================================================
# Что такое JWT (JSON Web Token)
# ============================================================
#
# JWT — это компактный, самодостаточный способ передачи информации
# между сторонами в виде JSON-объекта, подписанного цифровой подписью.
#
# Структура JWT: header.payload.signature
#   header    — тип токена и алгоритм подписи (base64url)
#   payload   — данные (claims): user_id, exp, iat и т.д. (base64url)
#   signature — HMAC-SHA256(header + "." + payload, secret_key)
#
# Ключевое: payload можно ДЕКОДИРОВАТЬ без ключа (это не шифрование!).
# Но ПОДДЕЛАТЬ подпись без secret_key — невозможно.
# → Не храните в JWT секретные данные (пароли, номера карт)!

import time
from datetime import datetime, timedelta, timezone

from jose import ExpiredSignatureError, JWTError, jwt

# ============================================================
# Константы — в реальном приложении берутся из переменных окружения
# ============================================================

# Секретный ключ: длинная случайная строка
# Генерация: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"  # HMAC + SHA-256 — стандарт для большинства случаев
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ============================================================
# Функции для работы с токенами
# ============================================================


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """Создать JWT access token.

    Args:
        data: данные для payload (обычно {"sub": username})
        expires_delta: время жизни токена (по умолчанию 30 минут)

    Returns:
        подписанный JWT-токен в виде строки
    """
    to_encode = data.copy()

    # Добавляем время истечения (exp — стандартный claim)
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire

    # jose.jwt.encode подписывает payload с SECRET_KEY
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Декодировать и верифицировать JWT token.

    Args:
        token: JWT-строка (из Authorization: Bearer <token>)

    Returns:
        payload словарь с данными токена

    Raises:
        JWTError: токен невалиден (неправильная подпись, плохой формат)
        ExpiredSignatureError: токен истёк (подкласс JWTError)
    """
    # jose автоматически проверяет:
    # 1. Подпись (SECRET_KEY + ALGORITHM)
    # 2. Время истечения (exp claim)
    return dict(jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]))


# ============================================================
# Демонстрации
# ============================================================


def demo_create_and_decode() -> None:
    """Создание и декодирование токена."""
    print("=" * 60)
    print("1. Создание и декодирование JWT")
    print("=" * 60)

    # Создаём токен для пользователя "alice"
    token = create_access_token(data={"sub": "alice"})

    print(f"\nТокен:\n{token}\n")
    print(f"Длина токена: {len(token)} символов")
    print(f"Части токена: {len(token.split('.'))} (header.payload.signature)")

    # Декодируем токен
    payload = decode_access_token(token)
    print(f"\nPayload:\n  sub = {payload['sub']}")
    exp_dt = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    print(f"  exp = {exp_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")


def demo_token_structure() -> None:
    """Показываем структуру JWT (без верификации)."""
    print("\n" + "=" * 60)
    print("2. Структура JWT (base64url декодирование)")
    print("=" * 60)

    import base64
    import json

    token = create_access_token(data={"sub": "alice", "role": "admin"})
    parts = token.split(".")

    for name, part in zip(["Header", "Payload", "Signature"], parts, strict=False):
        if name == "Signature":
            print(f"\n{name}: {part[:20]}... (бинарные данные подписи)")
        else:
            # Добавляем padding для base64url
            padded = part + "=" * (4 - len(part) % 4)
            decoded = json.loads(base64.urlsafe_b64decode(padded))
            print(f"\n{name}: {json.dumps(decoded, indent=2, ensure_ascii=False)}")

    print(
        """
  Важно: payload НЕ зашифрован — его можно прочитать без ключа!
  Секрет защищает только ПОДПИСЬ: никто не может изменить payload
  и сделать валидную подпись без SECRET_KEY.
"""
    )


def demo_expired_token() -> None:
    """Демонстрация истёкшего токена."""
    print("=" * 60)
    print("3. Истёкший токен")
    print("=" * 60)

    # Токен с истечением в прошлом
    expired_token = create_access_token(
        data={"sub": "alice"},
        expires_delta=timedelta(seconds=-1),  # уже истёк!
    )

    print("\nПытаемся декодировать истёкший токен...")
    try:
        decode_access_token(expired_token)
    except ExpiredSignatureError as e:
        print(f"✓ ExpiredSignatureError: {e}")
        print("  → Клиент должен запросить новый токен (refresh или повторный логин)")


def demo_tampered_token() -> None:
    """Демонстрация подделанного токена."""
    print("\n" + "=" * 60)
    print("4. Подделанный токен")
    print("=" * 60)

    import base64
    import json

    token = create_access_token(data={"sub": "alice"})
    parts = token.split(".")

    # Пробуем изменить payload (подменить "alice" на "admin")
    padded = parts[1] + "=" * (4 - len(parts[1]) % 4)
    original_payload = json.loads(base64.urlsafe_b64decode(padded))
    original_payload["sub"] = "admin"  # злоумышленник хочет стать admin

    # Кодируем изменённый payload
    fake_payload = (
        base64.urlsafe_b64encode(json.dumps(original_payload).encode())
        .rstrip(b"=")
        .decode()
    )
    tampered_token = f"{parts[0]}.{fake_payload}.{parts[2]}"

    print(f"\nОригинальный токен (конец): ...{token[-20:]}")
    print(f"Подделанный токен  (конец): ...{tampered_token[-20:]}")

    print("\nПытаемся декодировать подделанный токен...")
    try:
        decode_access_token(tampered_token)
    except JWTError as e:
        print(f"✓ JWTError: {e}")
        print("  → Подпись не совпадает — токен отклонён!")


def demo_wrong_secret() -> None:
    """Демонстрация токена с неправильным ключом."""
    print("\n" + "=" * 60)
    print("5. Токен от другого сервера (другой SECRET_KEY)")
    print("=" * 60)

    # Другой SECRET_KEY (как если бы токен пришёл с другого сервера)
    other_secret = "completely_different_secret_key_from_another_server"
    token_from_other_server = jwt.encode(
        {"sub": "hacker", "exp": time.time() + 3600},
        other_secret,
        algorithm=ALGORITHM,
    )

    print("\nПытаемся принять токен с чужим секретом...")
    try:
        decode_access_token(token_from_other_server)
    except JWTError as e:
        print(f"✓ JWTError: {e}")
        print("  → Наш SECRET_KEY не подходит — токен отклонён!")


def main() -> None:
    """Запускает все демонстрации."""
    demo_create_and_decode()
    demo_token_structure()
    demo_expired_token()
    demo_tampered_token()
    demo_wrong_secret()

    print("\n" + "=" * 60)
    print("Итог: python-jose + JWT")
    print("  create_access_token(data)  → подписанный JWT-токен")
    print("  decode_access_token(token) → payload dict или JWTError")
    print("  Всегда используйте SECRET_KEY из переменных окружения!")
    print("=" * 60)


if __name__ == "__main__":
    main()
