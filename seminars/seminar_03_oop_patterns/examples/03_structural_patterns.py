"""
Структурные паттерны (Structural Patterns).

Структурные паттерны описывают способы компоновки классов и объектов
в более крупные структуры, сохраняя при этом гибкость и эффективность.

Рассмотренные паттерны:
- Adapter (Адаптер)
- Decorator (Декоратор)
- Facade (Фасад)
- Composite (Компоновщик)
- Proxy (Заместитель)
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from time import sleep, time
from typing import Any

# =============================================================================
# Adapter (Адаптер)
# =============================================================================
# Позволяет объектам с несовместимыми интерфейсами работать вместе.


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


# Ещё один пример: адаптер для разных форматов данных
class XMLDataProvider:
    """Провайдер данных в XML формате."""

    def get_data_xml(self) -> str:
        return "<users><user><name>Alice</name><age>30</age></user></users>"


class JSONDataAdapter:
    """Адаптер XML -> JSON."""

    def __init__(self, xml_provider: XMLDataProvider) -> None:
        self._xml_provider = xml_provider

    def get_data_json(self) -> dict[str, Any]:
        # Простая конвертация (в реальности использовался бы парсер)
        _ = self._xml_provider.get_data_xml()  # В реальности был бы парсинг
        # Имитация парсинга XML в JSON
        return {"users": [{"name": "Alice", "age": 30}]}


def demo_adapter() -> None:
    """Демонстрация паттерна Adapter."""
    print("=" * 60)
    print("Adapter Pattern")
    print("=" * 60)

    # Адаптер платежей
    old_system = OldPaymentSystem()
    adapter = PaymentAdapter(old_system)

    print("\nPayment Adapter:")
    print(f"  {adapter.pay(1500.50)}")
    print(f"  {adapter.refund('TXN-123', 500.00)}")

    # Адаптер данных
    xml_provider = XMLDataProvider()
    json_adapter = JSONDataAdapter(xml_provider)

    print("\nData Format Adapter:")
    print(f"  XML: {xml_provider.get_data_xml()}")
    print(f"  JSON: {json_adapter.get_data_json()}")
    print()


# =============================================================================
# Decorator (Декоратор)
# =============================================================================
# Позволяет динамически добавлять объектам новую функциональность,
# оборачивая их в полезные обёртки.


# Паттерн Декоратор для классов
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
    """Базовый декоратор кофе."""

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


# Декоратор как функция (Python-way)
def timing_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """Измеряет время выполнения функции."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"  {func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper


def logging_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """Логирует вызовы функции."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"  Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"  {func.__name__} returned {result}")
        return result

    return wrapper


def retry_decorator(max_attempts: int = 3) -> Callable[..., Any]:
    """Повторяет вызов функции при ошибке."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"  Attempt {attempt} failed: {e}")
            raise last_exception  # type: ignore

        return wrapper

    return decorator


@timing_decorator
@logging_decorator
def slow_function(x: int) -> int:
    """Медленная функция для демонстрации."""
    sleep(0.1)
    return x * 2


def demo_decorator() -> None:
    """Демонстрация паттерна Decorator."""
    print("=" * 60)
    print("Decorator Pattern")
    print("=" * 60)

    # Декораторы для классов
    print("\nCoffee Decorators:")

    # Простой кофе
    coffee: Coffee = SimpleCoffee()
    print(f"  {coffee.description()}: {coffee.cost()} RUB")

    # Кофе с молоком
    coffee_with_milk: Coffee = MilkDecorator(SimpleCoffee())
    print(f"  {coffee_with_milk.description()}: {coffee_with_milk.cost()} RUB")

    # Кофе с молоком, сахаром и сливками
    fancy_coffee: Coffee = WhippedCreamDecorator(
        SugarDecorator(MilkDecorator(SimpleCoffee()))
    )
    print(f"  {fancy_coffee.description()}: {fancy_coffee.cost()} RUB")

    # Супер-кофе со всеми добавками
    super_coffee: Coffee = VanillaDecorator(
        WhippedCreamDecorator(SugarDecorator(MilkDecorator(SimpleCoffee())))
    )
    print(f"  {super_coffee.description()}: {super_coffee.cost()} RUB")

    # Декораторы-функции
    print("\nFunction Decorators:")
    result = slow_function(5)
    print(f"  Final result: {result}")
    print()


# =============================================================================
# Facade (Фасад)
# =============================================================================
# Предоставляет простой интерфейс к сложной системе классов.


# Сложная подсистема
class CPU:
    """Центральный процессор."""

    def freeze(self) -> None:
        print("    CPU: Freezing processor")

    def jump(self, address: int) -> None:
        print(f"    CPU: Jumping to address {address}")

    def execute(self) -> None:
        print("    CPU: Executing instructions")


class Memory:
    """Оперативная память."""

    def load(self, address: int, data: str) -> None:
        print(f"    Memory: Loading '{data}' at address {address}")


class HardDrive:
    """Жёсткий диск."""

    def read(self, sector: int, size: int) -> str:
        print(f"    HDD: Reading {size} bytes from sector {sector}")
        return "boot_data"


class BIOS:
    """BIOS."""

    def initialize(self) -> None:
        print("    BIOS: Initializing hardware")

    def load_boot_sector(self) -> int:
        print("    BIOS: Loading boot sector")
        return 0x7C00


class OperatingSystem:
    """Операционная система."""

    def boot(self) -> None:
        print("    OS: Booting operating system")

    def show_desktop(self) -> None:
        print("    OS: Showing desktop")


# Фасад
class ComputerFacade:
    """
    Фасад — предоставляет простой интерфейс для запуска компьютера.

    Скрывает сложность взаимодействия компонентов.
    """

    def __init__(self) -> None:
        self._cpu = CPU()
        self._memory = Memory()
        self._hdd = HardDrive()
        self._bios = BIOS()
        self._os = OperatingSystem()

    def start(self) -> None:
        """Запуск компьютера — простой метод для пользователя."""
        print("  Starting computer...")

        # Сложная последовательность действий скрыта от пользователя
        self._bios.initialize()
        boot_address = self._bios.load_boot_sector()

        self._cpu.freeze()
        boot_data = self._hdd.read(sector=0, size=512)
        self._memory.load(boot_address, boot_data)
        self._cpu.jump(boot_address)
        self._cpu.execute()

        self._os.boot()
        self._os.show_desktop()

        print("  Computer started successfully!")

    def shutdown(self) -> None:
        """Выключение компьютера."""
        print("  Shutting down...")
        print("  Computer is off.")


# Ещё один пример: фасад для работы с файлами
class FileReader:
    def read(self, path: str) -> str:
        return f"Content of {path}"


class FileParser:
    def parse_json(self, content: str) -> dict[str, Any]:
        return {"parsed": content}


class DataValidator:
    def validate(self, data: dict[str, Any]) -> bool:
        return "parsed" in data


class DataProcessor:
    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        return {**data, "processed": True}


class DataPipelineFacade:
    """Фасад для пайплайна обработки данных."""

    def __init__(self) -> None:
        self._reader = FileReader()
        self._parser = FileParser()
        self._validator = DataValidator()
        self._processor = DataProcessor()

    def process_file(self, path: str) -> dict[str, Any]:
        """Обрабатывает файл — один простой вызов."""
        content = self._reader.read(path)
        data = self._parser.parse_json(content)
        if not self._validator.validate(data):
            raise ValueError("Invalid data")
        return self._processor.process(data)


def demo_facade() -> None:
    """Демонстрация паттерна Facade."""
    print("=" * 60)
    print("Facade Pattern")
    print("=" * 60)

    # Фасад компьютера
    print("\nComputer Facade:")
    computer = ComputerFacade()
    computer.start()
    computer.shutdown()

    # Фасад пайплайна данных
    print("\nData Pipeline Facade:")
    pipeline = DataPipelineFacade()
    result = pipeline.process_file("data.json")
    print(f"  Result: {result}")
    print()


# =============================================================================
# Composite (Компоновщик)
# =============================================================================
# Позволяет сгруппировать объекты в древовидную структуру
# и работать с ними как с единым объектом.


class FileSystemComponent(ABC):
    """Абстрактный компонент файловой системы."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def get_size(self) -> int:
        """Возвращает размер в байтах."""
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """Отображает структуру."""
        pass


@dataclass
class File(FileSystemComponent):
    """Файл — листовой элемент."""

    name: str
    size: int

    def get_size(self) -> int:
        return self.size

    def display(self, indent: int = 0) -> str:
        return f"{'  ' * indent}📄 {self.name} ({self.size} bytes)"


class Directory(FileSystemComponent):
    """Директория — составной элемент."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._children: list[FileSystemComponent] = []

    def add(self, component: FileSystemComponent) -> None:
        self._children.append(component)

    def remove(self, component: FileSystemComponent) -> None:
        self._children.remove(component)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self._children)

    def display(self, indent: int = 0) -> str:
        lines = [f"{'  ' * indent}📁 {self.name}/ ({self.get_size()} bytes)"]
        for child in self._children:
            lines.append(child.display(indent + 1))
        return "\n".join(lines)


def demo_composite() -> None:
    """Демонстрация паттерна Composite."""
    print("=" * 60)
    print("Composite Pattern")
    print("=" * 60)

    # Создаём структуру файловой системы
    root = Directory("root")

    documents = Directory("documents")
    documents.add(File("report.pdf", 1024))
    documents.add(File("notes.txt", 256))

    images = Directory("images")
    images.add(File("photo.jpg", 2048))
    images.add(File("logo.png", 512))

    projects = Directory("projects")
    python_project = Directory("python_project")
    python_project.add(File("main.py", 128))
    python_project.add(File("utils.py", 64))
    projects.add(python_project)

    root.add(documents)
    root.add(images)
    root.add(projects)
    root.add(File("readme.md", 512))

    print("\nFile System Structure:")
    print(root.display())
    print()


# =============================================================================
# Proxy (Заместитель)
# =============================================================================
# Предоставляет объект-заменитель, который контролирует доступ
# к другому объекту.


class Image(ABC):
    """Абстрактное изображение."""

    @abstractmethod
    def display(self) -> str:
        pass


class RealImage(Image):
    """Реальное изображение — загружается с диска."""

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        print(f"    Loading image from disk: {self.filename}")
        sleep(0.5)  # Имитация долгой загрузки

    def display(self) -> str:
        return f"Displaying {self.filename}"


class ImageProxy(Image):
    """
    Прокси для изображения — ленивая загрузка.

    Загружает реальное изображение только при первом обращении.
    """

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._real_image: RealImage | None = None

    def display(self) -> str:
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        return self._real_image.display()


# Кэширующий прокси
class DataService(ABC):
    """Абстрактный сервис данных."""

    @abstractmethod
    def get_data(self, key: str) -> str:
        pass


class RealDataService(DataService):
    """Реальный сервис — медленный запрос к БД."""

    def get_data(self, key: str) -> str:
        print(f"    Fetching data for key '{key}' from database...")
        sleep(0.3)  # Имитация запроса
        return f"Data for {key}"


class CachingProxy(DataService):
    """Кэширующий прокси."""

    def __init__(self, service: DataService) -> None:
        self._service = service
        self._cache: dict[str, str] = {}

    def get_data(self, key: str) -> str:
        if key not in self._cache:
            print(f"    Cache MISS for '{key}'")
            self._cache[key] = self._service.get_data(key)
        else:
            print(f"    Cache HIT for '{key}'")
        return self._cache[key]


# Защитный прокси
class SecureDocument:
    """Защищённый документ."""

    def __init__(self, content: str) -> None:
        self.content = content

    def read(self) -> str:
        return self.content

    def write(self, content: str) -> None:
        self.content = content


class SecureDocumentProxy:
    """Прокси для контроля доступа."""

    def __init__(self, document: SecureDocument, user_role: str) -> None:
        self._document = document
        self._user_role = user_role

    def read(self) -> str:
        return self._document.read()

    def write(self, content: str) -> None:
        if self._user_role != "admin":
            raise PermissionError("Only admin can write to this document")
        self._document.write(content)


def demo_proxy() -> None:
    """Демонстрация паттерна Proxy."""
    print("=" * 60)
    print("Proxy Pattern")
    print("=" * 60)

    # Прокси для ленивой загрузки изображений
    print("\nLazy Loading Proxy:")
    print("  Creating proxy (no loading yet)...")
    image_proxy = ImageProxy("large_photo.jpg")
    print("  Proxy created.")

    print("  First display:")
    print(f"    {image_proxy.display()}")

    print("  Second display (already loaded):")
    print(f"    {image_proxy.display()}")

    # Кэширующий прокси
    print("\nCaching Proxy:")
    real_service = RealDataService()
    cached_service = CachingProxy(real_service)

    print("  Getting 'user_1':")
    print(f"    Result: {cached_service.get_data('user_1')}")

    print("  Getting 'user_1' again:")
    print(f"    Result: {cached_service.get_data('user_1')}")

    print("  Getting 'user_2':")
    print(f"    Result: {cached_service.get_data('user_2')}")

    # Защитный прокси
    print("\nProtection Proxy:")
    doc = SecureDocument("Secret content")

    user_proxy = SecureDocumentProxy(doc, "user")
    admin_proxy = SecureDocumentProxy(doc, "admin")

    print(f"  User reading: {user_proxy.read()}")
    print(f"  Admin reading: {admin_proxy.read()}")

    try:
        user_proxy.write("Hacked!")
    except PermissionError as e:
        print(f"  User writing: Error - {e}")

    admin_proxy.write("Updated by admin")
    print("  Admin writing: Success")
    print(f"  New content: {admin_proxy.read()}")
    print()


# =============================================================================
# Main
# =============================================================================


def main() -> None:
    """Запуск всех демонстраций."""
    demo_adapter()
    demo_decorator()
    demo_facade()
    demo_composite()
    demo_proxy()

    print("=" * 60)
    print("All Structural Patterns demonstrated!")
    print("=" * 60)


if __name__ == "__main__":
    main()
