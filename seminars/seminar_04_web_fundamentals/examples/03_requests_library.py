"""
Семинар 4: Библиотека requests — полное руководство.

Этот модуль демонстрирует:
- GET, POST, PUT, PATCH, DELETE запросы
- Параметры запроса и заголовки
- Обработку ответов (JSON, текст, бинарные данные)
- Обработку ошибок и таймауты
- Работу с сессиями
"""

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

# ============================================================
# 1. GET запросы
# ============================================================


def demonstrate_get_requests() -> None:
    """Демонстрация GET-запросов."""
    print("=" * 60)
    print("1. GET запросы")
    print("=" * 60)

    # Простой GET запрос
    print("\n  1.1 Простой GET запрос:")
    response = requests.get("https://httpbin.org/get", timeout=10)
    print(f"    URL: {response.url}")
    print(f"    Статус: {response.status_code} {response.reason}")
    print(f"    OK: {response.ok}")

    # GET с query-параметрами
    print("\n  1.2 GET с параметрами (query string):")
    params = {
        "name": "Alice",
        "age": 25,
        "city": "Moscow",
    }
    response = requests.get("https://httpbin.org/get", params=params, timeout=10)
    print(f"    URL (с параметрами): {response.url}")
    data = response.json()
    print(f"    Параметры на сервере: {data['args']}")

    # GET с заголовками
    print("\n  1.3 GET с кастомными заголовками:")
    headers = {
        "User-Agent": "MyPythonApp/1.0",
        "Accept-Language": "ru-RU,en",
        "Authorization": "Bearer my-secret-token",
    }
    response = requests.get("https://httpbin.org/headers", headers=headers, timeout=10)
    received = response.json()["headers"]
    print(f"    User-Agent: {received.get('User-Agent')}")
    print(f"    Authorization: {received.get('Authorization')}")


# ============================================================
# 2. POST запросы
# ============================================================


def demonstrate_post_requests() -> None:
    """Демонстрация POST-запросов."""
    print("\n" + "=" * 60)
    print("2. POST запросы")
    print("=" * 60)

    # POST с JSON телом
    print("\n  2.1 POST с JSON телом:")
    json_data = {
        "username": "alice",
        "email": "alice@example.com",
        "roles": ["user", "admin"],
    }
    response = requests.post("https://httpbin.org/post", json=json_data, timeout=10)
    result = response.json()
    print(f"    Content-Type запроса: {result['headers'].get('Content-Type')}")
    print(f"    Данные на сервере: {result['json']}")

    # POST с form-data
    print("\n  2.2 POST с form-data:")
    form_data = {
        "username": "alice",
        "password": "secret123",
    }
    response = requests.post("https://httpbin.org/post", data=form_data, timeout=10)
    result = response.json()
    print(f"    Content-Type запроса: {result['headers'].get('Content-Type')}")
    print(f"    Form данные: {result['form']}")

    # POST без тела
    print("\n  2.3 POST без тела (например, для trigger-эндпоинтов):")
    response = requests.post("https://httpbin.org/post", timeout=10)
    print(f"    Статус: {response.status_code}")


# ============================================================
# 3. PUT, PATCH, DELETE запросы
# ============================================================


def demonstrate_other_methods() -> None:
    """Демонстрация PUT, PATCH, DELETE запросов."""
    print("\n" + "=" * 60)
    print("3. PUT, PATCH, DELETE запросы")
    print("=" * 60)

    # PUT — полная замена ресурса
    print("\n  3.1 PUT (полная замена ресурса):")
    full_data = {
        "id": 1,
        "name": "Alice Updated",
        "email": "alice.new@example.com",
        "active": True,
    }
    response = requests.put("https://httpbin.org/put", json=full_data, timeout=10)
    print(f"    Статус: {response.status_code}")
    print(f"    Отправленные данные: {response.json()['json']}")

    # PATCH — частичное обновление
    print("\n  3.2 PATCH (частичное обновление):")
    partial_data = {"name": "Alice Patched"}
    response = requests.patch(
        "https://httpbin.org/patch", json=partial_data, timeout=10
    )
    print(f"    Статус: {response.status_code}")
    print(f"    Отправленные данные: {response.json()['json']}")

    # DELETE — удаление
    print("\n  3.3 DELETE (удаление ресурса):")
    response = requests.delete("https://httpbin.org/delete", timeout=10)
    print(f"    Статус: {response.status_code}")


# ============================================================
# 4. Работа с ответом (Response)
# ============================================================


def demonstrate_response_handling() -> None:
    """Демонстрация работы с объектом Response."""
    print("\n" + "=" * 60)
    print("4. Работа с объектом Response")
    print("=" * 60)

    response = requests.get("https://httpbin.org/get", timeout=10)

    print("\n  4.1 Статус ответа:")
    print(f"    status_code: {response.status_code}")
    print(f"    reason: {response.reason}")
    print(f"    ok: {response.ok}")

    print("\n  4.2 Заголовки ответа:")
    print(f"    Content-Type: {response.headers.get('Content-Type')}")
    print(f"    Content-Length: {response.headers.get('Content-Length')}")
    print(f"    Date: {response.headers.get('Date')}")

    print("\n  4.3 Тело ответа:")
    print(f"    text (строка): {response.text[:80]}...")
    print(f"    json() (dict): {type(response.json())}")
    print(f"    content (bytes): {len(response.content)} байт")

    print("\n  4.4 Метаданные:")
    print(f"    url (финальный): {response.url}")
    print(f"    elapsed (время): {response.elapsed}")
    print(f"    encoding: {response.encoding}")


# ============================================================
# 5. Таймауты — ОБЯЗАТЕЛЬНЫ!
# ============================================================


def demonstrate_timeouts() -> None:
    """Демонстрация работы с таймаутами."""
    print("\n" + "=" * 60)
    print("5. Таймауты — ОБЯЗАТЕЛЬНЫ!")
    print("=" * 60)

    print("""
  ⚠️  ВАЖНО: Всегда указывайте timeout!
      Без таймаута запрос может зависнуть НАВСЕГДА.
    """)

    # Простой таймаут
    print("  5.1 Простой таймаут (общий):")
    response = requests.get(
        "https://httpbin.org/delay/1",  # Сервер отвечает через 1 сек
        timeout=5,  # Ждём максимум 5 секунд
    )
    print(f"    Ответ получен за {response.elapsed}")

    # Раздельные таймауты
    print("\n  5.2 Раздельные таймауты (connect, read):")
    response = requests.get(
        "https://httpbin.org/delay/1",
        timeout=(3, 10),  # connect=3с, read=10с
    )
    print(f"    Ответ получен за {response.elapsed}")

    # Демонстрация истечения таймаута
    print("\n  5.3 Истечение таймаута:")
    try:
        response = requests.get(
            "https://httpbin.org/delay/5",  # Сервер отвечает через 5 сек
            timeout=2,  # Ждём максимум 2 секунды
        )
    except Timeout:
        print("    ✗ Timeout — время ожидания истекло!")


# ============================================================
# 6. Обработка ошибок
# ============================================================


def demonstrate_error_handling() -> None:
    """Демонстрация обработки ошибок."""
    print("\n" + "=" * 60)
    print("6. Обработка ошибок")
    print("=" * 60)

    print("""
  Иерархия исключений requests:
    RequestException (базовый)
    ├── ConnectionError (нет соединения)
    ├── Timeout (истёк таймаут)
    └── HTTPError (4xx/5xx коды)
    """)

    # HTTPError с raise_for_status()
    print("  6.1 HTTPError (код 404):")
    try:
        response = requests.get("https://httpbin.org/status/404", timeout=10)
        response.raise_for_status()  # Выбросит HTTPError для 4xx/5xx
    except HTTPError as e:
        print(f"    ✗ HTTPError: {e.response.status_code}")

    # ConnectionError
    print("\n  6.2 ConnectionError (несуществующий хост):")
    try:
        response = requests.get(
            "https://this-domain-does-not-exist.invalid/", timeout=5
        )
    except ConnectionError:
        print("    ✗ ConnectionError: не удалось подключиться")

    # Паттерн обработки всех ошибок
    print("\n  6.3 Паттерн полной обработки ошибок:")

    def safe_get(url: str) -> dict | None:
        """Безопасный GET-запрос с обработкой всех ошибок."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Timeout:
            print(f"    Таймаут: {url}")
        except ConnectionError:
            print(f"    Нет соединения: {url}")
        except HTTPError as e:
            print(f"    HTTP {e.response.status_code}: {url}")
        except RequestException as e:
            print(f"    Ошибка: {e}")
        return None

    result = safe_get("https://httpbin.org/get")
    if result:
        print(f"    ✓ Успех! Получено {len(result)} ключей")


# ============================================================
# 7. Сессии
# ============================================================


def demonstrate_sessions() -> None:
    """Демонстрация работы с сессиями."""
    print("\n" + "=" * 60)
    print("7. Сессии (Sessions)")
    print("=" * 60)

    print("""
  Сессия позволяет:
    - Сохранять cookies между запросами
    - Использовать общие заголовки
    - Поддерживать keep-alive соединения
    """)

    # Сессия сохраняет cookies
    print("  7.1 Сессия сохраняет cookies:")
    with requests.Session() as session:
        # Устанавливаем cookies
        session.get("https://httpbin.org/cookies/set/user_id/123", timeout=10)
        session.get("https://httpbin.org/cookies/set/token/abc", timeout=10)

        # Проверяем cookies
        response = session.get("https://httpbin.org/cookies", timeout=10)
        print(f"    Cookies в сессии: {response.json()['cookies']}")

    # Сессия с общими заголовками
    print("\n  7.2 Сессия с общими заголовками:")
    with requests.Session() as session:
        session.headers.update(
            {
                "User-Agent": "MyApp/2.0",
                "Authorization": "Bearer session-token",
            }
        )

        response = session.get("https://httpbin.org/headers", timeout=10)
        headers = response.json()["headers"]
        print(f"    User-Agent: {headers.get('User-Agent')}")
        print(f"    Authorization: {headers.get('Authorization')}")


# ============================================================
# 8. Практический пример: REST API клиент
# ============================================================


def demonstrate_rest_client() -> None:
    """Демонстрация работы с REST API."""
    print("\n" + "=" * 60)
    print("8. Практический пример: REST API клиент")
    print("=" * 60)

    # Используем JSONPlaceholder — фейковый REST API
    base_url = "https://jsonplaceholder.typicode.com"

    # GET — список ресурсов
    print("\n  8.1 GET /posts?_limit=3 (список постов):")
    response = requests.get(f"{base_url}/posts", params={"_limit": 3}, timeout=10)
    posts = response.json()
    for post in posts:
        print(f"    [{post['id']}] {post['title'][:40]}...")

    # GET — один ресурс
    print("\n  8.2 GET /posts/1 (один пост):")
    response = requests.get(f"{base_url}/posts/1", timeout=10)
    post = response.json()
    print(f"    ID: {post['id']}")
    print(f"    Title: {post['title']}")

    # POST — создание ресурса
    print("\n  8.3 POST /posts (создание поста):")
    new_post = {
        "title": "Мой новый пост",
        "body": "Содержимое поста...",
        "userId": 1,
    }
    response = requests.post(f"{base_url}/posts", json=new_post, timeout=10)
    print(f"    Статус: {response.status_code}")
    print(f"    Созданный ID: {response.json()['id']}")

    # PUT — обновление ресурса
    print("\n  8.4 PUT /posts/1 (обновление поста):")
    updated_post = {
        "id": 1,
        "title": "Обновлённый заголовок",
        "body": "Новое содержимое",
        "userId": 1,
    }
    response = requests.put(f"{base_url}/posts/1", json=updated_post, timeout=10)
    print(f"    Статус: {response.status_code}")
    print(f"    Title: {response.json()['title']}")

    # DELETE — удаление ресурса
    print("\n  8.5 DELETE /posts/1 (удаление поста):")
    response = requests.delete(f"{base_url}/posts/1", timeout=10)
    print(f"    Статус: {response.status_code}")


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 4: БИБЛИОТЕКА REQUESTS — ПОЛНОЕ РУКОВОДСТВО")
    print("=" * 60)

    demonstrate_get_requests()
    demonstrate_post_requests()
    demonstrate_other_methods()
    demonstrate_response_handling()
    demonstrate_timeouts()
    demonstrate_error_handling()
    demonstrate_sessions()
    demonstrate_rest_client()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
