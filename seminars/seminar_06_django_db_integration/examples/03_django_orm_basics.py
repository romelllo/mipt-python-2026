"""
Семинар 6: Django ORM — модели и CRUD-операции.

Этот модуль демонстрирует:
- Определение моделей Django (поля, Meta, __str__)
- CRUD-операции через Django ORM
- Методы QuerySet (all, filter, exclude, get, count, order_by)
- Создание и применение миграций

Примечание: этот файл содержит примеры кода Django для изучения.
Он выводит примеры на экран. Для запуска реального Django-приложения
используйте команды manage.py.
"""

# ============================================================
# 1. Определение моделей
# ============================================================

MODEL_DEFINITION = """
# cafe/models.py
from django.db import models


class Category(models.Model):
    \"\"\"Категория блюд в кафе.\"\"\"

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    \"\"\"Позиция в меню кафе.\"\"\"

    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True, default="")
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} — {self.price} ₽"
"""

# ============================================================
# 2. Основные типы полей Django
# ============================================================

FIELD_TYPES = """
=== Основные типы полей Django ===

Текстовые:
  CharField(max_length=N)     — строка ограниченной длины
  TextField()                 — текст без ограничения
  EmailField()                — email (с валидацией)
  URLField()                  — URL (с валидацией)
  SlugField()                 — URL-совместимая строка (буквы, цифры, -)

Числовые:
  IntegerField()              — целое число
  FloatField()                — число с плавающей точкой
  DecimalField(max_digits, decimal_places) — точное десятичное число
  PositiveIntegerField()      — положительное целое

Логические:
  BooleanField()              — True / False
  NullBooleanField()          — True / False / None

Дата и время:
  DateField()                 — дата (YYYY-MM-DD)
  TimeField()                 — время (HH:MM:SS)
  DateTimeField()             — дата и время

Связи:
  ForeignKey(Model)           — «многие к одному»
  ManyToManyField(Model)      — «многие ко многим»
  OneToOneField(Model)        — «один к одному»

Параметры полей:
  null=True         — разрешить NULL в БД
  blank=True        — разрешить пустое значение в формах
  default=значение  — значение по умолчанию
  unique=True       — уникальное значение
  choices=CHOICES   — ограниченный набор значений
  auto_now_add=True — автоматическая дата при создании
  auto_now=True     — автоматическая дата при каждом сохранении
"""

# ============================================================
# 3. Миграции
# ============================================================

MIGRATIONS_EXAMPLE = """
=== Миграции — управление схемой БД ===

# Шаг 1: Создать файл миграции
$ python manage.py makemigrations
# Создаёт файл: cafe/migrations/0001_initial.py
# Содержит инструкции: какие таблицы создать, какие поля добавить

# Шаг 2: Применить миграцию
$ python manage.py migrate
# Выполняет SQL-запросы для создания/изменения таблиц

# Шаг 3: Посмотреть SQL, который сгенерирует миграция
$ python manage.py sqlmigrate cafe 0001
# BEGIN;
# CREATE TABLE "cafe_category" (
#     "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
#     "name" varchar(100) NOT NULL UNIQUE,
#     "description" text NOT NULL
# );
# ...
# COMMIT;

# Полезные команды:
$ python manage.py showmigrations        # Статус миграций
$ python manage.py makemigrations --name описание  # Имя миграции
"""

# ============================================================
# 4. CRUD-операции
# ============================================================

CRUD_EXAMPLES = """
=== CRUD-операции через Django ORM ===

# Откройте Django shell: python manage.py shell
from cafe.models import Category, MenuItem

# --- CREATE (создание) ---

# Способ 1: create() — создаёт и сохраняет сразу
drinks = Category.objects.create(name="Напитки")

# Способ 2: создаём объект, затем save()
pastry = Category(name="Выпечка")
pastry.save()

# Создание с ForeignKey
cappuccino = MenuItem.objects.create(
    name="Капучино",
    category=drinks,
    price=250.00,
    description="Классический капучино",
)


# --- READ (чтение) ---

# all() — все записи (QuerySet)
all_items = MenuItem.objects.all()

# filter() — фильтрация (QuerySet)
cheap_items = MenuItem.objects.filter(price__lt=300)
available = MenuItem.objects.filter(is_available=True)
drinks_items = MenuItem.objects.filter(category__name="Напитки")

# exclude() — исключение (QuerySet)
not_drinks = MenuItem.objects.exclude(category__name="Напитки")

# get() — один объект (или исключение!)
item = MenuItem.objects.get(pk=1)           # По первичному ключу
# MenuItem.objects.get(name="Несуществующий")  # DoesNotExist!
# MenuItem.objects.get(price__lt=300)           # MultipleObjectsReturned!

# first(), last() — первая/последняя запись (или None)
first_item = MenuItem.objects.first()
last_item = MenuItem.objects.order_by("-price").first()

# exists() — проверка наличия
has_items = MenuItem.objects.filter(price__gt=1000).exists()  # False

# count() — количество
total = MenuItem.objects.count()

# order_by() — сортировка
by_price = MenuItem.objects.order_by("price")         # По возрастанию
by_price_desc = MenuItem.objects.order_by("-price")    # По убыванию

# values() / values_list() — только нужные поля
names = MenuItem.objects.values_list("name", flat=True)
# <QuerySet ['Капучино', 'Латте', ...]>

# Срез (LIMIT/OFFSET)
top_5 = MenuItem.objects.order_by("-price")[:5]


# --- UPDATE (обновление) ---

# Способ 1: изменить объект и save()
item = MenuItem.objects.get(pk=1)
item.price = 270.00
item.save()

# Способ 2: массовое обновление (без вызова save())
MenuItem.objects.filter(category=drinks).update(is_available=True)


# --- DELETE (удаление) ---

# Удалить один объект
item = MenuItem.objects.get(pk=1)
item.delete()

# Массовое удаление
MenuItem.objects.filter(is_available=False).delete()
"""

# ============================================================
# 5. Lookup-выражения (фильтры)
# ============================================================

LOOKUPS = """
=== Lookup-выражения для filter() ===

Точное совпадение:
  .filter(name="Капучино")            # WHERE name = 'Капучино'
  .filter(name__exact="Капучино")     # То же самое

Регистронезависимое:
  .filter(name__iexact="капучино")    # WHERE UPPER(name) = 'КАПУЧИНО'

Содержит:
  .filter(name__contains="кофе")      # WHERE name LIKE '%кофе%'
  .filter(name__icontains="КОФЕ")     # Регистронезависимо

Начинается / заканчивается:
  .filter(name__startswith="Кап")     # WHERE name LIKE 'Кап%'
  .filter(name__endswith="ино")       # WHERE name LIKE '%ино'

Сравнение:
  .filter(price__gt=200)              # WHERE price > 200
  .filter(price__gte=200)             # WHERE price >= 200
  .filter(price__lt=300)              # WHERE price < 300
  .filter(price__lte=300)             # WHERE price <= 300

Диапазон:
  .filter(price__range=(200, 300))    # WHERE price BETWEEN 200 AND 300

Вхождение в список:
  .filter(id__in=[1, 2, 3])          # WHERE id IN (1, 2, 3)

NULL:
  .filter(description__isnull=True)   # WHERE description IS NULL

По связанным объектам (через __):
  .filter(category__name="Напитки")   # JOIN + WHERE category.name = ...
"""


# ============================================================
# Функции демонстрации
# ============================================================


def demonstrate_models() -> None:
    """Демонстрация определения моделей."""
    print("=" * 60)
    print("1. Определение моделей Django")
    print("=" * 60)
    print(MODEL_DEFINITION)


def demonstrate_field_types() -> None:
    """Демонстрация типов полей."""
    print("\n" + "=" * 60)
    print("2. Типы полей Django")
    print("=" * 60)
    print(FIELD_TYPES)


def demonstrate_migrations() -> None:
    """Демонстрация миграций."""
    print("\n" + "=" * 60)
    print("3. Миграции — управление схемой БД")
    print("=" * 60)
    print(MIGRATIONS_EXAMPLE)


def demonstrate_crud() -> None:
    """Демонстрация CRUD-операций."""
    print("\n" + "=" * 60)
    print("4. CRUD-операции через Django ORM")
    print("=" * 60)
    print(CRUD_EXAMPLES)


def demonstrate_lookups() -> None:
    """Демонстрация lookup-выражений."""
    print("\n" + "=" * 60)
    print("5. Lookup-выражения для фильтрации")
    print("=" * 60)
    print(LOOKUPS)


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 6: DJANGO ORM — МОДЕЛИ И CRUD")
    print("=" * 60)

    demonstrate_models()
    demonstrate_field_types()
    demonstrate_migrations()
    demonstrate_crud()
    demonstrate_lookups()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
