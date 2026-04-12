"""Тесты для auth_app — полный flow аутентификации.

Запуск:
    pytest seminars/seminar_11_fastapi_security_testing/examples/04_testing/ -v

Покрытие:
    pytest seminars/seminar_11_fastapi_security_testing/examples/04_testing/ --cov -v
"""

import importlib
from datetime import timedelta

from fastapi.testclient import TestClient

# Загружаем auth модуль через importlib (имя папки начинается с цифры)
_auth = importlib.import_module(
    "seminars.seminar_11_fastapi_security_testing.examples.03_auth_app.auth"
)
create_access_token = _auth.create_access_token


# ============================================================
# Тесты регистрации (POST /auth/register)
# ============================================================


class TestRegistration:
    """Тесты эндпоинта регистрации."""

    def test_register_success(self, client: TestClient) -> None:
        """Успешная регистрация нового пользователя."""
        response = client.post(
            "/auth/register",
            json={"username": "alice", "password": "secret123"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "alice"
        assert data["is_active"] is True
        # Пароль НИКОГДА не должен возвращаться в ответе
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_duplicate_username(self, client: TestClient) -> None:
        """Нельзя зарегистрировать двух пользователей с одинаковым username."""
        user = {"username": "alice", "password": "secret123"}
        client.post("/auth/register", json=user)  # первая регистрация

        # Вторая регистрация с тем же username
        response = client.post("/auth/register", json=user)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_register_short_password(self, client: TestClient) -> None:
        """Пароль меньше 6 символов должен быть отклонён."""
        response = client.post(
            "/auth/register",
            json={"username": "alice", "password": "123"},
        )
        assert response.status_code == 422  # Unprocessable Entity

    def test_register_short_username(self, client: TestClient) -> None:
        """Username меньше 3 символов должен быть отклонён."""
        response = client.post(
            "/auth/register",
            json={"username": "ab", "password": "secret123"},
        )
        assert response.status_code == 422


# ============================================================
# Тесты логина (POST /auth/login)
# ============================================================


class TestLogin:
    """Тесты эндпоинта логина."""

    def test_login_success(self, client: TestClient, registered_user: dict) -> None:
        """Успешный логин возвращает JWT токен."""
        response = client.post(
            "/auth/login",
            data={  # OAuth2PasswordRequestForm требует form-data!
                "username": registered_user["username"],
                "password": registered_user["password"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        # Токен — это непустая строка
        assert len(data["access_token"]) > 10

    def test_login_wrong_password(
        self, client: TestClient, registered_user: dict
    ) -> None:
        """Неверный пароль → 401 Unauthorized."""
        response = client.post(
            "/auth/login",
            data={
                "username": registered_user["username"],
                "password": "wrong_password",
            },
        )
        assert response.status_code == 401
        assert "Incorrect" in response.json()["detail"]

    def test_login_nonexistent_user(self, client: TestClient) -> None:
        """Попытка войти за несуществующего пользователя → 401."""
        response = client.post(
            "/auth/login",
            data={"username": "nobody", "password": "any_password"},
        )
        assert response.status_code == 401

    def test_login_returns_jwt_structure(
        self, client: TestClient, registered_user: dict
    ) -> None:
        """Токен имеет структуру JWT (три части разделённые точками)."""
        response = client.post(
            "/auth/login",
            data={
                "username": registered_user["username"],
                "password": registered_user["password"],
            },
        )
        token = response.json()["access_token"]
        parts = token.split(".")
        assert len(parts) == 3, "JWT должен состоять из трёх частей"


# ============================================================
# Тесты защищённых эндпоинтов
# ============================================================


class TestProtectedEndpoints:
    """Тесты эндпоинтов, требующих аутентификации."""

    def test_get_me_success(
        self, client: TestClient, registered_user: dict, auth_headers: dict
    ) -> None:
        """GET /me с валидным токеном → данные пользователя."""
        response = client.get("/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == registered_user["username"]
        assert data["is_active"] is True

    def test_get_me_no_token(self, client: TestClient) -> None:
        """GET /me без токена → 401."""
        response = client.get("/me")
        assert response.status_code == 401

    def test_get_me_invalid_token(self, client: TestClient) -> None:
        """GET /me с невалидным токеном → 401."""
        response = client.get(
            "/me",
            headers={"Authorization": "Bearer this.is.not.a.valid.jwt"},
        )
        assert response.status_code == 401

    def test_get_items_requires_auth(self, client: TestClient) -> None:
        """GET /items без токена → 401."""
        response = client.get("/items")
        assert response.status_code == 401

    def test_get_items_with_auth(self, client: TestClient, auth_headers: dict) -> None:
        """GET /items с токеном → список элементов (может быть пустым)."""
        response = client.get("/items", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# ============================================================
# Тест полного flow: регистрация → логин → защищённый ресурс
# ============================================================


class TestFullAuthFlow:
    """Интеграционный тест полного пути аутентификации."""

    def test_register_login_access_protected(self, client: TestClient) -> None:
        """Полный flow: регистрация → логин → доступ к /me."""
        # Шаг 1: Регистрация
        register_response = client.post(
            "/auth/register",
            json={"username": "newuser", "password": "newpass123"},
        )
        assert register_response.status_code == 201

        # Шаг 2: Логин
        login_response = client.post(
            "/auth/login",
            data={"username": "newuser", "password": "newpass123"},
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Шаг 3: Доступ к защищённому эндпоинту
        me_response = client.get(
            "/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert me_response.status_code == 200
        assert me_response.json()["username"] == "newuser"


# ============================================================
# Тесты с истёкшим токеном
# ============================================================


class TestExpiredToken:
    """Тесты поведения при истёкшем токене."""

    def test_expired_token_rejected(
        self, client: TestClient, registered_user: dict
    ) -> None:
        """Истёкший JWT токен должен отклоняться с 401."""
        # Создаём токен с отрицательным временем жизни (уже истёк)
        expired_token = create_access_token(
            data={"sub": registered_user["username"]},
            expires_delta=timedelta(seconds=-1),
        )

        response = client.get(
            "/me",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert response.status_code == 401

    def test_malformed_bearer_header(self, client: TestClient) -> None:
        """Неправильный формат заголовка Authorization → 401/403."""
        # Без слова "Bearer"
        response = client.get(
            "/me",
            headers={"Authorization": "some_token_without_bearer"},
        )
        # FastAPI вернёт 403 (нет корректной схемы Bearer)
        assert response.status_code in (401, 403)
