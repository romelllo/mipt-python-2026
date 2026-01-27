# Практические задания: Паттерны проектирования ООП

## Задание 1: Принципы SOLID (SRP + DIP)

### Условие

Рефакторингом исправьте нарушения принципов SOLID в следующем коде:

```python
class OrderProcessor:
    def __init__(self):
        self.db_connection = MySQLConnection()  # Жёсткая зависимость
    
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

### Требования

1. Разделите класс на несколько классов с единственной ответственностью
2. Используйте абстракции (ABC) для зависимостей
3. Примените Dependency Injection

<details>
<summary>Решение</summary>

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


# Модель данных
@dataclass
class Order:
    items: list[str]
    customer_email: str
    total: float


# Абстракции
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
class BasicOrderValidator(OrderValidator):
    def validate(self, order: Order) -> tuple[bool, str]:
        if not order.items:
            return False, "No items in order"
        if not order.customer_email:
            return False, "No customer email"
        if "@" not in order.customer_email:
            return False, "Invalid email format"
        return True, "OK"


class SQLOrderRepository(OrderRepository):
    def __init__(self, connection) -> None:
        self.connection = connection
    
    def save(self, order: Order) -> int:
        # Безопасное сохранение с параметризованными запросами
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO orders (items, email, total) VALUES (?, ?, ?)",
            (str(order.items), order.customer_email, order.total)
        )
        return cursor.lastrowid


class EmailNotificationService(NotificationService):
    def __init__(self, smtp_host: str, smtp_port: int) -> None:
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
    
    def send_confirmation(self, order: Order) -> None:
        print(f"Sending email to {order.customer_email}")
        # Реальная отправка email


class FileLogger(Logger):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
    
    def log(self, message: str) -> None:
        with open(self.filepath, "a") as f:
            f.write(f"{message}\n")


# Координатор (использует DIP)
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
        # Валидация
        is_valid, message = self.validator.validate(order)
        if not is_valid:
            self.logger.log(f"Validation failed: {message}")
            return False, message
        
        # Сохранение
        order_id = self.repository.save(order)
        
        # Уведомление
        self.notification.send_confirmation(order)
        
        # Логирование
        self.logger.log(f"Order {order_id} processed successfully")
        
        return True, f"Order {order_id} created"


# Использование
if __name__ == "__main__":
    # Легко подменить реализации для тестирования
    processor = OrderProcessor(
        validator=BasicOrderValidator(),
        repository=SQLOrderRepository(connection=None),  # Mock
        notification=EmailNotificationService("smtp.example.com", 587),
        logger=FileLogger("orders.log"),
    )
    
    order = Order(
        items=["Laptop", "Mouse"],
        customer_email="user@example.com",
        total=90000.0,
    )
    
    success, message = processor.process(order)
    print(f"Result: {success}, {message}")
```

</details>

---

## Задание 2: Паттерн Factory Method

### Условие

Создайте систему для генерации отчётов в разных форматах (PDF, Excel, HTML).

### Требования

1. Используйте паттерн Factory Method
2. Реализуйте минимум 3 типа отчётов
3. Добавьте возможность регистрации новых типов отчётов

<details>
<summary>Решение</summary>

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ReportData:
    title: str
    headers: list[str]
    rows: list[list[str]]


class Report(ABC):
    @abstractmethod
    def generate(self, data: ReportData) -> str:
        pass
    
    @abstractmethod
    def get_extension(self) -> str:
        pass


class PDFReport(Report):
    def generate(self, data: ReportData) -> str:
        content = f"=== PDF: {data.title} ===\n"
        content += " | ".join(data.headers) + "\n"
        content += "-" * 40 + "\n"
        for row in data.rows:
            content += " | ".join(row) + "\n"
        return content
    
    def get_extension(self) -> str:
        return "pdf"


class ExcelReport(Report):
    def generate(self, data: ReportData) -> str:
        content = f"Excel Workbook: {data.title}\n"
        content += f"Sheet1: {','.join(data.headers)}\n"
        for i, row in enumerate(data.rows, 1):
            content += f"Row {i}: {','.join(row)}\n"
        return content
    
    def get_extension(self) -> str:
        return "xlsx"


class HTMLReport(Report):
    def generate(self, data: ReportData) -> str:
        html = f"<html><head><title>{data.title}</title></head><body>\n"
        html += f"<h1>{data.title}</h1>\n<table border='1'>\n"
        html += "<tr>" + "".join(f"<th>{h}</th>" for h in data.headers) + "</tr>\n"
        for row in data.rows:
            html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>\n"
        html += "</table></body></html>"
        return html
    
    def get_extension(self) -> str:
        return "html"


class ReportFactory:
    _report_types: dict[str, type[Report]] = {
        "pdf": PDFReport,
        "excel": ExcelReport,
        "html": HTMLReport,
    }
    
    @classmethod
    def register(cls, name: str, report_class: type[Report]) -> None:
        cls._report_types[name.lower()] = report_class
    
    @classmethod
    def create(cls, report_type: str) -> Report:
        report_type = report_type.lower()
        if report_type not in cls._report_types:
            available = ", ".join(cls._report_types.keys())
            raise ValueError(f"Unknown type: {report_type}. Available: {available}")
        return cls._report_types[report_type]()
    
    @classmethod
    def available_types(cls) -> list[str]:
        return list(cls._report_types.keys())


# Использование
if __name__ == "__main__":
    data = ReportData(
        title="Sales Report Q4 2024",
        headers=["Product", "Quantity", "Revenue"],
        rows=[
            ["Laptop", "150", "$225,000"],
            ["Phone", "500", "$350,000"],
            ["Tablet", "200", "$100,000"],
        ],
    )
    
    for report_type in ReportFactory.available_types():
        report = ReportFactory.create(report_type)
        print(f"\n--- {report_type.upper()} Report ---")
        print(report.generate(data))
```

</details>

---

## Задание 3: Паттерн Builder

### Условие

Создайте Builder для конфигурации HTTP-запроса с поддержкой:
- URL, метода (GET, POST, PUT, DELETE)
- Заголовков (headers)
- Query-параметров
- Body (для POST/PUT)
- Timeout

### Требования

1. Fluent interface (цепочка вызовов)
2. Валидация при build()
3. Создайте Director с предустановленными конфигурациями

<details>
<summary>Решение</summary>

```python
from dataclasses import dataclass, field
from enum import Enum


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class HTTPRequest:
    url: str
    method: HTTPMethod
    headers: dict[str, str] = field(default_factory=dict)
    params: dict[str, str] = field(default_factory=dict)
    body: str | dict | None = None
    timeout: int = 30
    
    def __str__(self) -> str:
        lines = [
            f"{self.method.value} {self.url}",
            f"Headers: {self.headers}",
            f"Params: {self.params}",
            f"Body: {self.body}",
            f"Timeout: {self.timeout}s",
        ]
        return "\n".join(lines)


class HTTPRequestBuilder:
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> "HTTPRequestBuilder":
        self._url: str = ""
        self._method: HTTPMethod = HTTPMethod.GET
        self._headers: dict[str, str] = {}
        self._params: dict[str, str] = {}
        self._body: str | dict | None = None
        self._timeout: int = 30
        return self
    
    def url(self, url: str) -> "HTTPRequestBuilder":
        self._url = url
        return self
    
    def method(self, method: HTTPMethod) -> "HTTPRequestBuilder":
        self._method = method
        return self
    
    def get(self, url: str) -> "HTTPRequestBuilder":
        return self.url(url).method(HTTPMethod.GET)
    
    def post(self, url: str) -> "HTTPRequestBuilder":
        return self.url(url).method(HTTPMethod.POST)
    
    def put(self, url: str) -> "HTTPRequestBuilder":
        return self.url(url).method(HTTPMethod.PUT)
    
    def delete(self, url: str) -> "HTTPRequestBuilder":
        return self.url(url).method(HTTPMethod.DELETE)
    
    def header(self, key: str, value: str) -> "HTTPRequestBuilder":
        self._headers[key] = value
        return self
    
    def headers(self, headers: dict[str, str]) -> "HTTPRequestBuilder":
        self._headers.update(headers)
        return self
    
    def param(self, key: str, value: str) -> "HTTPRequestBuilder":
        self._params[key] = value
        return self
    
    def params(self, params: dict[str, str]) -> "HTTPRequestBuilder":
        self._params.update(params)
        return self
    
    def body(self, body: str | dict) -> "HTTPRequestBuilder":
        self._body = body
        return self
    
    def json(self, data: dict) -> "HTTPRequestBuilder":
        self._body = data
        self._headers["Content-Type"] = "application/json"
        return self
    
    def timeout(self, seconds: int) -> "HTTPRequestBuilder":
        self._timeout = seconds
        return self
    
    def auth_bearer(self, token: str) -> "HTTPRequestBuilder":
        self._headers["Authorization"] = f"Bearer {token}"
        return self
    
    def build(self) -> HTTPRequest:
        # Валидация
        if not self._url:
            raise ValueError("URL is required")
        
        if self._method in (HTTPMethod.POST, HTTPMethod.PUT) and self._body is None:
            raise ValueError(f"{self._method.value} requests should have a body")
        
        if self._method == HTTPMethod.GET and self._body is not None:
            raise ValueError("GET requests should not have a body")
        
        request = HTTPRequest(
            url=self._url,
            method=self._method,
            headers=self._headers.copy(),
            params=self._params.copy(),
            body=self._body,
            timeout=self._timeout,
        )
        self.reset()
        return request


class HTTPRequestDirector:
    def __init__(self, builder: HTTPRequestBuilder) -> None:
        self._builder = builder
    
    def api_get(self, url: str, token: str) -> HTTPRequest:
        """Стандартный GET-запрос к API."""
        return (
            self._builder.reset()
            .get(url)
            .header("Accept", "application/json")
            .auth_bearer(token)
            .timeout(10)
            .build()
        )
    
    def api_post(self, url: str, data: dict, token: str) -> HTTPRequest:
        """Стандартный POST-запрос к API."""
        return (
            self._builder.reset()
            .post(url)
            .json(data)
            .auth_bearer(token)
            .timeout(30)
            .build()
        )
    
    def file_upload(self, url: str, token: str) -> HTTPRequest:
        """Запрос для загрузки файла."""
        return (
            self._builder.reset()
            .post(url)
            .header("Content-Type", "multipart/form-data")
            .auth_bearer(token)
            .timeout(120)
            .body("file_content_placeholder")
            .build()
        )


# Использование
if __name__ == "__main__":
    builder = HTTPRequestBuilder()
    director = HTTPRequestDirector(builder)
    
    # Использование директора
    print("=== API GET ===")
    request = director.api_get("https://api.example.com/users", "my_token")
    print(request)
    
    print("\n=== API POST ===")
    request = director.api_post(
        "https://api.example.com/users",
        {"name": "Alice", "email": "alice@example.com"},
        "my_token"
    )
    print(request)
    
    # Ручная сборка
    print("\n=== Custom Request ===")
    request = (
        builder.reset()
        .put("https://api.example.com/users/123")
        .json({"name": "Bob"})
        .header("X-Custom", "value")
        .param("notify", "true")
        .auth_bearer("custom_token")
        .timeout(60)
        .build()
    )
    print(request)
```

</details>

---

## Задание 4: Паттерн Decorator

### Условие

Создайте систему декораторов для текстового сообщения:
- Шифрование (Base64)
- Сжатие (имитация)
- Добавление временной метки
- Добавление подписи

### Требования

1. Декораторы должны быть комбинируемыми
2. Порядок декораторов должен влиять на результат
3. Реализуйте метод для получения описания всех применённых трансформаций

<details>
<summary>Решение</summary>

```python
from abc import ABC, abstractmethod
from base64 import b64encode, b64decode
from datetime import datetime


class Message(ABC):
    @abstractmethod
    def get_content(self) -> str:
        pass
    
    @abstractmethod
    def get_transformations(self) -> list[str]:
        pass


class SimpleMessage(Message):
    def __init__(self, content: str) -> None:
        self._content = content
    
    def get_content(self) -> str:
        return self._content
    
    def get_transformations(self) -> list[str]:
        return ["Original"]


class MessageDecorator(Message):
    def __init__(self, message: Message) -> None:
        self._message = message
    
    def get_content(self) -> str:
        return self._message.get_content()
    
    def get_transformations(self) -> list[str]:
        return self._message.get_transformations()


class EncryptionDecorator(MessageDecorator):
    def get_content(self) -> str:
        content = self._message.get_content()
        encoded = b64encode(content.encode()).decode()
        return encoded
    
    def get_transformations(self) -> list[str]:
        return self._message.get_transformations() + ["Base64 Encrypted"]
    
    @staticmethod
    def decrypt(encoded: str) -> str:
        return b64decode(encoded.encode()).decode()


class CompressionDecorator(MessageDecorator):
    def get_content(self) -> str:
        content = self._message.get_content()
        # Имитация сжатия (в реальности использовался бы zlib)
        return f"[COMPRESSED:{len(content)}]{content[:20]}..."
    
    def get_transformations(self) -> list[str]:
        return self._message.get_transformations() + ["Compressed"]


class TimestampDecorator(MessageDecorator):
    def get_content(self) -> str:
        content = self._message.get_content()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {content}"
    
    def get_transformations(self) -> list[str]:
        return self._message.get_transformations() + ["Timestamped"]


class SignatureDecorator(MessageDecorator):
    def __init__(self, message: Message, signature: str) -> None:
        super().__init__(message)
        self._signature = signature
    
    def get_content(self) -> str:
        content = self._message.get_content()
        return f"{content}\n\n-- {self._signature}"
    
    def get_transformations(self) -> list[str]:
        return self._message.get_transformations() + [f"Signed by '{self._signature}'"]


class HTMLFormattingDecorator(MessageDecorator):
    def get_content(self) -> str:
        content = self._message.get_content()
        # Простое HTML-форматирование
        content = content.replace("\n", "<br>\n")
        return f"<div class='message'>{content}</div>"
    
    def get_transformations(self) -> list[str]:
        return self._message.get_transformations() + ["HTML Formatted"]


# Использование
if __name__ == "__main__":
    # Простое сообщение
    message = SimpleMessage("Hello, World! This is a secret message.")
    print("=== Original ===")
    print(f"Content: {message.get_content()}")
    print(f"Transformations: {message.get_transformations()}")
    
    # С временной меткой и подписью
    print("\n=== Timestamp + Signature ===")
    decorated = SignatureDecorator(
        TimestampDecorator(message),
        "John Doe"
    )
    print(f"Content:\n{decorated.get_content()}")
    print(f"Transformations: {decorated.get_transformations()}")
    
    # Шифрование
    print("\n=== Encrypted ===")
    encrypted = EncryptionDecorator(message)
    print(f"Content: {encrypted.get_content()}")
    print(f"Decrypted: {EncryptionDecorator.decrypt(encrypted.get_content())}")
    
    # Комбинация: подпись -> метка -> шифрование
    print("\n=== Full Pipeline ===")
    full = EncryptionDecorator(
        TimestampDecorator(
            SignatureDecorator(message, "Alice")
        )
    )
    print(f"Content: {full.get_content()}")
    print(f"Transformations: {' -> '.join(full.get_transformations())}")
    
    # Порядок важен: шифрование -> подпись -> метка
    print("\n=== Different Order ===")
    different_order = TimestampDecorator(
        SignatureDecorator(
            EncryptionDecorator(message),
            "Bob"
        )
    )
    print(f"Content:\n{different_order.get_content()}")
    print(f"Transformations: {' -> '.join(different_order.get_transformations())}")
```

</details>

---

## Задание 5: Паттерн Observer

### Условие

Создайте систему мониторинга сервера с разными типами уведомлений:
- Email-уведомления
- SMS-уведомления
- Slack-уведомления
- Запись в лог

### Требования

1. Сервер может отправлять разные типы событий (CPU high, Memory high, Disk full, Service down)
2. Каждый подписчик может фильтровать события по типу
3. Добавьте приоритеты событий (info, warning, critical)

<details>
<summary>Решение</summary>

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EventPriority(Enum):
    INFO = 1
    WARNING = 2
    CRITICAL = 3


class EventType(Enum):
    CPU_HIGH = "cpu_high"
    MEMORY_HIGH = "memory_high"
    DISK_FULL = "disk_full"
    SERVICE_DOWN = "service_down"
    SERVICE_UP = "service_up"


@dataclass
class ServerEvent:
    event_type: EventType
    priority: EventPriority
    message: str
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def __str__(self) -> str:
        return f"[{self.priority.name}] {self.event_type.value}: {self.message}"


class AlertSubscriber(ABC):
    def __init__(
        self,
        event_types: list[EventType] | None = None,
        min_priority: EventPriority = EventPriority.INFO,
    ) -> None:
        self.event_types = event_types  # None = все типы
        self.min_priority = min_priority
    
    def should_handle(self, event: ServerEvent) -> bool:
        # Проверка приоритета
        if event.priority.value < self.min_priority.value:
            return False
        # Проверка типа события
        if self.event_types is not None and event.event_type not in self.event_types:
            return False
        return True
    
    @abstractmethod
    def handle(self, event: ServerEvent) -> None:
        pass


class EmailAlert(AlertSubscriber):
    def __init__(
        self,
        email: str,
        event_types: list[EventType] | None = None,
        min_priority: EventPriority = EventPriority.WARNING,
    ) -> None:
        super().__init__(event_types, min_priority)
        self.email = email
    
    def handle(self, event: ServerEvent) -> None:
        if not self.should_handle(event):
            return
        print(f"  📧 Email to {self.email}: {event}")


class SMSAlert(AlertSubscriber):
    def __init__(
        self,
        phone: str,
        event_types: list[EventType] | None = None,
        min_priority: EventPriority = EventPriority.CRITICAL,
    ) -> None:
        super().__init__(event_types, min_priority)
        self.phone = phone
    
    def handle(self, event: ServerEvent) -> None:
        if not self.should_handle(event):
            return
        print(f"  📱 SMS to {self.phone}: {event}")


class SlackAlert(AlertSubscriber):
    def __init__(
        self,
        channel: str,
        event_types: list[EventType] | None = None,
        min_priority: EventPriority = EventPriority.INFO,
    ) -> None:
        super().__init__(event_types, min_priority)
        self.channel = channel
    
    def handle(self, event: ServerEvent) -> None:
        if not self.should_handle(event):
            return
        emoji = {"INFO": "ℹ️", "WARNING": "⚠️", "CRITICAL": "🚨"}
        print(f"  💬 Slack #{self.channel}: {emoji[event.priority.name]} {event}")


class LogAlert(AlertSubscriber):
    def __init__(
        self,
        filepath: str,
        event_types: list[EventType] | None = None,
        min_priority: EventPriority = EventPriority.INFO,
    ) -> None:
        super().__init__(event_types, min_priority)
        self.filepath = filepath
    
    def handle(self, event: ServerEvent) -> None:
        if not self.should_handle(event):
            return
        print(f"  📝 Log to {self.filepath}: {event.timestamp} - {event}")


class ServerMonitor:
    def __init__(self, server_name: str) -> None:
        self.server_name = server_name
        self._subscribers: list[AlertSubscriber] = []
    
    def subscribe(self, subscriber: AlertSubscriber) -> None:
        self._subscribers.append(subscriber)
    
    def unsubscribe(self, subscriber: AlertSubscriber) -> None:
        self._subscribers.remove(subscriber)
    
    def emit(self, event: ServerEvent) -> None:
        print(f"\n[{self.server_name}] Event: {event}")
        for subscriber in self._subscribers:
            subscriber.handle(event)


# Использование
if __name__ == "__main__":
    # Создаём монитор сервера
    monitor = ServerMonitor("production-server-01")
    
    # Подписываем различные алерты
    monitor.subscribe(EmailAlert(
        "admin@example.com",
        min_priority=EventPriority.WARNING
    ))
    
    monitor.subscribe(SMSAlert(
        "+7-999-123-4567",
        event_types=[EventType.SERVICE_DOWN],
        min_priority=EventPriority.CRITICAL
    ))
    
    monitor.subscribe(SlackAlert(
        "ops-alerts",
        min_priority=EventPriority.INFO
    ))
    
    monitor.subscribe(LogAlert(
        "/var/log/server.log",
        min_priority=EventPriority.INFO
    ))
    
    # Эмитим события
    print("=== Server Monitoring Events ===")
    
    monitor.emit(ServerEvent(
        EventType.CPU_HIGH,
        EventPriority.INFO,
        "CPU usage at 75%"
    ))
    
    monitor.emit(ServerEvent(
        EventType.MEMORY_HIGH,
        EventPriority.WARNING,
        "Memory usage at 90%"
    ))
    
    monitor.emit(ServerEvent(
        EventType.SERVICE_DOWN,
        EventPriority.CRITICAL,
        "Database service is not responding"
    ))
    
    monitor.emit(ServerEvent(
        EventType.SERVICE_UP,
        EventPriority.INFO,
        "Database service restored"
    ))
```

</details>

---

## Задание 6: Паттерн Strategy + Command

### Условие

Создайте систему обработки изображений с:
- Разными стратегиями изменения размера (crop, fit, stretch)
- Разными стратегиями фильтров (grayscale, blur, sharpen)
- Поддержкой undo/redo операций

### Требования

1. Комбинируйте паттерны Strategy и Command
2. Сохраняйте историю операций
3. Позвольте применять несколько операций последовательно

<details>
<summary>Решение</summary>

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from copy import deepcopy


@dataclass
class Image:
    name: str
    width: int
    height: int
    filters: list[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        filters_str = ", ".join(self.filters) if self.filters else "none"
        return f"Image '{self.name}' ({self.width}x{self.height}), filters: [{filters_str}]"
    
    def copy(self) -> "Image":
        return deepcopy(self)


# === Strategies ===

class ResizeStrategy(ABC):
    @abstractmethod
    def resize(self, image: Image, target_width: int, target_height: int) -> None:
        pass
    
    @abstractmethod
    def name(self) -> str:
        pass


class CropStrategy(ResizeStrategy):
    def resize(self, image: Image, target_width: int, target_height: int) -> None:
        image.width = min(image.width, target_width)
        image.height = min(image.height, target_height)
    
    def name(self) -> str:
        return "crop"


class FitStrategy(ResizeStrategy):
    def resize(self, image: Image, target_width: int, target_height: int) -> None:
        ratio = min(target_width / image.width, target_height / image.height)
        image.width = int(image.width * ratio)
        image.height = int(image.height * ratio)
    
    def name(self) -> str:
        return "fit"


class StretchStrategy(ResizeStrategy):
    def resize(self, image: Image, target_width: int, target_height: int) -> None:
        image.width = target_width
        image.height = target_height
    
    def name(self) -> str:
        return "stretch"


class FilterStrategy(ABC):
    @abstractmethod
    def apply(self, image: Image) -> None:
        pass
    
    @abstractmethod
    def name(self) -> str:
        pass


class GrayscaleFilter(FilterStrategy):
    def apply(self, image: Image) -> None:
        if "grayscale" not in image.filters:
            image.filters.append("grayscale")
    
    def name(self) -> str:
        return "grayscale"


class BlurFilter(FilterStrategy):
    def __init__(self, radius: int = 5) -> None:
        self.radius = radius
    
    def apply(self, image: Image) -> None:
        image.filters.append(f"blur({self.radius})")
    
    def name(self) -> str:
        return f"blur({self.radius})"


class SharpenFilter(FilterStrategy):
    def apply(self, image: Image) -> None:
        image.filters.append("sharpen")
    
    def name(self) -> str:
        return "sharpen"


# === Commands ===

class ImageCommand(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass
    
    @abstractmethod
    def undo(self) -> str:
        pass


class ResizeCommand(ImageCommand):
    def __init__(
        self,
        image: Image,
        strategy: ResizeStrategy,
        target_width: int,
        target_height: int,
    ) -> None:
        self._image = image
        self._strategy = strategy
        self._target_width = target_width
        self._target_height = target_height
        self._previous_state: Image | None = None
    
    def execute(self) -> str:
        self._previous_state = self._image.copy()
        self._strategy.resize(self._image, self._target_width, self._target_height)
        return f"Resized using '{self._strategy.name()}' to {self._image.width}x{self._image.height}"
    
    def undo(self) -> str:
        if self._previous_state:
            self._image.width = self._previous_state.width
            self._image.height = self._previous_state.height
            return f"Undid resize, restored to {self._image.width}x{self._image.height}"
        return "Nothing to undo"


class FilterCommand(ImageCommand):
    def __init__(self, image: Image, strategy: FilterStrategy) -> None:
        self._image = image
        self._strategy = strategy
        self._previous_filters: list[str] = []
    
    def execute(self) -> str:
        self._previous_filters = self._image.filters.copy()
        self._strategy.apply(self._image)
        return f"Applied filter '{self._strategy.name()}'"
    
    def undo(self) -> str:
        self._image.filters = self._previous_filters
        return f"Undid filter '{self._strategy.name()}'"


class ImageEditor:
    def __init__(self) -> None:
        self._history: list[ImageCommand] = []
        self._redo_stack: list[ImageCommand] = []
    
    def execute(self, command: ImageCommand) -> str:
        result = command.execute()
        self._history.append(command)
        self._redo_stack.clear()
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
    
    def history_count(self) -> int:
        return len(self._history)


# Использование
if __name__ == "__main__":
    image = Image("photo.jpg", 1920, 1080)
    editor = ImageEditor()
    
    print("=== Image Processing with Strategy + Command ===\n")
    print(f"Initial: {image}")
    
    # Применяем операции
    print(f"\n{editor.execute(ResizeCommand(image, FitStrategy(), 800, 600))}")
    print(f"Current: {image}")
    
    print(f"\n{editor.execute(FilterCommand(image, GrayscaleFilter()))}")
    print(f"Current: {image}")
    
    print(f"\n{editor.execute(FilterCommand(image, BlurFilter(10)))}")
    print(f"Current: {image}")
    
    print(f"\n{editor.execute(FilterCommand(image, SharpenFilter()))}")
    print(f"Current: {image}")
    
    # Undo
    print(f"\n{editor.undo()}")
    print(f"Current: {image}")
    
    print(f"\n{editor.undo()}")
    print(f"Current: {image}")
    
    # Redo
    print(f"\n{editor.redo()}")
    print(f"Current: {image}")
    
    # Новая операция (очищает redo stack)
    print(f"\n{editor.execute(ResizeCommand(image, CropStrategy(), 400, 300))}")
    print(f"Current: {image}")
    
    print(f"\nHistory count: {editor.history_count()}")
```

</details>

---

## Дополнительные задания

### Задание 7 (продвинутое): Паттерн State

Реализуйте конечный автомат для заказа в интернет-магазине:
- Состояния: Created → Paid → Shipped → Delivered / Cancelled
- Переходы зависят от текущего состояния
- Добавьте возврат (Refunded) только для Delivered заказов

### Задание 8 (продвинутое): Комбинация паттернов

Создайте систему логирования, которая использует:
- **Singleton** для глобального логгера
- **Factory** для создания разных хендлеров (Console, File, Network)
- **Decorator** для форматирования сообщений (Timestamp, Level, Color)
- **Observer** для подписки на события определённого уровня

---

## Критерии оценки

| Критерий | Баллы |
|----------|-------|
| Корректная реализация паттерна | 40% |
| Соблюдение SOLID принципов | 20% |
| Типизация и документация | 20% |
| Тестируемость кода | 20% |

---

## Полезные ресурсы

- [Refactoring Guru](https://refactoring.guru/design-patterns/python) — визуализация паттернов
- [Python Patterns](https://python-patterns.guide/) — идиоматичные реализации
- [Real Python - SOLID](https://realpython.com/solid-principles-python/) — подробно о SOLID
