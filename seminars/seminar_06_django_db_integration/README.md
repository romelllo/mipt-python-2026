# Семинар 6: Взаимодействие с базами данных с помощью Django

**Модуль:** 3 — Создание Web-сервисов на Python  
**Дата:** 11.03.2026  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1AuwIRsYsjZsVHoJJx2QsjvOWl-QPFu6ysFhxAvnD-Lw/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:
- Выполнять SQL-запросы из Python через `sqlite3` и защищать код от SQL-инъекций
- Описывать модели Django и применять миграции для создания таблиц в БД
- Выполнять CRUD-операции через Django ORM в `manage.py shell`
- Настраивать связи `ForeignKey` и выбирать стратегию `on_delete`
- Переводить SQL-запросы в эквивалентные вызовы Django ORM

> **Важно:** На семинарах 1–2 вы уже освоили SQL. Сегодня научимся делать то же самое через Python — сначала напрямую через `sqlite3`, а потом безопасно и удобно через Django ORM.

---

## Подготовка

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate  # Linux/Mac

# Проверьте, что Django установлен
python -c "import django; print(django.get_version())"

# Загрузите тестовую базу данных кафе (для первого задания)
sqlite3 cafe.db < seminars/seminar_06_django_db_integration/data/cafe_menu.sql
```

---

## План семинара

Семинар построен по принципу **«теория → практика»**: после каждого блока теории вы переходите к соответствующим упражнениям в файле [`exercises/django_db_practice.md`](exercises/django_db_practice.md).

| Время | Тема | Практика |
|-------|------|----------|
| 10 мин | Блок 1: SQL из Python и SQL-инъекции | → Упражнения: Часть 1 |
| 5 мин | Блок 2: Типы баз данных и настройка Django | — |
| 25 мин | Блок 3: Django ORM — модели и CRUD | → Упражнения: Часть 2 |
| 20 мин | Блок 4: ForeignKey и связи между моделями | → Упражнения: Часть 3 |
| 15 мин | Блок 5: SQL vs Django ORM | → Упражнения: Часть 4 |
| 15 мин | Подведение итогов | — |

**Итого:** ~90 минут

---

## Блок 1: SQL из Python и SQL-инъекции (10 мин)

### Модуль sqlite3

Python имеет встроенный модуль `sqlite3` для работы с SQLite:

```python
import sqlite3

# Подключение к БД (файл создаётся автоматически)
conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()

# Параметризованный запрос — всегда используйте ?
cursor.execute("SELECT name, price FROM menu_items WHERE price < ?", (300,))
rows = cursor.fetchall()  # Список кортежей

for name, price in rows:
    print(f"{name} — {price} ₽")

conn.close()
```

### Опасность: SQL-инъекции

**Проблема:** подстановка пользовательского ввода напрямую в SQL-строку.

```python
# ❌ ОПАСНО! f-строка + пользовательский ввод = SQL-инъекция
user_input = "' OR '1'='1"
cursor.execute(f"SELECT * FROM menu_items WHERE name = '{user_input}'")
# Выполняется: WHERE name = '' OR '1'='1'  → возвращаются ВСЕ записи!
```

**Решение:** параметры через `?`.

```python
# ✅ БЕЗОПАСНО — sqlite3 сам экранирует параметр
cursor.execute("SELECT * FROM menu_items WHERE name = ?", (user_input,))
# Инъекция невозможна
```

**Правило:** никогда не используйте f-строки или конкатенацию для SQL-запросов. Только `?`.

> **Подробнее:** см. файл [`examples/02_sqlite3_and_injections.py`](examples/02_sqlite3_and_injections.py) — полная демонстрация sqlite3 и SQL-инъекций.

### Практика

Перейдите к файлу [`exercises/django_db_practice.md`](exercises/django_db_practice.md) и выполните **Часть 1: Повторение SQL и sqlite3** (задание 1.1).

---

## Блок 2: Типы баз данных и настройка Django (5 мин)

### Реляционные vs нереляционные

| Тип | Примеры | Когда |
|-----|---------|-------|
| **Реляционные (SQL)** | SQLite, PostgreSQL, MySQL | Структурированные данные, связи между таблицами |
| **Нереляционные (NoSQL)** | MongoDB, Redis, Neo4j | Гибкая схема, кэши, графы |

Django по умолчанию работает с **реляционными** базами данных. Выбор СУБД в `settings.py`:

```python
# SQLite — для разработки и обучения
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# PostgreSQL — для продакшна
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydb",
        "USER": "myuser",
        "PASSWORD": "mypassword",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

**Когда использовать:** SQLite — для разработки и обучения, PostgreSQL — для продакшна.

---

## Блок 3: Django ORM — модели и CRUD (25 мин)

### Что такое ORM?

**ORM** (Object-Relational Mapping) — прослойка между Python-кодом и базой данных. Вместо SQL вы работаете с Python-объектами.

```
Python-объект        ORM              SQL              База данных
MenuItem(...)  ──►  Django ORM  ──►  INSERT INTO ...  ──►  SQLite/PostgreSQL
```

### Определение модели

Модель — Python-класс, описывающий таблицу в БД:

```python
# cafe/models.py
from django.db import models


class Category(models.Model):
    """Категория блюд."""

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class MenuItem(models.Model):
    """Позиция в меню кафе."""

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} — {self.price} ₽"
```

### Миграции

После создания или изменения моделей нужно обновить БД:

```bash
# Шаг 1: создать файл миграции
python manage.py makemigrations

# Шаг 2: применить миграцию
python manage.py migrate
```

### CRUD-операции

```python
# Запустите: python manage.py shell
from cafe.models import Category, MenuItem

# CREATE
drinks = Category.objects.create(name="Напитки")
item = MenuItem.objects.create(name="Капучино", category=drinks, price=250)

# READ
all_items = MenuItem.objects.all()            # Все записи
cheap = MenuItem.objects.filter(price__lt=300)  # Фильтрация
one = MenuItem.objects.get(pk=1)              # Один объект (или исключение!)
count = MenuItem.objects.count()              # Количество

# UPDATE
item.price = 270
item.save()
# Или массово:
MenuItem.objects.filter(category=drinks).update(is_available=True)

# DELETE
item.delete()
MenuItem.objects.filter(is_available=False).delete()
```

> **Подробнее:** см. файл [`examples/03_django_orm_basics.py`](examples/03_django_orm_basics.py) — полные примеры моделей и CRUD, типы полей и lookup-выражения.

### Практика

Перейдите к файлу [`exercises/django_db_practice.md`](exercises/django_db_practice.md) и выполните **Часть 2: Django ORM — модели и CRUD** (задания 2.1–2.2).

---

## Блок 4: ForeignKey и связи между моделями (20 мин)

### ForeignKey — связь «многие к одному»

`ForeignKey` создаёт связь: каждый пункт меню принадлежит одной категории, но у категории может быть много пунктов.

```python
class MenuItem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,  # Стратегия при удалении родителя
        related_name="items",       # Имя для обратной связи
    )
```

### on_delete — стратегии при удалении

Что происходит с пунктами меню, когда удаляется их категория?

| Стратегия | Поведение | Пример |
|-----------|-----------|--------|
| `CASCADE` | Удалить связанные объекты | Удалили пост → удалились комментарии |
| `PROTECT` | Запретить удаление | Нельзя удалить категорию, пока в ней есть блюда |
| `SET_NULL` | Установить NULL (`null=True`) | Удалён отдел → сотрудник без отдела |
| `SET_DEFAULT` | Установить дефолт | Блюда переносятся в категорию «Разное» |
| `DO_NOTHING` | Ничего (опасно!) | Только если БД сама управляет каскадами |

### Работа со связанными объектами

```python
# Прямой доступ: от дочернего к родительскому
item = MenuItem.objects.get(pk=1)
print(item.category.name)  # "Напитки"

# Обратный доступ: от родительского к дочерним (через related_name)
drinks = Category.objects.get(name="Напитки")
drinks.items.all()              # Все пункты меню в категории
drinks.items.count()            # Количество
drinks.items.filter(price__lt=200)  # Фильтрация

# Фильтрация через связь (через двойное подчёркивание)
MenuItem.objects.filter(category__name="Напитки")
```

**Когда использовать:** `CASCADE` — когда дочерний объект не имеет смысла без родительского. `PROTECT` — когда удаление должно быть осознанным. `SET_NULL` — когда объект может существовать без связи.

> **Подробнее:** см. файл [`examples/04_foreignkey_relations.py`](examples/04_foreignkey_relations.py) — ForeignKey, on_delete и связанные запросы.

### Практика

Перейдите к файлу [`exercises/django_db_practice.md`](exercises/django_db_practice.md) и выполните **Часть 3: ForeignKey и связи** (задания 3.1–3.2).

---

## Блок 5: SQL vs Django ORM (15 мин)

### Таблица соответствий

| Операция | SQL | Django ORM |
|----------|-----|------------|
| Все записи | `SELECT * FROM menu_items` | `MenuItem.objects.all()` |
| Фильтрация (=) | `WHERE name = 'Капучино'` | `.filter(name="Капучино")` |
| Фильтрация (<) | `WHERE price < 300` | `.filter(price__lt=300)` |
| Фильтрация (>=) | `WHERE price >= 200` | `.filter(price__gte=200)` |
| LIKE | `WHERE name LIKE '%кофе%'` | `.filter(name__contains="кофе")` |
| IN | `WHERE id IN (1, 2, 3)` | `.filter(id__in=[1, 2, 3])` |
| NOT | `WHERE NOT is_available` | `.exclude(is_available=True)` |
| ORDER BY | `ORDER BY price DESC` | `.order_by("-price")` |
| LIMIT | `LIMIT 5` | `[:5]` |
| COUNT | `SELECT COUNT(*)` | `.count()` |
| INSERT | `INSERT INTO ... VALUES ...` | `.objects.create(...)` |
| UPDATE | `UPDATE ... SET ... WHERE ...` | `.filter(...).update(...)` |
| DELETE | `DELETE FROM ... WHERE ...` | `.filter(...).delete()` |

### Агрегация

```python
from django.db.models import Count, Avg, Sum, Min, Max

# SELECT AVG(price) FROM menu_items
MenuItem.objects.aggregate(avg_price=Avg("price"))
# → {'avg_price': 261.5}

# SELECT category_id, COUNT(*) FROM menu_items GROUP BY category_id
MenuItem.objects.values("category").annotate(count=Count("id"))
```

> **Подробнее:** см. файл [`examples/05_sql_vs_orm.py`](examples/05_sql_vs_orm.py) — полные таблицы соответствий SQL и Django ORM, включая JOIN и GROUP BY.

### Практика

Перейдите к файлу [`exercises/django_db_practice.md`](exercises/django_db_practice.md) и выполните **Часть 4: SQL vs Django ORM** (задание 4.1).

---

## Подведение итогов

### Шпаргалка

| Концепция | Ключевое |
|-----------|----------|
| `sqlite3` | Встроенный модуль Python для работы с SQLite |
| SQL-инъекция | Вредоносный SQL через пользовательский ввод |
| Параметризованный запрос | `cursor.execute("... WHERE id = ?", (id,))` |
| Django ORM | Работа с БД через Python-объекты |
| Модель | Python-класс = таблица в БД |
| Миграция | `makemigrations` → `migrate` |
| `ForeignKey` | Связь «многие к одному» |
| `on_delete` | `CASCADE` / `PROTECT` / `SET_NULL` |
| `filter(price__lt=300)` | `WHERE price < 300` |
| `order_by("-price")[:5]` | `ORDER BY price DESC LIMIT 5` |

### Ключевые выводы

1. **Никогда не используйте f-строки для SQL.** Всегда применяйте параметризованные запросы (`?` для sqlite3) или ORM.

2. **Django ORM = SQL, но безопаснее и читаемее.** Модель описывает таблицу, QuerySet — запрос, миграции — управляют схемой.

3. **`ForeignKey` + `on_delete` — ключевой инструмент связи.** Выбирайте `CASCADE` для зависимых данных, `PROTECT` для важных.

> **Главное правило:** навык работы с базами данных приходит только через практику. Пишите запросы, создавайте модели, экспериментируйте в `shell` — и ORM станет вашим привычным инструментом.

---

## Файлы семинара

```
seminar_06_django_db_integration/
├── README.md                              # Этот файл
├── data/
│   └── cafe_menu.sql                      # SQL-скрипт для создания БД кафе
├── examples/
│   ├── 01_sql_repetition.py               # Базовые SQL-операции через sqlite3
│   ├── 02_sqlite3_and_injections.py       # sqlite3 и SQL-инъекции
│   ├── 03_django_orm_basics.py            # Django ORM: модели, CRUD, lookups
│   ├── 04_foreignkey_relations.py         # ForeignKey, on_delete, связи
│   ├── 05_sql_vs_orm.py                   # Сравнение SQL и Django ORM
│   └── 06_django_tools.py                 # inspectdb, AutoField, dbshell
└── exercises/
    └── django_db_practice.md              # Практические задания
```

---

## Дополнительные материалы

- [Django Models](https://docs.djangoproject.com/en/5.0/topics/db/models/) — официальная документация по моделям
- [Django QuerySet API](https://docs.djangoproject.com/en/5.0/ref/models/querysets/) — полный справочник QuerySet
- [Django ForeignKey](https://docs.djangoproject.com/en/5.0/ref/models/fields/#foreignkey) — документация по ForeignKey
- [sqlite3 — Python docs](https://docs.python.org/3/library/sqlite3.html) — документация модуля sqlite3
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) — подробно о SQL-инъекциях
