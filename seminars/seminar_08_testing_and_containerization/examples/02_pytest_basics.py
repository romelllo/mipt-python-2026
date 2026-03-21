"""
Семинар 8: pytest — основы.

Демонстрация pytest без Django:
- Простые тест-функции (не TestCase)
- pytest.mark.parametrize — множество случаев одним тестом
- pytest.raises — проверка исключений
- Чёткий вывод при падении теста

Запуск (из корня репозитория):
    pytest seminars/seminar_08_testing_and_containerization/examples/02_pytest_basics.py -v

Или напрямую (демонстрационный режим):
    python seminars/seminar_08_testing_and_containerization/examples/02_pytest_basics.py
"""

import sys
from decimal import Decimal, InvalidOperation

# ============================================================
# Тестируемая функция — calculate_order_total
# ============================================================


def calculate_order_total(items: list[dict]) -> Decimal:
    """Подсчитать итоговую сумму заказа.

    Args:
        items: список позиций, каждая с ключами 'price' и 'quantity'

    Returns:
        Итоговая сумма заказа в виде Decimal

    Raises:
        ValueError: если price или quantity некорректны
        InvalidOperation: если price нельзя преобразовать в Decimal
    """
    if not isinstance(items, list):
        raise ValueError("items должен быть списком")

    total = Decimal("0")
    for item in items:
        if "price" not in item or "quantity" not in item:
            raise ValueError("Каждая позиция должна содержать 'price' и 'quantity'")
        price = Decimal(str(item["price"]))  # может поднять InvalidOperation
        quantity = int(item["quantity"])
        if quantity < 0:
            raise ValueError(f"Количество не может быть отрицательным: {quantity}")
        total += price * quantity
    return total


# ============================================================
# 1. Простые тест-функции pytest
# ============================================================
# В pytest нет необходимости в классах TestCase.
# Достаточно функции с именем, начинающимся на test_.


def test_empty_order_returns_zero() -> None:
    """Пустой список позиций → итоговая сумма 0."""
    assert calculate_order_total([]) == Decimal("0")


def test_single_item() -> None:
    """Одна позиция → price * quantity."""
    items = [{"price": "250.00", "quantity": 2}]
    assert calculate_order_total(items) == Decimal("500.00")


def test_multiple_items() -> None:
    """Несколько позиций — суммируем корректно."""
    items = [
        {"price": "250.00", "quantity": 2},  # 500
        {"price": "180.00", "quantity": 1},  # 180
        {"price": "350.00", "quantity": 3},  # 1050
    ]
    assert calculate_order_total(items) == Decimal("1730.00")


def test_zero_quantity_item() -> None:
    """Позиция с нулевым quantity не влияет на сумму."""
    items = [
        {"price": "500.00", "quantity": 0},
        {"price": "200.00", "quantity": 1},
    ]
    assert calculate_order_total(items) == Decimal("200.00")


# ============================================================
# 2. pytest.mark.parametrize — несколько случаев одним тестом
# ============================================================
# Вместо написания отдельного теста для каждого случая —
# передаём список пар (ввод, ожидаемый результат).

import pytest  # noqa: E402 — импорт после блока демонстрации


@pytest.mark.parametrize(
    "items, expected",
    [
        # (ввод, ожидаемый результат)
        ([], Decimal("0")),
        ([{"price": "100", "quantity": 1}], Decimal("100")),
        ([{"price": "100", "quantity": 3}], Decimal("300")),
        (
            [{"price": "250", "quantity": 2}, {"price": "180", "quantity": 1}],
            Decimal("680"),
        ),
        # Дробные цены — важно проверить корректность Decimal
        ([{"price": "99.99", "quantity": 2}], Decimal("199.98")),
    ],
)
def test_calculate_order_total_parametrized(
    items: list[dict], expected: Decimal
) -> None:
    """Параметризованный тест для разных комбинаций заказов."""
    result = calculate_order_total(items)
    assert result == expected, f"Ожидали {expected}, получили {result}"


# ============================================================
# 3. pytest.raises — проверяем, что функция поднимает исключение
# ============================================================


def test_raises_on_negative_quantity() -> None:
    """Отрицательное количество должно поднять ValueError."""
    items = [{"price": "250", "quantity": -1}]
    with pytest.raises(ValueError, match="отрицательным"):
        calculate_order_total(items)


def test_raises_on_missing_keys() -> None:
    """Позиция без ключа 'price' должна поднять ValueError."""
    items = [{"quantity": 2}]  # нет ключа 'price'
    with pytest.raises(ValueError, match="price"):
        calculate_order_total(items)


def test_raises_on_invalid_price() -> None:
    """Нечисловая цена должна поднять InvalidOperation."""
    items = [{"price": "не_число", "quantity": 1}]
    with pytest.raises(InvalidOperation):
        calculate_order_total(items)


def test_raises_on_non_list_input() -> None:
    """Передача не-списка должна поднять ValueError."""
    with pytest.raises(ValueError):
        calculate_order_total("не список")  # type: ignore[arg-type]


# ============================================================
# 4. Именование тестов и структура assert
# ============================================================
# Хорошие имена тестов — как документация:
#   test_<что_тестируем>_<условие>_<ожидаемый_результат>
#
# При провале pytest показывает:
#   - имя теста (поэтому имя должно быть понятным)
#   - строку с assert
#   - значения обеих сторон выражения


def test_total_is_decimal_not_float() -> None:
    """Результат должен быть Decimal, а не float — важно для финансов."""
    items = [{"price": "250.00", "quantity": 1}]
    result = calculate_order_total(items)
    assert isinstance(result, Decimal), "Для финансовых расчётов используем Decimal!"


# ============================================================
# Демонстрационный запуск (не pytest, а прямой запуск скрипта)
# ============================================================


def main() -> None:
    """Демонстрационный запуск тестов вручную (без pytest)."""
    print("=" * 60)
    print("СЕМИНАР 8: PYTEST — ОСНОВЫ")
    print("Демонстрационный режим (запуск через Python, не pytest)")
    print("=" * 60)
    print()
    print("Для запуска через pytest используйте:")
    print(
        "  pytest seminars/seminar_08_testing_and_containerization/examples/02_pytest_basics.py -v"
    )
    print()

    # Ручной запуск тестов для демонстрации
    tests = [
        ("test_empty_order_returns_zero", test_empty_order_returns_zero),
        ("test_single_item", test_single_item),
        ("test_multiple_items", test_multiple_items),
        ("test_zero_quantity_item", test_zero_quantity_item),
        ("test_total_is_decimal_not_float", test_total_is_decimal_not_float),
    ]

    passed = 0
    failed = 0
    for name, func in tests:
        try:
            func()
            print(f"  ✅ {name}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ {name}: неожиданная ошибка — {e}")
            failed += 1

    print()
    print(f"  Результат: {passed} passed, {failed} failed")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
