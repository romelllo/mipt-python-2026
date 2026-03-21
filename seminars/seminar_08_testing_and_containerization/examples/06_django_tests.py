"""
Семинар 8: Django TestCase + Client — тестирование views.

Этот файл демонстрирует паттерны тестирования Django-приложений.
Содержит:
  - Шаблоны тестов для cafe_project (готовый код для copy-paste)
  - Объяснение setUpTestData vs setUp
  - self.client.get() / self.client.post()
  - Проверка status_code, содержимого ответа

Для запуска реальных Django-тестов используйте cafe_project:
    python manage.py test cafe

Для проверки этого файла без cafe_project запустите напрямую:
    python seminars/seminar_08_testing_and_containerization/examples/06_django_tests.py
"""

import sys

# ============================================================
# Паттерны тестирования Django — шаблоны кода
# ============================================================
# Следующие классы показывают, как писать тесты для cafe_project.
# В реальном проекте скопируйте их в cafe/tests.py.

DJANGO_TEST_PATTERNS = """
# ============================================================
# cafe/tests.py — скопируйте этот код в ваш cafe_project
# ============================================================
from decimal import Decimal
from django.test import TestCase
from cafe.models import Category, MenuItem, Order, OrderItem


# ============================================================
# 1. Тесты с setUpTestData — данные один раз на класс
# ============================================================

class MenuViewTestCase(TestCase):
    \"\"\"Тесты для view cafe.views.menu_list.\"\"\"

    @classmethod
    def setUpTestData(cls):
        # setUpTestData: вызывается ОДИН РАЗ для всего класса.
        # Django откатывает изменения каждого теста через savepoint.
        # Это быстрее, чем setUp (который вызывается перед каждым тестом).
        cls.drinks = Category.objects.create(name="Напитки")
        cls.pastry = Category.objects.create(name="Выпечка")

        cls.cappuccino = MenuItem.objects.create(
            name="Капучино",
            category=cls.drinks,
            price=Decimal("250.00"),
            is_available=True,
        )
        cls.latte = MenuItem.objects.create(
            name="Латте",
            category=cls.drinks,
            price=Decimal("280.00"),
            is_available=True,
        )
        cls.croissant = MenuItem.objects.create(
            name="Круассан",
            category=cls.pastry,
            price=Decimal("180.00"),
            is_available=True,
        )
        # Недоступная позиция — не должна показываться на странице
        cls.unavailable_item = MenuItem.objects.create(
            name="Недоступный товар",
            category=cls.drinks,
            price=Decimal("999.00"),
            is_available=False,
        )

    def test_menu_page_returns_200(self):
        \"\"\"GET /menu/ возвращает статус 200.\"\"\"
        # self.client — тестовый HTTP-клиент Django
        response = self.client.get("/menu/")
        self.assertEqual(response.status_code, 200)

    def test_available_items_shown(self):
        \"\"\"Страница показывает доступные позиции.\"\"\"
        response = self.client.get("/menu/")
        content = response.content.decode("utf-8")
        self.assertIn("Капучино", content)
        self.assertIn("Латте", content)
        self.assertIn("Круассан", content)

    def test_unavailable_item_not_shown(self):
        \"\"\"Позиции is_available=False не отображаются.\"\"\"
        response = self.client.get("/menu/")
        content = response.content.decode("utf-8")
        # Ключевая проверка: скрытые товары не должны попасть на страницу
        self.assertNotIn("Недоступный товар", content)

    def test_category_filter(self):
        \"\"\"Фильтрация ?category=N возвращает только её позиции.\"\"\"
        response = self.client.get(f"/menu/?category={self.drinks.pk}")
        content = response.content.decode("utf-8")
        self.assertIn("Капучино", content)
        self.assertIn("Латте", content)
        self.assertNotIn("Круассан", content)  # другая категория

    def test_invalid_category_returns_empty_200(self):
        \"\"\"Фильтрация по несуществующему category ID не падает.\"\"\"
        response = self.client.get("/menu/?category=99999")
        self.assertEqual(response.status_code, 200)


# ============================================================
# 2. Тесты с setUp — данные перед каждым тестом (полная изоляция)
# ============================================================

class MenuItemModelTestCase(TestCase):
    \"\"\"Тесты для модели MenuItem.

    setUp vs setUpTestData:
    - setUp: вызывается ПЕРЕД каждым тестом → полная изоляция,
      но медленнее (пересоздаёт данные каждый раз)
    - setUpTestData: вызывается ОДИН РАЗ → быстрее, но тесты
      не должны изменять данные cls.*
    \"\"\"

    def setUp(self):
        self.category = Category.objects.create(name="Тест-категория")
        self.item = MenuItem.objects.create(
            name="Тест-блюдо",
            category=self.category,
            price=Decimal("100.00"),
        )

    def test_str_representation(self):
        \"\"\"__str__ содержит имя и цену.\"\"\"
        self.assertIn("Тест-блюдо", str(self.item))
        self.assertIn("100", str(self.item))

    def test_default_is_available_true(self):
        \"\"\"По умолчанию is_available=True.\"\"\"
        self.assertTrue(self.item.is_available)

    def test_update_price_persists(self):
        \"\"\"Обновлённая цена сохраняется в БД.\"\"\"
        self.item.price = Decimal("150.00")
        self.item.save()
        refreshed = MenuItem.objects.get(pk=self.item.pk)
        self.assertEqual(refreshed.price, Decimal("150.00"))


# ============================================================
# 3. Тест для order_detail view
# ============================================================

class OrderDetailViewTestCase(TestCase):
    \"\"\"Тесты для view cafe.views.order_detail.\"\"\"

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Напитки")
        cappuccino = MenuItem.objects.create(
            name="Капучино", category=category, price=Decimal("250.00")
        )
        cls.order = Order.objects.create(
            customer_name="Алиса",
            total_amount=Decimal("500.00"),
            status="completed",
        )
        OrderItem.objects.create(
            order=cls.order,
            menu_item=cappuccino,
            quantity=2,
            item_price=Decimal("250.00"),
        )

    def test_order_detail_returns_200(self):
        response = self.client.get(f"/orders/{self.order.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_order_detail_shows_customer_name(self):
        response = self.client.get(f"/orders/{self.order.pk}/")
        self.assertIn("Алиса", response.content.decode())

    def test_order_detail_404_for_missing(self):
        \"\"\"Несуществующий заказ возвращает 404.\"\"\"
        response = self.client.get("/orders/99999/")
        self.assertEqual(response.status_code, 404)
"""


# ============================================================
# Демонстрация паттернов тестирования (без запуска Django)
# ============================================================


def explain_setup_vs_setupclassdata() -> None:
    """Объяснение разницы setUp и setUpTestData."""
    print("=" * 60)
    print("setUp vs setUpTestData")
    print("=" * 60)
    print("""
  setUp()                       setUpTestData()
  ─────────────────────────     ─────────────────────────
  Вызов: перед КАЖДЫМ тестом    Вызов: ОДИН РАЗ на класс
  Скорость: медленнее           Скорость: быстрее
  Изоляция: полная              Изоляция: через savepoint
  Когда: тесты меняют данные    Когда: тесты только читают

  СОВЕТ: используйте setUpTestData если тесты не изменяют
  данные через cls.item.save() или cls.item.delete().
  Если изменяете — используйте setUp.
""")


def explain_test_client() -> None:
    """Объяснение Django test client."""
    print("=" * 60)
    print("Django Test Client — self.client")
    print("=" * 60)
    print("""
  self.client — встроенный HTTP-клиент для тестов.
  Делает запросы к вашему Django-приложению БЕЗ реального сервера.

  Основные методы:
  ┌─────────────────────────────────────────────────────────┐
  │ response = self.client.get("/menu/")                    │
  │ response = self.client.get("/menu/?category=1")         │
  │ response = self.client.post("/orders/", data={...})     │
  │ response = self.client.post("/login/", {                │
  │     "username": "admin", "password": "pass"             │
  │ })                                                      │
  └─────────────────────────────────────────────────────────┘

  Что проверять в response:
  ┌─────────────────────────────────────────────────────────┐
  │ response.status_code           # 200, 404, 302, ...     │
  │ response.content.decode()      # HTML-содержимое        │
  │ response.context["items"]      # контекст шаблона       │
  │ response["Location"]           # заголовок redirect     │
  └─────────────────────────────────────────────────────────┘

  Утверждения (assertions) Django TestCase:
  ┌─────────────────────────────────────────────────────────┐
  │ self.assertEqual(response.status_code, 200)             │
  │ self.assertIn("Капучино", content)                      │
  │ self.assertTemplateUsed(response, "cafe/menu_list.html")│
  │ self.assertContains(response, "Капучино")               │
  │ self.assertRedirects(response, "/login/")               │
  └─────────────────────────────────────────────────────────┘
""")


def show_test_template() -> None:
    """Вывод шаблона кода для cafe_project."""
    print("=" * 60)
    print("ШАБЛОН КОДА: cafe/tests.py")
    print("=" * 60)
    print("Скопируйте следующий код в cafe/tests.py вашего проекта:")
    print()
    # Показываем первые 30 строк шаблона
    lines = DJANGO_TEST_PATTERNS.strip().split("\n")
    for line in lines[:30]:
        print(f"  {line}")
    print("  ...")
    print(f"  (всего {len(lines)} строк — см. переменную DJANGO_TEST_PATTERNS)")


def main() -> None:
    """Запуск демонстрации паттернов Django-тестирования."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 8: DJANGO TESTCASE + CLIENT")
    print("=" * 60)
    print()
    print("Запуск в реальном cafe_project:")
    print("  python manage.py test cafe -v 2")
    print()
    print("Или через pytest (с pytest-django):")
    print("  pytest cafe/ -v")
    print()

    explain_setup_vs_setupclassdata()
    explain_test_client()
    show_test_template()

    print()
    print("=" * 60)
    print("Демонстрация завершена!")
    print("Полный шаблон кода в переменной DJANGO_TEST_PATTERNS.")
    print("=" * 60)

    sys.exit(0)


if __name__ == "__main__":
    main()
