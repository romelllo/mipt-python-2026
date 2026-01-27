"""
Семинар 4: Основы HTTP — примеры работы с библиотекой requests.

Этот модуль демонстрирует:
- Базовые HTTP запросы (GET, POST, PUT, DELETE)
- Работу с заголовками и параметрами
- Обработку ответов и ошибок
- Использование сессий

Для работы примеров используется сервис httpbin.org —
бесплатный сервис для тестирования HTTP запросов.
"""

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout
from urllib.parse import parse_qs, urlencode, urljoin, urlparse


def demonstrate_url_parsing() -> None:
    """Демонстрация разбора и создания URL."""
    print("=" * 60)
    print("1. Разбор URL (URL Parsing)")
    print("=" * 60)

    url = "https://api.example.com:8080/users/123?active=true&limit=10#section"

    parsed = urlparse(url)
    print(f"\nИсходный URL: {url}")
    print(f"  Схема (scheme):   {parsed.scheme}")
    print(f"  Хост (netloc):    {parsed.netloc}")
    print(f"  Порт (port):      {parsed.port}")
    print(f"  Путь (path):      {parsed.path}")
    print(f"  Параметры (query): {parsed.query}")
    print(f"  Якорь (fragment): {parsed.fragment}")

    # Парсинг параметров запроса
    params = parse_qs(parsed.query)
    print(f"\n  Распарсенные параметры: {params}")

    # Создание строки параметров
    new_params = {"search": "python", "page": 1, "sort": "name"}
    query_string = urlencode(new_params)
    print(f"\n  Новая строка параметров: {query_string}")

    # Объединение URL
    base_url = "https://api.example.com/v1/"
    endpoint = "users/123"
    full_url = urljoin(base_url, endpoint)
    print(f"\n  Объединение URL: {base_url} + {endpoint} = {full_url}")


def demonstrate_get_request() -> None:
    """Демонстрация GET запросов."""
    print("\n" + "=" * 60)
    print("2. GET запросы")
    print("=" * 60)

    # Простой GET запрос
    print("\n2.1 Простой GET запрос:")
    response = requests.get("https://httpbin.org/get", timeout=10)
    print(f"  Статус: {response.status_code}")
    print(f"  OK: {response.ok}")
    print(f"  Причина: {response.reason}")
    print(f"  Content-Type: {response.headers.get('Content-Type')}")

    # GET с параметрами
    print("\n2.2 GET с параметрами:")
    params = {"name": "Alice", "age": 25, "city": "Moscow"}
    response = requests.get("https://httpbin.org/get", params=params, timeout=10)
    data = response.json()
    print(f"  URL запроса: {response.url}")
    print(f"  Параметры на сервере: {data['args']}")

    # GET с заголовками
    print("\n2.3 GET с кастомными заголовками:")
    headers = {
        "User-Agent": "MyPythonApp/1.0",
        "Accept-Language": "ru-RU,en-US",
        "X-Custom-Header": "custom-value",
    }
    response = requests.get("https://httpbin.org/headers", headers=headers, timeout=10)
    data = response.json()
    print("  Заголовки, полученные сервером:")
    for key in ["User-Agent", "Accept-Language", "X-Custom-Header"]:
        print(f"    {key}: {data['headers'].get(key)}")


def demonstrate_post_request() -> None:
    """Демонстрация POST запросов."""
    print("\n" + "=" * 60)
    print("3. POST запросы")
    print("=" * 60)

    # POST с JSON телом
    print("\n3.1 POST с JSON:")
    json_data = {
        "username": "alice",
        "email": "alice@example.com",
        "roles": ["user", "editor"],
    }
    response = requests.post("https://httpbin.org/post", json=json_data, timeout=10)
    data = response.json()
    print(f"  Content-Type запроса: {data['headers'].get('Content-Type')}")
    print(f"  Данные на сервере: {data['json']}")

    # POST с form-data
    print("\n3.2 POST с form-data:")
    form_data = {"username": "alice", "password": "secret123"}
    response = requests.post("https://httpbin.org/post", data=form_data, timeout=10)
    data = response.json()
    print(f"  Content-Type запроса: {data['headers'].get('Content-Type')}")
    print(f"  Form данные: {data['form']}")


def demonstrate_other_methods() -> None:
    """Демонстрация других HTTP методов."""
    print("\n" + "=" * 60)
    print("4. Другие HTTP методы")
    print("=" * 60)

    # PUT запрос
    print("\n4.1 PUT запрос (полное обновление):")
    response = requests.put(
        "https://httpbin.org/put",
        json={"id": 1, "name": "Updated Name", "email": "new@example.com"},
        timeout=10,
    )
    print(f"  Статус: {response.status_code}")
    print(f"  Данные: {response.json()['json']}")

    # PATCH запрос
    print("\n4.2 PATCH запрос (частичное обновление):")
    response = requests.patch(
        "https://httpbin.org/patch", json={"name": "Only Name Updated"}, timeout=10
    )
    print(f"  Статус: {response.status_code}")
    print(f"  Данные: {response.json()['json']}")

    # DELETE запрос
    print("\n4.3 DELETE запрос:")
    response = requests.delete("https://httpbin.org/delete", timeout=10)
    print(f"  Статус: {response.status_code}")

    # HEAD запрос
    print("\n4.4 HEAD запрос (только заголовки):")
    response = requests.head("https://httpbin.org/get", timeout=10)
    print(f"  Статус: {response.status_code}")
    print(f"  Content-Type: {response.headers.get('Content-Type')}")
    print(f"  Тело ответа пустое: {len(response.content) == 0}")

    # OPTIONS запрос
    print("\n4.5 OPTIONS запрос (доступные методы):")
    response = requests.options("https://httpbin.org/get", timeout=10)
    print(f"  Статус: {response.status_code}")
    print(f"  Allow: {response.headers.get('Allow', 'не указано')}")


def demonstrate_status_codes() -> None:
    """Демонстрация различных HTTP статус-кодов."""
    print("\n" + "=" * 60)
    print("5. HTTP статус-коды")
    print("=" * 60)

    status_codes = [200, 201, 204, 301, 400, 401, 403, 404, 500]

    for code in status_codes:
        response = requests.get(
            f"https://httpbin.org/status/{code}", allow_redirects=False, timeout=10
        )
        category = {
            1: "Информационный",
            2: "Успех",
            3: "Перенаправление",
            4: "Ошибка клиента",
            5: "Ошибка сервера",
        }[code // 100]

        print(f"  {code}: {response.reason} ({category})")


def demonstrate_error_handling() -> None:
    """Демонстрация обработки ошибок."""
    print("\n" + "=" * 60)
    print("6. Обработка ошибок")
    print("=" * 60)

    # Таймаут
    print("\n6.1 Таймаут:")
    try:
        response = requests.get(
            "https://httpbin.org/delay/5",
            timeout=2,  # Ответ через 5 сек, таймаут 2 сек
        )
    except Timeout:
        print("  Поймано исключение: Timeout - превышено время ожидания")

    # HTTP ошибка
    print("\n6.2 HTTP ошибка (404):")
    try:
        response = requests.get("https://httpbin.org/status/404", timeout=10)
        response.raise_for_status()  # Выбросит HTTPError для 4xx/5xx
    except HTTPError as e:
        print(f"  Поймано исключение: HTTPError - {e.response.status_code}")

    # Ошибка подключения
    print("\n6.3 Ошибка подключения:")
    try:
        response = requests.get("https://nonexistent.invalid/", timeout=5)
    except ConnectionError:
        print("  Поймано исключение: ConnectionError - не удалось подключиться")

    # Общая обработка
    print("\n6.4 Общий паттерн обработки ошибок:")

    def safe_request(url: str) -> dict | None:
        """Безопасный HTTP запрос с обработкой всех ошибок."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Timeout:
            print(f"  Таймаут при запросе к {url}")
        except ConnectionError:
            print(f"  Не удалось подключиться к {url}")
        except HTTPError as e:
            print(f"  HTTP ошибка {e.response.status_code} для {url}")
        except RequestException as e:
            print(f"  Общая ошибка запроса: {e}")
        return None

    result = safe_request("https://httpbin.org/get")
    if result:
        print(f"  Успешный запрос, получено {len(result)} ключей")


def demonstrate_sessions() -> None:
    """Демонстрация использования сессий."""
    print("\n" + "=" * 60)
    print("7. HTTP сессии")
    print("=" * 60)

    print("\n7.1 Сессия сохраняет cookies:")
    with requests.Session() as session:
        # Устанавливаем cookie
        session.get("https://httpbin.org/cookies/set/session_id/abc123", timeout=10)
        session.get("https://httpbin.org/cookies/set/user/alice", timeout=10)

        # Проверяем cookies в следующем запросе
        response = session.get("https://httpbin.org/cookies", timeout=10)
        print(f"  Cookies в сессии: {response.json()['cookies']}")

    print("\n7.2 Сессия с базовыми заголовками:")
    with requests.Session() as session:
        # Устанавливаем заголовки для всех запросов в сессии
        session.headers.update(
            {
                "User-Agent": "MyApp/2.0",
                "Authorization": "Bearer my-secret-token",
            }
        )

        response = session.get("https://httpbin.org/headers", timeout=10)
        headers = response.json()["headers"]
        print(f"  User-Agent: {headers.get('User-Agent')}")
        print(f"  Authorization: {headers.get('Authorization')}")


def demonstrate_response_content() -> None:
    """Демонстрация различных типов содержимого ответа."""
    print("\n" + "=" * 60)
    print("8. Типы содержимого ответа")
    print("=" * 60)

    # JSON
    print("\n8.1 JSON ответ:")
    response = requests.get("https://httpbin.org/json", timeout=10)
    print(f"  Content-Type: {response.headers.get('Content-Type')}")
    data = response.json()
    print(f"  Тип данных: {type(data).__name__}")
    print(f"  Ключи: {list(data.keys())}")

    # HTML
    print("\n8.2 HTML ответ:")
    response = requests.get("https://httpbin.org/html", timeout=10)
    print(f"  Content-Type: {response.headers.get('Content-Type')}")
    print(f"  Первые 100 символов: {response.text[:100]}...")

    # Бинарные данные (изображение)
    print("\n8.3 Бинарный ответ (изображение):")
    response = requests.get("https://httpbin.org/image/png", timeout=10)
    print(f"  Content-Type: {response.headers.get('Content-Type')}")
    print(f"  Размер: {len(response.content)} байт")
    print(f"  Первые байты (PNG signature): {response.content[:8].hex()}")


def main() -> None:
    """Главная функция — запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 4: ОСНОВЫ HTTP")
    print("Примеры работы с библиотекой requests")
    print("=" * 60)

    demonstrate_url_parsing()
    demonstrate_get_request()
    demonstrate_post_request()
    demonstrate_other_methods()
    demonstrate_status_codes()
    demonstrate_error_handling()
    demonstrate_sessions()
    demonstrate_response_content()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
