"""
Семинар 8: pytest fixtures — фикстуры для тестов.

Демонстрирует:
- @pytest.fixture — объявление фикстуры
- scope: function / module — когда пересоздавать фикстуру
- yield — setup + teardown в одной фикстуре
- Зависимости между фикстурами (фикстура принимает другую фикстуру)
- conftest.py — общие фикстуры для всего пакета
- Примеры для моделей кафе (без реальной БД)

Запуск (из корня репозитория):
    pytest seminars/seminar_08_testing_and_containerization/examples/03_pytest_fixtures.py -v

Или напрямую (демонстрационный режим):
    python seminars/seminar_08_testing_and_containerization/examples/03_pytest_fixtures.py
"""

import sys
from dataclasses import dataclass, field
from decimal import Decimal

import pytest

# ============================================================
# Предметная область: dataclass-модели кафе (без Django)
# ============================================================
# В реальном cafe_project вместо них будут Django-модели.
# Здесь мы используем простые Python-объекты, чтобы показать
# концепции фикстур без зависимости от БД.


@dataclass
class Category:
    """Категория блюд."""

    id: int
    name: str


@dataclass
class MenuItem:
    """Позиция в меню."""

    id: int
    name: str
    category: Category
    price: Decimal
    is_available: bool = True


@dataclass
class OrderItem:
    """Позиция в заказе."""

    menu_item: MenuItem
    quantity: int
    price: Decimal


@dataclass
class Order:
    """Заказ клиента."""

    id: int
    customer_name: str
    items: list[OrderItem] = field(default_factory=list)

    @property
    def total(self) -> Decimal:
        """Итоговая сумма заказа."""
        return sum(
            (item.price * item.quantity for item in self.items),
            Decimal("0"),
        )


# ============================================================
# 1. @pytest.fixture — базовые фикстуры
# ============================================================
# Фикстура — функция с декоратором @pytest.fixture.
# pytest вызывает её и передаёт результат в тест по имени параметра.


@pytest.fixture
def category_drinks() -> Category:
    """Фикстура: категория 'Напитки'.

    Пересоздаётся для каждого теста (scope='function' по умолчанию).
    Это обеспечивает изоляцию: каждый тест получает свежий объект.
    """
    return Category(id=1, name="Напитки")


@pytest.fixture
def category_pastry() -> Category:
    """Фикстура: категория 'Выпечка'."""
    return Category(id=2, name="Выпечка")


@pytest.fixture
def menu_item_cappuccino(category_drinks: Category) -> MenuItem:
    """Фикстура: позиция 'Капучино'.

    Принимает category_drinks как параметр — pytest автоматически
    разрешает зависимости между фикстурами!
    """
    return MenuItem(
        id=1,
        name="Капучино",
        category=category_drinks,
        price=Decimal("250.00"),
        is_available=True,
    )


@pytest.fixture
def menu_item_espresso_unavailable(category_drinks: Category) -> MenuItem:
    """Фикстура: недоступный Эспрессо."""
    return MenuItem(
        id=2,
        name="Эспрессо",
        category=category_drinks,
        price=Decimal("180.00"),
        is_available=False,  # недоступен
    )


@pytest.fixture
def sample_order(menu_item_cappuccino: MenuItem) -> Order:
    """Фикстура: заказ с одной позицией.

    Зависит от menu_item_cappuccino, которая зависит от category_drinks.
    pytest строит граф зависимостей и вызывает фикстуры в нужном порядке.
    """
    order = Order(id=42, customer_name="Алиса")
    order.items.append(
        OrderItem(
            menu_item=menu_item_cappuccino,
            quantity=2,
            price=Decimal("250.00"),
        )
    )
    return order


# ============================================================
# 2. scope='module' — фикстура создаётся один раз на модуль
# ============================================================


@pytest.fixture(scope="module")
def heavy_config() -> dict:
    """Дорогая фикстура (scope='module'): создаётся один раз.

    Подходит для дорогих операций: загрузка конфига, подключение к БД.
    """
    # Имитация загрузки конфигурации
    return {
        "db_url": "sqlite:///:memory:",
        "max_items_per_order": 100,
        "currency": "RUB",
    }


# ============================================================
# 3. yield — setup + teardown в одной фикстуре
# ============================================================


@pytest.fixture
def temp_order_log(tmp_path: pytest.TempPathFactory) -> str:  # type: ignore[type-arg]
    """Фикстура с yield: файл создаётся до теста, очищается после.

    Всё ДО yield — setup (инициализация).
    Всё ПОСЛЕ yield — teardown (очистка, закрытие соединений и т.д.).
    """
    log_file = tmp_path / "orders.log"  # type: ignore[operator]
    log_file.write_text("# Лог заказов\n")

    yield str(log_file)  # передаём путь тесту

    # Teardown: выполняется ПОСЛЕ теста, даже если тест упал
    # (здесь tmp_path удаляется pytest автоматически)


# ============================================================
# 4. Тесты, использующие фикстуры
# ============================================================


def test_category_has_correct_name(category_drinks: Category) -> None:
    """Фикстура category_drinks создаёт категорию с правильным именем."""
    assert category_drinks.name == "Напитки"
    assert category_drinks.id == 1


def test_menu_item_belongs_to_category(
    menu_item_cappuccino: MenuItem,
    category_drinks: Category,
) -> None:
    """Капучино принадлежит категории Напитки."""
    assert menu_item_cappuccino.category == category_drinks
    assert menu_item_cappuccino.price == Decimal("250.00")
    assert menu_item_cappuccino.is_available is True


def test_unavailable_item(
    menu_item_espresso_unavailable: MenuItem,
) -> None:
    """Недоступный Эспрессо имеет is_available=False."""
    assert menu_item_espresso_unavailable.is_available is False
    assert menu_item_espresso_unavailable.name == "Эспрессо"


def test_order_total(sample_order: Order) -> None:
    """Заказ с Капучино x2 стоит 500 ₽."""
    assert sample_order.total == Decimal("500.00")
    assert sample_order.customer_name == "Алиса"


def test_filtering_available_items(
    menu_item_cappuccino: MenuItem,
    menu_item_espresso_unavailable: MenuItem,
) -> None:
    """Фильтрация по is_available работает корректно."""
    all_items = [menu_item_cappuccino, menu_item_espresso_unavailable]
    available = [item for item in all_items if item.is_available]
    unavailable = [item for item in all_items if not item.is_available]

    assert len(available) == 1
    assert available[0].name == "Капучино"
    assert len(unavailable) == 1
    assert unavailable[0].name == "Эспрессо"


def test_scope_module_fixture(heavy_config: dict) -> None:
    """Фикстура с scope='module' передаётся одним объектом на модуль."""
    assert heavy_config["currency"] == "RUB"
    assert heavy_config["max_items_per_order"] == 100


def test_temp_log_file_readable(temp_order_log: str) -> None:
    """Тест читает файл лога, созданный фикстурой с yield."""
    with open(temp_order_log) as f:
        content = f.read()
    assert "Лог заказов" in content


# ============================================================
# Шаблон для Django-фикстур (для cafe_project)
# ============================================================

DJANGO_FIXTURE_EXAMPLE = """
# В cafe_project/conftest.py:
import pytest
from decimal import Decimal
from cafe.models import Category, MenuItem, Order, OrderItem

@pytest.fixture
def category_drinks(db):
    # db — фикстура из pytest-django, открывает доступ к БД
    return Category.objects.create(name="Напитки")

@pytest.fixture
def menu_item_cappuccino(db, category_drinks):
    return MenuItem.objects.create(
        name="Капучино",
        category=category_drinks,
        price=Decimal("250.00"),
    )

@pytest.fixture
def sample_order(db, menu_item_cappuccino):
    order = Order.objects.create(
        customer_name="Алиса",
        total_amount=Decimal("500.00"),
    )
    OrderItem.objects.create(
        order=order,
        menu_item=menu_item_cappuccino,
        quantity=2,
        item_price=Decimal("250.00"),
    )
    return order

# В cafe/tests/test_views.py:
@pytest.mark.django_db
def test_order_created(sample_order):
    assert sample_order.customer_name == "Алиса"
    assert Order.objects.count() == 1
"""


# ============================================================
# Демонстрационный запуск
# ============================================================


def main() -> None:
    """Демонстрационный запуск (без pytest)."""
    print("=" * 60)
    print("СЕМИНАР 8: PYTEST FIXTURES")
    print("=" * 60)
    print()
    print("Запуск через pytest (рекомендуется):")
    print(
        "  pytest seminars/seminar_08_testing_and_containerization/examples/03_pytest_fixtures.py -v"
    )
    print()
    print("Ключевые концепции:")
    print("  @pytest.fixture          — объявить фикстуру")
    print("  scope='function'         — пересоздаётся для каждого теста (default)")
    print("  scope='module'           — один раз на файл")
    print("  scope='session'          — один раз на всю pytest-сессию")
    print("  yield в фикстуре         — код до yield = setup, после = teardown")
    print("  параметр = фикстура      — зависимость между фикстурами")
    print()
    print("conftest.py:")
    print("  Файл с общими фикстурами — pytest находит его автоматически.")
    print("  Фикстуры из conftest.py доступны всем тестам в директории.")
    print()
    print("Для Django-моделей (pytest-django):")
    print("  @pytest.mark.django_db   — разрешить доступ к БД в тесте")
    print("  db (фикстура)            — передаётся как параметр фикстуры")
    print()
    print("Шаблон фикстур для Django-моделей:")
    print(DJANGO_FIXTURE_EXAMPLE)

    # Ручная демонстрация фикстур
    print("=" * 60)
    print("Ручная демонстрация (имитация pytest):")
    print()

    cat = Category(id=1, name="Напитки")
    print(f"  category_drinks(): {cat}")

    item = MenuItem(
        id=1,
        name="Капучино",
        category=cat,
        price=Decimal("250.00"),
    )
    print(f"  menu_item_cappuccino: {item.name}, {item.price} ₽")

    order = Order(id=42, customer_name="Алиса")
    order.items.append(OrderItem(menu_item=item, quantity=2, price=Decimal("250.00")))
    print(f"  sample_order: заказ #{order.id}, итого {order.total} ₽")

    sys.exit(0)


if __name__ == "__main__":
    main()
