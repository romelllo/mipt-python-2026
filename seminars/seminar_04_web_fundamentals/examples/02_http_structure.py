"""
Семинар 4: Структура HTTP запроса и ответа.

Этот модуль демонстрирует:
- Структуру HTTP-запроса: стартовая строка, заголовки, тело
- Структуру HTTP-ответа: статус, заголовки, тело
- Различные HTTP-методы
- Коды ответов HTTP
"""

import requests

# ============================================================
# 1. Структура HTTP-запроса
# ============================================================


def demonstrate_request_structure() -> None:
    """Демонстрация структуры HTTP-запроса."""
    print("=" * 60)
    print("1. Структура HTTP-запроса")
    print("=" * 60)

    print("""
  HTTP-запрос состоит из 3 частей:

  ┌─────────────────────────────────────────────────────────┐
  │ 1. СТАРТОВАЯ СТРОКА (Request Line)                      │
  │    GET /users?page=1 HTTP/1.1                           │
  │    ^^^  ^^^^^^^^^^^^  ^^^^^^^                           │
  │   метод    путь       версия                            │
  ├─────────────────────────────────────────────────────────┤
  │ 2. ЗАГОЛОВКИ (Headers)                                  │
  │    Host: api.example.com                                │
  │    Content-Type: application/json                       │
  │    Authorization: Bearer token123                       │
  │    User-Agent: MyApp/1.0                                │
  │                                                         │
  ├─────────────────────────────────────────────────────────┤
  │ 3. ТЕЛО (Body) — опционально                            │
  │    {"name": "Alice", "email": "alice@example.com"}      │
  └─────────────────────────────────────────────────────────┘
    """)

    # Пример реального запроса
    print("  Пример реального запроса (requests показывает PreparedRequest):")
    req = requests.Request(
        method="POST",
        url="https://api.example.com/users",
        headers={
            "Authorization": "Bearer my-token",
            "Content-Type": "application/json",
        },
        json={"name": "Alice", "email": "alice@example.com"},
    )
    prepared = req.prepare()

    print(f"\n    Метод: {prepared.method}")
    print(f"    URL: {prepared.url}")
    print("    Заголовки:")
    for key, value in prepared.headers.items():
        print(f"      {key}: {value}")
    print(f"    Тело: {prepared.body}")


# ============================================================
# 2. HTTP методы
# ============================================================


def demonstrate_http_methods() -> None:
    """Демонстрация различных HTTP-методов."""
    print("\n" + "=" * 60)
    print("2. HTTP методы")
    print("=" * 60)

    print("""
  ┌─────────┬────────────────────────────┬───────────┬──────────────┐
  │ Метод   │ Назначение                 │ Есть тело │ Идемпотентный│
  ├─────────┼────────────────────────────┼───────────┼──────────────┤
  │ GET     │ Получить ресурс            │ Нет       │ Да           │
  │ POST    │ Создать новый ресурс       │ Да        │ Нет          │
  │ PUT     │ Заменить ресурс целиком    │ Да        │ Да           │
  │ PATCH   │ Частично обновить ресурс   │ Да        │ Нет          │
  │ DELETE  │ Удалить ресурс             │ Обычно нет│ Да           │
  │ HEAD    │ Получить только заголовки  │ Нет       │ Да           │
  │ OPTIONS │ Узнать доступные методы    │ Нет       │ Да           │
  └─────────┴────────────────────────────┴───────────┴──────────────┘

  Идемпотентность: повторный запрос даёт тот же результат.
    """)

    # Демонстрация методов на httpbin.org
    print("  Демонстрация на httpbin.org:")

    # GET
    print("\n  GET /get — получаем данные:")
    response = requests.get("https://httpbin.org/get", timeout=10)
    print(f"    Статус: {response.status_code} {response.reason}")

    # POST
    print("\n  POST /post — отправляем данные:")
    response = requests.post(
        "https://httpbin.org/post",
        json={"action": "create"},
        timeout=10,
    )
    print(f"    Статус: {response.status_code} {response.reason}")

    # PUT
    print("\n  PUT /put — заменяем ресурс:")
    response = requests.put(
        "https://httpbin.org/put",
        json={"id": 1, "name": "Updated"},
        timeout=10,
    )
    print(f"    Статус: {response.status_code} {response.reason}")

    # DELETE
    print("\n  DELETE /delete — удаляем ресурс:")
    response = requests.delete("https://httpbin.org/delete", timeout=10)
    print(f"    Статус: {response.status_code} {response.reason}")


# ============================================================
# 3. Заголовки запроса
# ============================================================


def demonstrate_request_headers() -> None:
    """Демонстрация заголовков HTTP-запроса."""
    print("\n" + "=" * 60)
    print("3. Заголовки запроса (Request Headers)")
    print("=" * 60)

    print("""
  Важные заголовки запроса:

  ┌──────────────────┬──────────────────────────────────────────┐
  │ Заголовок        │ Описание                                 │
  ├──────────────────┼──────────────────────────────────────────┤
  │ Host             │ Имя сервера (обязательный в HTTP/1.1)    │
  │ Content-Type     │ Формат тела запроса                      │
  │ Accept           │ Ожидаемый формат ответа                  │
  │ Authorization    │ Данные аутентификации                    │
  │ User-Agent       │ Информация о клиенте                     │
  │ Accept-Language  │ Предпочитаемые языки                     │
  │ Accept-Encoding  │ Поддерживаемые алгоритмы сжатия          │
  │ Content-Length   │ Размер тела в байтах                     │
  │ Cookie           │ Cookies для отправки на сервер           │
  └──────────────────┴──────────────────────────────────────────┘
    """)

    # Отправляем запрос с заголовками и смотрим, что получил сервер
    print("  Отправляем запрос с кастомными заголовками:")
    headers = {
        "User-Agent": "MyPythonApp/1.0",
        "Accept": "application/json",
        "Accept-Language": "ru-RU,en-US",
        "Authorization": "Bearer my-secret-token",
        "X-Custom-Header": "custom-value",
    }

    response = requests.get(
        "https://httpbin.org/headers",
        headers=headers,
        timeout=10,
    )

    print("\n  Заголовки, которые получил сервер:")
    received_headers = response.json()["headers"]
    for key, value in received_headers.items():
        print(f"    {key}: {value}")


# ============================================================
# 4. Структура HTTP-ответа
# ============================================================


def demonstrate_response_structure() -> None:
    """Демонстрация структуры HTTP-ответа."""
    print("\n" + "=" * 60)
    print("4. Структура HTTP-ответа")
    print("=" * 60)

    print("""
  HTTP-ответ состоит из 3 частей:

  ┌─────────────────────────────────────────────────────────┐
  │ 1. СТРОКА СТАТУСА (Status Line)                         │
  │    HTTP/1.1 200 OK                                      │
  │    ^^^^^^^  ^^^ ^^                                      │
  │    версия   код описание                                │
  ├─────────────────────────────────────────────────────────┤
  │ 2. ЗАГОЛОВКИ ОТВЕТА (Response Headers)                  │
  │    Content-Type: application/json                       │
  │    Content-Length: 156                                  │
  │    Date: Tue, 25 Feb 2026 10:00:00 GMT                  │
  │    Server: nginx/1.18.0                                 │
  │                                                         │
  ├─────────────────────────────────────────────────────────┤
  │ 3. ТЕЛО ОТВЕТА (Response Body)                          │
  │    {"id": 1, "name": "Alice", "email": "a@example.com"} │
  └─────────────────────────────────────────────────────────┘
    """)

    # Получаем реальный ответ
    print("  Пример реального ответа:")
    response = requests.get("https://httpbin.org/get", timeout=10)

    print("\n    Строка статуса:")
    print("      HTTP версия: HTTP/1.1")
    print(f"      Код: {response.status_code}")
    print(f"      Описание: {response.reason}")

    print("\n    Заголовки ответа:")
    important_headers = ["Content-Type", "Content-Length", "Date", "Server"]
    for header in important_headers:
        value = response.headers.get(header, "не указан")
        print(f"      {header}: {value}")

    print("\n    Тело ответа (первые 200 символов):")
    print(f"      {response.text[:200]}...")


# ============================================================
# 5. Коды ответов HTTP
# ============================================================


def demonstrate_status_codes() -> None:
    """Демонстрация кодов ответов HTTP."""
    print("\n" + "=" * 60)
    print("5. Коды ответов HTTP")
    print("=" * 60)

    print("""
  ┌─────────┬─────────────────────┬───────────────────────────────┐
  │ Диапазон│ Категория           │ Примеры                       │
  ├─────────┼─────────────────────┼───────────────────────────────┤
  │ 1xx     │ Информационные      │ 100 Continue                  │
  │ 2xx     │ Успех               │ 200 OK, 201 Created, 204 None │
  │ 3xx     │ Перенаправление     │ 301 Moved, 302 Found          │
  │ 4xx     │ Ошибка клиента      │ 400 Bad, 401 Unauth, 404 None │
  │ 5xx     │ Ошибка сервера      │ 500 Internal, 502 Bad Gateway │
  └─────────┴─────────────────────┴───────────────────────────────┘
    """)

    # Демонстрация разных кодов
    print("  Демонстрация разных кодов на httpbin.org:")
    codes = [200, 201, 204, 301, 400, 401, 404, 500]

    for code in codes:
        response = requests.get(
            f"https://httpbin.org/status/{code}",
            allow_redirects=False,
            timeout=10,
        )

        category = {
            2: "✓ Успех",
            3: "→ Редирект",
            4: "✗ Ошибка клиента",
            5: "✗ Ошибка сервера",
        }.get(code // 100, "?")

        print(f"    {code} {response.reason:20} ({category})")


# ============================================================
# 6. Content-Type: форматы данных
# ============================================================


def demonstrate_content_types() -> None:
    """Демонстрация различных Content-Type."""
    print("\n" + "=" * 60)
    print("6. Content-Type: форматы данных")
    print("=" * 60)

    print("""
  Популярные значения Content-Type:

  ┌────────────────────────────────────┬──────────────────────────┐
  │ Content-Type                       │ Описание                 │
  ├────────────────────────────────────┼──────────────────────────┤
  │ application/json                   │ JSON данные              │
  │ application/x-www-form-urlencoded  │ Form данные (по умолчан.)│
  │ multipart/form-data                │ Файлы и форма            │
  │ text/html                          │ HTML страница            │
  │ text/plain                         │ Обычный текст            │
  │ application/xml                    │ XML данные               │
  │ image/png, image/jpeg              │ Изображения              │
  │ application/octet-stream           │ Бинарные данные          │
  └────────────────────────────────────┴──────────────────────────┘
    """)

    # Демонстрация разных форматов
    print("  Примеры ответов с разными Content-Type:")

    # JSON
    response = requests.get("https://httpbin.org/json", timeout=10)
    print(f"\n    JSON: {response.headers.get('Content-Type')}")
    print(f"    Тело: {str(response.json())[:60]}...")

    # HTML
    response = requests.get("https://httpbin.org/html", timeout=10)
    print(f"\n    HTML: {response.headers.get('Content-Type')}")
    print(f"    Тело: {response.text[:60]}...")

    # Изображение
    response = requests.get("https://httpbin.org/image/png", timeout=10)
    print(f"\n    PNG: {response.headers.get('Content-Type')}")
    print(f"    Размер: {len(response.content)} байт")


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 4: СТРУКТУРА HTTP ЗАПРОСА И ОТВЕТА")
    print("=" * 60)

    demonstrate_request_structure()
    demonstrate_http_methods()
    demonstrate_request_headers()
    demonstrate_response_structure()
    demonstrate_status_codes()
    demonstrate_content_types()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
