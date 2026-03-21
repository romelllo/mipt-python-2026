"""
conftest.py — общие pytest-фикстуры для семинара 8.

Этот файл автоматически находится pytest и его фикстуры
доступны всем тестовым файлам в директории seminar_08_testing_and_containerization/.

Содержит:
- Настройку Django (django_settings / DJANGO_SETTINGS_MODULE)
- Базовые фикстуры для моделей кафе
- Документацию по использованию pytest-django
"""

import django.conf
import pytest

# ============================================================
# Настройка Django для pytest-django
# ============================================================
# Вариант 1 (рекомендуемый): через pyproject.toml
# Добавьте в pyproject.toml:
#
#   [tool.pytest.ini_options]
#   DJANGO_SETTINGS_MODULE = "cafe_project.settings"
#
# Вариант 2: через переменную окружения перед запуском pytest:
#   DJANGO_SETTINGS_MODULE=cafe_project.settings pytest
#
# Вариант 3 (здесь): программно через django.conf.settings.configure()
# Используется для автономной работы без полного cafe_project.

if not django.conf.settings.configured:
    django.conf.settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                # :memory: — БД в RAM, уничтожается после каждого теста
                # Это быстрее, чем файловая БД, и не оставляет следов
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
        ],
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
    )

import django  # noqa: E402

django.setup()


# ============================================================
# Фикстуры для тестов с реальной БД
# ============================================================
# Используйте @pytest.mark.django_db в тестах, которые работают с БД.
# Фикстура db передаётся из pytest-django и открывает доступ к БД.


@pytest.fixture
def sample_category(db: pytest.FixtureRequest) -> dict:
    """Возвращает словарь с данными категории для тестов без Django-моделей."""
    return {"name": "Напитки", "description": "Горячие и холодные напитки"}


@pytest.fixture
def sample_menu_items() -> list[dict]:
    """Список позиций меню кафе для unit-тестов (без БД)."""
    return [
        {
            "name": "Капучино",
            "category": "Напитки",
            "price": "250.00",
            "quantity": 1,
            "is_available": True,
        },
        {
            "name": "Латте",
            "category": "Напитки",
            "price": "280.00",
            "quantity": 2,
            "is_available": True,
        },
        {
            "name": "Круассан",
            "category": "Выпечка",
            "price": "180.00",
            "quantity": 1,
            "is_available": True,
        },
        {
            "name": "Эспрессо",
            "category": "Напитки",
            "price": "180.00",
            "quantity": 1,
            "is_available": False,  # Недоступен
        },
    ]


@pytest.fixture
def order_items_for_total() -> list[dict]:
    """Список позиций заказа для тестирования calculate_order_total."""
    return [
        {"price": "250.00", "quantity": 2},  # 500 ₽
        {"price": "180.00", "quantity": 1},  # 180 ₽
    ]
    # Итого: 680 ₽


# ============================================================
# Примеры использования фикстур в тестах
# ============================================================
# В тест-файле:
#
#   def test_something(sample_menu_items):
#       available = [i for i in sample_menu_items if i["is_available"]]
#       assert len(available) == 3
#
# Фикстуры из conftest.py не нужно импортировать —
# pytest находит их автоматически по имени параметра функции.
