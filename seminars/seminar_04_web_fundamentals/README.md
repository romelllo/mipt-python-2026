# Семинар 4: Общее представление о WEB

**Модуль:** 3 — Создание Web-сервисов на Python
**Дата:** 25.02.2026
**Презентация:** [ссылка на презентацию]

---

## Цели семинара

После этого семинара студенты смогут:
- Понимать архитектуру клиент-сервер и принципы работы веба
- Работать с протоколом HTTP: методы, заголовки, коды ответов
- Формировать URL с параметрами запросов
- Работать с форматами данных JSON и XML
- Понимать принципы REST архитектуры
- Использовать инструменты для тестирования API

---

## План занятия

| Время | Тема | Материалы |
|-------|------|-----------|
| 10-15 мин | Введение: клиент-сервер, история веба | Презентация |
| 25 мин | HTTP протокол: методы, заголовки, статусы | `examples/01_http_basics.py` |
| 20 мин | Форматы данных: JSON и XML | `examples/02_json_xml.py` |
| 20 мин | Простой HTTP сервер на Python | `examples/03_simple_server.py` |
| 25 мин | REST API и работа с внешними сервисами | `examples/04_rest_client.py` |
| 30 мин | Практика | `exercises/web_fundamentals_practice.md` |

---

## 1. Архитектура клиент-сервер

### Основные понятия

**Клиент** — программа, которая отправляет запросы (браузер, мобильное приложение, скрипт).

**Сервер** — программа, которая принимает запросы и отправляет ответы.

```
┌─────────┐    HTTP Request     ┌─────────┐
│         │ ─────────────────>  │         │
│ Client  │                     │ Server  │
│         │ <─────────────────  │         │
└─────────┘    HTTP Response    └─────────┘
```

### URL (Uniform Resource Locator)

Структура URL:

```
https://api.example.com:8080/users/123?active=true&limit=10#section
└─┬─┘   └──────┬──────┘└─┬─┘└────┬───┘└──────────┬────────┘└───┬──┘
схема       хост      порт   путь          параметры      якорь
```

```python
from urllib.parse import urlparse, parse_qs, urlencode, urljoin

# Разбор URL
url = "https://api.example.com/users?name=John&age=25"
parsed = urlparse(url)
print(parsed.scheme)    # https
print(parsed.netloc)    # api.example.com
print(parsed.path)      # /users
print(parsed.query)     # name=John&age=25

# Парсинг параметров
params = parse_qs(parsed.query)
print(params)           # {'name': ['John'], 'age': ['25']}

# Создание строки параметров
query = urlencode({'search': 'python', 'page': 1})
print(query)            # search=python&page=1
```

---

## 2. Протокол HTTP

### HTTP методы

| Метод | Описание | Идемпотентность | Тело запроса |
|-------|----------|-----------------|--------------|
| GET | Получить ресурс | Да | Нет |
| POST | Создать ресурс | Нет | Да |
| PUT | Заменить ресурс полностью | Да | Да |
| PATCH | Частично обновить ресурс | Нет | Да |
| DELETE | Удалить ресурс | Да | Обычно нет |
| HEAD | Получить только заголовки | Да | Нет |
| OPTIONS | Получить доступные методы | Да | Нет |

**Идемпотентность** — многократное выполнение запроса даёт тот же результат, что и однократное.

### HTTP заголовки

```python
# Частые заголовки запроса
headers = {
    "Content-Type": "application/json",      # Формат тела запроса
    "Accept": "application/json",            # Ожидаемый формат ответа
    "Authorization": "Bearer <token>",       # Аутентификация
    "User-Agent": "MyApp/1.0",              # Информация о клиенте
    "Accept-Language": "ru-RU,en-US",       # Предпочитаемые языки
}

# Частые заголовки ответа
# Content-Type: application/json            # Формат тела ответа
# Content-Length: 1234                      # Размер тела в байтах
# Set-Cookie: session=abc123                # Установка cookie
# Cache-Control: max-age=3600               # Кэширование
# Location: /new-url                        # Редирект
```

### Коды ответов HTTP

| Диапазон | Категория | Примеры |
|----------|-----------|---------|
| 1xx | Информационные | 100 Continue |
| 2xx | Успех | 200 OK, 201 Created, 204 No Content |
| 3xx | Перенаправление | 301 Moved Permanently, 302 Found, 304 Not Modified |
| 4xx | Ошибка клиента | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| 5xx | Ошибка сервера | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable |

```python
import requests

response = requests.get("https://httpbin.org/status/404")
print(response.status_code)     # 404
print(response.ok)              # False (True для 2xx)
print(response.reason)          # NOT FOUND
```

---

## 3. Библиотека requests

### Базовое использование

```python
import requests

# GET запрос
response = requests.get("https://httpbin.org/get")
print(response.status_code)     # 200
print(response.headers)         # Заголовки ответа
print(response.text)            # Тело как строка
print(response.json())          # Парсинг JSON

# GET с параметрами
response = requests.get(
    "https://httpbin.org/get",
    params={"name": "Alice", "age": 25}
)
# URL станет: https://httpbin.org/get?name=Alice&age=25

# POST с JSON телом
response = requests.post(
    "https://httpbin.org/post",
    json={"username": "alice", "email": "alice@example.com"}
)

# POST с form-data
response = requests.post(
    "https://httpbin.org/post",
    data={"username": "alice", "password": "secret"}
)

# Кастомные заголовки
response = requests.get(
    "https://httpbin.org/headers",
    headers={"Authorization": "Bearer my-token"}
)
```

### Обработка ошибок

```python
import requests
from requests.exceptions import (
    RequestException,
    ConnectionError,
    Timeout,
    HTTPError
)

try:
    response = requests.get(
        "https://httpbin.org/delay/5",
        timeout=3  # Таймаут в секундах
    )
    response.raise_for_status()  # Выбросит HTTPError для 4xx/5xx

except ConnectionError:
    print("Ошибка подключения")
except Timeout:
    print("Превышено время ожидания")
except HTTPError as e:
    print(f"HTTP ошибка: {e.response.status_code}")
except RequestException as e:
    print(f"Ошибка запроса: {e}")
```

### Сессии

```python
# Сессия сохраняет cookies и настройки между запросами
with requests.Session() as session:
    # Установить базовые заголовки для всех запросов
    session.headers.update({"User-Agent": "MyApp/1.0"})

    # Первый запрос — сервер установит cookie
    session.get("https://httpbin.org/cookies/set/session_id/abc123")

    # Второй запрос — cookie автоматически отправится
    response = session.get("https://httpbin.org/cookies")
    print(response.json())  # {'cookies': {'session_id': 'abc123'}}
```

---

## 4. Форматы данных

### JSON (JavaScript Object Notation)

Самый популярный формат для веб-API.

```python
import json

# Python объект -> JSON строка
data = {
    "name": "Alice",
    "age": 25,
    "courses": ["Python", "SQL"],
    "active": True,
    "gpa": None
}

json_string = json.dumps(data, ensure_ascii=False, indent=2)
print(json_string)

# JSON строка -> Python объект
parsed = json.loads(json_string)
print(parsed["name"])  # Alice

# Работа с файлами
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
```

### XML (eXtensible Markup Language)

Используется в legacy системах, SOAP, RSS.

```python
import xml.etree.ElementTree as ET

# Создание XML
root = ET.Element("students")
student = ET.SubElement(root, "student", id="1")
ET.SubElement(student, "name").text = "Alice"
ET.SubElement(student, "gpa").text = "4.5"

xml_string = ET.tostring(root, encoding="unicode")
print(xml_string)
# <students><student id="1"><name>Alice</name><gpa>4.5</gpa></student></students>

# Парсинг XML
root = ET.fromstring(xml_string)
for student in root.findall("student"):
    name = student.find("name").text
    gpa = student.find("gpa").text
    print(f"{name}: {gpa}")
```

### Сравнение JSON и XML

| Критерий | JSON | XML |
|----------|------|-----|
| Читаемость | Высокая | Средняя |
| Размер | Компактный | Больше |
| Типы данных | Нативные (числа, bool, null) | Только строки |
| Схема | JSON Schema | XSD, DTD |
| Комментарии | Нет | Да |
| Применение | REST API, конфиги | SOAP, RSS, конфиги |

---

## 5. REST архитектура

### Принципы REST

**REST** (Representational State Transfer) — архитектурный стиль для веб-сервисов.

1. **Клиент-сервер** — разделение ответственности
2. **Без состояния (Stateless)** — каждый запрос содержит всю информацию
3. **Кэширование** — ответы можно кэшировать
4. **Единообразный интерфейс** — стандартные методы и URL
5. **Многоуровневая система** — клиент не знает, общается ли с сервером напрямую

### RESTful URL дизайн

```
# Ресурс: коллекция
GET    /api/users          # Получить список пользователей
POST   /api/users          # Создать пользователя

# Ресурс: элемент
GET    /api/users/123      # Получить пользователя 123
PUT    /api/users/123      # Обновить пользователя 123
PATCH  /api/users/123      # Частично обновить пользователя 123
DELETE /api/users/123      # Удалить пользователя 123

# Вложенные ресурсы
GET    /api/users/123/orders        # Заказы пользователя 123
GET    /api/users/123/orders/456    # Заказ 456 пользователя 123

# Фильтрация и пагинация через query-параметры
GET    /api/users?role=admin&active=true
GET    /api/users?page=2&limit=20&sort=-created_at
```

### CRUD операции и HTTP методы

| Операция | HTTP метод | Успешный код |
|----------|------------|--------------|
| Create | POST | 201 Created |
| Read (list) | GET | 200 OK |
| Read (item) | GET | 200 OK |
| Update (full) | PUT | 200 OK |
| Update (partial) | PATCH | 200 OK |
| Delete | DELETE | 204 No Content |

### Пример REST API ответов

```python
# GET /api/users/123 - успех
{
    "id": 123,
    "name": "Alice",
    "email": "alice@example.com",
    "created_at": "2024-01-15T10:30:00Z"
}

# GET /api/users - список с пагинацией
{
    "data": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ],
    "meta": {
        "total": 100,
        "page": 1,
        "per_page": 20
    }
}

# POST /api/users - ошибка валидации (400)
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": [
            {"field": "email", "message": "Invalid email format"}
        ]
    }
}
```

---

## 6. Простой HTTP сервер

### Встроенный сервер Python

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/hello":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"message": "Hello, World!"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)

        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {"received": data}
        self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), SimpleHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()
```

---

## 7. Инструменты для тестирования API

### curl

```bash
# GET запрос
curl https://httpbin.org/get

# GET с заголовками
curl -H "Authorization: Bearer token" https://httpbin.org/headers

# POST с JSON
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'

# Подробный вывод
curl -v https://httpbin.org/get

# Только заголовки ответа
curl -I https://httpbin.org/get
```

### HTTPie (более удобный CLI)

```bash
# Установка
pip install httpie

# GET запрос
http https://httpbin.org/get

# POST с JSON (по умолчанию)
http POST https://httpbin.org/post name=Alice age:=25

# С заголовками
http https://httpbin.org/headers Authorization:"Bearer token"
```

### Python REPL

```python
>>> import requests
>>> r = requests.get("https://httpbin.org/get")
>>> r.status_code
200
>>> r.json()
{'args': {}, 'headers': {...}, ...}
```

---

## Файлы семинара

```
seminar_04_web_fundamentals/
├── README.md                       # Этот файл
├── examples/
│   ├── 01_http_basics.py           # HTTP запросы с requests
│   ├── 02_json_xml.py              # Работа с JSON и XML
│   ├── 03_simple_server.py         # Простой HTTP сервер
│   └── 04_rest_client.py           # REST API клиент
└── exercises/
    └── web_fundamentals_practice.md # Практические задания
```

---

## Дополнительные материалы

- [MDN Web Docs - HTTP](https://developer.mozilla.org/ru/docs/Web/HTTP) — подробное описание HTTP
- [HTTP Status Codes](https://httpstatuses.com/) — справочник по кодам ответов
- [REST API Tutorial](https://restfulapi.net/) — руководство по REST
- [requests Documentation](https://docs.python-requests.org/) — документация библиотеки requests
- [httpbin.org](https://httpbin.org/) — сервис для тестирования HTTP запросов
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) — фейковый REST API для тестирования

---

## Запуск примеров

```bash
# Установка зависимостей (если нужно)
uv add requests

# Запуск примеров
python seminars/seminar_04_web_fundamentals/examples/01_http_basics.py
python seminars/seminar_04_web_fundamentals/examples/02_json_xml.py
python seminars/seminar_04_web_fundamentals/examples/03_simple_server.py  # Запустить в отдельном терминале
python seminars/seminar_04_web_fundamentals/examples/04_rest_client.py
```
