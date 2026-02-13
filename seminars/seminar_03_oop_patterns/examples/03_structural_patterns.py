"""
Структурные паттерны (Structural Patterns).

Структурные паттерны описывают способы компоновки классов и объектов
в более крупные структуры, сохраняя при этом гибкость и эффективность.

Рассмотренные паттерны:
- Adapter (Адаптер)
- Decorator (Декоратор)
"""

from abc import ABC, abstractmethod
from typing import Any

# =============================================================================
# Adapter (Адаптер)
# =============================================================================
# Позволяет объектам с несовместимыми интерфейсами работать вместе.
#
# Когда использовать:
# - Интеграция с legacy-кодом или внешними библиотеками
# - Интерфейс существующего класса не подходит к вашему коду
# - Нужно «перевести» один формат данных в другой


# Старая система платежей (legacy)
class OldPaymentSystem:
    """Старая система платежей — работает с копейками."""

    def make_payment(self, amount_kopecks: int) -> dict[str, Any]:
        return {
            "status": "success",
            "amount_kopecks": amount_kopecks,
            "message": f"Payment of {amount_kopecks} kopecks processed",
        }

    def refund_payment(
        self, transaction_id: str, amount_kopecks: int
    ) -> dict[str, Any]:
        return {
            "status": "refunded",
            "transaction_id": transaction_id,
            "amount_kopecks": amount_kopecks,
        }


# Новый интерфейс платежей
class PaymentProcessor(ABC):
    """Новый интерфейс платежей — работает с рублями."""

    @abstractmethod
    def pay(self, amount_rubles: float) -> str:
        """Выполняет платёж."""
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount_rubles: float) -> str:
        """Выполняет возврат."""
        pass


# Адаптер
class PaymentAdapter(PaymentProcessor):
    """
    Адаптер — преобразует интерфейс старой системы в новый.

    Конвертирует рубли в копейки и обратно.
    """

    def __init__(self, old_system: OldPaymentSystem) -> None:
        self._old_system = old_system

    def pay(self, amount_rubles: float) -> str:
        amount_kopecks = int(amount_rubles * 100)
        result = self._old_system.make_payment(amount_kopecks)
        return f"Paid {amount_rubles} RUB: {result['message']}"

    def refund(self, transaction_id: str, amount_rubles: float) -> str:
        amount_kopecks = int(amount_rubles * 100)
        self._old_system.refund_payment(transaction_id, amount_kopecks)
        return f"Refunded {amount_rubles} RUB for transaction {transaction_id}"


def demo_adapter() -> None:
    """Демонстрация паттерна Adapter."""
    print("=" * 60)
    print("Adapter Pattern")
    print("=" * 60)

    old_system = OldPaymentSystem()
    adapter = PaymentAdapter(old_system)

    print("\nPayment Adapter:")
    print(f"  {adapter.pay(1500.50)}")
    print(f"  {adapter.refund('TXN-123', 500.00)}")
    print()


# =============================================================================
# Decorator (Декоратор)
# =============================================================================
# Позволяет динамически добавлять объектам новую функциональность,
# оборачивая их в полезные обёртки.
#
# Когда использовать:
# - Нужно добавлять функциональность без изменения исходного класса
# - Комбинации добавок произвольные (молоко + сахар, только молоко, и т.д.)
# - Нужна гибкость, которую не даёт наследование


class Coffee(ABC):
    """Абстрактный кофе."""

    @abstractmethod
    def cost(self) -> float:
        """Стоимость."""
        pass

    @abstractmethod
    def description(self) -> str:
        """Описание."""
        pass


class SimpleCoffee(Coffee):
    """Простой кофе."""

    def cost(self) -> float:
        return 100.0

    def description(self) -> str:
        return "Simple Coffee"


class CoffeeDecorator(Coffee):
    """Базовый декоратор кофе — делегирует всё обёрнутому объекту."""

    def __init__(self, coffee: Coffee) -> None:
        self._coffee = coffee

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()


class MilkDecorator(CoffeeDecorator):
    """Добавляет молоко."""

    def cost(self) -> float:
        return self._coffee.cost() + 30.0

    def description(self) -> str:
        return f"{self._coffee.description()} + Milk"


class SugarDecorator(CoffeeDecorator):
    """Добавляет сахар."""

    def cost(self) -> float:
        return self._coffee.cost() + 10.0

    def description(self) -> str:
        return f"{self._coffee.description()} + Sugar"


class WhippedCreamDecorator(CoffeeDecorator):
    """Добавляет взбитые сливки."""

    def cost(self) -> float:
        return self._coffee.cost() + 50.0

    def description(self) -> str:
        return f"{self._coffee.description()} + Whipped Cream"


class VanillaDecorator(CoffeeDecorator):
    """Добавляет ваниль."""

    def cost(self) -> float:
        return self._coffee.cost() + 40.0

    def description(self) -> str:
        return f"{self._coffee.description()} + Vanilla"


def demo_decorator() -> None:
    """Демонстрация паттерна Decorator."""
    print("=" * 60)
    print("Decorator Pattern")
    print("=" * 60)

    # Простой кофе
    print("\nCoffee Decorators:")
    coffee: Coffee = SimpleCoffee()
    print(f"  {coffee.description()}: {coffee.cost()} RUB")

    # Кофе с молоком
    coffee_with_milk: Coffee = MilkDecorator(SimpleCoffee())
    print(f"  {coffee_with_milk.description()}: {coffee_with_milk.cost()} RUB")

    # Кофе с молоком, сахаром и сливками — декораторы комбинируются!
    fancy_coffee: Coffee = WhippedCreamDecorator(
        SugarDecorator(MilkDecorator(SimpleCoffee()))
    )
    print(f"  {fancy_coffee.description()}: {fancy_coffee.cost()} RUB")

    # Супер-кофе со всеми добавками
    super_coffee: Coffee = VanillaDecorator(
        WhippedCreamDecorator(SugarDecorator(MilkDecorator(SimpleCoffee())))
    )
    print(f"  {super_coffee.description()}: {super_coffee.cost()} RUB")
    print()


# =============================================================================
# Main
# =============================================================================


def main() -> None:
    """Запуск всех демонстраций."""
    demo_adapter()
    demo_decorator()

    print("=" * 60)
    print("Structural Patterns demonstrated: Adapter, Decorator")
    print("=" * 60)


if __name__ == "__main__":
    main()
