# Семинар 3: Паттерны проектирования ООП в Python

**Модуль:** 2 — Объектно-ориентированное программирование и базы данных в Python  
**Дата:** ДД.ММ.ГГГГ  
**Презентация:** [ссылка на презентацию]

---

## Цели семинара

После этого семинара студенты смогут:
- Понимать и применять принципы SOLID
- Реализовывать основные паттерны проектирования на Python
- Выбирать подходящий паттерн для решения конкретных задач
- Писать гибкий и поддерживаемый код

---

## План занятия

| Время | Тема | Материалы |
|-------|------|-----------|
| 10-15 мин | Введение в паттерны и SOLID | Презентация |
| 20 мин | Принципы SOLID с примерами | `examples/01_solid_principles.py` |
| 25 мин | Порождающие паттерны | `examples/02_creational_patterns.py` |
| 25 мин | Структурные паттерны | `examples/03_structural_patterns.py` |
| 25 мин | Поведенческие паттерны | `examples/04_behavioral_patterns.py` |
| 25 мин | Практика | `exercises/oop_patterns_practice.md` |

---

## 1. Принципы SOLID

SOLID — это пять принципов объектно-ориентированного проектирования:

### S — Single Responsibility Principle (Принцип единственной ответственности)

Класс должен иметь только одну причину для изменения.

```python
# Плохо: класс делает слишком много
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
    
    def save_to_db(self): ...      # Работа с БД
    def send_email(self): ...       # Отправка email
    def generate_report(self): ...  # Генерация отчёта

# Хорошо: разделяем ответственности
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user: User): ...

class EmailService:
    def send(self, user: User, message: str): ...
```

### O — Open/Closed Principle (Принцип открытости/закрытости)

Классы должны быть открыты для расширения, но закрыты для модификации.

```python
from abc import ABC, abstractmethod

class Discount(ABC):
    @abstractmethod
    def calculate(self, price: float) -> float:
        pass

class NoDiscount(Discount):
    def calculate(self, price: float) -> float:
        return price

class PercentDiscount(Discount):
    def __init__(self, percent: float):
        self.percent = percent
    
    def calculate(self, price: float) -> float:
        return price * (1 - self.percent / 100)

# Легко добавить новый тип скидки без изменения существующего кода
class FixedDiscount(Discount):
    def __init__(self, amount: float):
        self.amount = amount
    
    def calculate(self, price: float) -> float:
        return max(0, price - self.amount)
```

### L — Liskov Substitution Principle (Принцип подстановки Барбары Лисков)

Объекты подклассов должны быть взаимозаменяемы с объектами базового класса.

```python
class Bird:
    def fly(self) -> str:
        return "Flying"

# Плохо: пингвин — птица, но не летает
class Penguin(Bird):
    def fly(self) -> str:
        raise NotImplementedError("Penguins can't fly!")

# Хорошо: разделяем интерфейсы
class Bird(ABC):
    @abstractmethod
    def move(self) -> str:
        pass

class FlyingBird(Bird):
    def move(self) -> str:
        return "Flying"

class SwimmingBird(Bird):
    def move(self) -> str:
        return "Swimming"
```

### I — Interface Segregation Principle (Принцип разделения интерфейса)

Клиенты не должны зависеть от интерфейсов, которые они не используют.

```python
# Плохо: один большой интерфейс
class Worker(ABC):
    @abstractmethod
    def work(self): pass
    @abstractmethod
    def eat(self): pass
    @abstractmethod
    def sleep(self): pass

# Хорошо: маленькие специализированные интерфейсы
class Workable(ABC):
    @abstractmethod
    def work(self): pass

class Eatable(ABC):
    @abstractmethod
    def eat(self): pass

class Human(Workable, Eatable):
    def work(self): ...
    def eat(self): ...

class Robot(Workable):  # Роботу не нужно есть
    def work(self): ...
```

### D — Dependency Inversion Principle (Принцип инверсии зависимостей)

Модули верхнего уровня не должны зависеть от модулей нижнего уровня. Оба должны зависеть от абстракций.

```python
# Плохо: жёсткая зависимость
class MySQLDatabase:
    def connect(self): ...
    def execute(self, query: str): ...

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # Жёсткая связь

# Хорошо: зависимость от абстракции
class Database(ABC):
    @abstractmethod
    def connect(self): pass
    @abstractmethod
    def execute(self, query: str): pass

class UserService:
    def __init__(self, db: Database):  # Инъекция зависимости
        self.db = db
```

---

## 2. Порождающие паттерны (Creational Patterns)

Отвечают за создание объектов.

### Singleton (Одиночка)

Гарантирует существование только одного экземпляра класса.

```python
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.connection = "Connected to DB"
        self._initialized = True

# Использование
db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(db1 is db2)  # True
```

### Factory Method (Фабричный метод)

Определяет интерфейс для создания объектов, но позволяет подклассам решать, какой класс создавать.

```python
class Document(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class PDFDocument(Document):
    def render(self) -> str:
        return "Rendering PDF"

class HTMLDocument(Document):
    def render(self) -> str:
        return "Rendering HTML"

class DocumentFactory:
    @staticmethod
    def create(doc_type: str) -> Document:
        factories = {
            "pdf": PDFDocument,
            "html": HTMLDocument,
        }
        if doc_type not in factories:
            raise ValueError(f"Unknown document type: {doc_type}")
        return factories[doc_type]()
```

### Builder (Строитель)

Позволяет создавать сложные объекты пошагово.

```python
class Pizza:
    def __init__(self):
        self.size = ""
        self.cheese = False
        self.pepperoni = False
        self.mushrooms = False

class PizzaBuilder:
    def __init__(self):
        self._pizza = Pizza()
    
    def set_size(self, size: str) -> "PizzaBuilder":
        self._pizza.size = size
        return self
    
    def add_cheese(self) -> "PizzaBuilder":
        self._pizza.cheese = True
        return self
    
    def add_pepperoni(self) -> "PizzaBuilder":
        self._pizza.pepperoni = True
        return self
    
    def build(self) -> Pizza:
        return self._pizza

# Использование (fluent interface)
pizza = (PizzaBuilder()
         .set_size("large")
         .add_cheese()
         .add_pepperoni()
         .build())
```

---

## 3. Структурные паттерны (Structural Patterns)

Отвечают за компоновку классов и объектов.

### Adapter (Адаптер)

Позволяет объектам с несовместимыми интерфейсами работать вместе.

```python
# Старый интерфейс
class OldPaymentSystem:
    def make_payment(self, amount: int) -> str:
        return f"Paid {amount} kopecks"

# Новый интерфейс
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

# Адаптер
class PaymentAdapter(PaymentProcessor):
    def __init__(self, old_system: OldPaymentSystem):
        self.old_system = old_system
    
    def pay(self, amount: float) -> str:
        kopecks = int(amount * 100)
        return self.old_system.make_payment(kopecks)
```

### Decorator (Декоратор)

Динамически добавляет объекту новые обязанности.

```python
class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass
    
    @abstractmethod
    def description(self) -> str:
        pass

class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 100.0
    
    def description(self) -> str:
        return "Coffee"

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 20.0
    
    def description(self) -> str:
        return f"{self._coffee.description()} + Milk"

# Использование
coffee = SimpleCoffee()
coffee_with_milk = MilkDecorator(coffee)
print(coffee_with_milk.description())  # "Coffee + Milk"
print(coffee_with_milk.cost())         # 120.0
```

### Facade (Фасад)

Предоставляет простой интерфейс к сложной подсистеме.

```python
class CPU:
    def freeze(self): print("CPU freeze")
    def execute(self): print("CPU execute")

class Memory:
    def load(self, data: str): print(f"Memory load: {data}")

class HardDrive:
    def read(self) -> str: return "boot data"

class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hdd = HardDrive()
    
    def start(self):
        self.cpu.freeze()
        self.memory.load(self.hdd.read())
        self.cpu.execute()

# Простой интерфейс для пользователя
computer = ComputerFacade()
computer.start()
```

---

## 4. Поведенческие паттерны (Behavioral Patterns)

Отвечают за взаимодействие между объектами.

### Observer (Наблюдатель)

Определяет зависимость один-ко-многим между объектами.

```python
class Subject:
    def __init__(self):
        self._observers: list[Observer] = []
        self._state = None
    
    def attach(self, observer: "Observer"):
        self._observers.append(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self._state)
    
    def set_state(self, state):
        self._state = state
        self.notify()

class Observer(ABC):
    @abstractmethod
    def update(self, state): pass

class EmailNotifier(Observer):
    def update(self, state):
        print(f"Email: State changed to {state}")

class SMSNotifier(Observer):
    def update(self, state):
        print(f"SMS: State changed to {state}")
```

### Strategy (Стратегия)

Определяет семейство алгоритмов, инкапсулирует каждый из них и делает взаимозаменяемыми.

```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass

class QuickSort(SortStrategy):
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        pivot = data[0]
        less = [x for x in data[1:] if x <= pivot]
        greater = [x for x in data[1:] if x > pivot]
        return self.sort(less) + [pivot] + self.sort(greater)

class BubbleSort(SortStrategy):
    def sort(self, data: list) -> list:
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def sort(self, data: list) -> list:
        return self._strategy.sort(data)
```

### Command (Команда)

Инкапсулирует запрос как объект.

```python
class Command(ABC):
    @abstractmethod
    def execute(self): pass
    
    @abstractmethod
    def undo(self): pass

class Light:
    def on(self): print("Light is ON")
    def off(self): print("Light is OFF")

class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self):
        self.light.on()
    
    def undo(self):
        self.light.off()

class RemoteControl:
    def __init__(self):
        self._history: list[Command] = []
    
    def execute(self, command: Command):
        command.execute()
        self._history.append(command)
    
    def undo_last(self):
        if self._history:
            self._history.pop().undo()
```

---

## Файлы семинара

```
seminar_03_oop_patterns/
├── README.md                      # Этот файл
├── examples/
│   ├── 01_solid_principles.py     # Примеры SOLID
│   ├── 02_creational_patterns.py  # Singleton, Factory, Builder
│   ├── 03_structural_patterns.py  # Adapter, Decorator, Facade
│   └── 04_behavioral_patterns.py  # Observer, Strategy, Command
└── exercises/
    └── oop_patterns_practice.md   # Практические задания
```

---

## Дополнительные материалы

- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns) — отличные визуализации паттернов
- [Python Design Patterns](https://python-patterns.guide/) — паттерны на Python
- [SOLID Principles in Python](https://realpython.com/solid-principles-python/) — подробно о SOLID
- [Паттерны проектирования (Банда четырёх)](https://ru.wikipedia.org/wiki/Design_Patterns) — классическая книга

---

## Запуск примеров

```bash
# Запуск примеров
python seminars/seminar_03_oop_patterns/examples/01_solid_principles.py
python seminars/seminar_03_oop_patterns/examples/02_creational_patterns.py
python seminars/seminar_03_oop_patterns/examples/03_structural_patterns.py
python seminars/seminar_03_oop_patterns/examples/04_behavioral_patterns.py
```
