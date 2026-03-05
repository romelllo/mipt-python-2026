"""
Семинар 6: SQL vs Django ORM — сравнение запросов.

Этот модуль демонстрирует эквивалентные запросы на SQL и Django ORM.
Для каждой SQL-операции показан соответствующий вызов Django ORM.

Примечание: этот файл выводит таблицу соответствий.
SQL-запросы также выполняются на реальной sqlite3 БД в памяти.
"""

import sqlite3

# ============================================================
# 1. Таблица соответствий: чтение данных
# ============================================================

SELECT_COMPARISON = """
=== SELECT — чтение данных ===

┌─────────────────────────────────────────┬──────────────────────────────────────────────┐
│ SQL                                     │ Django ORM                                   │
├─────────────────────────────────────────┼──────────────────────────────────────────────┤
│ SELECT * FROM menu_items                │ MenuItem.objects.all()                        │
│ SELECT * FROM menu_items WHERE id = 1   │ MenuItem.objects.get(pk=1)                    │
│ SELECT * ... WHERE name = 'Капучино'    │ .filter(name="Капучино")                     │
│ SELECT * ... WHERE price < 300          │ .filter(price__lt=300)                        │
│ SELECT * ... WHERE price >= 200         │ .filter(price__gte=200)                       │
│ SELECT * ... WHERE price BETWEEN 200    │ .filter(price__range=(200, 300))              │
│   AND 300                               │                                              │
│ SELECT * ... WHERE name LIKE '%кофе%'   │ .filter(name__contains="кофе")                │
│ SELECT * ... WHERE name LIKE 'Кап%'     │ .filter(name__startswith="Кап")               │
│ SELECT * ... WHERE id IN (1, 2, 3)      │ .filter(id__in=[1, 2, 3])                    │
│ SELECT * ... WHERE category_id IS NULL  │ .filter(category__isnull=True)                │
│ SELECT * ... WHERE NOT is_available     │ .exclude(is_available=True)                   │
│ SELECT * ... ORDER BY price             │ .order_by("price")                            │
│ SELECT * ... ORDER BY price DESC        │ .order_by("-price")                           │
│ SELECT * ... LIMIT 5                    │ [:5]                                          │
│ SELECT * ... LIMIT 5 OFFSET 10         │ [10:15]                                       │
│ SELECT COUNT(*) FROM menu_items         │ MenuItem.objects.count()                      │
│ SELECT DISTINCT category_id ...         │ .values("category").distinct()                │
└─────────────────────────────────────────┴──────────────────────────────────────────────┘
"""

# ============================================================
# 2. Таблица соответствий: запись данных
# ============================================================

WRITE_COMPARISON = """
=== INSERT, UPDATE, DELETE ===

┌─────────────────────────────────────────┬──────────────────────────────────────────────┐
│ SQL                                     │ Django ORM                                   │
├─────────────────────────────────────────┼──────────────────────────────────────────────┤
│ INSERT INTO menu_items (name, price)    │ MenuItem.objects.create(                     │
│   VALUES ('Латте', 280)                 │     name="Латте", price=280                  │
│                                         │ )                                            │
├─────────────────────────────────────────┼──────────────────────────────────────────────┤
│ UPDATE menu_items                       │ MenuItem.objects.filter(                     │
│   SET price = 300                       │     name="Латте"                             │
│   WHERE name = 'Латте'                  │ ).update(price=300)                          │
├─────────────────────────────────────────┼──────────────────────────────────────────────┤
│ DELETE FROM menu_items                  │ MenuItem.objects.filter(                     │
│   WHERE is_available = 0               │     is_available=False                        │
│                                         │ ).delete()                                   │
└─────────────────────────────────────────┴──────────────────────────────────────────────┘
"""

# ============================================================
# 3. Таблица соответствий: агрегация и группировка
# ============================================================

AGGREGATION_COMPARISON = """
=== Агрегация и GROUP BY ===

┌─────────────────────────────────────────┬──────────────────────────────────────────────┐
│ SQL                                     │ Django ORM                                   │
├─────────────────────────────────────────┼──────────────────────────────────────────────┤
│ SELECT COUNT(*) FROM menu_items         │ MenuItem.objects.count()                      │
│                                         │                                              │
│ SELECT AVG(price) FROM menu_items       │ from django.db.models import Avg             │
│                                         │ MenuItem.objects.aggregate(                   │
│                                         │     avg=Avg("price")                         │
│                                         │ )                                            │
│                                         │ # {'avg': 261.5}                             │
│                                         │                                              │
│ SELECT MIN(price), MAX(price)           │ from django.db.models import Min, Max        │
│   FROM menu_items                       │ MenuItem.objects.aggregate(                   │
│                                         │     min=Min("price"),                        │
│                                         │     max=Max("price"),                        │
│                                         │ )                                            │
│                                         │                                              │
│ SELECT category_id, COUNT(*)            │ from django.db.models import Count           │
│   FROM menu_items                       │ MenuItem.objects.values(                     │
│   GROUP BY category_id                  │     "category"                               │
│                                         │ ).annotate(count=Count("id"))                │
│                                         │                                              │
│ SELECT category_id, COUNT(*)            │ MenuItem.objects.values(                     │
│   FROM menu_items                       │     "category"                               │
│   GROUP BY category_id                  │ ).annotate(                                  │
│   HAVING COUNT(*) > 3                   │     count=Count("id")                        │
│                                         │ ).filter(count__gt=3)                        │
└─────────────────────────────────────────┴──────────────────────────────────────────────┘
"""

# ============================================================
# 4. Таблица соответствий: JOIN
# ============================================================

JOIN_COMPARISON = """
=== JOIN — объединение таблиц ===

┌─────────────────────────────────────────┬──────────────────────────────────────────────┐
│ SQL                                     │ Django ORM                                   │
├─────────────────────────────────────────┼──────────────────────────────────────────────┤
│ SELECT m.name, c.name                   │ # Django делает JOIN автоматически           │
│ FROM menu_items m                       │ # при обращении через ForeignKey:            │
│ INNER JOIN categories c                 │                                              │
│   ON m.category_id = c.id              │ items = MenuItem.objects.select_related(      │
│                                         │     "category"                               │
│                                         │ )                                            │
│                                         │ for item in items:                           │
│                                         │     print(item.name, item.category.name)     │
│                                         │                                              │
│ SELECT c.name, COUNT(m.id)              │ Category.objects.annotate(                   │
│ FROM categories c                       │     item_count=Count("items")                │
│ LEFT JOIN menu_items m                  │ )                                            │
│   ON c.id = m.category_id              │                                              │
│ GROUP BY c.id                           │                                              │
└─────────────────────────────────────────┴──────────────────────────────────────────────┘
"""


# ============================================================
# 5. Живая демонстрация SQL-запросов
# ============================================================


def demonstrate_sql_queries() -> None:
    """Выполнение SQL-запросов на реальной БД для сравнения."""
    print("\n" + "=" * 60)
    print("5. Живая демонстрация SQL-запросов")
    print("=" * 60)

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Создаём таблицы
    cursor.execute("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER,
            price REAL NOT NULL,
            is_available INTEGER DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)

    # Наполняем данными
    categories = [("Напитки",), ("Выпечка",), ("Завтраки",)]
    cursor.executemany("INSERT INTO categories (name) VALUES (?)", categories)

    items = [
        ("Капучино", 1, 250.0, 1),
        ("Латте", 1, 280.0, 1),
        ("Эспрессо", 1, 180.0, 1),
        ("Американо", 1, 200.0, 1),
        ("Круассан", 2, 180.0, 1),
        ("Чизкейк", 2, 350.0, 1),
        ("Овсянка", 3, 280.0, 1),
        ("Какао", 1, 220.0, 0),
    ]
    cursor.executemany(
        "INSERT INTO menu_items (name, category_id, price, is_available) "
        "VALUES (?, ?, ?, ?)",
        items,
    )
    conn.commit()

    # --- Демонстрация запросов ---

    # WHERE + ORDER BY
    print("\n  SQL: SELECT name, price FROM menu_items")
    print("       WHERE price < 250 ORDER BY price")
    print("  ORM: MenuItem.objects.filter(price__lt=250).order_by('price')")
    cursor.execute(
        "SELECT name, price FROM menu_items WHERE price < 250 ORDER BY price"
    )
    for row in cursor.fetchall():
        print(f"    {row[0]} — {row[1]} ₽")

    # COUNT
    print("\n  SQL: SELECT COUNT(*) FROM menu_items WHERE is_available = 1")
    print("  ORM: MenuItem.objects.filter(is_available=True).count()")
    cursor.execute("SELECT COUNT(*) FROM menu_items WHERE is_available = 1")
    print(f"    Результат: {cursor.fetchone()[0]}")

    # JOIN + GROUP BY
    print("\n  SQL: SELECT c.name, COUNT(m.id) FROM categories c")
    print("       LEFT JOIN menu_items m ON c.id = m.category_id")
    print("       GROUP BY c.id")
    print(
        "  ORM: Category.objects.annotate(count=Count('items')).values('name', 'count')"
    )
    cursor.execute("""
        SELECT c.name, COUNT(m.id) AS item_count
        FROM categories c
        LEFT JOIN menu_items m ON c.id = m.category_id
        GROUP BY c.id
    """)
    for row in cursor.fetchall():
        print(f"    {row[0]}: {row[1]} позиций")

    # AVG
    print("\n  SQL: SELECT AVG(price) FROM menu_items")
    print("  ORM: MenuItem.objects.aggregate(avg=Avg('price'))")
    cursor.execute("SELECT ROUND(AVG(price), 2) FROM menu_items")
    print(f"    Средняя цена: {cursor.fetchone()[0]} ₽")

    conn.close()


# ============================================================
# Функции демонстрации
# ============================================================


def demonstrate_select_comparison() -> None:
    """Демонстрация соответствий SELECT."""
    print("=" * 60)
    print("1. SELECT — чтение данных")
    print("=" * 60)
    print(SELECT_COMPARISON)


def demonstrate_write_comparison() -> None:
    """Демонстрация соответствий INSERT/UPDATE/DELETE."""
    print("\n" + "=" * 60)
    print("2. INSERT, UPDATE, DELETE")
    print("=" * 60)
    print(WRITE_COMPARISON)


def demonstrate_aggregation_comparison() -> None:
    """Демонстрация соответствий агрегации."""
    print("\n" + "=" * 60)
    print("3. Агрегация и GROUP BY")
    print("=" * 60)
    print(AGGREGATION_COMPARISON)


def demonstrate_join_comparison() -> None:
    """Демонстрация соответствий JOIN."""
    print("\n" + "=" * 60)
    print("4. JOIN — объединение таблиц")
    print("=" * 60)
    print(JOIN_COMPARISON)


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 6: SQL vs DJANGO ORM — СРАВНЕНИЕ")
    print("=" * 60)

    demonstrate_select_comparison()
    demonstrate_write_comparison()
    demonstrate_aggregation_comparison()
    demonstrate_join_comparison()
    demonstrate_sql_queries()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
