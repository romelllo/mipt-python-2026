# Модуль 2: Объектно-ориентированное программирование и паттерны проектирования

## Описание

Второй модуль посвящен объектно-ориентированному программированию в Python и основным паттернам проектирования.

## Темы

### 1. Основы ООП
- Классы и объекты
- Атрибуты и методы
- `__init__` конструктор
- `self` и экземпляры класса
- Атрибуты класса vs атрибуты экземпляра

### 2. Наследование
- Базовые и производные классы
- Переопределение методов
- `super()`
- Множественное наследование
- MRO (Method Resolution Order)

### 3. Инкапсуляция
- Публичные, защищенные и приватные атрибуты
- Property декораторы
- Геттеры и сеттеры
- `@property`, `@setter`, `@deleter`

### 4. Полиморфизм
- Duck typing
- Перегрузка операторов
- Magic methods (`__str__`, `__repr__`, `__add__`, и т.д.)
- Abstract Base Classes (ABC)

### 5. SOLID принципы
- Single Responsibility Principle
- Open/Closed Principle
- Liskov Substitution Principle
- Interface Segregation Principle
- Dependency Inversion Principle

### 6. Паттерны проектирования

#### Порождающие паттерны (Creational)
- Singleton
- Factory Method
- Abstract Factory
- Builder
- Prototype

#### Структурные паттерны (Structural)
- Adapter
- Bridge
- Composite
- Decorator
- Facade
- Proxy

#### Поведенческие паттерны (Behavioral)
- Strategy
- Observer
- Command
- Iterator
- State
- Template Method

### 7. Дополнительные концепции
- Dataclasses
- Named Tuples
- Slots
- Metaclasses (введение)
- Context Managers

## Структура модуля

```
module_2_oop_patterns/
├── README.md (этот файл)
├── examples/          # Примеры реализации паттернов
├── exercises/         # Практические упражнения по ООП
└── homework/          # Домашние задания
```

## Практические задания

В директории `exercises/` вы найдете:
- Задачи на создание классов
- Реализация наследования и полиморфизма
- Применение паттернов проектирования
- SOLID принципы на практике

## Домашние задания

Домашние задания включают:
- Проектирование системы классов
- Реализация паттернов проектирования
- Рефакторинг кода с применением ООП

## Ресурсы

- [Python Classes Tutorial](https://docs.python.org/3/tutorial/classes.html)
- [Design Patterns in Python](https://refactoring.guru/design-patterns/python)
- [SOLID Principles](https://www.digitalocean.com/community/conceptual_articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design)
- [Python Patterns](https://python-patterns.guide/)

## Требования для выполнения

- Python 3.10+
- Понимание основ Python (Модуль 1)
- IDE с поддержкой рефакторинга

## Дополнительно

Рекомендуется изучить книги:
- "Design Patterns: Elements of Reusable Object-Oriented Software" (Gang of Four)
- "Head First Design Patterns"
- "Clean Code" by Robert Martin
