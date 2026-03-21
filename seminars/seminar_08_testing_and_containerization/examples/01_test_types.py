"""
Семинар 8: Виды тестов — unit, component, integration, E2E.

Этот модуль демонстрирует разницу между типами тестов на примере
простого приложения кафе без Django (чистый Python).

Запуск: python examples/01_test_types.py
"""

from decimal import Decimal

# ============================================================
# Предметная область: функции и классы приложения кафе
# ============================================================


def calculate_order_total(items: list[dict]) -> Decimal:
    """Подсчитать итоговую сумму заказа.

    Args:
        items: список позиций, каждая с ключами 'price' и 'quantity'

    Returns:
        Итоговая сумма заказа в виде Decimal
    """
    total = Decimal("0")
    for item in items:
        price = Decimal(str(item["price"]))
        quantity = int(item["quantity"])
        total += price * quantity
    return total


class Menu:
    """Простое меню кафе (хранится в памяти).

    Используется для демонстрации component-теста (тест небольшой
    подсистемы — класса с несколькими методами).
    """

    def __init__(self) -> None:
        self._items: list[dict] = []

    def add_item(
        self,
        name: str,
        category: str,
        price: float,
        is_available: bool = True,
    ) -> None:
        """Добавить позицию в меню."""
        self._items.append(
            {
                "name": name,
                "category": category,
                "price": price,
                "is_available": is_available,
            }
        )

    def get_available(self) -> list[dict]:
        """Вернуть только доступные позиции."""
        return [item for item in self._items if item["is_available"]]

    def filter_by_category(self, category: str) -> list[dict]:
        """Отфильтровать позиции по категории (только доступные)."""
        return [
            item
            for item in self._items
            if item["category"] == category and item["is_available"]
        ]

    def get_cheapest(self, n: int = 3) -> list[dict]:
        """Вернуть n самых дешёвых доступных позиций."""
        available = self.get_available()
        return sorted(available, key=lambda x: x["price"])[:n]


# ============================================================
# 1. UNIT-тест — тестируем одну чистую функцию
# ============================================================


def demo_unit_test() -> None:
    """Демонстрация unit-теста для функции calculate_order_total."""
    print("=" * 60)
    print("1. UNIT-ТЕСТ")
    print("=" * 60)
    print(
        "  Тестируем: calculate_order_total(items) — одна чистая функция,"
        " без зависимостей, без БД, без сети."
    )

    # Тест 1: обычный заказ
    items = [
        {"price": "250.00", "quantity": 2},  # Капучино x2 = 500 ₽
        {"price": "180.00", "quantity": 1},  # Эспрессо x1 = 180 ₽
    ]
    result = calculate_order_total(items)
    assert result == Decimal("680.00"), f"Ожидали 680, получили {result}"
    print("  ✅ Тест 1 (обычный заказ): PASSED")

    # Тест 2: пустой заказ
    result_empty = calculate_order_total([])
    assert result_empty == Decimal("0"), f"Ожидали 0, получили {result_empty}"
    print("  ✅ Тест 2 (пустой заказ): PASSED")

    # Тест 3: один элемент
    result_single = calculate_order_total([{"price": "350.00", "quantity": 1}])
    assert result_single == Decimal("350.00"), f"Ожидали 350, получили {result_single}"
    print("  ✅ Тест 3 (один элемент): PASSED")

    print()
    print("  КЛЮЧЕВЫЕ ПРИЗНАКИ unit-теста:")
    print("  - Тестирует ровно ОДНУ функцию или метод")
    print("  - Нет зависимостей: нет БД, нет сети, нет файлов")
    print("  - Очень быстрый (миллисекунды)")
    print("  - При падении сразу ясно, ЧТО сломалось")


# ============================================================
# 2. COMPONENT-тест — тестируем небольшую подсистему
# ============================================================


def demo_component_test() -> None:
    """Демонстрация component-теста для класса Menu."""
    print("\n" + "=" * 60)
    print("2. COMPONENT-ТЕСТ (интеграция внутри подсистемы)")
    print("=" * 60)
    print(
        "  Тестируем: класс Menu — несколько методов работают вместе."
        " Реальных внешних зависимостей нет, но тест охватывает"
        " взаимодействие нескольких частей."
    )

    menu = Menu()
    menu.add_item("Капучино", "Напитки", 250.0)
    menu.add_item("Латте", "Напитки", 280.0)
    menu.add_item("Круассан", "Выпечка", 180.0)
    menu.add_item("Чизкейк", "Выпечка", 350.0)
    menu.add_item("Эспрессо", "Напитки", 180.0, is_available=False)  # недоступен

    # Тест: get_available не возвращает недоступные позиции
    available = menu.get_available()
    assert len(available) == 4, f"Ожидали 4, получили {len(available)}"
    assert all(item["is_available"] for item in available)
    print("  ✅ Тест: get_available() не возвращает недоступные: PASSED")

    # Тест: фильтрация по категории
    drinks = menu.filter_by_category("Напитки")
    assert len(drinks) == 2, f"Ожидали 2 напитка, получили {len(drinks)}"
    print("  ✅ Тест: filter_by_category('Напитки') = 2 позиции: PASSED")

    # Тест: cheapest не включает недоступные
    cheapest = menu.get_cheapest(2)
    names = [item["name"] for item in cheapest]
    assert "Эспрессо" not in names, "Недоступный Эспрессо не должен попасть в cheapest!"
    print("  ✅ Тест: get_cheapest() не включает недоступные: PASSED")

    print()
    print("  КЛЮЧЕВЫЕ ПРИЗНАКИ component-теста:")
    print("  - Тестирует взаимодействие нескольких методов/классов")
    print("  - Ещё нет реальных внешних зависимостей (БД, API)")
    print("  - Быстрый, но чуть сложнее unit-теста")
    print("  - При падении нужно чуть больше разбираться, что сломалось")


# ============================================================
# 3. INTEGRATION-тест — реальные внешние зависимости
# ============================================================


def demo_integration_test_stub() -> None:
    """Демонстрация концепции integration-теста (заглушка без БД)."""
    print("\n" + "=" * 60)
    print("3. INTEGRATION-ТЕСТ (концепция)")
    print("=" * 60)
    print("  Integration-тест проверяет, что компоненты работают ВМЕСТЕ")
    print("  с реальными внешними зависимостями: БД, файловой системой,")
    print("  внешним API.")
    print()
    print("  Пример (требует Django + pytest-django):")
    print(
        """
  @pytest.mark.django_db
  def test_create_menu_item_in_db():
      # Реальная БД (тестовая SQLite)
      category = Category.objects.create(name="Напитки")
      item = MenuItem.objects.create(
          name="Капучино",
          category=category,
          price=Decimal("250.00"),
      )

      # Проверяем, что объект реально сохранился в БД
      found = MenuItem.objects.get(pk=item.pk)
      assert found.name == "Капучино"
      assert found.price == Decimal("250.00")
  """
    )
    print("  КЛЮЧЕВЫЕ ПРИЗНАКИ integration-теста:")
    print("  - Использует реальную (тестовую) БД или другой сервис")
    print("  - Медленнее unit-теста (поднимает реальные зависимости)")
    print("  - Проверяет, что 'стыки' между компонентами работают")
    print("  - В Django: помечается @pytest.mark.django_db")


# ============================================================
# 4. E2E-тест — конец-в-конец через браузер или HTTP
# ============================================================


def demo_e2e_test_stub() -> None:
    """Демонстрация концепции E2E-теста (заглушка)."""
    print("\n" + "=" * 60)
    print("4. E2E-ТЕСТ (End-to-End, концепция)")
    print("=" * 60)
    print("  E2E тестирует ВЕСЬ путь: браузер → HTTP → Django view → БД → ответ.")
    print("  Инструменты: Selenium, Playwright, httpx TestClient.")
    print()
    print("  Пример (Django test client — простой E2E):")
    print(
        """
  from django.test import Client

  def test_menu_page_shows_available_items():
      client = Client()

      # Реальный HTTP GET-запрос к приложению
      response = client.get("/menu/")

      # Проверяем ответ целиком
      assert response.status_code == 200
      assert "Капучино" in response.content.decode()
      assert "Недоступный товар" not in response.content.decode()
  """
    )
    print("  КЛЮЧЕВЫЕ ПРИЗНАКИ E2E-теста:")
    print("  - Тестирует систему «снаружи», как настоящий пользователь")
    print("  - Самый медленный вид тестов")
    print("  - Самый хрупкий (зависит от UI, URL-маршрутов)")
    print("  - Тестирует наиболее критичные user journey")


# ============================================================
# Таблица сравнения всех видов тестов
# ============================================================


def print_comparison_table() -> None:
    """Вывести сравнительную таблицу видов тестов."""
    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ ВИДОВ ТЕСТОВ")
    print("=" * 60)
    print(f"  {'Вид':<15} {'Скорость':<12} {'Зависимости':<20} {'Что тестирует'}")
    print("  " + "-" * 62)

    rows = [
        ("Unit", "⚡ ~1 мс", "нет", "одна функция/метод"),
        ("Component", "⚡ ~5 мс", "нет (in-memory)", "подсистема (класс)"),
        ("Integration", "🐢 ~100 мс", "реальная БД/API", "стыки компонентов"),
        ("E2E", "🐢🐢 ~1 с", "всё приложение", "пользовательский сценарий"),
    ]
    for kind, speed, deps, what in rows:
        print(f"  {kind:<15} {speed:<12} {deps:<20} {what}")

    print()
    print("  ЗОЛОТАЯ ПИРАМИДА ТЕСТИРОВАНИЯ:")
    print("           /\\")
    print("          /E2E\\      ← мало, но обязательно")
    print("         /------\\")
    print("        /Integr. \\   ← умеренно")
    print("       /----------\\")
    print("      / Unit/Comp. \\ ← большинство тестов")
    print("     /______________\\")


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций видов тестов."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 8: ВИДЫ ТЕСТОВ")
    print("=" * 60)

    demo_unit_test()
    demo_component_test()
    demo_integration_test_stub()
    demo_e2e_test_stub()
    print_comparison_table()

    print("\n" + "=" * 60)
    print("Итог: выбирайте вид теста под задачу.")
    print("  Unit → самый быстрый, пишите их много.")
    print("  Integration → для критичных стыков с БД.")
    print("  E2E → для ключевых сценариев пользователя.")
    print("=" * 60)


if __name__ == "__main__":
    main()
