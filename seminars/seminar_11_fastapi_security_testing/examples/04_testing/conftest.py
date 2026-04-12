"""Конфигурация pytest для тестов auth_app.

conftest.py автоматически загружается pytest перед тестами.
Здесь определяем fixtures, которые используются во всех тестах.
"""

import importlib
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

# Загружаем auth_app через importlib (имя папки начинается с цифры)
_BASE = "seminars.seminar_11_fastapi_security_testing.examples"
_main = importlib.import_module(f"{_BASE}.03_auth_app.main")
_deps = importlib.import_module(f"{_BASE}.03_auth_app.dependencies")

app = _main.app
fake_users_db: dict = _deps.fake_users_db


@pytest.fixture
def client() -> TestClient:
    """Создать TestClient для тестирования FastAPI приложения.

    TestClient использует httpx под капотом и не запускает реальный сервер.
    Он вызывает приложение напрямую — быстро и без сетевых задержек.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_users_db() -> Generator[None, None, None]:
    """Очистить базу пользователей перед каждым тестом.

    autouse=True означает, что fixture применяется ко всем тестам
    автоматически — не нужно явно указывать его в параметрах.

    Это обеспечивает ИЗОЛЯЦИЮ тестов: каждый тест начинает
    с чистой "базой данных".
    """
    fake_users_db.clear()
    yield
    # После теста тоже чистим
    fake_users_db.clear()


@pytest.fixture
def registered_user(client: TestClient) -> dict:
    """Зарегистрировать тестового пользователя.

    Returns:
        словарь с username и password для использования в тестах
    """
    user_data = {"username": "testuser", "password": "testpass123"}
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    return user_data


@pytest.fixture
def auth_token(client: TestClient, registered_user: dict) -> str:
    """Получить JWT токен для тестового пользователя.

    Returns:
        JWT access token в виде строки
    """
    response = client.post(
        "/auth/login",
        data={  # form-encoded, не JSON!
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    return str(response.json()["access_token"])


@pytest.fixture
def auth_headers(auth_token: str) -> dict[str, str]:
    """Заголовки авторизации для защищённых эндпоинтов.

    Returns:
        словарь {"Authorization": "Bearer <token>"}
    """
    return {"Authorization": f"Bearer {auth_token}"}
