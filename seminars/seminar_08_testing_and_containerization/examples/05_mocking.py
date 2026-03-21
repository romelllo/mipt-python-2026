"""
Семинар 8: Mocking — имитация внешних зависимостей.

Демонстрирует:
- unittest.mock.patch как декоратор — патчить функцию на время теста
- unittest.mock.patch как контекстный менеджер (with patch(...))
- MagicMock — создание объекта-заглушки с произвольными атрибутами
- Зачем нужно мокирование: изоляция, скорость, надёжность тестов

Запуск:
    pytest seminars/seminar_08_testing_and_containerization/examples/05_mocking.py -v

Или напрямую:
    python seminars/seminar_08_testing_and_containerization/examples/05_mocking.py
"""

import sys
from decimal import Decimal
from unittest.mock import MagicMock, call, patch

# ============================================================
# Модуль с реальными функциями (которые мы будем мокировать)
# ============================================================


def get_exchange_rate(currency: str) -> float:
    """Получить курс валюты от внешнего API.

    В реальном коде делает HTTP-запрос к сервису обменных курсов.
    В тестах мы НЕ хотим реальных сетевых запросов:
    - тест замедляется
    - зависит от внешнего сервиса (может быть недоступен)
    - курс меняется → тест нестабилен

    Args:
        currency: код валюты ('USD', 'EUR', ...)

    Returns:
        Курс в рублях
    """
    # Имитация HTTP-запроса (в реальности здесь был бы requests.get)
    raise ConnectionError(
        "Нет подключения к API обменных курсов! Используйте mock в тестах."
    )


def calculate_price_in_currency(
    price_rub: Decimal,
    currency: str,
) -> Decimal:
    """Перевести цену из рублей в другую валюту.

    Вызывает get_exchange_rate() — внешний API.
    """
    rate = get_exchange_rate(currency)  # зависимость от внешнего сервиса
    return (price_rub / Decimal(str(rate))).quantize(Decimal("0.01"))


class OrderNotifier:
    """Уведомитель о заказах (отправляет email).

    В тестах мы не хотим реально отправлять письма.
    """

    def send_confirmation(self, email: str, order_id: int) -> bool:
        """Отправить подтверждение заказа на email.

        Returns:
            True если отправка успешна
        """
        # В реальности: smtplib.sendmail(...)
        raise ConnectionError("Нет SMTP-сервера! Используйте mock в тестах.")


# ============================================================
# 1. patch как ДЕКОРАТОР — @patch(...)
# ============================================================


def demonstrate_patch_decorator() -> None:
    """Демонстрация patch как декоратора."""
    print("=" * 60)
    print("1. @patch(...) — декоратор")
    print("=" * 60)

    # Симулируем pytest-тест с @patch
    print(
        """
  Пример теста с @patch:

  @patch(
      "seminars.seminar_08_testing_and_containerization.examples.05_mocking.get_exchange_rate"
  )
  def test_calculate_price_usd(mock_get_rate):
      # mock_get_rate — это MagicMock, который заменил get_exchange_rate
      mock_get_rate.return_value = 90.0  # курс: 1 USD = 90 ₽

      # Вызываем функцию — она обращается к моку, не к реальному API
      result = calculate_price_in_currency(Decimal("900.00"), "USD")

      assert result == Decimal("10.00")           # 900 / 90 = 10 USD
      mock_get_rate.assert_called_once_with("USD")  # проверяем вызов
  """
    )

    # Демонстрируем без декоратора (через ручной вызов для наглядности).
    # ВАЖНО: путь для patch — это полный Python-путь к функции в том модуле,
    # ГДЕ она ИСПОЛЬЗУЕТСЯ (не где определена!).
    # При запуске как __main__ модуль называется __main__, поэтому:
    _target = f"{__name__}.get_exchange_rate"
    with patch(_target, return_value=90.0) as mock_rate:
        result = calculate_price_in_currency(Decimal("900.00"), "USD")
        print(f"  Результат (900 ₽ → USD при курсе 90): {result} USD")
        print(f"  Мок был вызван с аргументом: {mock_rate.call_args}")
        assert result == Decimal("10.00")
        mock_rate.assert_called_once_with("USD")
        print("  ✅ Тест прошёл: результат верный, вызов проверен")


# ============================================================
# 2. patch как КОНТЕКСТНЫЙ МЕНЕДЖЕР — with patch(...)
# ============================================================


def demonstrate_patch_context_manager() -> None:
    """Демонстрация patch как контекстного менеджера."""
    print("\n" + "=" * 60)
    print("2. with patch(...) — контекстный менеджер")
    print("=" * 60)
    print("  Полезно когда нужно переключать несколько моков в одном тесте.")

    # При запуске через pytest модуль импортируется с полным путём;
    # при прямом запуске — как __main__. Используем __name__ для универсальности.
    path = f"{__name__}.get_exchange_rate"

    # Мок для EUR
    with patch(path, return_value=100.0) as mock_eur:
        result_eur = calculate_price_in_currency(Decimal("1000.00"), "EUR")
        print(f"  1000 ₽ → EUR при курсе 100: {result_eur} EUR")
        mock_eur.assert_called_with("EUR")
        assert result_eur == Decimal("10.00")

    # Мок для USD (другой курс)
    with patch(path, return_value=90.0) as mock_usd:
        result_usd = calculate_price_in_currency(Decimal("450.00"), "USD")
        print(f"  450 ₽ → USD при курсе 90: {result_usd} USD")
        mock_usd.assert_called_with("USD")
        assert result_usd == Decimal("5.00")

    print("  ✅ Оба теста прошли!")


# ============================================================
# 3. MagicMock — создание объектов-заглушек
# ============================================================


def demonstrate_magic_mock() -> None:
    """Демонстрация MagicMock для имитации сложных объектов."""
    print("\n" + "=" * 60)
    print("3. MagicMock — имитация сложных объектов")
    print("=" * 60)

    # Создаём мок вместо реального OrderNotifier
    mock_notifier = MagicMock(spec=OrderNotifier)

    # Настраиваем поведение метода
    mock_notifier.send_confirmation.return_value = True
    print("  mock_notifier.send_confirmation.return_value = True")

    # Вызываем метод
    result = mock_notifier.send_confirmation("alice@example.com", 42)
    print(f"  Результат вызова mock: {result}")
    assert result is True

    # Проверяем, что метод был вызван с правильными аргументами
    mock_notifier.send_confirmation.assert_called_once_with("alice@example.com", 42)
    print("  ✅ Метод вызван с правильными аргументами")

    # Несколько вызовов — возвращать разные значения
    mock_notifier.send_confirmation.side_effect = [True, False, True]
    print("\n  side_effect = [True, False, True] — разные ответы:")
    for i in range(3):
        res = mock_notifier.send_confirmation(f"user{i}@test.com", i)
        print(f"    Вызов {i + 1}: {res}")

    # Подсчёт вызовов
    print(
        f"\n  Всего вызовов send_confirmation: {mock_notifier.send_confirmation.call_count}"
    )

    # История вызовов
    print("  История вызовов:")
    for c in mock_notifier.send_confirmation.call_args_list:
        print(f"    {c}")


# ============================================================
# 4. Проверка что мок НЕ был вызван
# ============================================================


def demonstrate_assert_not_called() -> None:
    """Демонстрация проверки, что функция НЕ была вызвана."""
    print("\n" + "=" * 60)
    print("4. assert_not_called — функция не должна была вызываться")
    print("=" * 60)

    mock_notifier = MagicMock(spec=OrderNotifier)

    # Сценарий: если заказ пустой — уведомление НЕ отправляется
    order_items: list = []
    if order_items:
        mock_notifier.send_confirmation("test@test.com", 1)

    mock_notifier.send_confirmation.assert_not_called()
    print("  ✅ send_confirmation не был вызван для пустого заказа")

    # Проверка call_args с именованными аргументами
    mock_fn = MagicMock()
    mock_fn(currency="USD", amount=100)
    mock_fn.assert_called_once_with(currency="USD", amount=100)
    print("  ✅ Именованные аргументы проверены через assert_called_with")

    # call — для более сложных проверок
    mock_fn2 = MagicMock()
    mock_fn2(1, "a")
    mock_fn2(2, "b")
    expected_calls = [call(1, "a"), call(2, "b")]
    mock_fn2.assert_has_calls(expected_calls)
    print("  ✅ Последовательность вызовов проверена через assert_has_calls")


# ============================================================
# 5. Почему мокирование необходимо
# ============================================================


def demonstrate_why_mocking() -> None:
    """Объяснение зачем нужно мокирование."""
    print("\n" + "=" * 60)
    print("5. ПОЧЕМУ МОКИРОВАНИЕ НЕОБХОДИМО")
    print("=" * 60)
    print(
        """
  Представьте, что ваш код вызывает:
  - внешний API (погода, валюта, SMS-сервис)
  - базу данных
  - файловую систему
  - email-сервер

  БЕЗ мокирования тесты:
  ❌ Медленные (сетевой запрос ~100мс vs unit-тест ~1мс)
  ❌ Ненадёжные (сервис может быть недоступен)
  ❌ Дорогие (платные API, SMS)
  ❌ Трудно воспроизводимые (курс валюты меняется)
  ❌ Оставляют побочные эффекты (реальные письма, записи в БД)

  С мокированием тесты:
  ✅ Быстрые (всё выполняется в памяти)
  ✅ Надёжные (нет зависимости от внешних сервисов)
  ✅ Предсказуемые (мок всегда возвращает нужное значение)
  ✅ Без побочных эффектов

  ПРАВИЛО: мокируйте на границе вашего кода с внешним миром.
  """
    )


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций мокирования."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 8: MOCKING")
    print("=" * 60)

    demonstrate_patch_decorator()
    demonstrate_patch_context_manager()
    demonstrate_magic_mock()
    demonstrate_assert_not_called()
    demonstrate_why_mocking()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("  patch()        — заменяет функцию/объект на время теста")
    print("  MagicMock      — объект-заглушка с настраиваемым поведением")
    print("  return_value   — что возвращает мок при вызове")
    print("  side_effect    — список значений или исключение")
    print("  assert_called_with — проверить аргументы вызова")
    print("=" * 60)

    sys.exit(0)


if __name__ == "__main__":
    main()
