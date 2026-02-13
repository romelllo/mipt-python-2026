# Семинар 3: Паттерны ООП на Python для разработки приложения

**Модуль:** 2 — Объектно-ориентированное программирование и основы работы с базами данных в Python  
**Дата:** 16.02.2026  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1dNEvw8Oqo2K_PSQWNePlr4_KDWal2SAO0U9X-GEEIJw/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:
- Называть и кратко объяснять все 5 принципов SOLID
- Находить нарушения SOLID в чужом коде
- Понимать и реализовывать некоторые ключевые паттерны проектирования на Python: Factory Method, Builder, Adapter, Decorator, Strategy, Observer
- Выбирать подходящий паттерн для конкретной задачи

> **Важно:** Паттерны — мощный инструмент, но «видеть» их в собственном коде получается только с практикой. Цель семинара — познакомиться с основными паттернами, а не запомнить все сразу.

---

## Подготовка

Для этого семинара достаточно Python 3.10+ и знания основ ООП (классы, наследование, `ABC`).

```bash
# Запуск примеров
python seminars/seminar_03_oop_patterns/examples/01_solid_principles.py
python seminars/seminar_03_oop_patterns/examples/02_creational_patterns.py
python seminars/seminar_03_oop_patterns/examples/03_structural_patterns.py
python seminars/seminar_03_oop_patterns/examples/04_behavioral_patterns.py
```

---

## План семинара

Семинар построен по принципу **«теория → практика»**: после каждого блока теории вы переходите к упражнениям в файле [`exercises/oop_patterns_practice.md`](exercises/oop_patterns_practice.md).

| Время | Тема | Практика |
|-------|------|----------|
| 20 мин | Блок 1: Принципы SOLID | → Упражнения: Часть 1 (анализ кода) |
| 10 мин | Блок 2: Порождающие паттерны (Factory Method, Builder) | — |
| 10 мин | Блок 3: Структурные паттерны (Adapter, Decorator) | — |
| 10 мин | Блок 4: Поведенческие паттерны (Strategy, Observer) | → Упражнения: Часть 2 (2 задачи) |
| 20 мин | Интерактив: ситуационные задачи (Chat Polls) | → Упражнения: Часть 3 |
| 10 мин | Подведение итогов | — |

> **Примечание:** Суммарно в таблице 80 минут — оставшиеся ~10 минут отведены на переходы между блоками, вопросы и организационные моменты. После блоков теории по паттернам студенты решают **2 основные задачи** (Factory Method + Adapter). Дополнительные задачи по Builder, Decorator, Strategy и Observer доступны для тех, кто справится быстрее — см. раздел «Дополнительные задания» в файле упражнений.

---

## Блок 1: Принципы SOLID (20 мин)

SOLID — это пять принципов проектирования, которые помогают писать гибкий и поддерживаемый код:

| Буква | Принцип | Суть (одним предложением) |
|-------|---------|---------------------------|
| **S** | Single Responsibility | У класса одна причина для изменения |
| **O** | Open/Closed | Открыт для расширения, закрыт для модификации |
| **L** | Liskov Substitution | Подкласс можно подставить вместо базового класса |
| **I** | Interface Segregation | Много маленьких интерфейсов лучше одного большого |
| **D** | Dependency Inversion | Зависьте от абстракций, а не от конкретных реализаций |

### S — Single Responsibility Principle

Класс должен отвечать только за одну вещь.

```python
# Плохо: один класс делает всё
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def save_to_db(self): ...
    def send_email(self): ...
    def generate_report(self): ...

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

### O — Open/Closed Principle

Добавляем новое поведение через наследование, а не изменение существующего кода.

```python
from abc import ABC, abstractmethod

class Discount(ABC):
    @abstractmethod
    def calculate(self, price: float) -> float:
        pass

class PercentDiscount(Discount):
    def __init__(self, percent: float):
        self.percent = percent

    def calculate(self, price: float) -> float:
        return price * (1 - self.percent / 100)

# Новый тип скидки — без изменения существующего кода
class FixedDiscount(Discount):
    def __init__(self, amount: float):
        self.amount = amount

    def calculate(self, price: float) -> float:
        return max(0, price - self.amount)
```

### L — Liskov Substitution Principle

Подклассы должны быть взаимозаменяемы с базовым классом без неожиданного поведения.

```python
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

# Пингвин — птица, но не летает. Решаем через правильную иерархию.
class Penguin(SwimmingBird):
    pass
```

### I — Interface Segregation Principle

Не заставляйте класс реализовывать методы, которые ему не нужны.

```python
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

### D — Dependency Inversion Principle

Зависьте от абстракций, а не от конкретных реализаций.

```python
class Database(ABC):
    @abstractmethod
    def execute(self, query: str): pass

class UserService:
    def __init__(self, db: Database):  # Инъекция зависимости
        self.db = db
```

> **Подробнее:** см. файл [`examples/01_solid_principles.py`](examples/01_solid_principles.py) — полные примеры всех пяти принципов с демонстрацией.

### Практика

Перейдите к файлу [`exercises/oop_patterns_practice.md`](exercises/oop_patterns_practice.md) и выполните **Часть 1: Анализ нарушений SOLID** (задания 1.1–1.5). Вам будут показаны фрагменты кода — определите, какой принцип нарушен и почему.

---

## Блок 2: Порождающие паттерны — Factory Method и Builder (10 мин)

Порождающие паттерны отвечают за **создание объектов**.

### Factory Method (Фабричный метод)

**Проблема:** Код создания объектов разбросан по всей программе. При добавлении нового типа нужно менять код во многих местах.

**Решение:** Выносим создание объектов в отдельный метод/класс.

```python
from abc import ABC, abstractmethod

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
    _types: dict[str, type[Document]] = {
        "pdf": PDFDocument,
        "html": HTMLDocument,
    }

    @classmethod
    def create(cls, doc_type: str) -> Document:
        if doc_type not in cls._types:
            raise ValueError(f"Unknown type: {doc_type}")
        return cls._types[doc_type]()

# Использование
doc = DocumentFactory.create("pdf")
print(doc.render())  # "Rendering PDF"
```

**Когда использовать:** Вы не знаете заранее, какой именно объект нужно создать — решение принимается в runtime.

### Builder (Строитель)

**Проблема:** Конструктор класса принимает слишком много параметров. Часть из них опциональная. Создание объекта превращается в нечитаемый вызов.

**Решение:** Собираем объект пошагово через цепочку вызовов (fluent interface).

```python
from dataclasses import dataclass, field

@dataclass
class Pizza:
    size: str = ""
    cheese: bool = False
    pepperoni: bool = False
    mushrooms: bool = False

class PizzaBuilder:
    def __init__(self):
        self._pizza = Pizza()

    def set_size(self, size: str) -> "PizzaBuilder":
        self._pizza.size = size
        return self  # Возвращаем self для цепочки

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

**Когда использовать:** Объект сложный, с множеством опциональных параметров.

> **Подробнее:** см. файл [`examples/02_creational_patterns.py`](examples/02_creational_patterns.py) — Factory Method и Builder с полными примерами.

### Практика

После блока 4 вы выполните задание 2.1 (Factory Method) из **Части 2** файла [`exercises/oop_patterns_practice.md`](exercises/oop_patterns_practice.md).

---

## Блок 3: Структурные паттерны — Adapter и Decorator (10 мин)

Структурные паттерны отвечают за **компоновку объектов** в более крупные структуры.

### Adapter (Адаптер)

**Проблема:** Нужно использовать существующий класс, но его интерфейс не подходит к вашему коду.

**Решение:** Создаём обёртку, которая переводит один интерфейс в другой.

```python
# Старая система — работает с копейками
class OldPaymentSystem:
    def make_payment(self, amount_kopecks: int) -> str:
        return f"Paid {amount_kopecks} kopecks"

# Новый интерфейс — работает с рублями
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount_rubles: float) -> str:
        pass

# Адаптер: рубли → копейки
class PaymentAdapter(PaymentProcessor):
    def __init__(self, old_system: OldPaymentSystem):
        self._old_system = old_system

    def pay(self, amount_rubles: float) -> str:
        kopecks = int(amount_rubles * 100)
        return self._old_system.make_payment(kopecks)
```

**Когда использовать:** Интеграция с legacy-кодом или внешними библиотеками с неподходящим интерфейсом.

### Decorator (Декоратор)

**Проблема:** Нужно добавлять объекту новые обязанности, не изменяя его класс. При этом комбинации могут быть произвольными.

**Решение:** Оборачиваем объект в декораторы, каждый из которых добавляет свою функциональность.

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
        return self._coffee.cost() + 30.0

    def description(self) -> str:
        return f"{self._coffee.description()} + Milk"

# Использование: декораторы комбинируются
coffee = MilkDecorator(SimpleCoffee())
print(coffee.description())  # "Coffee + Milk"
print(coffee.cost())         # 130.0
```

**Когда использовать:** Нужно динамически комбинировать поведение объекта из «кирпичиков».

> **Подробнее:** см. файл [`examples/03_structural_patterns.py`](examples/03_structural_patterns.py) — Adapter и Decorator с развёрнутыми примерами.

### Практика

После блока 4 вы выполните задание 2.2 (Adapter) из **Части 2** файла [`exercises/oop_patterns_practice.md`](exercises/oop_patterns_practice.md).

---

## Блок 4: Поведенческие паттерны — Strategy и Observer (10 мин)

Поведенческие паттерны отвечают за **взаимодействие между объектами** и распределение обязанностей.

### Strategy (Стратегия)

**Проблема:** В коде много `if/elif/else`, которые выбирают алгоритм. При добавлении нового алгоритма нужно менять существующий код.

**Решение:** Выносим каждый алгоритм в отдельный класс с общим интерфейсом. Алгоритм можно менять в runtime.

```python
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f"Paid {amount} by Credit Card"

class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f"Paid {amount} via PayPal"

class ShoppingCart:
    def __init__(self):
        self._strategy: PaymentStrategy | None = None

    def set_payment(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    def checkout(self, amount: float) -> str:
        if not self._strategy:
            return "No payment method selected"
        return self._strategy.pay(amount)

# Стратегию можно менять в runtime
cart = ShoppingCart()
cart.set_payment(CreditCardPayment())
print(cart.checkout(5000))  # "Paid 5000 by Credit Card"
cart.set_payment(PayPalPayment())
print(cart.checkout(5000))  # "Paid 5000 via PayPal"
```

**Когда использовать:** Нужно выбирать между несколькими взаимозаменяемыми алгоритмами, особенно в runtime.

### Observer (Наблюдатель)

**Проблема:** При изменении состояния одного объекта нужно оповестить множество других объектов. Жёсткая связь между ними делает код хрупким.

**Решение:** Объект-издатель хранит список подписчиков и уведомляет их об изменениях.

```python
class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass

class NewsAgency:
    def __init__(self):
        self._subscribers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        self._subscribers.append(observer)

    def publish(self, news: str) -> None:
        for subscriber in self._subscribers:
            subscriber.update(news)

class EmailSubscriber(Observer):
    def __init__(self, email: str):
        self.email = email

    def update(self, message: str) -> None:
        print(f"Email to {self.email}: {message}")

class SMSSubscriber(Observer):
    def __init__(self, phone: str):
        self.phone = phone

    def update(self, message: str) -> None:
        print(f"SMS to {self.phone}: {message}")

# Использование
agency = NewsAgency()
agency.subscribe(EmailSubscriber("user@example.com"))
agency.subscribe(SMSSubscriber("+7-999-123-4567"))
agency.publish("Breaking News!")
# Email to user@example.com: Breaking News!
# SMS to +7-999-123-4567: Breaking News!
```

**Когда использовать:** Один объект должен уведомлять множество других о своих изменениях (событийная модель).

> **Подробнее:** см. файл [`examples/04_behavioral_patterns.py`](examples/04_behavioral_patterns.py) — Strategy и Observer с полными примерами.

### Практика

Перейдите к файлу [`exercises/oop_patterns_practice.md`](exercises/oop_patterns_practice.md) и выполните **Часть 2: Практика по паттернам** (задания 2.1–2.2). Это два коротких задания на Factory Method и Adapter.

> Если останется время — в разделе «Дополнительные задания» есть задачи на Builder, Decorator, Strategy и Observer.

---

## Интерактив: Chat Polls (20 мин)

Преподаватель зачитывает ситуации из реального мира разработки. Студенты голосуют в чате, какой паттерн лучше подходит.

> Ситуации и варианты ответов находятся в файле [`exercises/oop_patterns_practice.md`](exercises/oop_patterns_practice.md), **Часть 3: Ситуационные задачи (Chat Polls)**.

---

## Подведение итогов (10 мин)

### Шпаргалка по паттернам

| Группа | Паттерн | Решает проблему |
|--------|---------|----------------|
| Порождающие | **Factory Method** | Создание объектов без привязки к конкретным классам |
| Порождающие | **Builder** | Пошаговое создание сложных объектов |
| Структурные | **Adapter** | Несовместимые интерфейсы |
| Структурные | **Decorator** | Динамическое добавление функциональности |
| Поведенческие | **Strategy** | Выбор алгоритма в runtime |
| Поведенческие | **Observer** | Уведомление множества объектов об изменениях |

### Главная мысль

Паттерны — это **словарь** для общения между разработчиками. Вы не обязаны запоминать все детали реализации прямо сейчас. Важнее:

1. **Знать, что такой паттерн существует** — чтобы узнать его при встрече
2. **Понимать, какую проблему он решает** — чтобы вспомнить о нём в нужный момент
3. **Практиковаться** — распознавание паттернов приходит с опытом написания и чтения кода

> «Знание паттернов без практики — как знание рецептов без готовки. Полезно, но не сделает вас шефом.»

---

## Файлы семинара

В папке `examples/`:
- [`01_solid_principles.py`](examples/01_solid_principles.py) — все 5 принципов SOLID с демонстрацией
- [`02_creational_patterns.py`](examples/02_creational_patterns.py) — Factory Method и Builder
- [`03_structural_patterns.py`](examples/03_structural_patterns.py) — Adapter и Decorator
- [`04_behavioral_patterns.py`](examples/04_behavioral_patterns.py) — Strategy и Observer

В папке `exercises/`:
- [`oop_patterns_practice.md`](exercises/oop_patterns_practice.md) — анализ SOLID, 2 задачи по паттернам, ситуационные задачи (Chat Polls) и дополнительные задания

---

## Дополнительные материалы

- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns) — отличные визуализации паттернов
- [Python Design Patterns](https://python-patterns.guide/) — паттерны на Python
- [SOLID Principles in Python](https://realpython.com/solid-principles-python/) — подробно о SOLID
- [Паттерны проектирования (Банда четырёх)](https://ru.wikipedia.org/wiki/Design_Patterns) — классическая книга
