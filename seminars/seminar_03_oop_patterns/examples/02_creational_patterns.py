"""
Порождающие паттерны (Creational Patterns).

Порождающие паттерны отвечают за создание объектов,
скрывая логику их создания и делая систему независимой
от способа создания объектов.

Рассмотренные паттерны:
- Factory Method (Фабричный метод)
- Builder (Строитель)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

# =============================================================================
# Factory Method (Фабричный метод)
# =============================================================================
# Определяет интерфейс для создания объекта, но позволяет
# подклассам решать, какой класс инстанцировать.
#
# Когда использовать:
# - Вы не знаете заранее, какой именно объект нужно создать
# - Решение о типе объекта принимается в runtime
# - Хотите легко добавлять новые типы без изменения существующего кода


class Document(ABC):
    """Абстрактный документ."""

    def __init__(self, content: str) -> None:
        self.content = content

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

    def render(self) -> str:
        return f"<PDF>{self.content}</PDF>"

    def save(self, filename: str) -> str:
        return f"Saved PDF to {filename}.pdf"


class HTMLDocument(Document):
    """HTML документ."""

    def render(self) -> str:
        return f"<html><body>{self.content}</body></html>"

    def save(self, filename: str) -> str:
        return f"Saved HTML to {filename}.html"


class MarkdownDocument(Document):
    """Markdown документ."""

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
        """Регистрирует новый тип документа (расширяемость!)."""
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

    content = "Hello, World!"

    # Создание документов через фабрику — тип выбирается в runtime
    for doc_type in ["pdf", "html", "markdown"]:
        doc = DocumentFactory.create(doc_type, content)
        print(f"\n{doc_type.upper()} Document:")
        print(f"  Render: {doc.render()}")
        print(f"  Save: {doc.save('document')}")

    # Регистрация нового типа — не меняем существующий код (OCP!)
    class JSONDocument(Document):
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
# Builder (Строитель)
# =============================================================================
# Позволяет создавать сложные объекты пошагово.
# Позволяет использовать один и тот же код для создания различных объектов.
#
# Когда использовать:
# - Объект имеет множество параметров, часть из которых опциональные
# - Конструктор с 10+ параметрами становится нечитаемым
# - Хотите собирать объект пошагово (fluent interface)


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


def demo_builder() -> None:
    """Демонстрация паттерна Builder."""
    print("=" * 60)
    print("Builder Pattern")
    print("=" * 60)

    builder = ComputerBuilder()
    director = ComputerDirector(builder)

    # Использование директора — готовые рецепты
    print("\nGaming PC:")
    print(f"  {director.build_gaming_pc().specs()}")

    print("\nOffice PC:")
    print(f"  {director.build_office_pc().specs()}")

    # Ручная сборка — полная свобода
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
# Main
# =============================================================================


def main() -> None:
    """Запуск всех демонстраций."""
    demo_factory()
    demo_builder()

    print("=" * 60)
    print("Creational Patterns demonstrated: Factory Method, Builder")
    print("=" * 60)


if __name__ == "__main__":
    main()
