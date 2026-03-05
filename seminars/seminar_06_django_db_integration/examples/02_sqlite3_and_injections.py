"""
Семинар 6: Модуль sqlite3 и SQL-инъекции.

Этот модуль демонстрирует:
- Работу с sqlite3: connect, cursor, execute, fetchone/fetchall
- Опасность SQL-инъекций при использовании f-строк
- Безопасные параметризованные запросы
- Контекстный менеджер для соединений

Примечание: используем временную БД в памяти (:memory:).
"""

import sqlite3

# ============================================================
# 1. Основы работы с sqlite3
# ============================================================


def demonstrate_sqlite3_basics() -> None:
    """Демонстрация базовой работы с sqlite3."""
    print("=" * 60)
    print("1. Основы sqlite3: connect, cursor, execute, fetch")
    print("=" * 60)

    # Подключение к БД (в памяти для демонстрации)
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Создание таблицы и вставка данных
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
    """)

    users = [
        ("alice", "alice@example.com", 1),
        ("bob", "bob@example.com", 0),
        ("charlie", "charlie@example.com", 0),
    ]
    cursor.executemany(
        "INSERT INTO users (username, email, is_admin) VALUES (?, ?, ?)",
        users,
    )
    conn.commit()

    # fetchall() — все результаты (список кортежей)
    print("\n  fetchall() — все пользователи:")
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    for user in all_users:
        print(f"    {user}")

    # fetchone() — одна запись (кортеж или None)
    print("\n  fetchone() — первый пользователь:")
    cursor.execute("SELECT * FROM users WHERE id = 1")
    one_user = cursor.fetchone()
    print(f"    {one_user}")

    # fetchmany(n) — n записей
    print("\n  fetchmany(2) — два пользователя:")
    cursor.execute("SELECT * FROM users")
    two_users = cursor.fetchmany(2)
    for user in two_users:
        print(f"    {user}")

    # row_factory для получения словарей
    print("\n  row_factory=sqlite3.Row — доступ по имени столбца:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = 1")
    row = cursor.fetchone()
    print(f"    username={row['username']}, email={row['email']}")

    conn.close()


# ============================================================
# 2. SQL-инъекция — демонстрация уязвимости
# ============================================================


def demonstrate_sql_injection() -> None:
    """Демонстрация уязвимости SQL-инъекции."""
    print("\n" + "=" * 60)
    print("2. SQL-инъекция — уязвимый код")
    print("=" * 60)

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "secret123"),
    )
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("user1", "password1"),
    )
    conn.commit()

    # --- Уязвимый код (НИКОГДА так не делайте!) ---
    print("\n  ❌ Уязвимый код (f-строка):")
    print("  Пользователь вводит: ' OR '1'='1")

    malicious_input = "' OR '1'='1"
    # Формируется запрос:
    # SELECT * FROM users WHERE username = '' OR '1'='1'
    # Условие '1'='1' всегда истинно → возвращаются ВСЕ записи!
    unsafe_query = f"SELECT * FROM users WHERE username = '{malicious_input}'"
    print(f"  Сформированный SQL: {unsafe_query}")

    cursor.execute(unsafe_query)
    results = cursor.fetchall()
    print(f"  Результат: {len(results)} записей (утечка данных!)")
    for row in results:
        print(f"    {row}")

    # --- Ещё более опасный пример ---
    print("\n  ❌ Ещё опаснее — удаление таблицы:")
    print("  Пользователь вводит: '; DROP TABLE users; --")

    drop_input = "'; DROP TABLE users; --"
    drop_query = f"SELECT * FROM users WHERE username = '{drop_input}'"
    print(f"  Сформированный SQL: {drop_query}")
    print("  (К счастью, sqlite3 не выполняет несколько запросов")
    print("   через execute(), но другие СУБД могут!)")

    conn.close()


# ============================================================
# 3. Параметризованные запросы — безопасный подход
# ============================================================


def demonstrate_safe_queries() -> None:
    """Демонстрация безопасных параметризованных запросов."""
    print("\n" + "=" * 60)
    print("3. Параметризованные запросы — безопасный подход")
    print("=" * 60)

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "secret123"),
    )
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("user1", "password1"),
    )
    conn.commit()

    # --- Безопасный код ---
    print("\n  ✅ Безопасный код (параметризованный запрос):")

    malicious_input = "' OR '1'='1"
    print(f"  Пользователь вводит: {malicious_input}")

    # sqlite3 экранирует параметр — инъекция невозможна
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (malicious_input,),
    )
    results = cursor.fetchall()
    print(f"  Результат: {len(results)} записей (данные защищены!)")

    # Нормальный запрос
    print("\n  ✅ Нормальный безопасный запрос:")
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        ("admin",),
    )
    result = cursor.fetchone()
    print(f"  Найден: {result}")

    # Именованные параметры
    print("\n  ✅ Именованные параметры (:name):")
    cursor.execute(
        "SELECT * FROM users WHERE username = :user AND password = :pwd",
        {"user": "admin", "pwd": "secret123"},
    )
    result = cursor.fetchone()
    print(f"  Найден: {result}")

    conn.close()


# ============================================================
# 4. Контекстный менеджер (with)
# ============================================================


def demonstrate_context_manager() -> None:
    """Демонстрация использования контекстного менеджера."""
    print("\n" + "=" * 60)
    print("4. Контекстный менеджер — автоматический commit/rollback")
    print("=" * 60)

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    # with conn — автоматический commit при успехе, rollback при ошибке
    print("\n  Использование 'with conn':")
    with conn:
        conn.execute(
            "INSERT INTO items (name, price) VALUES (?, ?)",
            ("Капучино", 250.0),
        )
        conn.execute(
            "INSERT INTO items (name, price) VALUES (?, ?)",
            ("Латте", 280.0),
        )
    # Если код внутри with выполнился без ошибок — автоматический commit
    # Если произошла ошибка — автоматический rollback

    cursor.execute("SELECT * FROM items")
    print(f"  Записей после commit: {len(cursor.fetchall())}")

    print("\n  Попытка вставки с ошибкой:")
    try:
        with conn:
            conn.execute(
                "INSERT INTO items (name, price) VALUES (?, ?)",
                ("Эспрессо", 180.0),
            )
            # Ошибка: столбец 'bad_column' не существует
            conn.execute(
                "INSERT INTO items (bad_column) VALUES (?)",
                ("Ошибка",),
            )
    except sqlite3.OperationalError as e:
        print(f"  Ошибка: {e}")
        print("  Транзакция откачена (rollback)!")

    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    print(f"  Записей после rollback: {len(rows)} (Эспрессо не добавлен)")

    conn.close()


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 6: SQLITE3 И SQL-ИНЪЕКЦИИ")
    print("=" * 60)

    demonstrate_sqlite3_basics()
    demonstrate_sql_injection()
    demonstrate_safe_queries()
    demonstrate_context_manager()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)
    print("\n  Запомните: НИКОГДА не используйте f-строки для SQL!")
    print("  Всегда используйте параметризованные запросы (?, :name).")


if __name__ == "__main__":
    main()
