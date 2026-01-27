"""
Семинар 4: Форматы данных — JSON и XML.

Этот модуль демонстрирует:
- Работу с JSON: сериализация, десериализация, файлы
- Работу с XML: создание, парсинг, XPath
- Сравнение форматов и конвертация между ними
- Практические примеры с реальными данными
"""

import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any


# =============================================================================
# 1. Работа с JSON
# =============================================================================


def demonstrate_json_basics() -> None:
    """Базовые операции с JSON."""
    print("=" * 60)
    print("1. Основы JSON")
    print("=" * 60)

    # Python типы и их JSON эквиваленты
    print("\n1.1 Соответствие типов Python и JSON:")
    python_data = {
        "string": "Hello, World!",
        "integer": 42,
        "float": 3.14,
        "boolean_true": True,
        "boolean_false": False,
        "null_value": None,
        "array": [1, 2, 3],
        "nested_object": {"key": "value"},
    }

    json_string = json.dumps(python_data, indent=2)
    print(json_string)

    # Сериализация (Python -> JSON)
    print("\n1.2 Сериализация (dumps):")
    data = {"name": "Алиса", "age": 25, "courses": ["Python", "SQL"]}

    # Без ensure_ascii русские символы будут экранированы
    print(f"  С ensure_ascii=True:  {json.dumps(data)}")
    print(f"  С ensure_ascii=False: {json.dumps(data, ensure_ascii=False)}")

    # Форматирование
    print("\n  С отступами:")
    print(json.dumps(data, ensure_ascii=False, indent=2))

    # Сортировка ключей
    print("  С сортировкой ключей:")
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))

    # Десериализация (JSON -> Python)
    print("\n1.3 Десериализация (loads):")
    json_str = '{"name": "Bob", "scores": [85, 90, 78], "active": true}'
    parsed = json.loads(json_str)
    print(f"  Тип результата: {type(parsed)}")
    print(f"  Данные: {parsed}")
    print(f"  parsed['name'] = {parsed['name']}")
    print(f"  parsed['scores'][0] = {parsed['scores'][0]}")
    print(f"  parsed['active'] = {parsed['active']} (тип: {type(parsed['active'])})")


def demonstrate_json_files() -> None:
    """Работа с JSON файлами."""
    print("\n" + "=" * 60)
    print("2. JSON файлы")
    print("=" * 60)

    # Создаём тестовые данные
    students = [
        {"id": 1, "name": "Иванов Иван", "gpa": 4.5, "courses": ["Python", "ML"]},
        {"id": 2, "name": "Петрова Анна", "gpa": 4.8, "courses": ["SQL", "Web"]},
        {"id": 3, "name": "Сидоров Пётр", "gpa": 4.2, "courses": ["Python", "SQL"]},
    ]

    # Определяем путь к файлу
    file_path = Path(__file__).parent / "temp_students.json"

    # Запись в файл
    print(f"\n2.1 Запись в файл: {file_path.name}")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)
    print("  Файл записан успешно")

    # Чтение из файла
    print("\n2.2 Чтение из файла:")
    with open(file_path, encoding="utf-8") as f:
        loaded_students = json.load(f)

    for student in loaded_students:
        print(f"  {student['name']}: GPA {student['gpa']}")

    # Удаляем временный файл
    file_path.unlink()
    print(f"\n  Временный файл {file_path.name} удалён")


def demonstrate_json_custom_types() -> None:
    """Сериализация кастомных типов в JSON."""
    print("\n" + "=" * 60)
    print("3. Кастомные типы в JSON")
    print("=" * 60)

    # Проблема: datetime не сериализуется по умолчанию
    print("\n3.1 Проблема с datetime:")
    data_with_date = {"event": "Семинар", "date": datetime.now()}

    try:
        json.dumps(data_with_date)
    except TypeError as e:
        print(f"  Ошибка: {e}")

    # Решение 1: Кастомный encoder
    print("\n3.2 Решение: кастомный JSONEncoder:")

    class CustomEncoder(json.JSONEncoder):
        """JSON encoder с поддержкой datetime и date."""

        def default(self, obj: Any) -> Any:
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, date):
                return obj.strftime("%Y-%m-%d")
            return super().default(obj)

    result = json.dumps(data_with_date, cls=CustomEncoder, ensure_ascii=False)
    print(f"  Результат: {result}")

    # Решение 2: функция default
    print("\n3.3 Альтернатива: параметр default:")

    def json_serial(obj: Any) -> str:
        """Сериализатор для нестандартных типов."""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} is not JSON serializable")

    result = json.dumps(data_with_date, default=json_serial, ensure_ascii=False)
    print(f"  Результат: {result}")

    # Dataclasses
    print("\n3.4 Сериализация dataclass:")

    @dataclass
    class Student:
        id: int
        name: str
        gpa: float

    student = Student(id=1, name="Иванов", gpa=4.5)
    result = json.dumps(asdict(student), ensure_ascii=False)
    print(f"  Результат: {result}")


def demonstrate_json_validation() -> None:
    """Валидация и безопасный парсинг JSON."""
    print("\n" + "=" * 60)
    print("4. Валидация JSON")
    print("=" * 60)

    # Невалидный JSON
    print("\n4.1 Обработка невалидного JSON:")
    invalid_jsons = [
        "{'name': 'Alice'}",  # Одинарные кавычки
        '{"name": "Alice",}',  # Trailing comma
        "{name: 'Alice'}",  # Без кавычек у ключа
        "undefined",  # JavaScript значение
    ]

    for invalid in invalid_jsons:
        try:
            json.loads(invalid)
        except json.JSONDecodeError as e:
            print(f"  '{invalid[:20]}...' -> Ошибка: {e.msg}")

    # Безопасный парсинг
    print("\n4.2 Безопасный парсинг:")

    def safe_json_loads(json_string: str, default: Any = None) -> Any:
        """Безопасный парсинг JSON с значением по умолчанию."""
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            return default

    result = safe_json_loads('{"valid": true}')
    print(f"  Валидный JSON: {result}")

    result = safe_json_loads("invalid json", default={})
    print(f"  Невалидный JSON (default={{}}): {result}")


# =============================================================================
# 2. Работа с XML
# =============================================================================


def demonstrate_xml_creation() -> None:
    """Создание XML документов."""
    print("\n" + "=" * 60)
    print("5. Создание XML")
    print("=" * 60)

    # Создание элементов
    print("\n5.1 Создание XML структуры:")

    # Корневой элемент
    root = ET.Element("university")
    root.set("name", "МФТИ")
    root.set("founded", "1951")

    # Добавляем факультет
    faculty = ET.SubElement(root, "faculty")
    faculty.set("id", "1")

    name_elem = ET.SubElement(faculty, "name")
    name_elem.text = "Физтех-школа прикладной математики и информатики"

    # Добавляем студентов
    students_elem = ET.SubElement(faculty, "students")

    students_data = [
        {"id": "1", "name": "Иванов Иван", "gpa": "4.5"},
        {"id": "2", "name": "Петрова Анна", "gpa": "4.8"},
    ]

    for data in students_data:
        student = ET.SubElement(students_elem, "student", id=data["id"])
        ET.SubElement(student, "name").text = data["name"]
        ET.SubElement(student, "gpa").text = data["gpa"]

    # Вывод XML
    xml_string = ET.tostring(root, encoding="unicode")
    print(f"  Компактный XML:\n  {xml_string}")

    # Красивый вывод (Python 3.9+)
    print("\n5.2 Форматированный XML:")
    ET.indent(root, space="  ")
    xml_formatted = ET.tostring(root, encoding="unicode")
    print(xml_formatted)


def demonstrate_xml_parsing() -> None:
    """Парсинг XML документов."""
    print("\n" + "=" * 60)
    print("6. Парсинг XML")
    print("=" * 60)

    # XML для парсинга
    xml_data = """<?xml version="1.0" encoding="UTF-8"?>
    <catalog>
        <book id="1" category="programming">
            <title>Python Crash Course</title>
            <author>Eric Matthes</author>
            <year>2019</year>
            <price currency="USD">39.99</price>
        </book>
        <book id="2" category="programming">
            <title>Fluent Python</title>
            <author>Luciano Ramalho</author>
            <year>2022</year>
            <price currency="USD">59.99</price>
        </book>
        <book id="3" category="databases">
            <title>SQL Cookbook</title>
            <author>Anthony Molinaro</author>
            <year>2020</year>
            <price currency="USD">49.99</price>
        </book>
    </catalog>
    """

    # Парсинг из строки
    print("\n6.1 Парсинг XML из строки:")
    root = ET.fromstring(xml_data)
    print(f"  Корневой элемент: {root.tag}")
    print(f"  Количество книг: {len(root)}")

    # Итерация по элементам
    print("\n6.2 Итерация по элементам:")
    for book in root:
        title = book.find("title").text
        author = book.find("author").text
        print(f"  - {title} ({author})")

    # Доступ к атрибутам
    print("\n6.3 Доступ к атрибутам:")
    for book in root:
        book_id = book.get("id")
        category = book.get("category")
        title = book.find("title").text
        print(f"  ID={book_id}, Category={category}: {title}")

    # Поиск элементов
    print("\n6.4 Поиск элементов:")

    # find() - первый элемент
    first_book = root.find("book")
    print(f"  Первая книга: {first_book.find('title').text}")

    # findall() - все элементы
    all_books = root.findall("book")
    print(f"  Всего книг: {len(all_books)}")

    # Поиск с условием (XPath-подобный синтаксис)
    programming_books = root.findall("book[@category='programming']")
    print(f"  Книги по программированию: {len(programming_books)}")

    # Поиск вложенных элементов
    all_titles = root.findall(".//title")
    print(f"  Все заголовки: {[t.text for t in all_titles]}")


def demonstrate_xml_modification() -> None:
    """Модификация XML документов."""
    print("\n" + "=" * 60)
    print("7. Модификация XML")
    print("=" * 60)

    # Создаём простую структуру
    root = ET.Element("config")
    ET.SubElement(root, "setting", name="debug").text = "false"
    ET.SubElement(root, "setting", name="timeout").text = "30"

    print("\n7.1 Исходный XML:")
    print(f"  {ET.tostring(root, encoding='unicode')}")

    # Изменение текста элемента
    print("\n7.2 Изменение значения:")
    for setting in root.findall("setting[@name='debug']"):
        setting.text = "true"

    # Добавление нового элемента
    print("7.3 Добавление элемента:")
    ET.SubElement(root, "setting", name="max_connections").text = "100"

    # Удаление элемента
    print("7.4 Удаление элемента:")
    for setting in root.findall("setting[@name='timeout']"):
        root.remove(setting)

    print("\n  Результат:")
    ET.indent(root, space="  ")
    print(ET.tostring(root, encoding="unicode"))


# =============================================================================
# 3. Конвертация между форматами
# =============================================================================


def demonstrate_json_xml_conversion() -> None:
    """Конвертация между JSON и XML."""
    print("\n" + "=" * 60)
    print("8. Конвертация JSON <-> XML")
    print("=" * 60)

    # JSON -> XML
    print("\n8.1 JSON -> XML:")

    json_data = {
        "students": [
            {"id": 1, "name": "Иванов", "gpa": 4.5},
            {"id": 2, "name": "Петрова", "gpa": 4.8},
        ]
    }

    print(f"  JSON: {json.dumps(json_data, ensure_ascii=False)}")

    def json_to_xml(data: dict, root_name: str = "root") -> ET.Element:
        """Конвертирует словарь в XML элемент."""
        root = ET.Element(root_name)

        def add_element(parent: ET.Element, key: str, value: Any) -> None:
            if isinstance(value, dict):
                child = ET.SubElement(parent, key)
                for k, v in value.items():
                    add_element(child, k, v)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        child = ET.SubElement(
                            parent, key[:-1] if key.endswith("s") else key
                        )
                        for k, v in item.items():
                            add_element(child, k, v)
                    else:
                        ET.SubElement(parent, key).text = str(item)
            else:
                ET.SubElement(parent, key).text = (
                    str(value) if value is not None else ""
                )

        for key, value in data.items():
            add_element(root, key, value)

        return root

    xml_root = json_to_xml(json_data, "data")
    ET.indent(xml_root, space="  ")
    print(f"  XML:\n{ET.tostring(xml_root, encoding='unicode')}")

    # XML -> JSON
    print("\n8.2 XML -> JSON:")

    xml_string = """
    <data>
        <student id="1">
            <name>Иванов</name>
            <gpa>4.5</gpa>
        </student>
        <student id="2">
            <name>Петрова</name>
            <gpa>4.8</gpa>
        </student>
    </data>
    """

    def xml_to_json(element: ET.Element) -> dict | list | str:
        """Конвертирует XML элемент в словарь."""
        result: dict[str, Any] = {}

        # Добавляем атрибуты
        if element.attrib:
            result["@attributes"] = element.attrib

        # Добавляем текст
        if element.text and element.text.strip():
            if not element.attrib and len(element) == 0:
                return element.text.strip()
            result["#text"] = element.text.strip()

        # Добавляем дочерние элементы
        children: dict[str, list] = {}
        for child in element:
            child_data = xml_to_json(child)
            if child.tag in children:
                children[child.tag].append(child_data)
            else:
                children[child.tag] = [child_data]

        # Упрощаем одиночные элементы
        for tag, items in children.items():
            if len(items) == 1:
                result[tag] = items[0]
            else:
                result[tag] = items

        return result

    root = ET.fromstring(xml_string)
    json_result = xml_to_json(root)
    print(f"  Результат:\n{json.dumps(json_result, ensure_ascii=False, indent=2)}")


def demonstrate_format_comparison() -> None:
    """Сравнение JSON и XML."""
    print("\n" + "=" * 60)
    print("9. Сравнение JSON и XML")
    print("=" * 60)

    # Одни и те же данные в разных форматах
    data = {
        "person": {
            "name": "Иван Иванов",
            "age": 25,
            "email": "ivan@example.com",
            "skills": ["Python", "SQL", "JavaScript"],
            "active": True,
        }
    }

    # JSON версия
    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    # XML версия
    root = ET.Element("person")
    ET.SubElement(root, "name").text = data["person"]["name"]
    ET.SubElement(root, "age").text = str(data["person"]["age"])
    ET.SubElement(root, "email").text = data["person"]["email"]
    skills = ET.SubElement(root, "skills")
    for skill in data["person"]["skills"]:
        ET.SubElement(skills, "skill").text = skill
    ET.SubElement(root, "active").text = str(data["person"]["active"]).lower()
    ET.indent(root, space="  ")
    xml_str = ET.tostring(root, encoding="unicode")

    print("\n9.1 JSON формат:")
    print(json_str)

    print("\n9.2 XML формат:")
    print(xml_str)

    print("\n9.3 Сравнение:")
    print(f"  JSON размер: {len(json_str)} символов")
    print(f"  XML размер:  {len(xml_str)} символов")
    print(f"  JSON компактнее на {len(xml_str) - len(json_str)} символов")

    print("\n9.4 Когда использовать:")
    print(
        """
  JSON:
    + Компактнее и легче читается
    + Нативная поддержка типов (числа, boolean, null)
    + Стандарт для REST API
    + Лучше для JavaScript/веб-приложений

  XML:
    + Поддержка схем (XSD) и пространств имён
    + Поддержка комментариев
    + XSLT для трансформаций
    + Стандарт для SOAP, RSS, конфигов
    """
    )


def main() -> None:
    """Главная функция."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 4: ФОРМАТЫ ДАННЫХ — JSON И XML")
    print("=" * 60)

    # JSON
    demonstrate_json_basics()
    demonstrate_json_files()
    demonstrate_json_custom_types()
    demonstrate_json_validation()

    # XML
    demonstrate_xml_creation()
    demonstrate_xml_parsing()
    demonstrate_xml_modification()

    # Конвертация и сравнение
    demonstrate_json_xml_conversion()
    demonstrate_format_comparison()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
