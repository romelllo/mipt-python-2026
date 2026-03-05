"""
Семинар 6: Повторение SQL через Python sqlite3.

Этот модуль демонстрирует базовые SQL-операции (CREATE, INSERT,
SELECT, UPDATE, DELETE) через модуль sqlite3 в Python.

Примечание: используем временную БД в памяти (:memory:),
чтобы не создавать файлы на диске.
"""

import sqlite3

# ============================================================
# 1. Создание таблицы (CREATE TABLE)
# ============================================================


def demonstrate_create_table() -> None:
    """Демонстрация создания таблицы и вставки данных."""
    print("=" * 60)
    print("1. CREATE TABLE + INSERT — создание и наполнение")
    print("=" * 60)

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute("""
        CREATE TABLE menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            is_available INTEGER NOT NULL DEFAULT 1
        )
    """)

    # Вставка данных
    cursor.execute(
        "INSERT INTO menu_items (name, price) VALUES (?, ?)",
        ("Капучино", 250.0),
    )

    # Вставка нескольких записей
    items = [
        ("Латте", 280.0, 1),
        ("Эспрессо", 180.0, 1),
        ("Американо", 200.0, 1),
        ("Какао", 220.0, 0),
    ]
    cursor.executemany(
        "INSERT INTO menu_items (name, price, is_available) VALUES (?, ?, ?)",
        items,
    )
    conn.commit()

    # Проверяем
    cursor.execute("SELECT * FROM menu_items")
    rows = cursor.fetchall()
    print("\n  Все пункты меню:")
    for row in rows:
        status = "✓" if row[3] else "✗"
        print(f"    [{status}] {row[0]}. {row[1]} — {row[2]} ₽")

    conn.close()


# ============================================================
# 2. Чтение данных (SELECT)
# ============================================================


def demonstrate_select() -> None:
    """Демонстрация SELECT-запросов."""
    print("\n" + "=" * 60)
    print("2. SELECT — чтение данных")
    print("=" * 60)

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Подготовка данных
    cursor.execute("""
        CREATE TABLE menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            is_available INTEGER NOT NULL DEFAULT 1
        )
    """)
    items = [
        ("Капучино", 250.0, 1),
        ("Латте", 280.0, 1),
        ("Эспрессо", 180.0, 1),
        ("Американо", 200.0, 1),
        ("Какао", 220.0, 0),
        ("Чизкейк", 350.0, 1),
    ]
    cursor.executemany(
        "INSERT INTO menu_items (name, price, is_available) VALUES (?, ?, ?)",
        items,
    )
    conn.commit()

    # SELECT * — все записи
    print("\n  Все записи:")
    cursor.execute("SELECT * FROM menu_items")
    for row in cursor.fetchall():
        print(f"    {row}")

    # SELECT с WHERE
    print("\n  Напитки дешевле 250 ₽:")
    cursor.execute("SELECT name, price FROM menu_items WHERE price < 250")
    for row in cursor.fetchall():
        print(f"    {row[0]} — {row[1]} ₽")

    # SELECT с ORDER BY и LIMIT
    print("\n  Топ-3 самых дорогих:")
    cursor.execute("SELECT name, price FROM menu_items ORDER BY price DESC LIMIT 3")
    for row in cursor.fetchall():
        print(f"    {row[0]} — {row[1]} ₽")

    # COUNT
    cursor.execute("SELECT COUNT(*) FROM menu_items WHERE is_available = 1")
    count = cursor.fetchone()[0]
    print(f"\n  Доступных позиций: {count}")

    conn.close()


# ============================================================
# 3. Обновление данных (UPDATE)
# ============================================================


def demonstrate_update() -> None:
    """Демонстрация UPDATE-запросов."""
    print("\n" + "=" * 60)
    print("3. UPDATE — обновление данных")
    print("=" * 60)

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    cursor.execute(
        "INSERT INTO menu_items (name, price) VALUES (?, ?)",
        ("Капучино", 250.0),
    )
    conn.commit()

    # До обновления
    cursor.execute("SELECT * FROM menu_items WHERE name = 'Капучино'")
    print(f"\n  До обновления: {cursor.fetchone()}")

    # Обновляем цену
    cursor.execute(
        "UPDATE menu_items SET price = ? WHERE name = ?",
        (270.0, "Капучино"),
    )
    conn.commit()

    # После обновления
    cursor.execute("SELECT * FROM menu_items WHERE name = 'Капучино'")
    print(f"  После обновления: {cursor.fetchone()}")

    conn.close()


# ============================================================
# 4. Удаление данных (DELETE)
# ============================================================


def demonstrate_delete() -> None:
    """Демонстрация DELETE-запросов."""
    print("\n" + "=" * 60)
    print("4. DELETE — удаление данных")
    print("=" * 60)

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    items = [("Капучино", 250.0), ("Латте", 280.0), ("Эспрессо", 180.0)]
    cursor.executemany("INSERT INTO menu_items (name, price) VALUES (?, ?)", items)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM menu_items")
    print(f"\n  До удаления: {cursor.fetchone()[0]} записей")

    # Удаляем одну запись
    cursor.execute("DELETE FROM menu_items WHERE name = ?", ("Латте",))
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM menu_items")
    print(f"  После удаления Латте: {cursor.fetchone()[0]} записей")

    # Выводим оставшиеся
    cursor.execute("SELECT name, price FROM menu_items")
    print("  Оставшиеся позиции:")
    for row in cursor.fetchall():
        print(f"    {row[0]} — {row[1]} ₽")

    conn.close()


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 6: ПОВТОРЕНИЕ SQL ЧЕРЕЗ PYTHON sqlite3")
    print("=" * 60)

    demonstrate_create_table()
    demonstrate_select()
    demonstrate_update()
    demonstrate_delete()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
