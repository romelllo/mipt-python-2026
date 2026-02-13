"""
Поведенческие паттерны (Behavioral Patterns).

Поведенческие паттерны определяют алгоритмы и способы взаимодействия
между объектами так, чтобы они могли легко общаться,
сохраняя при этом слабую связанность.

Рассмотренные паттерны:
- Strategy (Стратегия)
- Observer (Наблюдатель)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

# =============================================================================
# Strategy (Стратегия)
# =============================================================================
# Определяет семейство алгоритмов, инкапсулирует каждый из них
# и делает их взаимозаменяемыми.
#
# Когда использовать:
# - Нужно выбирать между несколькими алгоритмами в runtime
# - Избавиться от множества if/elif/else для выбора поведения
# - Алгоритмы должны быть взаимозаменяемыми


class PaymentStrategy(ABC):
    """Абстрактная стратегия оплаты."""

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Выполняет оплату."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Проверяет валидность данных."""
        pass


class CreditCardPayment(PaymentStrategy):
    """Оплата кредитной картой."""

    def __init__(self, card_number: str, cvv: str, expiry: str) -> None:
        self.card_number = card_number
        self.cvv = cvv
        self.expiry = expiry

    def pay(self, amount: float) -> str:
        if not self.validate():
            return "Payment failed: Invalid card data"
        masked_card = f"****{self.card_number[-4:]}"
        return f"Paid {amount} RUB with Credit Card {masked_card}"

    def validate(self) -> bool:
        return len(self.card_number) == 16 and len(self.cvv) == 3


class PayPalPayment(PaymentStrategy):
    """Оплата через PayPal."""

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self._password = password

    def pay(self, amount: float) -> str:
        if not self.validate():
            return "Payment failed: Invalid PayPal credentials"
        return f"Paid {amount} RUB via PayPal ({self.email})"

    def validate(self) -> bool:
        return "@" in self.email and len(self._password) >= 8


class CryptoPayment(PaymentStrategy):
    """Оплата криптовалютой."""

    def __init__(self, wallet_address: str, currency: str = "BTC") -> None:
        self.wallet_address = wallet_address
        self.currency = currency

    def pay(self, amount: float) -> str:
        if not self.validate():
            return "Payment failed: Invalid wallet address"
        return (
            f"Paid {amount} RUB equivalent in {self.currency} "
            f"to {self.wallet_address[:10]}..."
        )

    def validate(self) -> bool:
        return len(self.wallet_address) >= 26


class ShoppingCart:
    """Корзина покупок — использует стратегию оплаты."""

    def __init__(self) -> None:
        self._items: list[tuple[str, float]] = []
        self._payment_strategy: PaymentStrategy | None = None

    def add_item(self, name: str, price: float) -> None:
        self._items.append((name, price))

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        """Стратегию можно менять в runtime!"""
        self._payment_strategy = strategy

    def get_total(self) -> float:
        return sum(price for _, price in self._items)

    def checkout(self) -> str:
        if not self._payment_strategy:
            return "Error: No payment method selected"
        if not self._items:
            return "Error: Cart is empty"
        return self._payment_strategy.pay(self.get_total())


def demo_strategy() -> None:
    """Демонстрация паттерна Strategy."""
    print("=" * 60)
    print("Strategy Pattern")
    print("=" * 60)

    # Создаём корзину и добавляем товары
    cart = ShoppingCart()
    cart.add_item("Laptop", 85000)
    cart.add_item("Mouse", 2500)
    cart.add_item("Keyboard", 5000)

    print(f"\n  Cart total: {cart.get_total()} RUB")

    # Оплата разными способами — стратегия меняется в runtime
    strategies: list[tuple[str, PaymentStrategy]] = [
        ("Credit Card", CreditCardPayment("1234567890123456", "123", "12/25")),
        ("PayPal", PayPalPayment("user@example.com", "securepassword")),
        ("Bitcoin", CryptoPayment("1A2b3C4d5E6f7G8h9I0jKlMnOpQr")),
    ]

    for name, strategy in strategies:
        cart.set_payment_strategy(strategy)
        print(f"\n  {name}:")
        print(f"    {cart.checkout()}")
    print()


# =============================================================================
# Observer (Наблюдатель)
# =============================================================================
# Определяет зависимость один-ко-многим между объектами так,
# что при изменении состояния одного объекта все зависящие от него
# объекты уведомляются и обновляются автоматически.
#
# Когда использовать:
# - Изменение одного объекта должно оповестить множество других
# - Набор «слушателей» может меняться в runtime
# - Событийная модель (publish/subscribe)


class Observer(ABC):
    """Абстрактный наблюдатель."""

    @abstractmethod
    def update(self, subject: "Subject", *args: Any, **kwargs: Any) -> None:
        """Получает уведомление от субъекта."""
        pass


class Subject:
    """Базовый субъект (издатель) — не абстрактный, готов к использованию."""

    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Подписывает наблюдателя."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Отписывает наблюдателя."""
        self._observers.remove(observer)

    def notify(self, *args: Any, **kwargs: Any) -> None:
        """Уведомляет всех наблюдателей."""
        for observer in self._observers:
            observer.update(self, *args, **kwargs)


@dataclass
class NewsAgency(Subject):
    """Новостное агентство — издатель новостей."""

    name: str
    _latest_news: str = ""

    def __post_init__(self) -> None:
        super().__init__()

    @property
    def latest_news(self) -> str:
        return self._latest_news

    def publish_news(self, news: str) -> None:
        """Публикует новость и уведомляет подписчиков."""
        print(f"\n  [{self.name}] Breaking News: {news}")
        self._latest_news = news
        self.notify(news=news)


class EmailSubscriber(Observer):
    """Подписчик по email."""

    def __init__(self, email: str) -> None:
        self.email = email

    def update(self, subject: Subject, *args: Any, **kwargs: Any) -> None:
        news = kwargs.get("news", "")
        print(f"    Email to {self.email}: {news}")


class SMSSubscriber(Observer):
    """Подписчик по SMS."""

    def __init__(self, phone: str) -> None:
        self.phone = phone

    def update(self, subject: Subject, *args: Any, **kwargs: Any) -> None:
        news = kwargs.get("news", "")
        print(f"    SMS to {self.phone}: {news[:50]}...")


class PushSubscriber(Observer):
    """Подписчик push-уведомлений."""

    def __init__(self, device_id: str) -> None:
        self.device_id = device_id

    def update(self, subject: Subject, *args: Any, **kwargs: Any) -> None:
        news = kwargs.get("news", "")
        print(f"    Push to {self.device_id}: {news}")


def demo_observer() -> None:
    """Демонстрация паттерна Observer."""
    print("=" * 60)
    print("Observer Pattern")
    print("=" * 60)

    # Создаём новостное агентство
    agency = NewsAgency(name="TechNews")

    # Создаём подписчиков
    email_sub = EmailSubscriber("user@example.com")
    sms_sub = SMSSubscriber("+7-999-123-4567")
    push_sub = PushSubscriber("device_abc123")

    # Подписываем
    agency.attach(email_sub)
    agency.attach(sms_sub)
    agency.attach(push_sub)

    # Публикуем новость — все подписчики получат уведомление
    agency.publish_news("Python 4.0 Released!")

    # Отписываем SMS
    print("\n  [Unsubscribing SMS]")
    agency.detach(sms_sub)

    # Публикуем ещё одну — SMS больше не получит
    agency.publish_news("AI achieves consciousness!")
    print()


# =============================================================================
# Main
# =============================================================================


def main() -> None:
    """Запуск всех демонстраций."""
    demo_strategy()
    demo_observer()

    print("=" * 60)
    print("Behavioral Patterns demonstrated: Strategy, Observer")
    print("=" * 60)


if __name__ == "__main__":
    main()
