# Практические задания: Паттерны проектирования и принципы SOLID

## Подготовка

Для работы необходим Python 3.10+. Примеры кода можно запустить следующим образом:

```bash
python seminars/seminar_03_oop_patterns/examples/01_solid_principles.py
python seminars/seminar_03_oop_patterns/examples/02_creational_patterns.py
python seminars/seminar_03_oop_patterns/examples/03_structural_patterns.py
python seminars/seminar_03_oop_patterns/examples/04_behavioral_patterns.py
```

> **Как работать с заданиями:** прочитайте условие, попробуйте ответить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: Анализ нарушений SOLID

> **Теория:** [README.md — Блок 1](../README.md#блок-1-повторение-принципов-solid-20-мин) | **Примеры:** [`examples/01_solid_principles.py`](../examples/01_solid_principles.py)

В каждом задании показан фрагмент кода. Определите, **какой принцип SOLID нарушен** и **почему**.

### Задание 1.1

```python
class Employee:
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

    def calculate_pay(self) -> float:
        return self.salary

    def save_to_database(self) -> None:
        print(f"INSERT INTO employees VALUES ('{self.name}', {self.salary})")

    def generate_report(self) -> str:
        return f"Report for {self.name}: salary = {self.salary}"

    def send_email(self, message: str) -> None:
        print(f"Sending '{message}' to {self.name}")
```

<details>
<summary>Подсказка</summary>

Сколько причин для изменения у этого класса? Что если изменится формат отчёта? Или способ отправки email? Или структура БД?

</details>

<details>
<summary>Решение</summary>

**Нарушен: S — Single Responsibility Principle**

Класс `Employee` имеет **4 ответственности**:
1. Хранение данных о сотруднике
2. Работа с базой данных (`save_to_database`)
3. Генерация отчётов (`generate_report`)
4. Отправка email (`send_email`)

Каждая из этих обязанностей — отдельная причина для изменения класса. Нужно разделить на `Employee` (данные), `EmployeeRepository` (БД), `ReportGenerator` (отчёты), `EmailService` (email).

</details>

### Задание 1.2

```python
class Shape:
    def __init__(self, shape_type: str, **kwargs):
        self.shape_type = shape_type
        self.kwargs = kwargs

    def area(self) -> float:
        if self.shape_type == "circle":
            return 3.14 * self.kwargs["radius"] ** 2
        elif self.shape_type == "rectangle":
            return self.kwargs["width"] * self.kwargs["height"]
        elif self.shape_type == "triangle":
            return 0.5 * self.kwargs["base"] * self.kwargs["height"]
        else:
            raise ValueError(f"Unknown shape: {self.shape_type}")
```

<details>
<summary>Подсказка</summary>

Что произойдёт, когда нужно добавить новую фигуру (например, трапецию)? Придётся ли менять существующий код?

</details>

<details>
<summary>Решение</summary>

**Нарушен: O — Open/Closed Principle**

Чтобы добавить новую фигуру, нужно **модифицировать** метод `area()` — добавить ещё один `elif`. Класс не открыт для расширения.

Правильный подход — абстрактный класс `Shape` с методом `area()` и отдельные подклассы `Circle`, `Rectangle`, `Triangle`, каждый со своей реализацией `area()`.

</details>

### Задание 1.3

```python
class Bird:
    def fly(self) -> str:
        return "Flying high!"

class Sparrow(Bird):
    def fly(self) -> str:
        return "Sparrow flying"

class Penguin(Bird):
    def fly(self) -> str:
        raise NotImplementedError("Penguins can't fly!")

def make_birds_fly(birds: list[Bird]) -> None:
    for bird in birds:
        print(bird.fly())  # Упадёт на пингвине!
```

<details>
<summary>Подсказка</summary>

Можно ли безопасно подставить `Penguin` туда, где ожидается `Bird`? Что произойдёт?

</details>

<details>
<summary>Решение</summary>

**Нарушен: L — Liskov Substitution Principle**

`Penguin` наследует от `Bird`, но **не может заменить** его — вызов `fly()` бросает исключение вместо возврата строки. Код, работающий с `Bird`, сломается при подстановке `Penguin`.

Решение: разделить иерархию. `Bird` с методом `move()`, `FlyingBird` и `SwimmingBird` — как показано в примерах.

</details>

### Задание 1.4

```python
from abc import ABC, abstractmethod

class MultiFunctionDevice(ABC):
    @abstractmethod
    def print_document(self, doc: str) -> None: pass

    @abstractmethod
    def scan_document(self) -> str: pass

    @abstractmethod
    def fax_document(self, doc: str, number: str) -> None: pass

    @abstractmethod
    def staple_document(self, doc: str) -> None: pass

class SimplePrinter(MultiFunctionDevice):
    def print_document(self, doc: str) -> None:
        print(f"Printing: {doc}")

    def scan_document(self) -> str:
        raise NotImplementedError("Can't scan!")

    def fax_document(self, doc: str, number: str) -> None:
        raise NotImplementedError("Can't fax!")

    def staple_document(self, doc: str) -> None:
        raise NotImplementedError("Can't staple!")
```

<details>
<summary>Подсказка</summary>

`SimplePrinter` вынужден реализовать 4 метода, но реально использует только один. Что это за принцип?

</details>

<details>
<summary>Решение</summary>

**Нарушен: I — Interface Segregation Principle**

`SimplePrinter` вынужден реализовать методы `scan_document`, `fax_document`, `staple_document`, которые ему не нужны. Интерфейс слишком «толстый».

Решение: разделить на маленькие интерфейсы — `Printable`, `Scannable`, `Faxable`, `Stapleable`. `SimplePrinter` реализует только `Printable`.

</details>

### Задание 1.5

```python
import sqlite3

class ReportService:
    def __init__(self):
        self.db = sqlite3.connect("production.db")  # Жёсткая зависимость

    def get_report(self, report_id: int) -> dict:
        cursor = self.db.execute(
            f"SELECT * FROM reports WHERE id = {report_id}"  # SQL injection!
        )
        row = cursor.fetchone()
        return {"id": row[0], "title": row[1], "data": row[2]}
```

<details>
<summary>Подсказка</summary>

`ReportService` сам создаёт подключение к конкретной БД. Можно ли протестировать этот класс без реальной базы данных?

</details>

<details>
<summary>Решение</summary>

**Нарушен: D — Dependency Inversion Principle**

`ReportService` напрямую зависит от конкретной реализации — `sqlite3.connect("production.db")`. Нельзя:
- Подменить БД для тестов (например, использовать in-memory SQLite)
- Переключиться на другую СУБД (PostgreSQL, MySQL)

Решение: принимать абстракцию `Database` через конструктор (Dependency Injection).

*Бонус:* здесь также есть SQL-injection уязвимость — `f"SELECT ... {report_id}"` вместо параметризованного запроса.

</details>

---

## Часть 2: Практика по паттернам (2 задания)

> **Теория:** [README.md — Блоки 2–4](../README.md#блок-2-порождающие-паттерны--factory-method-и-builder-10-мин) | **Примеры:** [`02_creational_patterns.py`](../examples/02_creational_patterns.py), [`03_structural_patterns.py`](../examples/03_structural_patterns.py), [`04_behavioral_patterns.py`](../examples/04_behavioral_patterns.py)

Решите **оба задания** ниже. Остальные задачи по паттернам — в разделе [Дополнительные задания](#дополнительные-задания) для тех, кто справится быстрее.

### Задание 2.1: Factory Method

Создайте фабрику уведомлений `NotificationFactory`, которая создаёт объекты уведомлений разных типов: `EmailNotification`, `SMSNotification`, `PushNotification`. Каждое уведомление должно иметь метод `send(message: str) -> str`.

<details>
<summary>Подсказка</summary>

Используйте абстрактный класс `Notification` с методом `send`. Фабрика хранит маппинг `str -> type[Notification]`.

</details>

<details>
<summary>Решение</summary>

```python
from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass


class EmailNotification(Notification):
    def send(self, message: str) -> str:
        return f"Email sent: {message}"


class SMSNotification(Notification):
    def send(self, message: str) -> str:
        return f"SMS sent: {message}"


class PushNotification(Notification):
    def send(self, message: str) -> str:
        return f"Push sent: {message}"


class NotificationFactory:
    _types: dict[str, type[Notification]] = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    @classmethod
    def create(cls, notification_type: str) -> Notification:
        notification_type = notification_type.lower()
        if notification_type not in cls._types:
            available = ", ".join(cls._types.keys())
            raise ValueError(
                f"Unknown type: {notification_type}. Available: {available}"
            )
        return cls._types[notification_type]()


# Использование
for ntype in ["email", "sms", "push"]:
    notification = NotificationFactory.create(ntype)
    print(notification.send("Hello!"))
```

</details>

### Задание 2.2: Adapter

У вас есть старая библиотека для работы с температурой в Фаренгейтах:

```python
class FahrenheitSensor:
    def get_temperature_f(self) -> float:
        return 98.6  # Имитация считывания датчика
```

Ваш код работает с интерфейсом:

```python
class TemperatureSensor(ABC):
    @abstractmethod
    def get_temperature_celsius(self) -> float:
        pass
```

Создайте адаптер `FahrenheitAdapter`, который преобразует Фаренгейты в Цельсии.

<details>
<summary>Подсказка</summary>

Формула: `celsius = (fahrenheit - 32) * 5 / 9`. Адаптер оборачивает `FahrenheitSensor` и реализует интерфейс `TemperatureSensor`.

</details>

<details>
<summary>Решение</summary>

```python
from abc import ABC, abstractmethod


class FahrenheitSensor:
    def get_temperature_f(self) -> float:
        return 98.6


class TemperatureSensor(ABC):
    @abstractmethod
    def get_temperature_celsius(self) -> float:
        pass


class FahrenheitAdapter(TemperatureSensor):
    def __init__(self, sensor: FahrenheitSensor) -> None:
        self._sensor = sensor

    def get_temperature_celsius(self) -> float:
        fahrenheit = self._sensor.get_temperature_f()
        return round((fahrenheit - 32) * 5 / 9, 2)


# Использование
sensor = FahrenheitAdapter(FahrenheitSensor())
print(f"{sensor.get_temperature_celsius()}°C")  # 37.0°C
```

</details>

---

## Часть 3: Ситуационные задачи (Chat Polls)

> **Теория:** [README.md — Блоки 2–4](../README.md#блок-2-порождающие-паттерны--factory-method-и-builder-10-мин) | **Примеры:** [`02_creational_patterns.py`](../examples/02_creational_patterns.py), [`03_structural_patterns.py`](../examples/03_structural_patterns.py), [`04_behavioral_patterns.py`](../examples/04_behavioral_patterns.py)

> Этот раздел используется преподавателем для интерактива в чате. Зачитывается ситуация, студенты голосуют за вариант ответа.

---

### Ситуация 1

> Вы разрабатываете систему уведомлений. Пользователь может получать уведомления по Email, SMS и Push. Способ отправки должен **легко переключаться в runtime** — например, пользователь сменил настройки с Email на SMS.

Какой паттерн лучше всего подойдёт?

- A) Observer
- B) Factory Method
- C) Strategy
- D) Decorator

<details>
<summary>Ответ</summary>

**C) Strategy**

Ключевое слово — «переключаться в runtime». Strategy позволяет менять алгоритм (способ отправки) на лету, не меняя код клиента.

Observer тоже связан с уведомлениями, но он решает другую задачу — оповещение множества подписчиков об одном событии.

</details>

---

### Ситуация 2

> В интернет-магазине нужно поддерживать генерацию чеков в разных форматах: PDF, HTML, JSON. Формат выбирается **на основе настроек пользователя**, и в будущем могут добавиться новые форматы.

Какой паттерн лучше всего подойдёт?

- A) Builder
- B) Adapter
- C) Decorator
- D) Factory Method

<details>
<summary>Ответ</summary>

**D) Factory Method**

Нужно создавать объекты разных типов (форматов чеков) на основе входного параметра. Factory Method инкапсулирует логику создания и позволяет легко добавлять новые форматы.

</details>

---

### Ситуация 3

> Вы интегрируете стороннюю библиотеку для отправки SMS. Её интерфейс (`send_sms(phone, text)`) отличается от вашего стандартного интерфейса `MessageSender.send(recipient, message)`. Менять стороннюю библиотеку нельзя.

Какой паттерн лучше всего подойдёт?

- A) Strategy
- B) Adapter
- C) Observer
- D) Builder

<details>
<summary>Ответ</summary>

**B) Adapter**

Классическая ситуация для Adapter — нужно «перевести» один интерфейс в другой, чтобы несовместимые компоненты могли работать вместе. Мы не можем менять стороннюю библиотеку, поэтому оборачиваем её в адаптер.

</details>

---

### Ситуация 4

> В системе логирования к каждому сообщению нужно **опционально** добавлять: временную метку, уровень важности, цветовую подсветку, шифрование. Пользователь может выбрать **любую комбинацию** этих добавок.

Какой паттерн лучше всего подойдёт?

- A) Decorator
- B) Builder
- C) Strategy
- D) Factory Method

<details>
<summary>Ответ</summary>

**A) Decorator**

Ключевое слово — «любая комбинация». Decorator позволяет динамически оборачивать объект в произвольное количество «слоёв», каждый из которых добавляет функциональность.

Builder тоже собирает объект пошагово, но он создаёт объект один раз. Decorator добавляет поведение к уже существующему объекту.

</details>

---

### Ситуация 5

> Биржевая система должна отслеживать изменение цены акции. Когда цена меняется, **несколько независимых компонентов** должны среагировать: обновить график, отправить алерт трейдеру, записать в лог, пересчитать портфель.

Какой паттерн лучше всего подойдёт?

- A) Strategy
- B) Observer
- C) Adapter
- D) Factory Method

<details>
<summary>Ответ</summary>

**B) Observer**

Ключевое слово — «несколько независимых компонентов должны среагировать». Observer реализует модель «один-ко-многим»: один издатель (цена акции) уведомляет множество подписчиков (график, алерт, лог, портфель).

</details>

---

### Ситуация 6

> Вы проектируете API для создания HTTP-запроса. Запрос может содержать URL, метод, заголовки, тело, query-параметры, timeout — но **большинство параметров опциональные**. Хочется удобный интерфейс для создания запросов.

Какой паттерн лучше всего подойдёт?

- A) Factory Method
- B) Observer
- C) Builder
- D) Adapter

<details>
<summary>Ответ</summary>

**C) Builder**

Ключевое слово — «множество опциональных параметров» и «удобный интерфейс». Builder с fluent interface позволяет пошагово собирать сложный объект, указывая только нужные параметры.

Пример из реальной жизни: `requests` библиотека в Python, `HttpRequest.Builder` в Java.

</details>

---

### Ситуация 7 (bonus — сложная)

> Мобильное приложение для фитнеса отправляет поздравления пользователю при достижении целей. Поздравление может быть отправлено через Push, Email или In-App. При этом к поздравлению можно **добавить GIF-анимацию, ссылку на соцсеть и кастомный текст**. Способ отправки выбирается один раз при настройке, а добавки — произвольные.

Какие паттерны здесь уместно скомбинировать?

- A) Strategy + Decorator
- B) Factory Method + Observer
- C) Builder + Adapter
- D) Observer + Strategy

<details>
<summary>Ответ</summary>

**A) Strategy + Decorator**

- **Strategy** — для выбора способа отправки (Push / Email / In-App)
- **Decorator** — для произвольной комбинации добавок (GIF, ссылка, кастомный текст)

Каждый паттерн решает свою часть задачи: Strategy отвечает за «как отправить», Decorator — за «что добавить к сообщению».

</details>

---

## Дополнительные задания

> **Теория:** [README.md — Блоки 2–4](../README.md#блок-2-порождающие-паттерны--factory-method-и-builder-10-мин) | **Примеры:** [`02_creational_patterns.py`](../examples/02_creational_patterns.py), [`03_structural_patterns.py`](../examples/03_structural_patterns.py), [`04_behavioral_patterns.py`](../examples/04_behavioral_patterns.py)

> Если вы справились с основными заданиями и у вас осталось время — попробуйте решить задачи ниже. Они более объёмные и потребуют написания кода с нуля.

### Задание Д.1: Builder

Создайте `QueryBuilder` для построения SQL-запросов с fluent interface. Поддержите:
- `select(*columns)` — выбор колонок
- `from_table(table)` — указание таблицы
- `where(condition)` — условие фильтрации
- `order_by(column)` — сортировка
- `limit(n)` — ограничение количества строк
- `build()` — возврат готовой строки запроса

<details>
<summary>Подсказка</summary>

Каждый метод возвращает `self` (fluent interface). В `build()` собираете итоговую строку из накопленных частей.

</details>

<details>
<summary>Решение</summary>

```python
class QueryBuilder:
    def __init__(self) -> None:
        self._columns: list[str] = ["*"]
        self._table: str = ""
        self._conditions: list[str] = []
        self._order: str = ""
        self._limit: int | None = None

    def select(self, *columns: str) -> "QueryBuilder":
        self._columns = list(columns) if columns else ["*"]
        return self

    def from_table(self, table: str) -> "QueryBuilder":
        self._table = table
        return self

    def where(self, condition: str) -> "QueryBuilder":
        self._conditions.append(condition)
        return self

    def order_by(self, column: str, desc: bool = False) -> "QueryBuilder":
        direction = "DESC" if desc else "ASC"
        self._order = f"{column} {direction}"
        return self

    def limit(self, n: int) -> "QueryBuilder":
        self._limit = n
        return self

    def build(self) -> str:
        if not self._table:
            raise ValueError("Table is required")

        query = f"SELECT {', '.join(self._columns)} FROM {self._table}"

        if self._conditions:
            query += " WHERE " + " AND ".join(self._conditions)

        if self._order:
            query += f" ORDER BY {self._order}"

        if self._limit is not None:
            query += f" LIMIT {self._limit}"

        return query


# Использование
query = (
    QueryBuilder()
    .select("name", "email", "age")
    .from_table("users")
    .where("age > 18")
    .where("active = 1")
    .order_by("name")
    .limit(10)
    .build()
)
print(query)
# SELECT name, email, age FROM users WHERE age > 18 AND active = 1 ORDER BY name ASC LIMIT 10
```

</details>

### Задание Д.2: Decorator

Создайте систему декораторов для текстового сообщения:
- `SimpleMessage` — базовое сообщение с текстом
- `TimestampDecorator` — добавляет временную метку перед текстом
- `UpperCaseDecorator` — преобразует весь текст в верхний регистр
- `BorderDecorator` — оборачивает текст в рамку из символов `*`

Декораторы должны комбинироваться в любом порядке.

<details>
<summary>Подсказка</summary>

Создайте абстрактный `Message` с методом `get_text() -> str`. Каждый декоратор принимает `Message` и добавляет свою трансформацию.

</details>

<details>
<summary>Решение</summary>

```python
from abc import ABC, abstractmethod
from datetime import datetime


class Message(ABC):
    @abstractmethod
    def get_text(self) -> str:
        pass


class SimpleMessage(Message):
    def __init__(self, text: str) -> None:
        self._text = text

    def get_text(self) -> str:
        return self._text


class MessageDecorator(Message):
    def __init__(self, message: Message) -> None:
        self._message = message

    def get_text(self) -> str:
        return self._message.get_text()


class TimestampDecorator(MessageDecorator):
    def get_text(self) -> str:
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"[{timestamp}] {self._message.get_text()}"


class UpperCaseDecorator(MessageDecorator):
    def get_text(self) -> str:
        return self._message.get_text().upper()


class BorderDecorator(MessageDecorator):
    def get_text(self) -> str:
        text = self._message.get_text()
        border = "*" * (len(text) + 4)
        return f"{border}\n* {text} *\n{border}"


# Использование — декораторы комбинируются
msg = SimpleMessage("Hello, World!")
print(msg.get_text())
# Hello, World!

msg2 = TimestampDecorator(UpperCaseDecorator(SimpleMessage("Hello")))
print(msg2.get_text())
# [14:30:00] HELLO

msg3 = BorderDecorator(TimestampDecorator(SimpleMessage("Important")))
print(msg3.get_text())
# ********************************
# * [14:30:00] Important *
# ********************************
```

</details>

### Задание Д.3: Strategy

Создайте систему расчёта стоимости доставки с разными стратегиями:
- `StandardDelivery` — фиксированная стоимость 300 руб.
- `ExpressDelivery` — 500 руб. + 50 руб. за каждый кг свыше 5 кг
- `FreeDelivery` — бесплатно при сумме заказа > 5000 руб., иначе 300 руб.

Класс `Order` должен позволять менять стратегию доставки.

<details>
<summary>Подсказка</summary>

Абстрактная стратегия `DeliveryStrategy` с методом `calculate(weight_kg: float, order_total: float) -> float`. `Order` хранит ссылку на текущую стратегию.

</details>

<details>
<summary>Решение</summary>

```python
from abc import ABC, abstractmethod


class DeliveryStrategy(ABC):
    @abstractmethod
    def calculate(self, weight_kg: float, order_total: float) -> float:
        pass


class StandardDelivery(DeliveryStrategy):
    def calculate(self, weight_kg: float, order_total: float) -> float:
        return 300.0


class ExpressDelivery(DeliveryStrategy):
    def calculate(self, weight_kg: float, order_total: float) -> float:
        base = 500.0
        if weight_kg > 5:
            base += (weight_kg - 5) * 50
        return base


class FreeDelivery(DeliveryStrategy):
    def calculate(self, weight_kg: float, order_total: float) -> float:
        return 0.0 if order_total > 5000 else 300.0


class Order:
    def __init__(self, total: float, weight_kg: float) -> None:
        self.total = total
        self.weight_kg = weight_kg
        self._delivery: DeliveryStrategy | None = None

    def set_delivery(self, strategy: DeliveryStrategy) -> None:
        self._delivery = strategy

    def delivery_cost(self) -> float:
        if not self._delivery:
            raise ValueError("No delivery strategy set")
        return self._delivery.calculate(self.weight_kg, self.total)


# Использование
order = Order(total=6000, weight_kg=8)

order.set_delivery(StandardDelivery())
print(f"Standard: {order.delivery_cost()} RUB")  # 300.0

order.set_delivery(ExpressDelivery())
print(f"Express: {order.delivery_cost()} RUB")  # 650.0

order.set_delivery(FreeDelivery())
print(f"Free: {order.delivery_cost()} RUB")  # 0.0 (total > 5000)
```

</details>

### Задание Д.4: Observer

Создайте систему мониторинга погоды:
- `WeatherStation` — субъект, у которого меняется температура
- `PhoneDisplay` — наблюдатель, выводит температуру на экран телефона
- `WebDashboard` — наблюдатель, обновляет веб-панель
- `AlertSystem` — наблюдатель, отправляет предупреждение если температура < 0

<details>
<summary>Подсказка</summary>

`WeatherStation` наследует от `Subject`, при `set_temperature` вызывает `notify`. Каждый наблюдатель реагирует по-своему.

</details>

<details>
<summary>Решение</summary>

```python
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float) -> None:
        pass


class WeatherStation:
    def __init__(self) -> None:
        self._observers: list[Observer] = []
        self._temperature: float = 0.0

    def subscribe(self, observer: Observer) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def set_temperature(self, temp: float) -> None:
        print(f"\nWeatherStation: temperature = {temp}°C")
        self._temperature = temp
        for observer in self._observers:
            observer.update(temp)


class PhoneDisplay(Observer):
    def update(self, temperature: float) -> None:
        print(f"  Phone: {temperature}°C")


class WebDashboard(Observer):
    def update(self, temperature: float) -> None:
        print(f"  Dashboard updated: {temperature}°C")


class AlertSystem(Observer):
    def update(self, temperature: float) -> None:
        if temperature < 0:
            print(f"  ALERT: Freezing temperature! ({temperature}°C)")


# Использование
station = WeatherStation()
station.subscribe(PhoneDisplay())
station.subscribe(WebDashboard())
station.subscribe(AlertSystem())

station.set_temperature(25)   # Без алерта
station.set_temperature(-5)   # С алертом
```

</details>

### Задание Д.5: Рефакторинг с применением SOLID и паттернов

Отрефакторите следующий код, используя принципы SOLID и подходящие паттерны:

```python
class OrderProcessor:
    def __init__(self):
        self.db_connection = MySQLConnection()

    def process_order(self, order_data: dict) -> bool:
        # Валидация
        if not order_data.get("items"):
            print("Validation error: No items")
            return False
        if not order_data.get("customer_email"):
            print("Validation error: No email")
            return False

        # Сохранение в БД
        self.db_connection.execute(
            f"INSERT INTO orders VALUES ({order_data})"
        )

        # Отправка email
        import smtplib
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.sendmail(
            "shop@example.com",
            order_data["customer_email"],
            f"Order confirmed: {order_data}"
        )

        # Логирование
        with open("orders.log", "a") as f:
            f.write(f"Order processed: {order_data}\n")

        return True
```

<details>
<summary>Подсказка</summary>

Этот класс нарушает SRP (4 ответственности) и DIP (жёсткая зависимость от MySQL). Разделите на несколько классов с абстракциями и используйте Dependency Injection.

</details>

<details>
<summary>Решение</summary>

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Order:
    items: list[str]
    customer_email: str
    total: float


class OrderValidator(ABC):
    @abstractmethod
    def validate(self, order: Order) -> tuple[bool, str]:
        pass


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> int:
        pass


class NotificationService(ABC):
    @abstractmethod
    def send_confirmation(self, order: Order) -> None:
        pass


class Logger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


# Реализации
class BasicValidator(OrderValidator):
    def validate(self, order: Order) -> tuple[bool, str]:
        if not order.items:
            return False, "No items"
        if not order.customer_email or "@" not in order.customer_email:
            return False, "Invalid email"
        return True, "OK"


class SQLOrderRepository(OrderRepository):
    def __init__(self, connection) -> None:
        self.connection = connection

    def save(self, order: Order) -> int:
        # Параметризованный запрос!
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO orders (items, email, total) VALUES (?, ?, ?)",
            (str(order.items), order.customer_email, order.total),
        )
        return cursor.lastrowid


class EmailNotification(NotificationService):
    def send_confirmation(self, order: Order) -> None:
        print(f"Email to {order.customer_email}: order confirmed")


class FileLogger(Logger):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def log(self, message: str) -> None:
        with open(self.filepath, "a") as f:
            f.write(f"{message}\n")


# Координатор — зависит от абстракций (DIP)
class OrderProcessor:
    def __init__(
        self,
        validator: OrderValidator,
        repository: OrderRepository,
        notification: NotificationService,
        logger: Logger,
    ) -> None:
        self.validator = validator
        self.repository = repository
        self.notification = notification
        self.logger = logger

    def process(self, order: Order) -> tuple[bool, str]:
        is_valid, message = self.validator.validate(order)
        if not is_valid:
            self.logger.log(f"Validation failed: {message}")
            return False, message

        order_id = self.repository.save(order)
        self.notification.send_confirmation(order)
        self.logger.log(f"Order {order_id} processed")
        return True, f"Order {order_id} created"
```

</details>

---

## Полезные ресурсы

- [Refactoring Guru](https://refactoring.guru/design-patterns/python) — визуализация паттернов
- [Python Patterns](https://python-patterns.guide/) — идиоматичные реализации
- [Real Python - SOLID](https://realpython.com/solid-principles-python/) — подробно о SOLID
