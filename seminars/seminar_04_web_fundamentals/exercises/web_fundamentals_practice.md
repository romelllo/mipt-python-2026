# Практические задания: Основы веба — сетевое взаимодействие и HTTP

## Подготовка

```bash
# Активируйте виртуальное окружение
source .venv/bin/activate  # Linux/Mac

# Убедитесь, что requests установлен
python -c "import requests; print('OK')"

# Запустите примеры для ознакомления
python seminars/seminar_04_web_fundamentals/examples/01_ip_ports.py
python seminars/seminar_04_web_fundamentals/examples/02_http_structure.py
python seminars/seminar_04_web_fundamentals/examples/03_requests_library.py
```

> **Как работать с заданиями:** прочитайте условие, попробуйте решить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: IP-адреса и порты

> **Теория:** [README.md — Блок 1](../README.md#блок-1-ip-адреса-и-порты-15-мин) | **Примеры:** [`examples/01_ip_ports.py`](../examples/01_ip_ports.py)

### Задание 1.1

Дан URL: `https://api.github.com:443/users/octocat/repos?per_page=5`

Напишите код, который извлечёт из него:
- Схему (protocol)
- Хост (hostname)
- Порт (port)
- Путь (path)
- Параметры запроса (query)

<details>
<summary>Подсказка</summary>

Используйте `urllib.parse.urlparse()`. Обратите внимание: если порт не указан явно, `parsed.port` вернёт `None`.

</details>

<details>
<summary>Решение</summary>

```python
from urllib.parse import urlparse, parse_qs

url = "https://api.github.com:443/users/octocat/repos?per_page=5"
parsed = urlparse(url)

print(f"Схема: {parsed.scheme}")          # https
print(f"Хост: {parsed.hostname}")          # api.github.com
print(f"Порт: {parsed.port}")              # 443
print(f"Путь: {parsed.path}")              # /users/octocat/repos
print(f"Параметры: {parsed.query}")        # per_page=5

# Бонус: парсинг параметров в словарь
params = parse_qs(parsed.query)
print(f"Параметры (dict): {params}")       # {'per_page': ['5']}
```

</details>

---

### Задание 1.2

Напишите функцию `get_ip_address(hostname: str) -> str | None`, которая возвращает IP-адрес по имени хоста. Если хост не найден, функция должна вернуть `None`.

Протестируйте на:
- `google.com`
- `localhost`
- `this-host-does-not-exist.invalid`

<details>
<summary>Подсказка</summary>

Используйте `socket.gethostbyname()`. Эта функция выбрасывает `socket.gaierror`, если хост не найден.

</details>

<details>
<summary>Решение</summary>

```python
import socket


def get_ip_address(hostname: str) -> str | None:
    """Возвращает IP-адрес по имени хоста или None, если не найден."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


# Тестирование
print(get_ip_address("google.com"))                      # Например: 142.250.74.206
print(get_ip_address("localhost"))                       # 127.0.0.1
print(get_ip_address("this-host-does-not-exist.invalid"))  # None
```

</details>

---

### Задание 1.3

Определите, какой порт используется по умолчанию для следующих URL (без явного указания порта):

1. `http://example.com/page`
2. `https://example.com/page`
3. `ftp://files.example.com/file.txt`
4. `ssh://server.example.com`

<details>
<summary>Подсказка</summary>

Стандартные порты: HTTP — 80, HTTPS — 443, FTP — 21, SSH — 22.

</details>

<details>
<summary>Решение</summary>

| URL | Порт по умолчанию |
|-----|-------------------|
| `http://example.com/page` | 80 |
| `https://example.com/page` | 443 |
| `ftp://files.example.com/file.txt` | 21 |
| `ssh://server.example.com` | 22 |

```python
from urllib.parse import urlparse

# urlparse не знает все порты по умолчанию, но знает некоторые
urls = [
    "http://example.com/page",
    "https://example.com/page",
]

for url in urls:
    parsed = urlparse(url)
    # parsed.port будет None, если порт не указан явно
    print(f"{url} -> port={parsed.port}")

# Для получения порта по умолчанию используем словарь
DEFAULT_PORTS = {
    "http": 80,
    "https": 443,
    "ftp": 21,
    "ssh": 22,
}

for url in urls:
    parsed = urlparse(url)
    port = parsed.port or DEFAULT_PORTS.get(parsed.scheme)
    print(f"{url} -> {port}")
```

</details>

---

## Часть 2: Структура HTTP-запроса

> **Теория:** [README.md — Блок 2](../README.md#блок-2-структура-http-запроса-20-мин) | **Примеры:** [`examples/02_http_structure.py`](../examples/02_http_structure.py)

### Задание 2.1

Дан следующий HTTP-запрос в текстовом виде:

```http
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer abc123
Content-Length: 45

{"username": "alice", "email": "a@test.com"}
```

Ответьте на вопросы:
1. Какой HTTP-метод используется?
2. Какой путь (endpoint)?
3. Какой формат данных в теле запроса?
4. Какой заголовок используется для аутентификации?

<details>
<summary>Решение</summary>

1. **Метод:** POST
2. **Путь:** `/api/users`
3. **Формат данных:** JSON (заголовок `Content-Type: application/json`)
4. **Заголовок аутентификации:** `Authorization: Bearer abc123`

</details>

---

### Задание 2.2

Для каждой операции выберите подходящий HTTP-метод:

| Операция | Метод? |
|----------|--------|
| Получить список всех пользователей | ? |
| Создать нового пользователя | ? |
| Полностью заменить данные пользователя | ? |
| Изменить только email пользователя | ? |
| Удалить пользователя | ? |

<details>
<summary>Решение</summary>

| Операция | Метод |
|----------|-------|
| Получить список всех пользователей | **GET** |
| Создать нового пользователя | **POST** |
| Полностью заменить данные пользователя | **PUT** |
| Изменить только email пользователя | **PATCH** |
| Удалить пользователя | **DELETE** |

</details>

---

### Задание 2.3

Сопоставьте коды ответов HTTP с их значениями:

Коды: `200`, `201`, `204`, `400`, `401`, `404`, `500`

| Ситуация | Код? |
|----------|------|
| Ресурс успешно получен | ? |
| Ресурс успешно создан | ? |
| Операция выполнена, тело ответа пустое | ? |
| Некорректный запрос (ошибка в данных) | ? |
| Требуется аутентификация | ? |
| Ресурс не найден | ? |
| Внутренняя ошибка сервера | ? |

<details>
<summary>Решение</summary>

| Ситуация | Код |
|----------|-----|
| Ресурс успешно получен | **200 OK** |
| Ресурс успешно создан | **201 Created** |
| Операция выполнена, тело ответа пустое | **204 No Content** |
| Некорректный запрос (ошибка в данных) | **400 Bad Request** |
| Требуется аутентификация | **401 Unauthorized** |
| Ресурс не найден | **404 Not Found** |
| Внутренняя ошибка сервера | **500 Internal Server Error** |

</details>

---

### Задание 2.4

Напишите код, который отправляет GET-запрос на `https://httpbin.org/headers` и выводит:
1. Все заголовки, которые сервер получил от вашего клиента
2. Значение заголовка `User-Agent`

<details>
<summary>Подсказка</summary>

httpbin.org возвращает JSON с ключом `"headers"`, содержащим словарь всех заголовков запроса.

</details>

<details>
<summary>Решение</summary>

```python
import requests

response = requests.get("https://httpbin.org/headers", timeout=10)
data = response.json()

print("Все заголовки:")
for key, value in data["headers"].items():
    print(f"  {key}: {value}")

print(f"\nUser-Agent: {data['headers'].get('User-Agent')}")
```

</details>

---

## Часть 3: Библиотека requests

> **Теория:** [README.md — Блок 3](../README.md#блок-3-библиотека-requests-25-мин) | **Примеры:** [`examples/03_requests_library.py`](../examples/03_requests_library.py)

### Задание 3.1

Отправьте GET-запрос на `https://httpbin.org/get` с query-параметрами:
- `name` = ваше имя
- `course` = "Python"
- `year` = 2026

Выведите финальный URL запроса и значения параметров, которые получил сервер.

<details>
<summary>Подсказка</summary>

Используйте параметр `params` в `requests.get()`. Финальный URL доступен через `response.url`.

</details>

<details>
<summary>Решение</summary>

```python
import requests

params = {
    "name": "Иван",
    "course": "Python",
    "year": 2026,
}

response = requests.get("https://httpbin.org/get", params=params, timeout=10)

print(f"Финальный URL: {response.url}")
print(f"Параметры на сервере: {response.json()['args']}")
```

Вывод:
```
Финальный URL: https://httpbin.org/get?name=Иван&course=Python&year=2026
Параметры на сервере: {'course': 'Python', 'name': 'Иван', 'year': '2026'}
```

</details>

---

### Задание 3.2

Отправьте POST-запрос на `https://httpbin.org/post` с JSON-телом:
```json
{
    "username": "student",
    "email": "student@mipt.ru",
    "roles": ["user"]
}
```

Выведите:
1. Код ответа
2. Content-Type запроса (из ответа сервера)
3. Данные, которые получил сервер

<details>
<summary>Подсказка</summary>

Используйте параметр `json` в `requests.post()` — он автоматически сериализует словарь и устанавливает `Content-Type: application/json`.

</details>

<details>
<summary>Решение</summary>

```python
import requests

data = {
    "username": "student",
    "email": "student@mipt.ru",
    "roles": ["user"],
}

response = requests.post("https://httpbin.org/post", json=data, timeout=10)
result = response.json()

print(f"Код ответа: {response.status_code}")
print(f"Content-Type запроса: {result['headers']['Content-Type']}")
print(f"Данные на сервере: {result['json']}")
```

</details>

---

### Задание 3.3

Напишите функцию `fetch_user(user_id: int) -> dict | None`, которая:
1. Отправляет GET-запрос на `https://jsonplaceholder.typicode.com/users/{user_id}`
2. Возвращает данные пользователя как словарь
3. Возвращает `None`, если пользователь не найден (код 404)
4. Обрабатывает ошибки соединения и таймаута

Протестируйте на `user_id=1` и `user_id=999`.

<details>
<summary>Подсказка</summary>

Используйте `response.raise_for_status()` для проверки кода ответа. Ловите `HTTPError`, `ConnectionError`, `Timeout`.

</details>

<details>
<summary>Решение</summary>

```python
import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout


def fetch_user(user_id: int) -> dict | None:
    """Получает данные пользователя по ID.
    
    Returns:
        Словарь с данными пользователя или None, если не найден.
    """
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        if e.response.status_code == 404:
            return None
        print(f"HTTP ошибка: {e.response.status_code}")
    except ConnectionError:
        print("Ошибка соединения")
    except Timeout:
        print("Таймаут запроса")
    
    return None


# Тестирование
user = fetch_user(1)
if user:
    print(f"Пользователь найден: {user['name']}")
else:
    print("Пользователь не найден")

user = fetch_user(999)
if user:
    print(f"Пользователь найден: {user['name']}")
else:
    print("Пользователь не найден")
```

</details>

---

### Задание 3.4

Напишите код, который:
1. Отправляет запрос на `https://httpbin.org/delay/5` с таймаутом 2 секунды
2. Ловит исключение таймаута
3. Выводит сообщение "Сервер не ответил вовремя"

<details>
<summary>Подсказка</summary>

Endpoint `/delay/5` отвечает с задержкой 5 секунд. Таймаут 2 секунды гарантированно истечёт.

</details>

<details>
<summary>Решение</summary>

```python
import requests
from requests.exceptions import Timeout

try:
    response = requests.get("https://httpbin.org/delay/5", timeout=2)
    print(f"Ответ получен: {response.status_code}")
except Timeout:
    print("Сервер не ответил вовремя")
```

</details>

---

### Задание 3.5

Используя сессию (`requests.Session`), выполните:
1. Установите cookie `session_token=abc123` через `https://httpbin.org/cookies/set/session_token/abc123`
2. Отправьте запрос на `https://httpbin.org/cookies` и убедитесь, что cookie сохранился
3. Добавьте в сессию заголовок `X-Custom-Header: MyValue`
4. Проверьте, что заголовок отправляется через `https://httpbin.org/headers`

<details>
<summary>Подсказка</summary>

Используйте `with requests.Session() as session:`. Для добавления заголовка: `session.headers.update({...})`.

</details>

<details>
<summary>Решение</summary>

```python
import requests

with requests.Session() as session:
    # 1. Устанавливаем cookie
    session.get("https://httpbin.org/cookies/set/session_token/abc123", timeout=10)
    
    # 2. Проверяем cookie
    response = session.get("https://httpbin.org/cookies", timeout=10)
    print(f"Cookies: {response.json()['cookies']}")
    
    # 3. Добавляем заголовок в сессию
    session.headers.update({"X-Custom-Header": "MyValue"})
    
    # 4. Проверяем заголовок
    response = session.get("https://httpbin.org/headers", timeout=10)
    headers = response.json()["headers"]
    print(f"X-Custom-Header: {headers.get('X-Custom-Header')}")
```

Вывод:
```
Cookies: {'session_token': 'abc123'}
X-Custom-Header: MyValue
```

</details>

---

## Часть 4: Ситуационные задачи (Chat Polls)

> Этот раздел используется преподавателем для интерактива в чате.
> Студенты отвечают A/B/C/D, затем обсуждаем правильный ответ.

---

### Ситуация 1: Выбор порта

> Вы разрабатываете веб-приложение на локальной машине. Какой порт лучше выбрать для сервера разработки?

- A) 80
- B) 443
- C) 22
- D) 8000

<details>
<summary>Ответ</summary>

**D) 8000**

- Порты 80 и 443 — стандартные для HTTP/HTTPS, требуют права администратора (root) на Unix-системах
- Порт 22 — зарезервирован для SSH
- Порт 8000 — типичный порт для разработки, не требует особых прав

Другие популярные порты для разработки: 3000, 5000, 8080.

</details>

---

### Ситуация 2: HTTP метод для получения данных

> Вам нужно получить список товаров из интернет-магазина. Какой HTTP-метод использовать?

- A) POST
- B) GET
- C) PUT
- D) DELETE

<details>
<summary>Ответ</summary>

**B) GET**

- **GET** — для получения данных (чтение)
- POST — для создания новых данных
- PUT — для замены данных
- DELETE — для удаления данных

GET не должен изменять состояние сервера — это "безопасный" метод.

</details>

---

### Ситуация 3: Код ответа при создании ресурса

> Ваш API успешно создал нового пользователя. Какой код ответа вернуть?

- A) 200 OK
- B) 201 Created
- C) 204 No Content
- D) 202 Accepted

<details>
<summary>Ответ</summary>

**B) 201 Created**

- 200 OK — общий успех, но не указывает на создание
- **201 Created** — ресурс успешно создан (семантически правильный)
- 204 No Content — успех, но ответ без тела (обычно для DELETE)
- 202 Accepted — запрос принят, но ещё не обработан (асинхронные операции)

При 201 хорошей практикой является вернуть созданный ресурс в теле ответа.

</details>

---

### Ситуация 4: Заголовок Content-Type

> Вы отправляете JSON-данные на сервер. Какой Content-Type указать?

- A) text/plain
- B) text/html
- C) application/json
- D) application/x-www-form-urlencoded

<details>
<summary>Ответ</summary>

**C) application/json**

- text/plain — обычный текст
- text/html — HTML страницы
- **application/json** — JSON данные
- application/x-www-form-urlencoded — данные HTML-форм

`requests.post(..., json={...})` автоматически устанавливает `Content-Type: application/json`.

</details>

---

### Ситуация 5: Обработка ошибки 401

> Ваш запрос вернул код 401 Unauthorized. Что это означает и что делать?

- A) Сервер сломан, подождать и повторить
- B) Ресурс не найден, проверить URL
- C) Требуется аутентификация, добавить токен/пароль
- D) Запрос некорректен, исправить данные

<details>
<summary>Ответ</summary>

**C) Требуется аутентификация, добавить токен/пароль**

Коды 4xx — ошибки клиента:
- 400 — некорректный запрос (D)
- **401 — нужна аутентификация** (C)
- 403 — доступ запрещён (даже с аутентификацией)
- 404 — ресурс не найден (B)
- 5xx — ошибки сервера (A)

Для исправления 401 нужно добавить заголовок `Authorization`.

</details>

---

### Ситуация 6: Зачем нужен timeout?

> Почему важно ВСЕГДА указывать timeout в HTTP-запросах?

- A) Чтобы запрос выполнялся быстрее
- B) Чтобы программа не зависла навсегда при проблемах с сетью
- C) Чтобы сервер быстрее обрабатывал запрос
- D) Это требование протокола HTTP

<details>
<summary>Ответ</summary>

**B) Чтобы программа не зависла навсегда при проблемах с сетью**

Без timeout:
- Если сервер не отвечает, программа будет ждать бесконечно
- Это может привести к "зависанию" всего приложения
- В продакшене это критическая ошибка

Timeout не ускоряет сервер и не является частью протокола HTTP — это защита клиента.

</details>

---

### Ситуация 7: POST vs PUT

> Чем отличается POST от PUT при работе с ресурсами?

- A) POST создаёт, PUT обновляет (полностью заменяет)
- B) POST обновляет, PUT создаёт
- C) Они идентичны
- D) POST быстрее, PUT надёжнее

<details>
<summary>Ответ</summary>

**A) POST создаёт, PUT обновляет (полностью заменяет)**

- **POST** — создание нового ресурса (сервер сам назначает ID)
- **PUT** — замена ресурса целиком по известному ID
- **PATCH** — частичное обновление ресурса

Важно: PUT идемпотентен (повторный запрос = тот же результат), POST — нет.

</details>

---

### Ситуация 8 (бонусная): Комбинированный вопрос

> Вы делаете запрос к API и получаете такой код:
> ```python
> response = requests.get("https://api.example.com/users/123")
> print(response.status_code)  # 403
> ```
> Что означает код 403 и как его исправить?

- A) Ресурс не найден — проверить ID пользователя
- B) Сервер перегружен — повторить позже
- C) Доступ запрещён — у вашего токена нет прав на этот ресурс
- D) Ошибка в запросе — проверить формат данных

<details>
<summary>Ответ</summary>

**C) Доступ запрещён — у вашего токена нет прав на этот ресурс**

403 Forbidden означает:
- Сервер понял запрос
- Аутентификация прошла (вы "залогинены")
- Но у вас нет **прав** на этот ресурс

Отличие от 401:
- 401 — "Кто ты? Представься!" (нужна аутентификация)
- 403 — "Я знаю кто ты, но тебе сюда нельзя!" (нужны права)

Исправление: запросить права у администратора или использовать другой токен.

</details>

---

## Бонусные задания

### Бонус 1: Мини-HTTP клиент

Напишите функцию `api_client(base_url: str)`, которая возвращает объект с методами:
- `get(endpoint, params=None)` — GET-запрос
- `post(endpoint, data=None)` — POST-запрос с JSON

Функция должна:
- Использовать сессию для всех запросов
- Автоматически добавлять `base_url` к endpoint
- Обрабатывать ошибки и возвращать `None` при неудаче

<details>
<summary>Решение</summary>

```python
import requests
from requests.exceptions import RequestException


class APIClient:
    """Простой HTTP-клиент для работы с API."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
    
    def get(self, endpoint: str, params: dict | None = None) -> dict | None:
        """Выполняет GET-запрос."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Ошибка GET {url}: {e}")
            return None
    
    def post(self, endpoint: str, data: dict | None = None) -> dict | None:
        """Выполняет POST-запрос с JSON-телом."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Ошибка POST {url}: {e}")
            return None
    
    def close(self):
        """Закрывает сессию."""
        self.session.close()


def api_client(base_url: str) -> APIClient:
    """Создаёт API-клиент."""
    return APIClient(base_url)


# Использование
client = api_client("https://jsonplaceholder.typicode.com")

# GET запрос
users = client.get("/users", params={"_limit": 2})
if users:
    for user in users:
        print(f"User: {user['name']}")

# POST запрос
new_post = client.post("/posts", data={"title": "Test", "body": "Content", "userId": 1})
if new_post:
    print(f"Created post ID: {new_post['id']}")

client.close()
```

</details>

---

### Бонус 2: Retry с экспоненциальной задержкой

Напишите функцию `fetch_with_retry(url: str, max_retries: int = 3) -> dict | None`, которая:
1. Пытается выполнить GET-запрос
2. При ошибке соединения или таймаута — повторяет запрос
3. Между попытками ждёт с экспоненциальной задержкой (1с, 2с, 4с...)
4. После исчерпания попыток возвращает `None`

<details>
<summary>Решение</summary>

```python
import time

import requests
from requests.exceptions import ConnectionError, RequestException, Timeout


def fetch_with_retry(url: str, max_retries: int = 3) -> dict | None:
    """Выполняет GET-запрос с повторными попытками.
    
    Args:
        url: URL для запроса
        max_retries: Максимальное количество попыток
        
    Returns:
        JSON-ответ или None при неудаче
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except (ConnectionError, Timeout) as e:
            wait_time = 2 ** attempt  # 1, 2, 4, 8...
            print(f"Попытка {attempt + 1}/{max_retries} не удалась: {e}")
            if attempt < max_retries - 1:
                print(f"Ждём {wait_time} сек...")
                time.sleep(wait_time)
        except RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None
    
    print("Все попытки исчерпаны")
    return None


# Тестирование (нормальный URL)
result = fetch_with_retry("https://httpbin.org/get")
if result:
    print("Успех!")

# Тестирование (проблемный URL — будут retry)
result = fetch_with_retry("https://httpbin.org/delay/10")  # Таймаут 5с < задержка 10с
if result is None:
    print("Не удалось получить ответ")
```

</details>

---

## Полезные ресурсы

- [requests Documentation](https://docs.python-requests.org/) — официальная документация
- [httpbin.org](https://httpbin.org/) — сервис для тестирования HTTP
- [HTTP Status Codes](https://httpstatuses.com/) — справочник кодов
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) — фейковый REST API
- [Real Python — HTTP Requests](https://realpython.com/python-requests/) — подробное руководство
