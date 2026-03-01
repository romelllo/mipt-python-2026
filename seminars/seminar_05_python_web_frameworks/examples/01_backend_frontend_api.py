"""
Семинар 5: Бэкенд, фронтенд и API — примеры запросов к публичным API.

Этот модуль демонстрирует:
- Что такое API на практике
- Как отправлять запросы к публичным REST API
- Разницу между разными HTTP-методами при работе с API
- Формат JSON-ответов
"""

import requests
from requests.exceptions import RequestException

# ============================================================
# 1. Что такое API — простой пример
# ============================================================


def demonstrate_api_basics() -> None:
    """Демонстрация базовых концепций API."""
    print("=" * 60)
    print("1. Что такое API — простой пример")
    print("=" * 60)

    # API — это интерфейс для взаимодействия с сервером.
    # Мы отправляем HTTP-запрос, сервер возвращает данные (обычно JSON).

    print("\n  1.1 GET-запрос к публичному API:")
    print("  Запрашиваем случайную шутку...")

    try:
        response = requests.get(
            "https://official-joke-api.appspot.com/random_joke",
            timeout=10,
        )
        if response.ok:
            joke = response.json()
            print(f"    Тип: {joke.get('type')}")
            print(f"    Вопрос: {joke.get('setup')}")
            print(f"    Ответ: {joke.get('punchline')}")
        else:
            print(f"    Ошибка: {response.status_code}")
    except RequestException as e:
        print(f"    Ошибка соединения: {e}")

    print("\n  1.2 API возвращает данные в формате JSON:")
    print("  JSON — это текстовый формат для обмена данными.")
    print("  В Python JSON автоматически конвертируется в dict/list.")

    try:
        response = requests.get(
            "https://jsonplaceholder.typicode.com/users/1",
            timeout=10,
        )
        user = response.json()
        print(f"    Тип ответа: {type(user).__name__}")
        print(f"    Имя: {user['name']}")
        print(f"    Email: {user['email']}")
        print(f"    Город: {user['address']['city']}")
    except RequestException as e:
        print(f"    Ошибка: {e}")


# ============================================================
# 2. REST API — CRUD операции
# ============================================================


def demonstrate_rest_api() -> None:
    """Демонстрация REST API: создание, чтение, обновление, удаление."""
    print("\n" + "=" * 60)
    print("2. REST API — CRUD операции")
    print("=" * 60)

    base_url = "https://jsonplaceholder.typicode.com"

    # CREATE — POST
    print("\n  2.1 CREATE (POST) — создание ресурса:")
    new_post = {
        "title": "Мой первый пост",
        "body": "Привет, мир!",
        "userId": 1,
    }
    try:
        response = requests.post(f"{base_url}/posts", json=new_post, timeout=10)
        print(f"    Статус: {response.status_code}")
        print(f"    Созданный пост: {response.json()}")
    except RequestException as e:
        print(f"    Ошибка: {e}")

    # READ — GET
    print("\n  2.2 READ (GET) — чтение ресурсов:")
    try:
        # Список ресурсов
        response = requests.get(f"{base_url}/posts", params={"_limit": 3}, timeout=10)
        posts = response.json()
        print(f"    Получено постов: {len(posts)}")
        for post in posts:
            print(f"    [{post['id']}] {post['title'][:50]}...")
    except RequestException as e:
        print(f"    Ошибка: {e}")

    # UPDATE — PUT
    print("\n  2.3 UPDATE (PUT) — обновление ресурса:")
    updated_post = {
        "id": 1,
        "title": "Обновлённый заголовок",
        "body": "Обновлённый текст",
        "userId": 1,
    }
    try:
        response = requests.put(f"{base_url}/posts/1", json=updated_post, timeout=10)
        print(f"    Статус: {response.status_code}")
        print(f"    Обновлённый пост: {response.json()['title']}")
    except RequestException as e:
        print(f"    Ошибка: {e}")

    # DELETE — DELETE
    print("\n  2.4 DELETE — удаление ресурса:")
    try:
        response = requests.delete(f"{base_url}/posts/1", timeout=10)
        print(f"    Статус: {response.status_code}")
        print("    Пост удалён (фейковое API, но статус корректный)")
    except RequestException as e:
        print(f"    Ошибка: {e}")


# ============================================================
# 3. Разница между фронтендом и бэкендом на примере
# ============================================================


def demonstrate_frontend_vs_backend() -> None:
    """Демонстрация разницы между фронтендом и бэкендом."""
    print("\n" + "=" * 60)
    print("3. Фронтенд vs Бэкенд")
    print("=" * 60)

    print("""
  Фронтенд (клиент):
  - Браузер отправляет запрос на сервер
  - Получает HTML/JSON ответ
  - Отображает данные пользователю

  Бэкенд (сервер):
  - Принимает HTTP-запросы
  - Обрабатывает бизнес-логику
  - Работает с базой данных
  - Формирует и возвращает ответ

  Пример: когда вы открываете github.com/users
  1. Браузер (фронтенд) отправляет GET /users
  2. Сервер (бэкенд) запрашивает пользователей из БД
  3. Сервер формирует HTML-страницу
  4. Браузер отображает страницу
    """)

    # Демонстрация: один и тот же ресурс может возвращать
    # HTML (для браузера) или JSON (для API)
    print("  Бэкенд может возвращать разные форматы:")

    try:
        # JSON-ответ (для API-клиентов)
        response = requests.get(
            "https://jsonplaceholder.typicode.com/posts/1",
            timeout=10,
        )
        print(f"\n  JSON-ответ (Content-Type: {response.headers.get('Content-Type')}):")
        data = response.json()
        print(f"    title: {data['title'][:50]}...")

        # HTML-ответ (для браузера)
        response = requests.get("https://httpbin.org/html", timeout=10)
        print(f"\n  HTML-ответ (Content-Type: {response.headers.get('Content-Type')}):")
        print(f"    Первые 80 символов: {response.text[:80]}...")
    except RequestException as e:
        print(f"    Ошибка: {e}")


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 5: БЭКЕНД, ФРОНТЕНД И API")
    print("=" * 60)

    demonstrate_api_basics()
    demonstrate_rest_api()
    demonstrate_frontend_vs_backend()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
