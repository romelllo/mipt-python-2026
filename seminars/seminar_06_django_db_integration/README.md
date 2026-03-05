# Семинар 6: Взаимодействие с базами данных с помощью Django

**Модуль:** 3 — Создание Web-сервисов на Python  
**Дата:** 11.03.2026  
**Презентация:** [ссылка на презентацию]

---

## Цели семинара

После этого семинара вы сможете:
- Работать с SQLite из Python через модуль `sqlite3` и понимать опасность SQL-инъекций
- Описывать модели Django и применять миграции для создания таблиц в БД
- Выполнять CRUD-операции (создание, чтение, обновление, удаление) через Django ORM
- Настраивать связи между моделями с помощью `ForeignKey` и выбирать стратегию `on_delete`
- Переводить SQL-запросы в эквивалентные вызовы Django ORM и наоборот
- Использовать утилиты `inspectdb`, `dbshell` и понимать роль `AutoField`

> **Важно:** На семинарах 1–2 вы уже освоили SQL. Сегодня мы научимся делать то же самое, но через Python — сначала напрямую через `sqlite3`, а затем безопасно и удобно через Django ORM.

---

## Подготовка

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# Установите зависимости (если ещё не установлены)
uv sync

# Проверьте, что Django установлен
python -c "import django; print(django.get_version())"

# Загрузите тестовую базу данных кафе
sqlite3 cafe.db < data/cafe_menu.sql
```

---

## План семинара

Семинар построен по принципу **«теория → практика»**: после каждого блока теории вы переходите к соответствующим упражнениям в файле [`exercises/django_db_practice.md`](exercises/django_db_practice.md).

| Время | Тема | Практика |
|-------|------|----------|
| 5 мин | Блок 1: Повторение SQL | → Упражнения: Часть 1 |
| 10 мин | Блок 2: Типы баз данных | — |
| 15 мин | Блок 3: Python sqlite3 и SQL-инъекции | → Упражнения: Часть 2 |
| 20 мин | Блок 4: Django ORM — модели и CRUD | → Упражнения: Часть 3 |
| 15 мин | Блок 5: ForeignKey и связи между моделями | → Упражнения: Часть 4 |
| 10 мин | Блок 6: SQL vs Django ORM | → Упражнения: Часть 5 |
| 5 мин | Блок 7: Утилиты Django — inspectdb, AutoField, dbshell | → Упражнения: Часть 6 |
| 10 мин | Подведение итогов | — |

**Итого:** ~90 минут

---

## Блок 1: Повторение SQL (5 мин)

На семинарах 1–2 вы уже изучили основные SQL-операции. Давайте кратко вспомним:

```sql
-- CREATE: создание таблицы
CREATE TABLE menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

-- INSERT: добавление данных
INSERT INTO menu_items (name, price) VALUES ('Капучино', 250.0);

-- SELECT: чтение данных
SELECT * FROM menu_items WHERE price < 300;

-- UPDATE: обновление данных
UPDATE menu_items SET price = 270.0 WHERE name = 'Капучино';

-- DELETE: удаление данных
DELETE FROM menu_items WHERE id = 1;
```

Эти операции — основа любой работы с базой данных. Сегодня мы научимся выполнять их из Python.

> **Подробнее:** см. файл [`examples/01_sql_repetition.py`](examples/01_sql_repetition.py) — все базовые SQL-операции через Python sqlite3.

### Практика

Перейдите к файлу [`exercises/django_db_practice.md`](exercises/django_db_practice.md) и выполните **Часть 1: Повторение SQL** (задания 1.1–1.2).

---

## Блок 2: Типы баз данных (10 мин)

### Реляционные базы данных (SQL)

Данные хранятся в **таблицах** со строгой схемой. Таблицы связаны через внешние ключи.

| СУБД | Особенности | Когда использовать |
|------|-------------|-------------------|
| **SQLite** | Файловая, без сервера, встроена в Python | Прототипы, мобильные приложения, тесты |
| **PostgreSQL** | Мощная, расширяемая, ACID-совместимая | Продакшн веб-приложений |
| **MySQL** | Популярная, быстрая для чтения | Веб-сайты, CMS (WordPress) |

### Нереляционные базы данных (NoSQL)

Данные хранятся **не в таблицах** — а в документах, ключ-значение парах, графах и т.д.

| СУБД | Тип хранения | Когда использовать |
|------|-------------|-------------------|
| **MongoDB** | Документы (JSON-подобные) | Гибкая схема, прототипирование |
| **Redis** | Ключ-значение (в памяти) | Кэширование, сессии, очереди |
| **Neo4j** | Графы (узлы + связи) | Социальные сети, рекомендации |

### Что использует Django?

Django по умолчанию работает с **реляционными** базами данных. В `settings.py`:

```python
# SQLite (по умолчанию — для разработки)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# PostgreSQL (для продакшна)
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

## Блок 3: Python sqlite3 и SQL-инъекции (15 мин)

### Модуль sqlite3

Python имеет встроенный модуль `sqlite3` для работы с SQLite:

```python
import sqlite3

# Подключение к БД (файл создаётся автоматически)
conn = sqlite3.connect("cafe.db")
cursor = conn.cursor()

# Выполнение запроса
cursor.execute("SELECT * FROM menu_items WHERE price < 300")
rows = cursor.fetchall()  # Список кортежей

for row in rows:
    print(row)  # (1, 'Капучино', 1, 250.0, True)

conn.close()
```

### Опасность: SQL-инъекции

**Проблема:** подстановка пользовательского ввода напрямую в SQL-запрос.

```python
# ❌ ОПАСНО! Уязвимость SQL-инъекции!
user_input = "'; DROP TABLE menu_items; --"
cursor.execute(f"SELECT * FROM menu_items WHERE name = '{user_input}'")
# Выполнится: SELECT * FROM menu_items WHERE name = '';
#             DROP TABLE menu_items; --'
# Таблица будет УДАЛЕНА!
```

**Решение:** параметризованные запросы.

```python
# ✅ БЕЗОПАСНО! Параметризованный запрос
user_input = "Капучино"
cursor.execute(
    "SELECT * FROM menu_items WHERE name = ?",
    (user_input,)
)
# sqlite3 сам экранирует параметры — инъекция невозможна
```

**Когда использовать:** `sqlite3` подходит для скриптов и простых задач. Для веб-приложений лучше использовать ORM (Django ORM, SQLAlchemy) — он автоматически защищает от инъекций.

> **Подробнее:** см. файл [`examples/02_sqlite3_and_injections.py`](examples/02_sqlite3_and_injections.py) — полная демонстрация sqlite3 и SQL-инъекций.

### Практика

Перейдите к файлу [`exercises/django_db_practice.md`](exercises/django_db_practice.md) и выполните **Часть 2: Python sqlite3 и SQL-инъекции** (задания 2.1–2.3).

---

## Блок 4: Django ORM — модели и CRUD (20 мин)

### Что такое ORM?

**ORM** (Object-Relational Mapping) — это прослойка между Python-кодом и базой данных. Вместо SQL-запросов вы работаете с Python-объектами.

```
Python-код          ORM             SQL              База данных
Post.objects.all() ──► Django ORM ──► SELECT * ... ──► SQLite/PostgreSQL
```

### Определение модели

Модель — это Python-класс, описывающий таблицу в БД:

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} — {self.price} ₽"
```

### Миграции

После создания или изменения моделей нужно обновить БД:

```bash
# 1. Создать файл миграции (инструкцию по изменению БД)
python manage.py makemigrations

# 2. Применить миграцию (выполнить изменения в БД)
python manage.py migrate
```

### CRUD-операции в Django ORM

```python
# Запустите Django shell: python manage.py shell
from cafe.models import Category, MenuItem

# CREATE — создание
drinks = Category.objects.create(name="Напитки")
item = MenuItem.objects.create(
    name="Капучино", category=drinks, price=250.00
)

# READ — чтение
all_items = MenuItem.objects.all()           # Все записи
cheap = MenuItem.objects.filter(price__lt=300)  # Фильтрация
one = MenuItem.objects.get(pk=1)             # Один объект по PK
count = MenuItem.objects.count()             # Количество

# UPDATE — обновление
item.price = 270.00
item.save()
# Или массовое обновление:
MenuItem.objects.filter(category=drinks).update(is_available=True)

# DELETE — удаление
item.delete()
MenuItem.objects.filter(is_available=False).delete()
```

> **Подробнее:** см. файл [`examples/03_django_orm_basics.py`](examples/03_django_orm_basics.py) — полные примеры моделей и CRUD-операций.

### Практика

Перейдите к файлу [`exercises/django_db_practice.md`](exercises/django_db_practice.md) и выполните **Часть 3: Django ORM** (задания 3.1–3.4).

---

## Блок 5: ForeignKey и связи между моделями (15 мин)

### ForeignKey — связь «многие к одному»

`ForeignKey` создаёт связь между моделями. Например, каждый пункт меню принадлежит одной категории, но в категории может быть много пунктов.

```python
class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,  # Что делать при удалении категории?
        related_name="items",       # Имя для обратной связи
    )
```

### on_delete — стратегии при удалении

Что происходит с пунктами меню, когда удаляется их категория?

| Стратегия | Поведение | Пример |
|-----------|-----------|--------|
| `CASCADE` | Удалить связанные объекты | Удалили категорию → удалились все её блюда |
| `PROTECT` | Запретить удаление | Нельзя удалить категорию, пока в ней есть блюда |
| `SET_NULL` | Установить NULL (нужно `null=True`) | Категория удалена → у блюд `category = NULL` |
| `SET_DEFAULT` | Установить значение по умолчанию | Категория удалена → блюда переносятся в «Разное» |
| `DO_NOTHING` | Ничего не делать (опасно!) | Ответственность на программисте |

```python
# CASCADE: при удалении автора удаляются все его посты
author = models.ForeignKey(Author, on_delete=models.CASCADE)

# PROTECT: нельзя удалить категорию с товарами
category = models.ForeignKey(Category, on_delete=models.PROTECT)

# SET_NULL: при удалении отдела сотрудник остаётся без отдела
department = models.ForeignKey(
    Department, on_delete=models.SET_NULL, null=True
)
```

### Работа со связанными объектами

```python
# Прямой доступ: от дочернего к родительскому
item = MenuItem.objects.get(pk=1)
print(item.category.name)  # "Напитки"

# Обратный доступ: от родительского к дочерним
drinks = Category.objects.get(name="Напитки")
drinks.items.all()        # Все пункты меню в категории
drinks.items.count()      # Количество пунктов
drinks.items.filter(price__lt=300)  # Фильтрация
```

**Когда использовать:** `CASCADE` — когда дочерние объекты не имеют смысла без родительского. `PROTECT` — когда удаление должно быть осознанным.

> **Подробнее:** см. файл [`examples/04_foreignkey_relations.py`](examples/04_foreignkey_relations.py) — ForeignKey, on_delete и связанные запросы.

### Практика

Перейдите к файлу [`exercises/django_db_practice.md`](exercises/django_db_practice.md) и выполните **Часть 4: ForeignKey и связи** (задания 4.1–4.3).

---

## Блок 6: SQL vs Django ORM (10 мин)

Сравним, как одни и те же операции записываются на SQL и через Django ORM:

### Чтение данных

| Операция | SQL | Django ORM |
|----------|-----|------------|
| Все записи | `SELECT * FROM menu_items` | `MenuItem.objects.all()` |
| Фильтрация (=) | `WHERE name = 'Капучино'` | `.filter(name="Капучино")` |
| Фильтрация (<) | `WHERE price < 300` | `.filter(price__lt=300)` |
| Фильтрация (>=) | `WHERE price >= 200` | `.filter(price__gte=200)` |
| LIKE | `WHERE name LIKE '%кофе%'` | `.filter(name__contains="кофе")` |
| IN | `WHERE id IN (1, 2, 3)` | `.filter(id__in=[1, 2, 3])` |
| IS NULL | `WHERE category IS NULL` | `.filter(category__isnull=True)` |
| NOT | `WHERE NOT is_available` | `.exclude(is_available=True)` |
| ORDER BY | `ORDER BY price DESC` | `.order_by("-price")` |
| LIMIT | `LIMIT 5` | `[:5]` |
| COUNT | `SELECT COUNT(*)` | `.count()` |
| DISTINCT | `SELECT DISTINCT category` | `.values("category").distinct()` |

### Создание, обновление, удаление

| Операция | SQL | Django ORM |
|----------|-----|------------|
| INSERT | `INSERT INTO ... VALUES ...` | `.objects.create(...)` |
| UPDATE | `UPDATE ... SET ... WHERE ...` | `.filter(...).update(...)` |
| DELETE | `DELETE FROM ... WHERE ...` | `.filter(...).delete()` |

### Агрегация

```python
from django.db.models import Count, Avg, Sum, Min, Max

# SELECT COUNT(*) FROM menu_items;
MenuItem.objects.count()

# SELECT AVG(price) FROM menu_items;
MenuItem.objects.aggregate(avg_price=Avg("price"))

# SELECT category_id, COUNT(*) FROM menu_items GROUP BY category_id;
MenuItem.objects.values("category").annotate(count=Count("id"))
```

> **Подробнее:** см. файл [`examples/05_sql_vs_orm.py`](examples/05_sql_vs_orm.py) — полная таблица соответствий SQL и Django ORM.

### Практика

Перейдите к файлу [`exercises/django_db_practice.md`](exercises/django_db_practice.md) и выполните **Часть 5: SQL vs Django ORM** (задания 5.1–5.4).

---

## Блок 7: Утилиты Django — inspectdb, AutoField, dbshell (5 мин)

### inspectdb — генерация моделей из существующей БД

Если у вас уже есть база данных с таблицами, Django может **автоматически сгенерировать модели**:

```bash
# Вывести модели для всех таблиц
python manage.py inspectdb

# Вывести модели для конкретной таблицы
python manage.py inspectdb menu_items

# Сохранить в файл
python manage.py inspectdb > cafe/models.py
```

```python
# Пример сгенерированной модели:
class MenuItems(models.Model):
    name = models.TextField()
    price = models.FloatField()

    class Meta:
        managed = False  # Django не будет управлять таблицей
        db_table = "menu_items"
```

**Когда использовать:** при подключении Django к уже существующей базе данных (legacy-проекты).

### AutoField — автоматический первичный ключ

Django автоматически добавляет поле `id` к каждой модели:

```python
# Эти два определения ЭКВИВАЛЕНТНЫ:

# Вариант 1: id создаётся автоматически
class MenuItem(models.Model):
    name = models.CharField(max_length=200)

# Вариант 2: id указан явно
class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляется автоматически!
    name = models.CharField(max_length=200)
```

В `settings.py` можно настроить тип AutoField:

```python
# BigAutoField — для больших таблиц (по умолчанию в Django 3.2+)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

### dbshell — интерактивная SQL-консоль

```bash
# Открыть SQL-консоль для базы данных проекта
python manage.py dbshell

# Внутри dbshell можно писать SQL-запросы:
sqlite> SELECT * FROM cafe_menuitem LIMIT 5;
sqlite> .tables
sqlite> .quit
```

**Когда использовать:** для быстрой проверки данных в БД без написания Python-кода.

> **Подробнее:** см. файл [`examples/06_django_tools.py`](examples/06_django_tools.py) — демонстрация inspectdb, AutoField и dbshell.

### Практика

Перейдите к файлу [`exercises/django_db_practice.md`](exercises/django_db_practice.md) и выполните **Часть 6: Утилиты Django** (задания 6.1–6.3).

---

## Подведение итогов

### Шпаргалка

| Концепция | Ключевое |
|-----------|----------|
| `sqlite3` | Встроенный модуль Python для работы с SQLite |
| SQL-инъекция | Подстановка вредоносного SQL через пользовательский ввод |
| Параметризованный запрос | `cursor.execute("... WHERE id = ?", (id,))` — защита от инъекций |
| Django ORM | Работа с БД через Python-объекты вместо SQL |
| Модель | Python-класс = таблица в БД |
| Миграция | `makemigrations` → `migrate` — обновление схемы БД |
| `ForeignKey` | Связь «многие к одному» между моделями |
| `on_delete` | Стратегия при удалении (CASCADE, PROTECT, SET_NULL) |
| `inspectdb` | Генерация моделей из существующей БД |
| `AutoField` | Автоматический первичный ключ (id) |
| `dbshell` | SQL-консоль Django |

### Ключевые выводы

1. **Никогда не используйте f-строки для SQL-запросов.** Всегда применяйте параметризованные запросы (`?` для sqlite3) или ORM.

2. **Django ORM = SQL, но безопаснее и удобнее.** Модель описывает таблицу, QuerySet описывает запрос, а миграции управляют схемой.

3. **`ForeignKey` + `on_delete`** — ключевой инструмент для связи таблиц. Выбирайте `CASCADE` для зависимых данных и `PROTECT` для важных.

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
│   ├── 03_django_orm_basics.py            # Django ORM: модели и CRUD
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
