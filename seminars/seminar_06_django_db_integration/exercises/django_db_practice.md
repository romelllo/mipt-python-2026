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

# Загрузите базу данных кафе (для первого задания)
sqlite3 cafe.db < seminars/seminar_06_django_db_integration/data/cafe_menu.sql
```

> **Как работать с заданиями:** прочитайте условие, попробуйте решить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: Повторение SQL и sqlite3

> **Теория:** [README.md — Блок 1](../README.md#блок-1-sql-из-python-и-sql-инъекции-10-мин) | **Примеры:** [`examples/02_sqlite3_and_injections.py`](../examples/02_sqlite3_and_injections.py)

### Задание 1.1

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

---

## Часть 2: Django ORM — модели и CRUD

> **Теория:** [README.md — Блок 3](../README.md#блок-3-django-orm--модели-и-crud-25-мин) | **Примеры:** [`examples/03_django_orm_basics.py`](../examples/03_django_orm_basics.py)

### Задание 2.1

Создайте Django-проект для кафе. Выполните шаги:

1. Создайте проект `cafe_project` и приложение `cafe`
2. Добавьте `"cafe"` в `INSTALLED_APPS`
3. Определите модели `Category` и `MenuItem` (с полями `name`, `price`, `is_available`, `category` как ForeignKey)
4. Создайте и примените миграции

<details>
<summary>Подсказка</summary>

```bash
django-admin startproject cafe_project
cd cafe_project
python manage.py startapp cafe
```

Модели — в `cafe/models.py`. После определения запустите `makemigrations` и `migrate`. ForeignKey добавьте сразу — не нужно делать это в два шага.

</details>

<details>
<summary>Решение</summary>

```bash
# Создание проекта
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

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        return f"{self.name} — {self.price} ₽"
```

```bash
python manage.py makemigrations
python manage.py migrate
```

</details>

### Задание 2.2

Откройте Django shell и выполните CRUD-операции:

1. Создайте категорию «Напитки» и 3 пункта меню в ней
2. Получите все пункты меню дешевле 250 ₽ и выведите их
3. Обновите цену одного пункта (`item.price = ...; item.save()`)
4. Удалите один пункт и проверьте количество оставшихся

<details>
<summary>Подсказка</summary>

Откройте shell: `python manage.py shell`. Используйте `objects.create()`, `objects.filter(price__lt=250)`, `.save()`, `.delete()`, `.count()`.

</details>

<details>
<summary>Решение</summary>

```python
# python manage.py shell
from cafe.models import Category, MenuItem

# 1. Создание
drinks = Category.objects.create(name="Напитки")
cappuccino = MenuItem.objects.create(name="Капучино", category=drinks, price=250)
latte = MenuItem.objects.create(name="Латте", category=drinks, price=280)
espresso = MenuItem.objects.create(name="Эспрессо", category=drinks, price=180)

# 2. Чтение с фильтрацией
cheap = MenuItem.objects.filter(price__lt=250)
for item in cheap:
    print(item)
# Эспрессо — 180 ₽

# 3. Обновление
espresso.price = 200
espresso.save()
print(espresso)  # Эспрессо — 200 ₽

# 4. Удаление
latte.delete()
print(MenuItem.objects.count())  # 2
```

</details>

---

## Часть 3: ForeignKey и связи

> **Теория:** [README.md — Блок 4](../README.md#блок-4-foreignkey-и-связи-между-моделями-20-мин) | **Примеры:** [`examples/04_foreignkey_relations.py`](../examples/04_foreignkey_relations.py)

### Задание 3.1

В Django shell создайте связанные объекты и выполните запросы:

1. Создайте 2 категории: «Напитки» и «Выпечка»
2. Добавьте по 2 пункта меню в каждую категорию
3. Получите все пункты меню категории «Напитки» через **обратную связь** (`drinks.items.all()`)
4. Для пункта «Капучино» выведите название его категории через **прямой доступ** (`item.category.name`)

<details>
<summary>Подсказка</summary>

Для обратного доступа используйте `related_name` — в нашей модели это `"items"`, значит `category.items.all()`. Для прямого: `item.category.name`.

</details>

<details>
<summary>Решение</summary>

```python
from cafe.models import Category, MenuItem

# 1–2. Создание категорий и пунктов меню
drinks = Category.objects.create(name="Напитки")
pastry = Category.objects.create(name="Выпечка")

MenuItem.objects.create(name="Капучино", category=drinks, price=250)
MenuItem.objects.create(name="Эспрессо", category=drinks, price=180)
MenuItem.objects.create(name="Круассан", category=pastry, price=180)
MenuItem.objects.create(name="Чизкейк", category=pastry, price=350)

# 3. Обратный доступ: от категории к пунктам меню
print("Напитки:")
for item in drinks.items.all():
    print(f"  {item}")
# Напитки:
#   Капучино — 250 ₽
#   Эспрессо — 180 ₽

# 4. Прямой доступ: от пункта к категории
cappuccino = MenuItem.objects.get(name="Капучино")
print(f"Категория: {cappuccino.category.name}")  # Напитки
```

</details>

### Задание 3.2

Для каждой ситуации выберите подходящую стратегию `on_delete` и объясните почему:

1. Модель `Comment` связана с `Post` (комментарий к посту)
2. Модель `Employee` связана с `Department` (сотрудник в отделе)
3. Модель `OrderItem` связана с `MenuItem` (позиция заказа — ссылка на блюдо)

<details>
<summary>Подсказка</summary>

Ключевой вопрос: **имеет ли смысл дочерний объект без родительского?**
- Нет и он не нужен → `CASCADE`
- Нет, но удалять нельзя случайно → `PROTECT`
- Да, может существовать без связи → `SET_NULL`

</details>

<details>
<summary>Решение</summary>

1. **Comment → Post: `CASCADE`**
   Комментарий не имеет смысла без поста. Удалили пост → автоматически удалились все его комментарии.

2. **Employee → Department: `SET_NULL` (с `null=True`)**
   Сотрудник может временно не принадлежать отделу (отдел расформирован, но сотрудник переводится).
   ```python
   department = models.ForeignKey(
       Department, on_delete=models.SET_NULL, null=True
   )
   ```

3. **OrderItem → MenuItem: `PROTECT`**
   Нельзя удалить блюдо из меню, если оно фигурирует в заказах — история заказов должна сохраняться.
   ```python
   menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
   ```

</details>

---

## Часть 4: SQL vs Django ORM

> **Теория:** [README.md — Блок 5](../README.md#блок-5-sql-vs-django-orm-15-мин) | **Примеры:** [`examples/05_sql_vs_orm.py`](../examples/05_sql_vs_orm.py)

### Задание 4.1

Переведите следующие SQL-запросы в Django ORM:

```sql
-- 1
SELECT * FROM menu_items WHERE price > 300;

-- 2
SELECT * FROM menu_items
WHERE is_available = 1
ORDER BY price DESC
LIMIT 5;

-- 3
SELECT COUNT(*) FROM menu_items WHERE category_id = 1;

-- 4
DELETE FROM menu_items WHERE is_available = 0;
```

<details>
<summary>Подсказка</summary>

Соответствия: `> 300` → `price__gt=300`, `is_available = 1` → `is_available=True`, `ORDER BY price DESC` → `.order_by("-price")`, `LIMIT 5` → `[:5]`, `DELETE ... WHERE` → `.filter(...).delete()`.

</details>

<details>
<summary>Решение</summary>

```python
from cafe.models import MenuItem

# 1. SELECT * FROM menu_items WHERE price > 300
MenuItem.objects.filter(price__gt=300)

# 2. WHERE is_available = 1 ORDER BY price DESC LIMIT 5
MenuItem.objects.filter(is_available=True).order_by("-price")[:5]

# 3. SELECT COUNT(*) WHERE category_id = 1
MenuItem.objects.filter(category_id=1).count()

# 4. DELETE WHERE is_available = 0
MenuItem.objects.filter(is_available=False).delete()
```

</details>

---

## Бонусные задания

Эти задания объединяют несколько тем семинара. Попробуйте решить их самостоятельно!

### Задание Б.1: sqlite3 с JOIN

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

### Задание Б.2: ORM-запросы с агрегацией

Напишите Django ORM-запросы для следующих задач:

1. Переведите ORM в SQL: `MenuItem.objects.filter(name__contains="кофе")`
2. Найдите 3 самых дорогих доступных позиции в категории «Напитки»
3. Для каждой категории выведите количество доступных позиций (используйте `annotate` + `Count`)

<details>
<summary>Подсказка</summary>

Для п. 3 используйте `Category.objects.annotate(...)` с `Count("items")`. Чтобы считать только доступные, добавьте фильтр через `filter=models.Q(items__is_available=True)`.

</details>

<details>
<summary>Решение</summary>

```python
from django.db.models import Count, Q
from cafe.models import Category, MenuItem

# 1. ORM → SQL
# MenuItem.objects.filter(name__contains="кофе")
# → SELECT * FROM menu_items WHERE name LIKE '%кофе%'

# 2. Топ-3 дорогих доступных напитка
top_drinks = MenuItem.objects.filter(
    category__name="Напитки",
    is_available=True,
).order_by("-price")[:3]

for item in top_drinks:
    print(f"{item.name} — {item.price} ₽")

# 3. Количество доступных позиций по категориям
categories = Category.objects.annotate(
    available_count=Count(
        "items", filter=Q(items__is_available=True)
    )
)

for cat in categories:
    print(f"{cat.name}: {cat.available_count} доступных позиций")
```

</details>

### Задание Б.3: Полная модель заказа

Добавьте в проект модели `Order` и `OrderItem`:

- `Order`: `customer_name` (CharField), `created_at` (DateTimeField, auto_now_add=True), `status` (CharField, default="new")
- `OrderItem`: ForeignKey на `Order` (CASCADE) и `MenuItem` (PROTECT), `quantity` (PositiveIntegerField)

Затем в Django shell создайте заказ с 2 позициями и выведите его содержимое с итоговой суммой.

<details>
<summary>Подсказка</summary>

После добавления моделей не забудьте `makemigrations` + `migrate`. Для подсчёта суммы используйте: `sum(oi.menu_item.price * oi.quantity for oi in order.items.all())`.

</details>

<details>
<summary>Решение</summary>

```python
# cafe/models.py — добавьте эти два класса:
from django.db import models


class Order(models.Model):
    """Заказ клиента."""

    customer_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="new")

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        return f"{self.menu_item.name} x{self.quantity}"
```

```python
# В Django shell:
from cafe.models import Category, MenuItem, Order, OrderItem

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
print(order)
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
- [Django ForeignKey](https://docs.djangoproject.com/en/5.0/ref/models/fields/#foreignkey) — документация по ForeignKey и on_delete
- [sqlite3 — Python docs](https://docs.python.org/3/library/sqlite3.html) — документация модуля sqlite3
- [Django Girls Tutorial](https://tutorial.djangogirls.org/ru/) — отличный туториал на русском
