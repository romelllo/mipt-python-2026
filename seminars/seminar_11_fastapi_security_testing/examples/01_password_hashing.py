"""Демонстрация хеширования паролей с passlib и bcrypt.

Запуск:
    python seminars/seminar_11_fastapi_security_testing/examples/01_password_hashing.py

Зависимости:
    uv add passlib[bcrypt]
"""

# ============================================================
# Почему нельзя хранить пароли в открытом виде
# ============================================================

# НИКОГДА не делайте так в production!
# users_db = {"alice": "secret123"}  # ← катастрофа при утечке БД

# Правильный подход: хранить только хеш пароля.
# Хеш — это односторонняя функция: из хеша нельзя получить пароль.
# При входе пользователь вводит пароль → мы хешируем его → сравниваем с хешем в БД.

# ============================================================
# passlib: библиотека хеширования паролей
# ============================================================

from passlib.context import CryptContext

# CryptContext задаёт алгоритм и параметры.
# bcrypt — современный стандарт для паролей: медленный специально,
# чтобы брутфорс был практически невозможен.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Захешировать пароль.

    Args:
        plain_password: пароль в открытом виде (например, от пользователя)

    Returns:
        bcrypt-хеш — строка вида $2b$12$...
        Каждый вызов возвращает РАЗНЫЙ хеш (из-за случайной соли),
        но verify() всегда работает корректно.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить пароль против хеша.

    Args:
        plain_password: пароль, введённый пользователем
        hashed_password: хеш из базы данных

    Returns:
        True если пароль верный, False иначе
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================
# Демонстрация: хеширование и проверка
# ============================================================


def demo_basic_hashing() -> None:
    """Показываем, как работает хеширование паролей."""
    print("=" * 60)
    print("1. Базовое хеширование паролей")
    print("=" * 60)

    password = "super_secret_42"

    # Хешируем пароль
    hashed = hash_password(password)
    print(f"\nОригинальный пароль : {password}")
    print(f"Хеш (bcrypt)        : {hashed}")
    print(f"Длина хеша          : {len(hashed)} символов")

    # Каждый вызов даёт РАЗНЫЙ хеш (разная соль)
    hashed2 = hash_password(password)
    print(f"\nВторой хеш того же пароля: {hashed2}")
    print(f"Хеши одинаковые?          : {hashed == hashed2}")  # False!
    print("(Это нормально — случайная соль защищает от Rainbow Table атак)")


def demo_verification() -> None:
    """Показываем проверку пароля."""
    print("\n" + "=" * 60)
    print("2. Проверка пароля")
    print("=" * 60)

    password = "my_password_123"
    hashed = hash_password(password)

    # Правильный пароль
    result_correct = verify_password(password, hashed)
    print(f"\nПроверка правильного пароля : {result_correct}")  # True

    # Неправильный пароль
    result_wrong = verify_password("wrong_password", hashed)
    print(f"Проверка неправильного      : {result_wrong}")  # False

    # Пустой пароль
    result_empty = verify_password("", hashed)
    print(f"Проверка пустого пароля     : {result_empty}")  # False


def demo_no_plaintext_storage() -> None:
    """Имитируем регистрацию и вход пользователя."""
    print("\n" + "=" * 60)
    print("3. Эмуляция регистрации и входа")
    print("=" * 60)

    # "База данных" — хранит только хеши, никогда не plain text
    fake_db: dict[str, str] = {}

    def register_user(username: str, plain_password: str) -> None:
        """Регистрация: сохраняем хеш, не пароль."""
        hashed = hash_password(plain_password)
        fake_db[username] = hashed
        print(f"\n  Пользователь '{username}' зарегистрирован")
        print(f"  В БД хранится: {hashed[:30]}...")
        # Оригинальный пароль НИГДЕ не сохраняется!

    def login_user(username: str, plain_password: str) -> bool:
        """Вход: проверяем пароль против хеша из БД."""
        hashed = fake_db.get(username)
        if hashed is None:
            print(f"\n  Пользователь '{username}' не найден")
            return False
        is_valid = verify_password(plain_password, hashed)
        print(
            f"\n  Вход '{username}': {'✓ успешно' if is_valid else '✗ неверный пароль'}"
        )
        return is_valid

    register_user("alice", "alice_secret")
    register_user("bob", "bob_secret_456")

    login_user("alice", "alice_secret")  # True
    login_user("alice", "wrong_password")  # False
    login_user("charlie", "any_password")  # не найден


def demo_timing_attack_protection() -> None:
    """Passlib защищает от timing attacks."""
    print("\n" + "=" * 60)
    print("4. Защита от timing attacks")
    print("=" * 60)
    print(
        """
  Timing attack: злоумышленник измеряет время ответа, чтобы угадать
  правильный пароль (если 'неверный пароль' возвращается быстрее).

  passlib.verify() ВСЕГДА выполняется примерно одинаковое время,
  независимо от того, правильный пароль или нет.
  Это реализовано через hmac.compare_digest() внутри библиотеки.

  ✓ bcrypt медленный (специально!) — ~100мс на современном CPU.
    Это делает брутфорс практически невозможным:
    10^6 попыток × 100мс = 28 часов на одно ядро CPU.
    Атакующий не может перебрать миллиарды паролей за секунды.
"""
    )


def main() -> None:
    """Запускает все демонстрации."""
    demo_basic_hashing()
    demo_verification()
    demo_no_plaintext_storage()
    demo_timing_attack_protection()

    print("\n" + "=" * 60)
    print("Итог: passlib + bcrypt — стандарт хеширования паролей")
    print("  hash_password(plain)       → bcrypt хеш")
    print("  verify_password(plain, hash) → True / False")
    print("=" * 60)


if __name__ == "__main__":
    main()
