"""
Порождающие паттерны (Creational Patterns).

Порождающие паттерны отвечают за создание объектов,
скрывая логику их создания и делая систему независимой
от способа создания объектов.

Рассмотренные паттерны:
- Singleton (Одиночка)
- Factory Method (Фабричный метод)
- Abstract Factory (Абстрактная фабрика)
- Builder (Строитель)
- Prototype (Прототип)
"""

from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field
from threading import Lock
from typing import Any

# =============================================================================
# Singleton (Одиночка)
# =============================================================================
# Гарантирует, что у класса есть только один экземпляр,
# и предоставляет глобальную точку доступа к нему.


class SingletonMeta(type):
    """
    Потокобезопасная реализация Singleton через метакласс.

    Метакласс позволяет контролировать создание классов.
    """

    _instances: dict[type, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    """
    Подключение к базе данных — должно быть единственным.

    Использует метакласс SingletonMeta для реализации паттерна.
    """

    def __init__(self, connection_string: str = "default_connection") -> None:
        self.connection_string = connection_string
        self._connected = False

    def connect(self) -> None:
        if not self._connected:
            print(f"Connecting to: {self.connection_string}")
            self._connected = True

    def disconnect(self) -> None:
        if self._connected:
            print("Disconnecting...")
            self._connected = False

    def execute(self, query: str) -> str:
        return f"Executing: {query}"


# Альтернативная реализация через __new__
class Logger:
    """
    Логгер — классическая реализация Singleton через __new__.
    """

    _instance: "Logger | None" = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._log: list[str] = []
        return cls._instance

    def log(self, message: str) -> None:
        self._log.append(message)
        print(f"[LOG] {message}")

    def get_logs(self) -> list[str]:
        return self._log.copy()


def demo_singleton() -> None:
    """Демонстрация паттерна Singleton."""
    print("=" * 60)
    print("Singleton Pattern")
    print("=" * 60)

    # DatabaseConnection
    db1 = DatabaseConnection("mysql://localhost/mydb")
    db2 = DatabaseConnection("postgres://localhost/other")  # Игнорируется

    print(f"db1 is db2: {db1 is db2}")  # True
    print(f"Connection string: {db1.connection_string}")  # mysql://...

    db1.connect()
    print(db1.execute("SELECT * FROM users"))

    # Logger
    logger1 = Logger()
    logger2 = Logger()

    print(f"\nlogger1 is logger2: {logger1 is logger2}")  # True

    logger1.log("First message")
    logger2.log("Second message")  # Тот же экземпляр

    print(f"All logs: {logger1.get_logs()}")
    print()


# =============================================================================
# Factory Method (Фабричный метод)
# =============================================================================
# Определяет интерфейс для создания объекта, но позволяет
# подклассам решать, какой класс инстанцировать.


class Document(ABC):
    """Абстрактный документ."""

    @abstractmethod
    def render(self) -> str:
        """Отрисовка документа."""
        pass

    @abstractmethod
    def save(self, filename: str) -> str:
        """Сохранение документа."""
        pass


class PDFDocument(Document):
    """PDF документ."""

    def __init__(self, content: str) -> None:
        self.content = content

    def render(self) -> str:
        return f"<PDF>{self.content}</PDF>"

    def save(self, filename: str) -> str:
        return f"Saved PDF to {filename}.pdf"


class HTMLDocument(Document):
    """HTML документ."""

    def __init__(self, content: str) -> None:
        self.content = content

    def render(self) -> str:
        return f"<html><body>{self.content}</body></html>"

    def save(self, filename: str) -> str:
        return f"Saved HTML to {filename}.html"


class MarkdownDocument(Document):
    """Markdown документ."""

    def __init__(self, content: str) -> None:
        self.content = content

    def render(self) -> str:
        return f"# Document\n\n{self.content}"

    def save(self, filename: str) -> str:
        return f"Saved Markdown to {filename}.md"


class DocumentFactory:
    """Фабрика документов."""

    _document_types: dict[str, type[Document]] = {
        "pdf": PDFDocument,
        "html": HTMLDocument,
        "markdown": MarkdownDocument,
        "md": MarkdownDocument,
    }

    @classmethod
    def register(cls, doc_type: str, document_class: type[Document]) -> None:
        """Регистрирует новый тип документа."""
        cls._document_types[doc_type.lower()] = document_class

    @classmethod
    def create(cls, doc_type: str, content: str) -> Document:
        """Создаёт документ указанного типа."""
        doc_type = doc_type.lower()
        if doc_type not in cls._document_types:
            available = ", ".join(cls._document_types.keys())
            raise ValueError(f"Unknown type: {doc_type}. Available: {available}")
        return cls._document_types[doc_type](content)


def demo_factory() -> None:
    """Демонстрация паттерна Factory Method."""
    print("=" * 60)
    print("Factory Method Pattern")
    print("=" * 60)

    # Создание документов через фабрику
    content = "Hello, World!"

    for doc_type in ["pdf", "html", "markdown"]:
        doc = DocumentFactory.create(doc_type, content)
        print(f"\n{doc_type.upper()} Document:")
        print(f"  Render: {doc.render()}")
        print(f"  Save: {doc.save('document')}")

    # Регистрация нового типа
    class JSONDocument(Document):
        def __init__(self, content: str) -> None:
            self.content = content

        def render(self) -> str:
            return f'{{"content": "{self.content}"}}'

        def save(self, filename: str) -> str:
            return f"Saved JSON to {filename}.json"

    DocumentFactory.register("json", JSONDocument)
    json_doc = DocumentFactory.create("json", content)
    print("\nJSON Document (newly registered):")
    print(f"  Render: {json_doc.render()}")
    print()


# =============================================================================
# Abstract Factory (Абстрактная фабрика)
# =============================================================================
# Предоставляет интерфейс для создания семейств связанных объектов
# без указания их конкретных классов.


class Button(ABC):
    """Абстрактная кнопка."""

    @abstractmethod
    def render(self) -> str:
        pass


class Checkbox(ABC):
    """Абстрактный чекбокс."""

    @abstractmethod
    def render(self) -> str:
        pass


class WindowsButton(Button):
    def render(self) -> str:
        return "[Windows Button]"


class WindowsCheckbox(Checkbox):
    def render(self) -> str:
        return "[X] Windows Checkbox"


class MacButton(Button):
    def render(self) -> str:
        return "(Mac Button)"


class MacCheckbox(Checkbox):
    def render(self) -> str:
        return "(✓) Mac Checkbox"


class LinuxButton(Button):
    def render(self) -> str:
        return "<Linux Button>"


class LinuxCheckbox(Checkbox):
    def render(self) -> str:
        return "[*] Linux Checkbox"


class GUIFactory(ABC):
    """Абстрактная фабрика GUI элементов."""

    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass


class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()


class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()


class LinuxFactory(GUIFactory):
    def create_button(self) -> Button:
        return LinuxButton()

    def create_checkbox(self) -> Checkbox:
        return LinuxCheckbox()


def render_ui(factory: GUIFactory) -> None:
    """Отрисовывает UI с использованием фабрики."""
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    print(f"  Button: {button.render()}")
    print(f"  Checkbox: {checkbox.render()}")


def demo_abstract_factory() -> None:
    """Демонстрация паттерна Abstract Factory."""
    print("=" * 60)
    print("Abstract Factory Pattern")
    print("=" * 60)

    factories: dict[str, GUIFactory] = {
        "Windows": WindowsFactory(),
        "macOS": MacFactory(),
        "Linux": LinuxFactory(),
    }

    for os_name, factory in factories.items():
        print(f"\n{os_name} UI:")
        render_ui(factory)
    print()


# =============================================================================
# Builder (Строитель)
# =============================================================================
# Позволяет создавать сложные объекты пошагово.
# Позволяет использовать один и тот же код для создания различных объектов.


@dataclass
class Computer:
    """Компьютер — сложный объект с множеством компонентов."""

    cpu: str = ""
    ram: int = 0
    storage: str = ""
    gpu: str = ""
    os: str = ""
    extras: list[str] = field(default_factory=list)

    def specs(self) -> str:
        specs = [
            f"CPU: {self.cpu}",
            f"RAM: {self.ram}GB",
            f"Storage: {self.storage}",
            f"GPU: {self.gpu}",
            f"OS: {self.os}",
        ]
        if self.extras:
            specs.append(f"Extras: {', '.join(self.extras)}")
        return "\n  ".join(specs)


class ComputerBuilder:
    """Строитель компьютера с fluent interface."""

    def __init__(self) -> None:
        self._computer = Computer()

    def reset(self) -> "ComputerBuilder":
        """Сброс для создания нового компьютера."""
        self._computer = Computer()
        return self

    def set_cpu(self, cpu: str) -> "ComputerBuilder":
        self._computer.cpu = cpu
        return self

    def set_ram(self, ram_gb: int) -> "ComputerBuilder":
        self._computer.ram = ram_gb
        return self

    def set_storage(self, storage: str) -> "ComputerBuilder":
        self._computer.storage = storage
        return self

    def set_gpu(self, gpu: str) -> "ComputerBuilder":
        self._computer.gpu = gpu
        return self

    def set_os(self, os: str) -> "ComputerBuilder":
        self._computer.os = os
        return self

    def add_extra(self, extra: str) -> "ComputerBuilder":
        self._computer.extras.append(extra)
        return self

    def build(self) -> Computer:
        """Возвращает готовый компьютер."""
        computer = self._computer
        self.reset()
        return computer


class ComputerDirector:
    """Директор — знает рецепты создания компьютеров."""

    def __init__(self, builder: ComputerBuilder) -> None:
        self._builder = builder

    def build_gaming_pc(self) -> Computer:
        """Собирает игровой ПК."""
        return (
            self._builder.reset()
            .set_cpu("Intel Core i9-13900K")
            .set_ram(64)
            .set_storage("2TB NVMe SSD")
            .set_gpu("NVIDIA RTX 4090")
            .set_os("Windows 11")
            .add_extra("RGB Lighting")
            .add_extra("Liquid Cooling")
            .build()
        )

    def build_office_pc(self) -> Computer:
        """Собирает офисный ПК."""
        return (
            self._builder.reset()
            .set_cpu("Intel Core i5-13400")
            .set_ram(16)
            .set_storage("512GB SSD")
            .set_gpu("Intel UHD Graphics")
            .set_os("Windows 11 Pro")
            .build()
        )

    def build_developer_pc(self) -> Computer:
        """Собирает ПК для разработчика."""
        return (
            self._builder.reset()
            .set_cpu("AMD Ryzen 9 7950X")
            .set_ram(128)
            .set_storage("4TB NVMe SSD")
            .set_gpu("NVIDIA RTX 4080")
            .set_os("Ubuntu 22.04 LTS")
            .add_extra("Multiple Monitors Support")
            .add_extra("Mechanical Keyboard")
            .build()
        )


def demo_builder() -> None:
    """Демонстрация паттерна Builder."""
    print("=" * 60)
    print("Builder Pattern")
    print("=" * 60)

    builder = ComputerBuilder()
    director = ComputerDirector(builder)

    # Использование директора
    print("\nGaming PC:")
    print(f"  {director.build_gaming_pc().specs()}")

    print("\nOffice PC:")
    print(f"  {director.build_office_pc().specs()}")

    print("\nDeveloper PC:")
    print(f"  {director.build_developer_pc().specs()}")

    # Ручная сборка
    print("\nCustom PC (manual build):")
    custom = (
        builder.set_cpu("Apple M3 Max")
        .set_ram(96)
        .set_storage("2TB SSD")
        .set_gpu("Integrated")
        .set_os("macOS Sonoma")
        .build()
    )
    print(f"  {custom.specs()}")
    print()


# =============================================================================
# Prototype (Прототип)
# =============================================================================
# Позволяет копировать объекты, не вдаваясь в подробности их реализации.


@dataclass
class Prototype(ABC):
    """Базовый класс с методом клонирования."""

    @abstractmethod
    def clone(self) -> "Prototype":
        """Создаёт копию объекта."""
        pass


@dataclass
class GameCharacter(Prototype):
    """Игровой персонаж — может быть склонирован."""

    name: str
    health: int
    level: int
    skills: list[str] = field(default_factory=list)
    inventory: dict[str, int] = field(default_factory=dict)

    def clone(self) -> "GameCharacter":
        """Создаёт глубокую копию персонажа."""
        return GameCharacter(
            name=self.name,
            health=self.health,
            level=self.level,
            skills=self.skills.copy(),
            inventory=self.inventory.copy(),
        )

    def __str__(self) -> str:
        return (
            f"{self.name} (Lv.{self.level}, HP:{self.health}, "
            f"Skills: {self.skills}, Inventory: {self.inventory})"
        )


class PrototypeRegistry:
    """Реестр прототипов."""

    def __init__(self) -> None:
        self._prototypes: dict[str, Prototype] = {}

    def register(self, name: str, prototype: Prototype) -> None:
        """Регистрирует прототип."""
        self._prototypes[name] = prototype

    def unregister(self, name: str) -> None:
        """Удаляет прототип."""
        del self._prototypes[name]

    def clone(self, name: str) -> Prototype:
        """Создаёт копию прототипа по имени."""
        if name not in self._prototypes:
            raise ValueError(f"Prototype '{name}' not found")
        return deepcopy(self._prototypes[name])


def demo_prototype() -> None:
    """Демонстрация паттерна Prototype."""
    print("=" * 60)
    print("Prototype Pattern")
    print("=" * 60)

    # Создание базовых персонажей (прототипов)
    warrior = GameCharacter(
        name="Warrior",
        health=100,
        level=1,
        skills=["Slash", "Block"],
        inventory={"sword": 1, "shield": 1},
    )

    mage = GameCharacter(
        name="Mage",
        health=60,
        level=1,
        skills=["Fireball", "Ice Shield"],
        inventory={"staff": 1, "mana_potion": 3},
    )

    # Регистрация в реестре
    registry = PrototypeRegistry()
    registry.register("warrior", warrior)
    registry.register("mage", mage)

    # Клонирование и модификация
    print("\nOriginal Warrior:")
    print(f"  {warrior}")

    warrior_clone = warrior.clone()
    warrior_clone.name = "Warrior Clone"
    warrior_clone.skills.append("Power Strike")
    warrior_clone.inventory["potion"] = 5

    print("\nCloned Warrior (modified):")
    print(f"  {warrior_clone}")

    print("\nOriginal Warrior (unchanged):")
    print(f"  {warrior}")

    # Клонирование из реестра
    print("\nMage from registry:")
    mage_from_registry = registry.clone("mage")
    print(f"  {mage_from_registry}")
    print()


# =============================================================================
# Main
# =============================================================================


def main() -> None:
    """Запуск всех демонстраций."""
    demo_singleton()
    demo_factory()
    demo_abstract_factory()
    demo_builder()
    demo_prototype()

    print("=" * 60)
    print("All Creational Patterns demonstrated!")
    print("=" * 60)


if __name__ == "__main__":
    main()
