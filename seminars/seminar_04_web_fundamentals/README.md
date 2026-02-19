# Семинар 4: Основы веба — сетевое взаимодействие и HTTP

**Модуль:** 3 — Создание Web-сервисов на Python  
**Дата:** 25.02.2026  
**Презентация:** [ссылка на презентацию]

---

## Цели семинара

После этого семинара студенты смогут:
- Объяснять разницу между IP-адресом и портом, понимать их роль в сетевом взаимодействии
- Описывать структуру HTTP-запроса: стартовая строка, заголовки, тело
- Различать HTTP-методы и выбирать подходящий для конкретной задачи
- Использовать библиотеку `requests` для отправки HTTP-запросов
- Обрабатывать ответы сервера и ошибки соединения

> **Важно:** Настоящее понимание HTTP приходит через практику. Теория — это фундамент, но уверенность появляется только после десятков отправленных запросов. Экспериментируйте!

---

## Подготовка

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# Установите зависимости (если ещё не установлены)
uv add requests

# Проверьте, что requests установлен
python -c "import requests; print(requests.__version__)"
```

---

## План семинара

> **Принцип работы:** после каждого блока теории — сразу переходите к практике. Не читайте весь документ целиком!

| Время | Тема | Практика |
|-------|------|----------|
| 15 мин | Блок 1: IP-адреса и порты | → Упражнения: Часть 1 |
| 20 мин | Блок 2: Структура HTTP-запроса | → Упражнения: Часть 2 |
| 25 мин | Блок 3: Библиотека requests | → Упражнения: Часть 3 |
| 20 мин | Блок 4: Ситуационные задачи (Chat Polls) | → Упражнения: Часть 4 |
| 10 мин | Подведение итогов | — |

**Итого:** ~90 минут

---

## Блок 1: IP-адреса и порты (15 мин)

### Что такое IP-адрес?

**IP-адрес** (Internet Protocol address) — уникальный числовой идентификатор устройства в сети. Это как почтовый адрес дома.

```
IPv4: 192.168.1.100      (4 числа от 0 до 255, разделённые точками)
IPv6: 2001:0db8:85a3::8a2e:0370:7334  (8 групп по 4 hex-цифры)
```

**Специальные адреса:**
- `127.0.0.1` (localhost) — "этот же компьютер"
- `0.0.0.0` — "все интерфейсы" (для серверов)
- `192.168.x.x`, `10.x.x.x` — локальные сети

### Что такое порт?

**Порт** — числовой идентификатор конкретного приложения на устройстве. Это как номер квартиры в доме.

```
IP-адрес + Порт = Сокет (полный адрес для соединения)
Пример: 192.168.1.100:8080
```

**Диапазоны портов:**

| Диапазон | Название | Описание |
|----------|----------|----------|
| 0–1023 | Well-known | Зарезервированы для системных служб (нужны права root) |
| 1024–49151 | Registered | Зарегистрированы для приложений |
| 49152–65535 | Dynamic | Временные, для клиентских соединений |

**Популярные порты:**

| Порт | Протокол/Сервис |
|------|-----------------|
| 80 | HTTP |
| 443 | HTTPS |
| 22 | SSH |
| 5432 | PostgreSQL |
| 3306 | MySQL |
| 8000, 8080 | Часто используются для разработки |

### Аналогия

```
Отправить письмо в офис:
  Город         = IP-адрес (какой компьютер)
  Улица, дом    = уточнение IP
  Номер офиса   = Порт (какое приложение на компьютере)
```

### Пример в Python

```python
from urllib.parse import urlparse

url = "https://api.example.com:8443/users"
parsed = urlparse(url)

print(parsed.hostname)  # api.example.com
print(parsed.port)      # 8443
print(parsed.scheme)    # https
```

> **Подробнее:** см. файл [`examples/01_ip_ports.py`](examples/01_ip_ports.py) — работа с URL, получение IP-адреса хоста.

### Практика

Перейдите к файлу [`exercises/web_fundamentals_practice.md`](exercises/web_fundamentals_practice.md) и выполните **Часть 1: IP-адреса и порты** (задания 1.1–1.3).

---

## Блок 2: Структура HTTP-запроса (20 мин)

### Что такое HTTP?

**HTTP** (HyperText Transfer Protocol) — протокол прикладного уровня для обмена данными в вебе. Работает по принципу "запрос-ответ": клиент отправляет запрос, сервер возвращает ответ.

### Структура HTTP-запроса

HTTP-запрос состоит из трёх частей:

```
┌─────────────────────────────────────────────────────────┐
│ 1. Стартовая строка (Request Line)                      │
│    GET /users?page=1 HTTP/1.1                           │
│    ^^^  ^^^^^^^^^^^^  ^^^^^^^                           │
│    метод   путь       версия                            │
├─────────────────────────────────────────────────────────┤
│ 2. Заголовки (Headers)                                  │
│    Host: api.example.com                                │
│    Content-Type: application/json                       │
│    Authorization: Bearer token123                       │
│    User-Agent: MyApp/1.0                                │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ 3. Тело запроса (Body) — опционально                    │
│    {"name": "Alice", "email": "alice@example.com"}      │
└─────────────────────────────────────────────────────────┘
```

### HTTP-методы

| Метод | Назначение | Есть тело? | Идемпотентный? |
|-------|------------|------------|----------------|
| GET | Получить данные | Нет | Да |
| POST | Создать ресурс | Да | Нет |
| PUT | Заменить ресурс целиком | Да | Да |
| PATCH | Частично обновить | Да | Нет |
| DELETE | Удалить ресурс | Обычно нет | Да |

**Идемпотентность** — повторный запрос даёт тот же результат.

### Важные заголовки запроса

| Заголовок | Описание | Пример |
|-----------|----------|--------|
| `Host` | Имя сервера | `Host: api.example.com` |
| `Content-Type` | Формат тела запроса | `Content-Type: application/json` |
| `Accept` | Ожидаемый формат ответа | `Accept: application/json` |
| `Authorization` | Данные аутентификации | `Authorization: Bearer abc123` |
| `User-Agent` | Информация о клиенте | `User-Agent: Mozilla/5.0...` |

### Структура HTTP-ответа

```
┌─────────────────────────────────────────────────────────┐
│ 1. Строка статуса                                       │
│    HTTP/1.1 200 OK                                      │
│    ^^^^^^^  ^^^ ^^                                      │
│    версия   код описание                                │
├─────────────────────────────────────────────────────────┤
│ 2. Заголовки ответа                                     │
│    Content-Type: application/json                       │
│    Content-Length: 156                                  │
│    Date: Tue, 25 Feb 2026 10:00:00 GMT                  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ 3. Тело ответа                                          │
│    {"id": 1, "name": "Alice"}                           │
└─────────────────────────────────────────────────────────┘
```

### Коды ответов HTTP

| Диапазон | Категория | Примеры |
|----------|-----------|---------|
| 1xx | Информационные | 100 Continue |
| 2xx | Успех | 200 OK, 201 Created, 204 No Content |
| 3xx | Перенаправление | 301 Moved, 302 Found, 304 Not Modified |
| 4xx | Ошибка клиента | 400 Bad Request, 401 Unauthorized, 404 Not Found |
| 5xx | Ошибка сервера | 500 Internal Error, 502 Bad Gateway, 503 Unavailable |

### Пример: сырой HTTP-запрос

```http
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer my-secret-token
Content-Length: 52

{"username": "alice", "email": "alice@example.com"}
```

> **Подробнее:** см. файл [`examples/02_http_structure.py`](examples/02_http_structure.py) — визуализация структуры запросов и ответов.

### Практика

Перейдите к файлу [`exercises/web_fundamentals_practice.md`](exercises/web_fundamentals_practice.md) и выполните **Часть 2: Структура HTTP-запроса** (задания 2.1–2.4).

---

## Блок 3: Библиотека requests (25 мин)

### Зачем нужна библиотека requests?

Стандартная библиотека `urllib` низкоуровневая и неудобная. `requests` — де-факто стандарт для HTTP в Python: простой, понятный, мощный.

### Установка

```bash
uv add requests
# или
pip install requests
```

### GET-запрос

```python
import requests

# Простой GET
response = requests.get("https://httpbin.org/get")
print(response.status_code)  # 200
print(response.text)         # тело как строка
print(response.json())       # парсинг JSON

# GET с параметрами (query string)
response = requests.get(
    "https://httpbin.org/get",
    params={"name": "Alice", "age": 25}
)
# URL станет: https://httpbin.org/get?name=Alice&age=25
```

### POST-запрос

```python
# POST с JSON-телом
response = requests.post(
    "https://httpbin.org/post",
    json={"username": "alice", "email": "alice@example.com"}
)
# Content-Type автоматически = application/json

# POST с form-data
response = requests.post(
    "https://httpbin.org/post",
    data={"username": "alice", "password": "secret"}
)
# Content-Type автоматически = application/x-www-form-urlencoded
```

### Кастомные заголовки

```python
headers = {
    "Authorization": "Bearer my-token",
    "User-Agent": "MyApp/1.0",
    "Accept-Language": "ru-RU"
}
response = requests.get("https://httpbin.org/headers", headers=headers)
```

### Таймауты — обязательны!

```python
# ВСЕГДА указывайте timeout!
response = requests.get(
    "https://httpbin.org/get",
    timeout=10  # секунды
)

# Раздельные таймауты
response = requests.get(
    "https://httpbin.org/get",
    timeout=(3, 10)  # (connect_timeout, read_timeout)
)
```

**Без таймаута запрос может зависнуть навсегда!**

### Обработка ошибок

```python
from requests.exceptions import (
    RequestException,
    ConnectionError,
    Timeout,
    HTTPError
)

try:
    response = requests.get("https://httpbin.org/status/404", timeout=10)
    response.raise_for_status()  # Выбросит HTTPError для 4xx/5xx
    
except ConnectionError:
    print("Не удалось подключиться к серверу")
except Timeout:
    print("Превышено время ожидания")
except HTTPError as e:
    print(f"HTTP ошибка: {e.response.status_code}")
except RequestException as e:
    print(f"Ошибка запроса: {e}")
```

### Объект Response

```python
response = requests.get("https://httpbin.org/get", timeout=10)

# Статус
response.status_code    # 200
response.ok             # True (для 2xx)
response.reason         # "OK"

# Заголовки ответа
response.headers        # dict-like объект
response.headers["Content-Type"]  # "application/json"

# Тело ответа
response.text           # как строка (декодируется автоматически)
response.content        # как bytes (сырые данные)
response.json()         # парсит JSON в dict/list

# Метаданные
response.url            # финальный URL (после редиректов)
response.elapsed        # время выполнения запроса
response.encoding       # кодировка
```

> **Подробнее:** см. файл [`examples/03_requests_library.py`](examples/03_requests_library.py) — полные примеры всех типов запросов.

### Практика

Перейдите к файлу [`exercises/web_fundamentals_practice.md`](exercises/web_fundamentals_practice.md) и выполните **Часть 3: Библиотека requests** (задания 3.1–3.5).

---

## Блок 4: Ситуационные задачи (20 мин)

Интерактивная часть семинара — обсуждение типичных ситуаций при работе с HTTP.

> **Формат:** преподаватель задаёт вопрос, студенты отвечают в чате (A/B/C/D).

Перейдите к файлу [`exercises/web_fundamentals_practice.md`](exercises/web_fundamentals_practice.md) и выполните **Часть 4: Ситуационные задачи (Chat Polls)**.

---

## Подведение итогов

### Шпаргалка

| Концепция | Ключевое |
|-----------|----------|
| IP-адрес | Адрес устройства в сети |
| Порт | Адрес приложения на устройстве |
| HTTP | Протокол "запрос-ответ" |
| Заголовки | Метаданные запроса/ответа |
| Тело | Данные запроса/ответа |
| `requests.get()` | Получить данные |
| `requests.post()` | Отправить данные |
| `timeout` | Всегда указывайте! |
| `raise_for_status()` | Проверить код ответа |

### Ключевые выводы

1. **IP + Port = полный адрес** для соединения с конкретным приложением на конкретном компьютере.

2. **HTTP-запрос** состоит из стартовой строки, заголовков и тела. Заголовки — это метаданные, тело — это данные.

3. **Всегда используйте `timeout`** в запросах и обрабатывайте исключения — сеть ненадёжна.

> **Помните:** Чтобы по-настоящему понять HTTP, нужно отправить сотни запросов. Используйте httpbin.org для экспериментов!

---

## Файлы семинара

```
seminar_04_web_fundamentals/
├── README.md                           # Этот файл
├── examples/
│   ├── 01_ip_ports.py                  # Работа с IP и портами
│   ├── 02_http_structure.py            # Структура HTTP запросов/ответов
│   └── 03_requests_library.py          # Полное руководство по requests
└── exercises/
    └── web_fundamentals_practice.md    # Практические задания и poll-вопросы
```

---

## Дополнительные материалы

- [MDN Web Docs — HTTP](https://developer.mozilla.org/ru/docs/Web/HTTP) — подробное описание HTTP
- [requests Documentation](https://docs.python-requests.org/) — официальная документация
- [httpbin.org](https://httpbin.org/) — сервис для тестирования HTTP-запросов
- [HTTP Status Codes](https://httpstatuses.com/) — справочник по кодам ответов
- [Real Python — Python requests](https://realpython.com/python-requests/) — руководство по requests
