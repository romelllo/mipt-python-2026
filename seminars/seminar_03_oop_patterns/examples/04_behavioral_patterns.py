"""
Поведенческие паттерны (Behavioral Patterns).

Поведенческие паттерны определяют алгоритмы и способы взаимодействия
между объектами так, чтобы они могли легко общаться,
сохраняя при этом слабую связанность.

Рассмотренные паттерны:
- Observer (Наблюдатель)
- Strategy (Стратегия)
- Command (Команда)
- State (Состояние)
- Template Method (Шаблонный метод)
- Iterator (Итератор)
"""

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

# =============================================================================
# Observer (Наблюдатель)
# =============================================================================
# Определяет зависимость один-ко-многим между объектами так,
# что при изменении состояния одного объекта все зависящие от него
# объекты уведомляются и обновляются автоматически.


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
        print(f"    📧 Email to {self.email}: {news}")


class SMSSubscriber(Observer):
    """Подписчик по SMS."""

    def __init__(self, phone: str) -> None:
        self.phone = phone

    def update(self, subject: Subject, *args: Any, **kwargs: Any) -> None:
        news = kwargs.get("news", "")
        print(f"    📱 SMS to {self.phone}: {news[:50]}...")


class PushSubscriber(Observer):
    """Подписчик push-уведомлений."""

    def __init__(self, device_id: str) -> None:
        self.device_id = device_id

    def update(self, subject: Subject, *args: Any, **kwargs: Any) -> None:
        news = kwargs.get("news", "")
        print(f"    🔔 Push to {self.device_id}: {news}")


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

    # Публикуем новость
    agency.publish_news("Python 4.0 Released!")

    # Отписываем SMS
    print("\n  [Unsubscribing SMS]")
    agency.detach(sms_sub)

    # Публикуем ещё одну новость
    agency.publish_news("AI achieves consciousness!")
    print()


# =============================================================================
# Strategy (Стратегия)
# =============================================================================
# Определяет семейство алгоритмов, инкапсулирует каждый из них
# и делает их взаимозаменяемыми.


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
        return f"Paid {amount} RUB equivalent in {self.currency} to {self.wallet_address[:10]}..."

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

    # Оплата разными способами
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
# Command (Команда)
# =============================================================================
# Инкапсулирует запрос как объект, позволяя параметризовать клиентов
# с различными запросами, ставить запросы в очередь и поддерживать
# отмену операций.


class Command(ABC):
    """Абстрактная команда."""

    @abstractmethod
    def execute(self) -> str:
        """Выполняет команду."""
        pass

    @abstractmethod
    def undo(self) -> str:
        """Отменяет команду."""
        pass


class TextEditor:
    """Текстовый редактор — получатель команд."""

    def __init__(self) -> None:
        self._text = ""

    @property
    def text(self) -> str:
        return self._text

    def insert(self, text: str, position: int) -> None:
        self._text = self._text[:position] + text + self._text[position:]

    def delete(self, start: int, end: int) -> str:
        deleted = self._text[start:end]
        self._text = self._text[:start] + self._text[end:]
        return deleted


class InsertCommand(Command):
    """Команда вставки текста."""

    def __init__(self, editor: TextEditor, text: str, position: int) -> None:
        self._editor = editor
        self._text = text
        self._position = position

    def execute(self) -> str:
        self._editor.insert(self._text, self._position)
        return f"Inserted '{self._text}' at position {self._position}"

    def undo(self) -> str:
        end_pos = self._position + len(self._text)
        self._editor.delete(self._position, end_pos)
        return f"Undid insert of '{self._text}'"


class DeleteCommand(Command):
    """Команда удаления текста."""

    def __init__(self, editor: TextEditor, start: int, end: int) -> None:
        self._editor = editor
        self._start = start
        self._end = end
        self._deleted_text = ""

    def execute(self) -> str:
        self._deleted_text = self._editor.delete(self._start, self._end)
        return f"Deleted '{self._deleted_text}'"

    def undo(self) -> str:
        self._editor.insert(self._deleted_text, self._start)
        return f"Undid delete, restored '{self._deleted_text}'"


class CommandHistory:
    """История команд — поддерживает undo/redo."""

    def __init__(self) -> None:
        self._history: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: Command) -> str:
        result = command.execute()
        self._history.append(command)
        self._redo_stack.clear()  # Очищаем redo при новой команде
        return result

    def undo(self) -> str:
        if not self._history:
            return "Nothing to undo"
        command = self._history.pop()
        self._redo_stack.append(command)
        return command.undo()

    def redo(self) -> str:
        if not self._redo_stack:
            return "Nothing to redo"
        command = self._redo_stack.pop()
        self._history.append(command)
        return command.execute()


def demo_command() -> None:
    """Демонстрация паттерна Command."""
    print("=" * 60)
    print("Command Pattern")
    print("=" * 60)

    editor = TextEditor()
    history = CommandHistory()

    print("\n  Text Editor with Undo/Redo:")

    # Выполняем команды
    print(f"    {history.execute(InsertCommand(editor, 'Hello', 0))}")
    print(f"    Current text: '{editor.text}'")

    print(f"    {history.execute(InsertCommand(editor, ' World', 5))}")
    print(f"    Current text: '{editor.text}'")

    print(f"    {history.execute(InsertCommand(editor, '!', 11))}")
    print(f"    Current text: '{editor.text}'")

    # Undo
    print(f"\n    {history.undo()}")
    print(f"    Current text: '{editor.text}'")

    print(f"    {history.undo()}")
    print(f"    Current text: '{editor.text}'")

    # Redo
    print(f"\n    {history.redo()}")
    print(f"    Current text: '{editor.text}'")

    # Новая команда после undo (очищает redo)
    print(f"\n    {history.execute(InsertCommand(editor, ' Python', 5))}")
    print(f"    Current text: '{editor.text}'")

    print(f"    {history.redo()}")  # Ничего не сделает
    print()


# =============================================================================
# State (Состояние)
# =============================================================================
# Позволяет объекту изменять своё поведение в зависимости
# от внутреннего состояния.


class DocumentState(ABC):
    """Абстрактное состояние документа."""

    @abstractmethod
    def publish(self, doc: "Document") -> str:
        pass

    @abstractmethod
    def edit(self, doc: "Document", content: str) -> str:
        pass

    @abstractmethod
    def reject(self, doc: "Document") -> str:
        pass


class DraftState(DocumentState):
    """Состояние 'Черновик'."""

    def publish(self, doc: "Document") -> str:
        doc.set_state(ModerationState())
        return "Document sent for moderation"

    def edit(self, doc: "Document", content: str) -> str:
        doc.content = content
        return f"Draft edited: '{content[:30]}...'"

    def reject(self, doc: "Document") -> str:
        return "Cannot reject a draft"


class ModerationState(DocumentState):
    """Состояние 'На модерации'."""

    def publish(self, doc: "Document") -> str:
        doc.set_state(PublishedState())
        return "Document approved and published!"

    def edit(self, doc: "Document", content: str) -> str:
        return "Cannot edit during moderation"

    def reject(self, doc: "Document") -> str:
        doc.set_state(DraftState())
        return "Document rejected, returned to draft"


class PublishedState(DocumentState):
    """Состояние 'Опубликован'."""

    def publish(self, doc: "Document") -> str:
        return "Document is already published"

    def edit(self, doc: "Document", content: str) -> str:
        doc.content = content
        doc.set_state(DraftState())
        return "Document edited, moved back to draft"

    def reject(self, doc: "Document") -> str:
        return "Cannot reject a published document"


class Document:
    """Документ — контекст, состояние которого меняется."""

    def __init__(self, title: str, content: str = "") -> None:
        self.title = title
        self.content = content
        self._state: DocumentState = DraftState()

    def set_state(self, state: DocumentState) -> None:
        self._state = state

    def get_state_name(self) -> str:
        return self._state.__class__.__name__.replace("State", "")

    def publish(self) -> str:
        return self._state.publish(self)

    def edit(self, content: str) -> str:
        return self._state.edit(self, content)

    def reject(self) -> str:
        return self._state.reject(self)


def demo_state() -> None:
    """Демонстрация паттерна State."""
    print("=" * 60)
    print("State Pattern")
    print("=" * 60)

    doc = Document("My Article", "Initial content")

    print(f"\n  Document: '{doc.title}'")
    print(f"    State: {doc.get_state_name()}")

    # Редактируем черновик
    print(f"    {doc.edit('Updated draft content')}")
    print(f"    State: {doc.get_state_name()}")

    # Отправляем на модерацию
    print(f"    {doc.publish()}")
    print(f"    State: {doc.get_state_name()}")

    # Пытаемся редактировать на модерации
    print(f"    {doc.edit('Try to edit')}")

    # Отклоняем
    print(f"    {doc.reject()}")
    print(f"    State: {doc.get_state_name()}")

    # Снова отправляем и публикуем
    print(f"    {doc.publish()}")
    print(f"    {doc.publish()}")
    print(f"    State: {doc.get_state_name()}")
    print()


# =============================================================================
# Template Method (Шаблонный метод)
# =============================================================================
# Определяет скелет алгоритма в базовом классе,
# позволяя подклассам переопределять отдельные шаги.


class DataMiner(ABC):
    """Абстрактный майнер данных — шаблонный метод."""

    def mine(self, path: str) -> dict[str, Any]:
        """
        Шаблонный метод — определяет алгоритм.

        Подклассы могут переопределять отдельные шаги.
        """
        raw_data = self.extract(path)
        parsed_data = self.parse(raw_data)
        analyzed_data = self.analyze(parsed_data)
        report = self.create_report(analyzed_data)
        return report

    @abstractmethod
    def extract(self, path: str) -> str:
        """Извлечение данных — абстрактный метод."""
        pass

    @abstractmethod
    def parse(self, data: str) -> list[dict[str, Any]]:
        """Парсинг данных — абстрактный метод."""
        pass

    def analyze(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        """Анализ данных — хук, может быть переопределён."""
        return {"records_count": len(data), "data": data}

    def create_report(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Создание отчёта — хук."""
        return {"status": "success", "analysis": analysis}


class CSVDataMiner(DataMiner):
    """Майнер CSV файлов."""

    def extract(self, path: str) -> str:
        print(f"    Extracting CSV from {path}")
        return "name,age\nAlice,30\nBob,25"

    def parse(self, data: str) -> list[dict[str, Any]]:
        print("    Parsing CSV data")
        lines = data.strip().split("\n")
        headers = lines[0].split(",")
        return [dict(zip(headers, line.split(","), strict=False)) for line in lines[1:]]


class JSONDataMiner(DataMiner):
    """Майнер JSON файлов."""

    def extract(self, path: str) -> str:
        print(f"    Extracting JSON from {path}")
        return '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]'

    def parse(self, data: str) -> list[dict[str, Any]]:
        print("    Parsing JSON data")
        # Простой парсинг (в реальности использовался бы json.loads)
        return [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]

    def analyze(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        """Переопределённый анализ с дополнительной статистикой."""
        base = super().analyze(data)
        ages = [int(record.get("age", 0)) for record in data]
        base["average_age"] = sum(ages) / len(ages) if ages else 0
        return base


def demo_template_method() -> None:
    """Демонстрация паттерна Template Method."""
    print("=" * 60)
    print("Template Method Pattern")
    print("=" * 60)

    print("\n  CSV Data Mining:")
    csv_miner = CSVDataMiner()
    csv_result = csv_miner.mine("data.csv")
    print(f"    Result: {csv_result}")

    print("\n  JSON Data Mining:")
    json_miner = JSONDataMiner()
    json_result = json_miner.mine("data.json")
    print(f"    Result: {json_result}")
    print()


# =============================================================================
# Iterator (Итератор)
# =============================================================================
# Предоставляет способ последовательного доступа к элементам
# составного объекта без раскрытия его внутреннего представления.


@dataclass
class Book:
    """Книга."""

    title: str
    author: str
    year: int


class BookCollection:
    """Коллекция книг с пользовательским итератором."""

    def __init__(self) -> None:
        self._books: list[Book] = []

    def add(self, book: Book) -> None:
        self._books.append(book)

    def __len__(self) -> int:
        return len(self._books)

    def __iter__(self) -> "BookIterator":
        """Возвращает итератор для прямого обхода."""
        return BookIterator(self._books)

    def reverse_iterator(self) -> "ReverseBookIterator":
        """Возвращает итератор для обратного обхода."""
        return ReverseBookIterator(self._books)

    def filter_by_author(self, author: str) -> "FilteredBookIterator":
        """Возвращает фильтрующий итератор."""
        return FilteredBookIterator(self._books, lambda b: b.author == author)


class BookIterator(Iterator[Book]):
    """Прямой итератор по книгам."""

    def __init__(self, books: list[Book]) -> None:
        self._books = books
        self._index = 0

    def __next__(self) -> Book:
        if self._index >= len(self._books):
            raise StopIteration
        book = self._books[self._index]
        self._index += 1
        return book

    def __iter__(self) -> "BookIterator":
        return self


class ReverseBookIterator(Iterator[Book]):
    """Обратный итератор по книгам."""

    def __init__(self, books: list[Book]) -> None:
        self._books = books
        self._index = len(books) - 1

    def __next__(self) -> Book:
        if self._index < 0:
            raise StopIteration
        book = self._books[self._index]
        self._index -= 1
        return book

    def __iter__(self) -> "ReverseBookIterator":
        return self


class FilteredBookIterator(Iterator[Book]):
    """Фильтрующий итератор по книгам."""

    def __init__(self, books: list[Book], predicate: Callable[[Book], bool]) -> None:
        self._books = books
        self._predicate = predicate
        self._index = 0

    def __next__(self) -> Book:
        while self._index < len(self._books):
            book = self._books[self._index]
            self._index += 1
            if self._predicate(book):
                return book
        raise StopIteration

    def __iter__(self) -> "FilteredBookIterator":
        return self


def demo_iterator() -> None:
    """Демонстрация паттерна Iterator."""
    print("=" * 60)
    print("Iterator Pattern")
    print("=" * 60)

    # Создаём коллекцию книг
    library = BookCollection()
    library.add(Book("Clean Code", "Robert Martin", 2008))
    library.add(Book("Design Patterns", "Gang of Four", 1994))
    library.add(Book("Refactoring", "Martin Fowler", 1999))
    library.add(Book("The Pragmatic Programmer", "David Thomas", 1999))
    library.add(Book("Clean Architecture", "Robert Martin", 2017))

    # Прямой обход
    print("\n  Forward iteration:")
    for book in library:
        print(f"    {book.title} by {book.author} ({book.year})")

    # Обратный обход
    print("\n  Reverse iteration:")
    for book in library.reverse_iterator():
        print(f"    {book.title} by {book.author}")

    # Фильтрация
    print("\n  Books by Robert Martin:")
    for book in library.filter_by_author("Robert Martin"):
        print(f"    {book.title} ({book.year})")
    print()


# =============================================================================
# Main
# =============================================================================


def main() -> None:
    """Запуск всех демонстраций."""
    demo_observer()
    demo_strategy()
    demo_command()
    demo_state()
    demo_template_method()
    demo_iterator()

    print("=" * 60)
    print("All Behavioral Patterns demonstrated!")
    print("=" * 60)


if __name__ == "__main__":
    main()
