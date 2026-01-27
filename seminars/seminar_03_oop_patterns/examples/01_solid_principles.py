"""
Принципы SOLID в Python.

SOLID — это пять принципов объектно-ориентированного проектирования,
которые помогают создавать гибкий, поддерживаемый и расширяемый код.

S - Single Responsibility Principle (Принцип единственной ответственности)
O - Open/Closed Principle (Принцип открытости/закрытости)
L - Liskov Substitution Principle (Принцип подстановки Барбары Лисков)
I - Interface Segregation Principle (Принцип разделения интерфейса)
D - Dependency Inversion Principle (Принцип инверсии зависимостей)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

# =============================================================================
# S - Single Responsibility Principle (Принцип единственной ответственности)
# =============================================================================
# Класс должен иметь только одну причину для изменения.


@dataclass
class User:
    """Модель пользователя — только данные."""

    name: str
    email: str


class UserRepository:
    """Отвечает только за сохранение/загрузку пользователей."""

    def __init__(self) -> None:
        self._storage: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._storage[user.email] = user
        print(f"User {user.name} saved to storage")

    def find_by_email(self, email: str) -> User | None:
        return self._storage.get(email)


class EmailService:
    """Отвечает только за отправку email."""

    def send_welcome(self, user: User) -> None:
        print(f"Sending welcome email to {user.email}")

    def send_notification(self, user: User, message: str) -> None:
        print(f"Sending to {user.email}: {message}")


class UserService:
    """Координирует работу с пользователями."""

    def __init__(self, repo: UserRepository, email_service: EmailService) -> None:
        self.repo = repo
        self.email_service = email_service

    def register(self, name: str, email: str) -> User:
        user = User(name=name, email=email)
        self.repo.save(user)
        self.email_service.send_welcome(user)
        return user


def demo_srp() -> None:
    """Демонстрация SRP."""
    print("=" * 60)
    print("Single Responsibility Principle")
    print("=" * 60)

    repo = UserRepository()
    email_service = EmailService()
    user_service = UserService(repo, email_service)

    user = user_service.register("Alice", "alice@example.com")
    print(f"Registered: {user}")
    print()


# =============================================================================
# O - Open/Closed Principle (Принцип открытости/закрытости)
# =============================================================================
# Классы должны быть открыты для расширения, но закрыты для модификации.


class Discount(ABC):
    """Базовый класс для скидок."""

    @abstractmethod
    def calculate(self, price: float) -> float:
        """Вычисляет цену после применения скидки."""
        pass

    @abstractmethod
    def description(self) -> str:
        """Описание скидки."""
        pass


class NoDiscount(Discount):
    """Без скидки."""

    def calculate(self, price: float) -> float:
        return price

    def description(self) -> str:
        return "No discount"


class PercentDiscount(Discount):
    """Процентная скидка."""

    def __init__(self, percent: float) -> None:
        self.percent = percent

    def calculate(self, price: float) -> float:
        return price * (1 - self.percent / 100)

    def description(self) -> str:
        return f"{self.percent}% discount"


class FixedDiscount(Discount):
    """Фиксированная скидка."""

    def __init__(self, amount: float) -> None:
        self.amount = amount

    def calculate(self, price: float) -> float:
        return max(0, price - self.amount)

    def description(self) -> str:
        return f"Fixed {self.amount} discount"


# Легко добавить новый тип скидки без изменения существующего кода
class BuyOneGetOneFree(Discount):
    """Скидка 'Купи один — получи второй бесплатно' (50%)."""

    def calculate(self, price: float) -> float:
        return price * 0.5

    def description(self) -> str:
        return "Buy one get one free"


class PriceCalculator:
    """Калькулятор цены — работает с любой скидкой."""

    def calculate_final_price(self, price: float, discount: Discount) -> float:
        return discount.calculate(price)


def demo_ocp() -> None:
    """Демонстрация OCP."""
    print("=" * 60)
    print("Open/Closed Principle")
    print("=" * 60)

    calculator = PriceCalculator()
    price = 1000.0

    discounts: list[Discount] = [
        NoDiscount(),
        PercentDiscount(10),
        FixedDiscount(150),
        BuyOneGetOneFree(),
    ]

    for discount in discounts:
        final_price = calculator.calculate_final_price(price, discount)
        print(f"{discount.description()}: {price} -> {final_price}")
    print()


# =============================================================================
# L - Liskov Substitution Principle (Принцип подстановки Барбары Лисков)
# =============================================================================
# Объекты подклассов должны быть взаимозаменяемы с объектами базового класса.


class Bird(ABC):
    """Базовый класс для птиц."""

    @abstractmethod
    def move(self) -> str:
        """Способ передвижения."""
        pass

    @abstractmethod
    def make_sound(self) -> str:
        """Звук, который издаёт птица."""
        pass


class FlyingBird(Bird):
    """Летающая птица."""

    def move(self) -> str:
        return "Flying in the sky"


class SwimmingBird(Bird):
    """Плавающая птица."""

    def move(self) -> str:
        return "Swimming in the water"


class Sparrow(FlyingBird):
    """Воробей."""

    def make_sound(self) -> str:
        return "Chirp chirp!"


class Eagle(FlyingBird):
    """Орёл."""

    def make_sound(self) -> str:
        return "Screech!"


class Penguin(SwimmingBird):
    """Пингвин — птица, но не летает."""

    def make_sound(self) -> str:
        return "Honk honk!"


class Duck(Bird):
    """Утка — может и летать, и плавать."""

    def move(self) -> str:
        return "Flying or swimming"

    def make_sound(self) -> str:
        return "Quack quack!"


def make_bird_move(bird: Bird) -> None:
    """Работает с любой птицей — соблюдается LSP."""
    print(f"{bird.__class__.__name__}: {bird.move()}, says '{bird.make_sound()}'")


def demo_lsp() -> None:
    """Демонстрация LSP."""
    print("=" * 60)
    print("Liskov Substitution Principle")
    print("=" * 60)

    birds: list[Bird] = [Sparrow(), Eagle(), Penguin(), Duck()]

    for bird in birds:
        make_bird_move(bird)
    print()


# =============================================================================
# I - Interface Segregation Principle (Принцип разделения интерфейса)
# =============================================================================
# Клиенты не должны зависеть от интерфейсов, которые они не используют.


class Workable(ABC):
    """Интерфейс для работы."""

    @abstractmethod
    def work(self) -> str:
        pass


class Eatable(ABC):
    """Интерфейс для еды."""

    @abstractmethod
    def eat(self) -> str:
        pass


class Sleepable(ABC):
    """Интерфейс для сна."""

    @abstractmethod
    def sleep(self) -> str:
        pass


class Human(Workable, Eatable, Sleepable):
    """Человек — может работать, есть и спать."""

    def __init__(self, name: str) -> None:
        self.name = name

    def work(self) -> str:
        return f"{self.name} is working"

    def eat(self) -> str:
        return f"{self.name} is eating"

    def sleep(self) -> str:
        return f"{self.name} is sleeping"


class Robot(Workable):
    """Робот — может только работать."""

    def __init__(self, model: str) -> None:
        self.model = model

    def work(self) -> str:
        return f"Robot {self.model} is working 24/7"


class Cat(Eatable, Sleepable):
    """Кот — может есть и спать, но не работать."""

    def __init__(self, name: str) -> None:
        self.name = name

    def eat(self) -> str:
        return f"{self.name} is eating fish"

    def sleep(self) -> str:
        return f"{self.name} is sleeping on keyboard"


def assign_work(worker: Workable) -> None:
    """Назначает работу — работает только с Workable."""
    print(worker.work())


def demo_isp() -> None:
    """Демонстрация ISP."""
    print("=" * 60)
    print("Interface Segregation Principle")
    print("=" * 60)

    human = Human("Alice")
    robot = Robot("T-800")
    cat = Cat("Whiskers")

    # Работать могут только Human и Robot
    assign_work(human)
    assign_work(robot)
    # assign_work(cat)  # TypeError — кот не может работать

    # Есть могут Human и Cat
    print(human.eat())
    print(cat.eat())
    # print(robot.eat())  # AttributeError — у робота нет метода eat

    print()


# =============================================================================
# D - Dependency Inversion Principle (Принцип инверсии зависимостей)
# =============================================================================
# Модули верхнего уровня не должны зависеть от модулей нижнего уровня.
# Оба должны зависеть от абстракций.


class Database(ABC):
    """Абстракция базы данных."""

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def execute(self, query: str) -> list[dict]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class MySQLDatabase(Database):
    """MySQL реализация."""

    def connect(self) -> None:
        print("Connecting to MySQL...")

    def execute(self, query: str) -> list[dict]:
        print(f"MySQL executing: {query}")
        return [{"id": 1, "name": "Test"}]

    def close(self) -> None:
        print("Closing MySQL connection")


class PostgreSQLDatabase(Database):
    """PostgreSQL реализация."""

    def connect(self) -> None:
        print("Connecting to PostgreSQL...")

    def execute(self, query: str) -> list[dict]:
        print(f"PostgreSQL executing: {query}")
        return [{"id": 1, "name": "Test"}]

    def close(self) -> None:
        print("Closing PostgreSQL connection")


class SQLiteDatabase(Database):
    """SQLite реализация."""

    def connect(self) -> None:
        print("Connecting to SQLite...")

    def execute(self, query: str) -> list[dict]:
        print(f"SQLite executing: {query}")
        return [{"id": 1, "name": "Test"}]

    def close(self) -> None:
        print("Closing SQLite connection")


class ProductRepository:
    """Репозиторий продуктов — зависит от абстракции Database."""

    def __init__(self, database: Database) -> None:
        self.db = database

    def get_all(self) -> list[dict]:
        self.db.connect()
        result = self.db.execute("SELECT * FROM products")
        self.db.close()
        return result


def demo_dip() -> None:
    """Демонстрация DIP."""
    print("=" * 60)
    print("Dependency Inversion Principle")
    print("=" * 60)

    # Легко переключаться между разными БД
    databases: list[Database] = [
        MySQLDatabase(),
        PostgreSQLDatabase(),
        SQLiteDatabase(),
    ]

    for db in databases:
        print(f"\nUsing {db.__class__.__name__}:")
        repo = ProductRepository(db)
        products = repo.get_all()
        print(f"Found {len(products)} products")

    print()


# =============================================================================
# Main
# =============================================================================


def main() -> None:
    """Запуск всех демонстраций."""
    demo_srp()
    demo_ocp()
    demo_lsp()
    demo_isp()
    demo_dip()

    print("=" * 60)
    print("All SOLID principles demonstrated!")
    print("=" * 60)


if __name__ == "__main__":
    main()
