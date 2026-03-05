"""
Семинар 6: Утилиты Django — inspectdb, AutoField, dbshell.

Этот модуль демонстрирует:
- inspectdb: генерация моделей из существующей БД
- AutoField / BigAutoField: автоматический первичный ключ
- dbshell: интерактивная SQL-консоль Django

Примечание: этот файл выводит примеры на экран.
Для реальной работы с утилитами используйте manage.py.
"""

# ============================================================
# 1. inspectdb — генерация моделей из существующей БД
# ============================================================

INSPECTDB_USAGE = """
=== inspectdb — генерация моделей из БД ===

Если у вас уже есть база данных с таблицами (например, legacy-проект),
Django может автоматически сгенерировать модели.

# Шаг 1: Подключите БД в settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "existing_database.db",
    }
}

# Шаг 2: Сгенерируйте модели
$ python manage.py inspectdb

# Шаг 3: Сохраните в файл
$ python manage.py inspectdb > myapp/models.py

# Шаг 4: Для конкретной таблицы
$ python manage.py inspectdb menu_items categories
"""

INSPECTDB_EXAMPLE = """
=== Пример вывода inspectdb ===

# Для таблицы cafe_menu.sql Django сгенерирует примерно:

class Categories(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False        # Django НЕ будет управлять этой таблицей
        db_table = "categories"  # Имя таблицы в БД


class MenuItems(models.Model):
    name = models.TextField()
    category = models.ForeignKey(
        Categories,
        models.DO_NOTHING,     # inspectdb ставит DO_NOTHING по умолчанию
        blank=True, null=True,
    )
    price = models.FloatField()
    is_available = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "menu_items"

=== Что нужно исправить после inspectdb ===

1. managed = False → True (если хотите, чтобы Django управлял таблицей)
2. DO_NOTHING → CASCADE/PROTECT (выберите правильную стратегию)
3. TextField → CharField (где нужна ограниченная длина)
4. IntegerField → BooleanField (для логических полей)
5. Добавьте __str__() и verbose_name
"""

# ============================================================
# 2. AutoField — автоматический первичный ключ
# ============================================================

AUTOFIELD_EXPLANATION = """
=== AutoField / BigAutoField — автоматический первичный ключ ===

Django автоматически добавляет поле `id` к каждой модели.
Вам НЕ нужно объявлять его вручную!

# Эти два определения полностью ЭКВИВАЛЕНТНЫ:

# Вариант 1: id создаётся автоматически
class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)


# Вариант 2: id указан явно (обычно не нужно)
class MenuItem(models.Model):
    id = models.BigAutoField(primary_key=True)  # Добавляется автоматически!
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)


=== Типы AutoField ===

AutoField       — 32-бит целое число (до 2,147,483,647)
BigAutoField    — 64-бит целое число (до 9,223,372,036,854,775,807)
SmallAutoField  — 16-бит целое число (до 32,767)

=== Настройка в settings.py ===

# Django 3.2+ по умолчанию использует BigAutoField
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Можно изменить на уровне приложения:
# myapp/apps.py
class MyAppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "myapp"


=== Когда нужен кастомный первичный ключ? ===

# UUID вместо числового ID:
import uuid
from django.db import models


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    customer_name = models.CharField(max_length=200)

# Использование:
# order = Order.objects.create(customer_name="Алиса")
# print(order.id)  # '550e8400-e29b-41d4-a716-446655440000'
"""

# ============================================================
# 3. dbshell — интерактивная SQL-консоль
# ============================================================

DBSHELL_USAGE = """
=== dbshell — SQL-консоль Django ===

dbshell открывает консоль SQL для базы данных, указанной в settings.py.
Это удобно для быстрой проверки данных без написания Python-кода.

# Запуск
$ python manage.py dbshell

# Для SQLite откроется sqlite3:
sqlite> .tables
# auth_group          auth_user           cafe_menuitem
# auth_group_perms    cafe_category       cafe_order

sqlite> SELECT * FROM cafe_menuitem LIMIT 3;
# 1|Капучино|1|250.00||1
# 2|Латте|1|280.00||1
# 3|Эспрессо|1|180.00||1

sqlite> SELECT COUNT(*) FROM cafe_menuitem;
# 18

sqlite> .schema cafe_menuitem
# CREATE TABLE "cafe_menuitem" (
#     "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
#     "name" varchar(200) NOT NULL,
#     "category_id" bigint NOT NULL REFERENCES "cafe_category" ("id"),
#     "price" decimal NOT NULL,
#     "description" text NOT NULL,
#     "is_available" bool NOT NULL
# );

sqlite> .quit


=== Полезные команды sqlite3 ===

.tables              — список всех таблиц
.schema имя_таблицы  — структура таблицы (CREATE TABLE)
.headers on          — включить заголовки столбцов
.mode column         — табличный формат вывода
.quit                — выход


=== Когда использовать dbshell ===

- Быстрая проверка данных в БД
- Отладка миграций (проверить, что таблица создана)
- Выполнение одноразовых SQL-запросов
- Проверка структуры таблиц

=== Альтернатива: Django shell ===

$ python manage.py shell

>>> from cafe.models import MenuItem
>>> MenuItem.objects.count()
18
>>> MenuItem.objects.filter(price__lt=200).values_list("name", flat=True)
<QuerySet ['Эспрессо', 'Чай зелёный', 'Чай чёрный', 'Круассан']>

dbshell — для SQL-запросов, shell — для Django ORM.
"""


# ============================================================
# Функции демонстрации
# ============================================================


def demonstrate_inspectdb() -> None:
    """Демонстрация inspectdb."""
    print("=" * 60)
    print("1. inspectdb — генерация моделей из БД")
    print("=" * 60)
    print(INSPECTDB_USAGE)
    print(INSPECTDB_EXAMPLE)


def demonstrate_autofield() -> None:
    """Демонстрация AutoField."""
    print("\n" + "=" * 60)
    print("2. AutoField — автоматический первичный ключ")
    print("=" * 60)
    print(AUTOFIELD_EXPLANATION)


def demonstrate_dbshell() -> None:
    """Демонстрация dbshell."""
    print("\n" + "=" * 60)
    print("3. dbshell — SQL-консоль Django")
    print("=" * 60)
    print(DBSHELL_USAGE)


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 6: УТИЛИТЫ DJANGO — INSPECTDB, AUTOFIELD, DBSHELL")
    print("=" * 60)

    demonstrate_inspectdb()
    demonstrate_autofield()
    demonstrate_dbshell()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
