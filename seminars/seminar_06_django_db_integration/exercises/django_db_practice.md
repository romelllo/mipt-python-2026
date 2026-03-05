# Практические задания: Взаимодействие с базами данных с помощью Django

## Подготовка

```bash
# Активируйте виртуальное окружение
source .venv/bin/activate  # Linux/Mac

# Убедитесь, что Django установлен
python -c "import django; print(django.get_version())"

# Запустите примеры для ознакомления
python seminars/seminar_06_django_db_integration/examples/01_sql_repetition.py
python seminars/seminar_06_django_db_integration/examples/02_sqlite3_and_injections.py
python seminars/seminar_06_django_db_integration/examples/03_django_orm_basics.py
python seminars/seminar_06_django_db_integration/examples/04_foreignkey_relations.py
python seminars/seminar_06_django_db_integration/examples/05_sql_vs_orm.py
python seminars/seminar_06_django_db_integration/examples/06_django_tools.py

# Загрузите базу данных кафе (для заданий с sqlite3)
sqlite3 cafe.db < seminars/seminar_06_django_db_integration/data/cafe_menu.sql
```

> **Как работать с заданиями:** прочитайте условие, попробуйте решить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: Повторение SQL

> **Теория:** [README.md — Блок 1](../README.md#блок-1-повторение-sql-5-мин) | **Примеры:** [`examples/01_sql_repetition.py`](../examples/01_sql_repetition.py)

### Задание 1.1

Напишите SQL-запрос, который выбирает все доступные пункты меню (`is_available = 1`) из таблицы `menu_items`, отсортированные по цене от дешёвых к дорогим.

<details>
<summary>Подсказка</summary>

Используйте `SELECT ... WHERE is_available = 1 ORDER BY price`.

</details>

<details>
<summary>Решение</summary>

```sql
SELECT name, price
FROM menu_items
WHERE is_available = 1
ORDER BY price;
```

</details>

### Задание 1.2

Напишите SQL-запрос, который подсчитывает количество пунктов меню в каждой категории. Выведите название категории и количество.

<details>
<summary>Подсказка</summary>

Используйте `JOIN` между `menu_items` и `categories`, затем `GROUP BY` по категории и `COUNT(*)`.

</details>

<details>
<summary>Решение</summary>

```sql
SELECT c.name AS category, COUNT(m.id) AS item_count
FROM categories c
LEFT JOIN menu_items m ON c.id = m.category_id
GROUP BY c.id
ORDER BY item_count DESC;
```

</details>

---

## Часть 2: Python sqlite3 и SQL-инъекции

> **Теория:** [README.md — Блок 3](../README.md#блок-3-python-sqlite3-и-sql-инъекции-15-мин) | **Примеры:** [`examples/02_sqlite3_and_injections.py`](../examples/02_sqlite3_and_injections.py)

### Задание 2.1

Напишите Python-скрипт, который подключается к БД `cafe.db` и выводит все пункты меню дешевле 250 рублей. Используйте модуль `sqlite3`.

<details>
<summary>Подсказка</summary>

Используйте `sqlite3.connect("cafe.db")`, затем `cursor.execute()` с параметризованным запросом и `cursor.fetchall()`.

</details>

<details>
<summary>Решение</summary>

```python
import sqlite3

conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()

cursor.execute(
    "SELECT name, price FROM menu_items WHERE price < ?",
    (250.0,),
)

for name, price in cursor.fetchall():
    print(f"{name} — {price} ₽")

conn.close()
```

</details>

### Задание 2.2

В коде ниже есть уязвимость SQL-инъекции. Найдите её и исправьте:

```python
import sqlite3

conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()

search_name = input("Введите название блюда: ")
cursor.execute(
    f"SELECT * FROM menu_items WHERE name = '{search_name}'"
)
results = cursor.fetchall()
print(results)

conn.close()
```

<details>
<summary>Подсказка</summary>

Проблема в f-строке: пользователь может ввести `' OR '1'='1` и получить все записи. Замените f-строку на параметризованный запрос с `?`.

</details>

<details>
<summary>Решение</summary>

```python
import sqlite3

conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()

search_name = input("Введите название блюда: ")

# ✅ Безопасный параметризованный запрос
cursor.execute(
    "SELECT * FROM menu_items WHERE name = ?",
    (search_name,),
)
results = cursor.fetchall()
print(results)

conn.close()
```

</details>

### Задание 2.3

Напишите Python-функцию `get_items_by_category(category_name: str)`, которая принимает название категории и возвращает список пунктов меню в этой категории. Используйте `sqlite3` с параметризованными запросами и `JOIN`.

<details>
<summary>Подсказка</summary>

Используйте `JOIN` между `menu_items` и `categories`, а название категории передавайте через `?`. Верните результат `cursor.fetchall()`.

</details>

<details>
<summary>Решение</summary>

```python
import sqlite3


def get_items_by_category(category_name: str) -> list[tuple]:
    """Получить пункты меню по названию категории."""
    conn = sqlite3.connect("cafe.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT m.name, m.price, m.is_available
        FROM menu_items m
        JOIN categories c ON m.category_id = c.id
        WHERE c.name = ?
        ORDER BY m.price
        """,
        (category_name,),
    )

    results = cursor.fetchall()
    conn.close()
    return results


# Использование:
items = get_items_by_category("Напитки")
for name, price, available in items:
    status = "✓" if available else "✗"
    print(f"  [{status}] {name} — {price} ₽")
```

</details>

---

## Часть 3: Django ORM

> **Теория:** [README.md — Блок 4](../README.md#блок-4-django-orm--модели-и-crud-20-мин) | **Примеры:** [`examples/03_django_orm_basics.py`](../examples/03_django_orm_basics.py)

### Задание 3.1

Создайте Django-проект для кафе. Выполните шаги:

1. Создайте проект `cafe_project`
2. Создайте приложение `cafe`
3. Добавьте `cafe` в `INSTALLED_APPS`
4. Определите модель `Category` с полем `name` (CharField, max_length=100)
5. Создайте и примените миграции

<details>
<summary>Подсказка</summary>

```bash
django-admin startproject cafe_project
cd cafe_project
python manage.py startapp cafe
```
Не забудьте добавить `"cafe"` в `INSTALLED_APPS` в `settings.py`.

</details>

<details>
<summary>Решение</summary>

```bash
# Создание проекта и приложения
cd /tmp
django-admin startproject cafe_project
cd cafe_project
python manage.py startapp cafe
```

```python
# cafe_project/settings.py — добавьте "cafe" в INSTALLED_APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cafe",  # Наше приложение
]
```

```python
# cafe/models.py
from django.db import models


class Category(models.Model):
    """Категория блюд в кафе."""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

```bash
# Создать и применить миграции
python manage.py makemigrations
python manage.py migrate
```

</details>

### Задание 3.2

Добавьте модель `MenuItem` с полями:
- `name` — название (CharField, max_length=200)
- `price` — цена (DecimalField, max_digits=8, decimal_places=2)
- `is_available` — доступность (BooleanField, default=True)

Создайте миграции и примените их.

<details>
<summary>Подсказка</summary>

Определите класс `MenuItem(models.Model)` в `cafe/models.py`. Пока без ForeignKey — связь с категорией добавим позже.

</details>

<details>
<summary>Решение</summary>

```python
# cafe/models.py
from django.db import models


class Category(models.Model):
    """Категория блюд."""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Позиция в меню кафе."""

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} — {self.price} ₽"
```

```bash
python manage.py makemigrations
python manage.py migrate
```

</details>

### Задание 3.3

Откройте Django shell и выполните CRUD-операции:

1. Создайте 3 категории: «Напитки», «Выпечка», «Завтраки»
2. Создайте 2 пункта меню
3. Получите все пункты меню и выведите их
4. Обновите цену одного пункта
5. Удалите один пункт

<details>
<summary>Подсказка</summary>

Откройте shell командой `python manage.py shell`. Используйте `Category.objects.create()`, `MenuItem.objects.create()`, `.all()`, `.save()`, `.delete()`.

</details>

<details>
<summary>Решение</summary>

```python
# python manage.py shell

from cafe.models import Category, MenuItem

# 1. Создание категорий
drinks = Category.objects.create(name="Напитки")
pastry = Category.objects.create(name="Выпечка")
breakfast = Category.objects.create(name="Завтраки")

# 2. Создание пунктов меню
cappuccino = MenuItem.objects.create(
    name="Капучино", price=250.00
)
croissant = MenuItem.objects.create(
    name="Круассан", price=180.00
)

# 3. Чтение
for item in MenuItem.objects.all():
    print(item)
# Капучино — 250.00 ₽
# Круассан — 180.00 ₽

# 4. Обновление
cappuccino.price = 270.00
cappuccino.save()
print(cappuccino)  # Капучино — 270.00 ₽

# 5. Удаление
croissant.delete()
print(MenuItem.objects.count())  # 1
```

</details>

### Задание 3.4

Используя Django shell, выполните следующие запросы:

1. Найдите все пункты меню дешевле 300 рублей
2. Найдите пункт меню по имени «Капучино»
3. Посчитайте общее количество пунктов меню
4. Отсортируйте пункты меню по цене (по убыванию)
5. Получите первые 3 самых дорогих пункта

<details>
<summary>Подсказка</summary>

Используйте `.filter(price__lt=300)`, `.get(name="Капучино")`, `.count()`, `.order_by("-price")`, `[:3]`.

</details>

<details>
<summary>Решение</summary>

```python
from cafe.models import MenuItem

# 1. Дешевле 300 ₽
cheap = MenuItem.objects.filter(price__lt=300)
for item in cheap:
    print(item)

# 2. По имени
cappuccino = MenuItem.objects.get(name="Капучино")
print(cappuccino)

# 3. Количество
total = MenuItem.objects.count()
print(f"Всего: {total}")

# 4. Сортировка по убыванию цены
by_price = MenuItem.objects.order_by("-price")
for item in by_price:
    print(f"  {item.name}: {item.price} ₽")

# 5. Топ-3 самых дорогих
top_3 = MenuItem.objects.order_by("-price")[:3]
for item in top_3:
    print(f"  {item.name}: {item.price} ₽")
```

</details>

---

## Часть 4: ForeignKey и связи

> **Теория:** [README.md — Блок 5](../README.md#блок-5-foreignkey-и-связи-между-моделями-15-мин) | **Примеры:** [`examples/04_foreignkey_relations.py`](../examples/04_foreignkey_relations.py)

### Задание 4.1

Добавьте поле `category` (ForeignKey) к модели `MenuItem`, связывающее её с моделью `Category`. Используйте `on_delete=models.CASCADE` и `related_name="items"`. Создайте и примените миграцию.

<details>
<summary>Подсказка</summary>

Добавьте `category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")`. При создании миграции Django спросит, какое значение по умолчанию использовать для существующих записей — можно указать ID существующей категории (например, 1).

</details>

<details>
<summary>Решение</summary>

```python
# cafe/models.py
from django.db import models


class Category(models.Model):
    """Категория блюд."""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Позиция в меню кафе."""

    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} — {self.price} ₽"
```

```bash
python manage.py makemigrations
# Django спросит про значение по умолчанию — введите 1 (ID первой категории)
python manage.py migrate
```

</details>

### Задание 4.2

В Django shell создайте связанные объекты и выполните запросы:

1. Создайте категорию «Напитки» и 3 пункта меню в ней
2. Получите все пункты меню в категории «Напитки» через обратную связь
3. Для пункта меню выведите название его категории (прямой доступ)

<details>
<summary>Подсказка</summary>

Для обратного доступа используйте `category.items.all()` (через `related_name`). Для прямого — `item.category.name`.

</details>

<details>
<summary>Решение</summary>

```python
from cafe.models import Category, MenuItem

# 1. Создание
drinks = Category.objects.create(name="Напитки")
MenuItem.objects.create(name="Капучино", category=drinks, price=250)
MenuItem.objects.create(name="Латте", category=drinks, price=280)
MenuItem.objects.create(name="Эспрессо", category=drinks, price=180)

# 2. Обратный доступ: от категории к пунктам меню
for item in drinks.items.all():
    print(item)
# Капучино — 250 ₽
# Латте — 280 ₽
# Эспрессо — 180 ₽

print(f"Всего в категории: {drinks.items.count()}")  # 3

# 3. Прямой доступ: от пункта к категории
cappuccino = MenuItem.objects.get(name="Капучино")
print(f"Категория: {cappuccino.category.name}")  # Напитки
```

</details>

### Задание 4.3

Для каждой ситуации выберите подходящую стратегию `on_delete` и объясните почему:

1. Модель `Comment` связана с моделью `Post` (комментарий к посту)
2. Модель `Employee` связана с моделью `Department` (сотрудник в отделе)
3. Модель `Product` связана с моделью `Category` (товар в категории)
4. Модель `OrderItem` связана с моделью `MenuItem` (позиция заказа)

<details>
<summary>Подсказка</summary>

Подумайте: имеет ли смысл дочерний объект без родительского? Если нет — `CASCADE`. Если да, но нужна защита — `PROTECT`. Если объект может существовать без связи — `SET_NULL`.

</details>

<details>
<summary>Решение</summary>

1. **Comment → Post: `CASCADE`**
   Комментарий не имеет смысла без поста. Удалили пост → удалились все комментарии.

2. **Employee → Department: `SET_NULL` (с `null=True`)**
   Сотрудник может временно не принадлежать отделу (отдел расформирован).
   ```python
   department = models.ForeignKey(
       Department, on_delete=models.SET_NULL, null=True
   )
   ```

3. **Product → Category: `PROTECT`**
   Нельзя случайно удалить категорию с товарами. Сначала нужно перенести товары.
   ```python
   category = models.ForeignKey(Category, on_delete=models.PROTECT)
   ```

4. **OrderItem → MenuItem: `PROTECT`**
   Нельзя удалить блюдо из меню, если оно есть в заказах (история заказов важна).
   ```python
   menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
   ```

</details>

---

## Часть 5: SQL vs Django ORM

> **Теория:** [README.md — Блок 6](../README.md#блок-6-sql-vs-django-orm-10-мин) | **Примеры:** [`examples/05_sql_vs_orm.py`](../examples/05_sql_vs_orm.py)

### Задание 5.1

Переведите следующие SQL-запросы в Django ORM:

```sql
-- 1
SELECT * FROM menu_items WHERE price > 300;

-- 2
SELECT * FROM menu_items WHERE is_available = 1 ORDER BY price DESC LIMIT 5;

-- 3
SELECT COUNT(*) FROM menu_items WHERE category_id = 1;

-- 4
DELETE FROM menu_items WHERE is_available = 0;
```

<details>
<summary>Подсказка</summary>

Используйте соответствия: `> 300` → `price__gt=300`, `= 1` → `True`, `ORDER BY ... DESC` → `.order_by("-...")`, `LIMIT 5` → `[:5]`, `COUNT(*)` → `.count()`.

</details>

<details>
<summary>Решение</summary>

```python
from cafe.models import MenuItem

# 1. SELECT * FROM menu_items WHERE price > 300
MenuItem.objects.filter(price__gt=300)

# 2. SELECT * ... WHERE is_available = 1 ORDER BY price DESC LIMIT 5
MenuItem.objects.filter(is_available=True).order_by("-price")[:5]

# 3. SELECT COUNT(*) FROM menu_items WHERE category_id = 1
MenuItem.objects.filter(category_id=1).count()

# 4. DELETE FROM menu_items WHERE is_available = 0
MenuItem.objects.filter(is_available=False).delete()
```

</details>

### Задание 5.2

Переведите следующие вызовы Django ORM в SQL:

```python
# 1
MenuItem.objects.filter(name__contains="кофе")

# 2
MenuItem.objects.filter(price__range=(200, 400)).order_by("price")

# 3
MenuItem.objects.exclude(category__name="Напитки").count()

# 4
MenuItem.objects.filter(category__name="Выпечка").update(is_available=False)
```

<details>
<summary>Подсказка</summary>

`name__contains` → `LIKE '%...%'`, `price__range` → `BETWEEN`, `exclude` → `NOT ... = ...` или `!= ...`, `update` → `UPDATE ... SET`.

</details>

<details>
<summary>Решение</summary>

```sql
-- 1. .filter(name__contains="кофе")
SELECT * FROM menu_items WHERE name LIKE '%кофе%';

-- 2. .filter(price__range=(200, 400)).order_by("price")
SELECT * FROM menu_items
WHERE price BETWEEN 200 AND 400
ORDER BY price;

-- 3. .exclude(category__name="Напитки").count()
SELECT COUNT(*)
FROM menu_items m
JOIN categories c ON m.category_id = c.id
WHERE c.name != 'Напитки';

-- 4. .filter(category__name="Выпечка").update(is_available=False)
UPDATE menu_items
SET is_available = 0
WHERE category_id IN (
    SELECT id FROM categories WHERE name = 'Выпечка'
);
```

</details>

### Задание 5.3

Напишите Django ORM запрос, который для каждой категории выводит количество доступных пунктов меню и среднюю цену.

<details>
<summary>Подсказка</summary>

Используйте `Category.objects.annotate(...)` с `Count` и `Avg`. Фильтруйте доступные пункты через `items__is_available=True`.

</details>

<details>
<summary>Решение</summary>

```python
from django.db.models import Avg, Count

categories = Category.objects.annotate(
    item_count=Count("items", filter=models.Q(items__is_available=True)),
    avg_price=Avg("items__price", filter=models.Q(items__is_available=True)),
)

for cat in categories:
    print(f"{cat.name}: {cat.item_count} позиций, "
          f"средняя цена: {cat.avg_price:.2f} ₽")
```

Эквивалентный SQL:

```sql
SELECT c.name,
       COUNT(CASE WHEN m.is_available = 1 THEN m.id END) AS item_count,
       AVG(CASE WHEN m.is_available = 1 THEN m.price END) AS avg_price
FROM categories c
LEFT JOIN menu_items m ON c.id = m.category_id
GROUP BY c.id;
```

</details>

### Задание 5.4

Напишите SQL-запрос и его Django ORM эквивалент: найти 3 самые дорогие доступные позиции в категории «Напитки».

<details>
<summary>Подсказка</summary>

SQL: `JOIN` + `WHERE` + `ORDER BY price DESC` + `LIMIT 3`.
ORM: `.filter(category__name=..., is_available=True).order_by("-price")[:3]`.

</details>

<details>
<summary>Решение</summary>

SQL:

```sql
SELECT m.name, m.price
FROM menu_items m
JOIN categories c ON m.category_id = c.id
WHERE c.name = 'Напитки' AND m.is_available = 1
ORDER BY m.price DESC
LIMIT 3;
```

Django ORM:

```python
top_drinks = MenuItem.objects.filter(
    category__name="Напитки",
    is_available=True,
).order_by("-price")[:3]

for item in top_drinks:
    print(f"{item.name} — {item.price} ₽")
```

</details>

---

## Часть 6: Утилиты Django

> **Теория:** [README.md — Блок 7](../README.md#блок-7-утилиты-django--inspectdb-autofield-dbshell-5-мин) | **Примеры:** [`examples/06_django_tools.py`](../examples/06_django_tools.py)

### Задание 6.1

В вашем Django-проекте выполните команду `inspectdb` для одной из существующих таблиц (например, `auth_user`). Изучите сгенерированную модель и ответьте:

1. Какой тип поля Django использовал для `username`?
2. Что означает `managed = False` в `class Meta`?
3. Что означает `db_table`?

<details>
<summary>Подсказка</summary>

Выполните `python manage.py inspectdb auth_user`. Посмотрите на сгенерированный код — `managed = False` означает, что Django не будет создавать/изменять эту таблицу через миграции.

</details>

<details>
<summary>Решение</summary>

```bash
python manage.py inspectdb auth_user
```

Ответы:
1. `username` — `models.CharField(unique=True, max_length=150)` (строка с ограничением длины и уникальностью)
2. `managed = False` — Django **не будет управлять** этой таблицей через миграции. Таблица уже существует в БД, и Django не должна её изменять.
3. `db_table = "auth_user"` — явное указание имени таблицы в БД (вместо авто-имени `приложение_модель`).

</details>

### Задание 6.2

Объясните, в чём разница между `AutoField`, `BigAutoField` и `SmallAutoField`. В каких случаях стоит менять тип по умолчанию?

<details>
<summary>Решение</summary>

| Тип | Размер | Максимум | Когда использовать |
|-----|--------|----------|-------------------|
| `SmallAutoField` | 16 бит | 32 767 | Справочники с малым количеством записей |
| `AutoField` | 32 бит | 2 147 483 647 | Большинство таблиц (старый стандарт) |
| `BigAutoField` | 64 бит | 9.2 × 10¹⁸ | Таблицы с очень большим количеством записей (стандарт с Django 3.2+) |

По умолчанию Django 3.2+ использует `BigAutoField`. Менять стоит только если:
- Нужна совместимость со старым проектом (`AutoField`)
- Нужно экономить место в таблице-справочнике (`SmallAutoField`)
- Нужен UUID вместо числового ID (`UUIDField`)

</details>

### Задание 6.3

Откройте `dbshell` в вашем Django-проекте и выполните:

1. Выведите список всех таблиц
2. Посмотрите структуру таблицы `cafe_menuitem`
3. Выполните SQL-запрос `SELECT COUNT(*) FROM cafe_menuitem`

<details>
<summary>Подсказка</summary>

Используйте `python manage.py dbshell`. Внутри sqlite3: `.tables` для списка, `.schema cafe_menuitem` для структуры.

</details>

<details>
<summary>Решение</summary>

```bash
# Открываем dbshell
python manage.py dbshell
```

```sql
-- 1. Список таблиц
.tables
-- auth_group          cafe_category       django_content_type
-- auth_group_perms    cafe_menuitem       django_migrations
-- ...

-- 2. Структура таблицы
.schema cafe_menuitem
-- CREATE TABLE "cafe_menuitem" (
--     "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
--     "name" varchar(200) NOT NULL,
--     "price" decimal NOT NULL,
--     "is_available" bool NOT NULL,
--     "category_id" bigint NOT NULL REFERENCES "cafe_category" ("id")
-- );

-- 3. Количество записей
SELECT COUNT(*) FROM cafe_menuitem;

-- 4. Выход
.quit
```

</details>

---

## Бонусные задания

Эти задания объединяют несколько тем семинара. Попробуйте решить их самостоятельно!

### Задание Б.1: Миграция с sqlite3 на Django ORM

Напишите Python-скрипт, который:
1. Читает данные из `cafe.db` (через `sqlite3`)
2. Выводит их в формате, готовом для вставки через Django ORM

Это имитация процесса миграции с «чистого SQL» на ORM.

<details>
<summary>Подсказка</summary>

Прочитайте данные через `sqlite3`, затем для каждой строки сформируйте строку вида `Category.objects.create(name="...")`.

</details>

<details>
<summary>Решение</summary>

```python
import sqlite3


def generate_orm_commands(db_path: str) -> None:
    """Генерация Django ORM команд из sqlite3 БД."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Категории
    print("# Создание категорий")
    cursor.execute("SELECT id, name, description FROM categories")
    for row in cursor.fetchall():
        print(
            f'cat_{row[0]} = Category.objects.create('
            f'name="{row[1]}", description="{row[2] or ""}")'
        )

    # Пункты меню
    print("\n# Создание пунктов меню")
    cursor.execute(
        "SELECT name, category_id, price, is_available "
        "FROM menu_items"
    )
    for row in cursor.fetchall():
        available = "True" if row[3] else "False"
        print(
            f'MenuItem.objects.create('
            f'name="{row[0]}", category=cat_{row[1]}, '
            f'price={row[2]}, is_available={available})'
        )

    conn.close()


generate_orm_commands("cafe.db")
```

</details>

### Задание Б.2: Полная модель кафе

Создайте полную систему моделей для кафе с Django ORM:

1. `Category` — категории блюд
2. `MenuItem` — пункты меню (ForeignKey на Category)
3. `Order` — заказы (customer_name, created_at, status)
4. `OrderItem` — позиции заказа (ForeignKey на Order и MenuItem, quantity)

Затем в Django shell:
- Создайте категорию, 2 пункта меню, заказ с 2 позициями
- Выведите все позиции заказа с названиями блюд и суммой

<details>
<summary>Подсказка</summary>

`OrderItem` имеет два `ForeignKey`: на `Order` (CASCADE) и на `MenuItem` (PROTECT). Для суммы используйте Python: `sum(oi.menu_item.price * oi.quantity for oi in order.items.all())`.

</details>

<details>
<summary>Решение</summary>

```python
# cafe/models.py
from django.db import models


class Category(models.Model):
    """Категория блюд."""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Позиция в меню."""

    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} — {self.price} ₽"


class Order(models.Model):
    """Заказ клиента."""

    customer_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="new")

    def __str__(self):
        return f"Заказ #{self.pk} — {self.customer_name}"


class OrderItem(models.Model):
    """Позиция в заказе."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"
```

```python
# В Django shell:
from cafe.models import Category, MenuItem, Order, OrderItem

# Создание
drinks = Category.objects.create(name="Напитки")
cappuccino = MenuItem.objects.create(
    name="Капучино", category=drinks, price=250
)
latte = MenuItem.objects.create(
    name="Латте", category=drinks, price=280
)

order = Order.objects.create(customer_name="Алиса")
OrderItem.objects.create(order=order, menu_item=cappuccino, quantity=2)
OrderItem.objects.create(order=order, menu_item=latte, quantity=1)

# Вывод заказа
print(f"Заказ: {order}")
total = 0
for oi in order.items.select_related("menu_item").all():
    subtotal = oi.menu_item.price * oi.quantity
    total += subtotal
    print(f"  {oi.menu_item.name} x{oi.quantity} = {subtotal} ₽")
print(f"Итого: {total} ₽")
# Капучино x2 = 500 ₽
# Латте x1 = 280 ₽
# Итого: 780 ₽
```

</details>

---

## Полезные ресурсы

- [Django Models](https://docs.djangoproject.com/en/5.0/topics/db/models/) — официальная документация по моделям
- [Django QuerySet API](https://docs.djangoproject.com/en/5.0/ref/models/querysets/) — полный справочник QuerySet
- [Django ForeignKey](https://docs.djangoproject.com/en/5.0/ref/models/fields/#foreignkey) — документация по ForeignKey
- [sqlite3 — Python docs](https://docs.python.org/3/library/sqlite3.html) — документация модуля sqlite3
- [Django Girls Tutorial](https://tutorial.djangogirls.org/ru/) — отличный туториал на русском
