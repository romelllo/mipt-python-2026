# Семинар 11: Безопасность и тестирование FastAPI

**Модуль:** 3 — Создание Web-сервисов на Python  
**Дата:** 13.04.2026  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1LcWnp_8_g75loBLA2z0tJqggWDb-BeyVrkiunS72NeE/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:

- **Объяснять** разницу между аутентификацией и авторизацией и показывать, как OAuth2PasswordBearer встраивается в FastAPI
- **Реализовывать** безопасную регистрацию пользователей с хешированием паролей через `passlib[bcrypt]`
- **Выпускать** JWT access токены с `python-jose`, задавать время жизни и SECRET_KEY
- **Защищать** роуты через `Depends(get_current_user)` и разбирать токен при каждом запросе
- **Писать** автоматизированные тесты с `TestClient` и `pytest`, включая полный flow signup → login → защищённый ресурс
- **Тестировать** ошибочные сценарии: неверный пароль, истёкший токен, отсутствующий токен

---

## Подготовка

```bash
# 1. Активируйте виртуальное окружение  
source .venv/bin/activate  # Linux/Mac

# 2. Установите новые зависимости
uv add "python-jose[cryptography]" "passlib[bcrypt]" python-multipart

# 3. Убедитесь, что зависимости установлены
python -c "from jose import jwt; print('jose OK')"
python -c "from passlib.context import CryptContext; print('passlib OK')"

# 4. Запустите standalone-примеры (без сервера)
python seminars/seminar_11_fastapi_security_testing/examples/01_password_hashing.py
python seminars/seminar_11_fastapi_security_testing/examples/02_jwt_tokens.py

# 5. Запустите полное auth API
uvicorn seminars.seminar_11_fastapi_security_testing.examples.03_auth_app.main:app --reload
# → Swagger UI: http://127.0.0.1:8000/docs

# 6. Запустите тесты
pytest seminars/seminar_11_fastapi_security_testing/examples/04_testing/ -v
```

---

## План семинара

Семинар построен по принципу **«теория → практика»**: после каждого блока теории сразу переходите к соответствующим упражнениям в файле [`exercises/exercises.md`](exercises/exercises.md).

| Время | Тема | Практика |
|-------|------|----------|
| 20 мин | Блок 1: Аутентификация vs авторизация + OAuth2 | → Упражнения: Часть 1 |
| 15 мин | Блок 2: Хеширование паролей с passlib + bcrypt | → Упражнения: Часть 2 |
| 25 мин | Блок 3: JWT токены + защита роутов | → Упражнения: Часть 3 |
| 20 мин | Блок 4: Тестирование с TestClient + pytest | → Упражнения: Часть 4 |
| 10 мин | Подведение итогов | — |

**Итого:** ~90 минут

---

## Блок 1: Аутентификация vs Авторизация + OAuth2 (20 мин)

Два понятия, которые часто путают:

| Понятие | Вопрос | Пример |
|---------|--------|--------|
| **Аутентификация** | *Кто ты?* | Ввод логина и пароля → получение токена |
| **Авторизация** | *Что тебе можно?* | Пользователь видит только *свои* записи |

В FastAPI аутентификация реализуется через **схемы безопасности**. Самая распространённая — OAuth2 с bearer-токенами.

### OAuth2PasswordBearer

**Проблема:** как FastAPI узнаёт, где в запросе лежит токен?  
**Решение:** `OAuth2PasswordBearer` — объявляем схему один раз, FastAPI автоматически читает заголовок `Authorization: Bearer <token>`.

```python
from fastapi.security import OAuth2PasswordBearer

# tokenUrl — куда клиент идёт за токеном (используется Swagger UI)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Используем как Depends в эндпоинте:
from typing import Annotated
from fastapi import Depends

@app.get("/me")
async def read_me(token: Annotated[str, Depends(oauth2_scheme)]):
    # token — это строка из заголовка Authorization: Bearer <token>
    return {"token_preview": token[:20] + "..."}
```

### Полная цепочка запроса с токеном

```
Клиент                          FastAPI
  │                               │
  │── POST /auth/login ──────────►│
  │   username + password         │── verify_password() ──►  ✓
  │◄── {"access_token": "..."} ───│
  │                               │
  │── GET /me ────────────────────►│
  │   Authorization: Bearer xyz    │── oauth2_scheme extracts token
  │                                │── decode_access_token(token)
  │◄── {"username": "alice"} ──────│── look up user in DB
```

**Когда использовать OAuth2PasswordBearer:** для API с логином по паролю (username + password) — стандартный выбор.

> **Подробнее:** см. файл [`examples/03_auth_app/dependencies.py`](examples/03_auth_app/dependencies.py) — полная реализация `get_current_user` с `OAuth2PasswordBearer` и зависимостью `CurrentUser`.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 1: Аутентификация vs Авторизация** (задания 1.1–1.2).

---

## Блок 2: Хеширование паролей (15 мин)

**Главное правило:** пароли никогда не хранятся в открытом виде. Только хеш.

### Почему нельзя хранить plaintext пароли

При утечке базы данных злоумышленник получает:
- **Plaintext:** сразу все пароли — катастрофа
- **MD5/SHA1 хеш:** можно сломать за часы (Rainbow Tables)
- **bcrypt хеш:** брутфорс практически невозможен (медленный специально)

### passlib + bcrypt

```python
from passlib.context import CryptContext

# Инициализация — делается один раз при старте приложения
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """Захешировать пароль. Каждый вызов даёт разный хеш (случайная соль)."""
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить пароль против хеша из БД."""
    return pwd_context.verify(plain_password, hashed_password)
```

```python
# Использование:
hashed = hash_password("my_secret")
print(hashed)  # $2b$12$... (60 символов, каждый раз разный!)

verify_password("my_secret", hashed)   # True
verify_password("wrong_pass", hashed)  # False
```

**Ключевые свойства bcrypt:**
- **Одностороннее:** из хеша нельзя получить пароль
- **Соль:** каждый хеш уникален — нельзя сравнивать хеши напрямую
- **Медленное:** ~100 мс/хеш — брутфорс требует лет, не часов
- **`deprecated="auto"`:** passlib автоматически предложит обновить хеши при следующем входе если алгоритм устарел

**Когда использовать:** для всех паролей — от API до внутренних систем. Альтернатива — `argon2` (ещё надёжнее, но passlib+bcrypt — проверенный стандарт).

> **Подробнее:** см. файл [`examples/01_password_hashing.py`](examples/01_password_hashing.py) — демонстрация хеширования, проверки, регистрации/логина и защиты от timing attacks.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 2: Хеширование паролей** (задания 2.1–2.2).

---

## Блок 3: JWT токены + защита роутов (25 мин)

### Что такое JWT

**JWT (JSON Web Token)** — компактный токен с тремя частями, разделёнными точками:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9   ← header (base64url)
.eyJzdWIiOiJhbGljZSIsImV4cCI6MTc3NTc1Njk5NH0   ← payload (base64url)
.oBK9PEuYDyyhYWJ_cHSl4lzr2Y5OEVjJ0h9b-Spf9AM  ← signature (HMAC-SHA256)
```

- **Header:** `{"alg": "HS256", "typ": "JWT"}`
- **Payload:** `{"sub": "alice", "exp": 1775756994}` — данные (claims)
- **Signature:** `HMAC-SHA256(header + "." + payload, SECRET_KEY)` — защита от подделки

> **Важно:** payload не зашифрован — его можно прочитать без ключа. Но подделать подпись без SECRET_KEY — невозможно. Не храните в токене пароли или секретные данные!

### Выдача токена (python-jose)

```python
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "ваш-секретный-ключ-минимум-32-символа"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Создать JWT access token с временем жизни."""
    to_encode = data.copy()
    # exp — стандартный JWT claim для времени истечения
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Использование:
token = create_access_token(data={"sub": "alice"})
# → "eyJhbGci..."
```

### Валидация токена и защита роутов

**Проблема:** как автоматически проверять токен на каждом защищённом эндпоинте?  
**Решение:** `Depends(get_current_user)` — FastAPI вызывает функцию перед каждым запросом.

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    """Проверить токен → вернуть пользователя или 401."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    user = fake_users_db.get(username or "")
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    return user

# Удобный тип-алиас:
CurrentUser = Annotated[UserInDB, Depends(get_current_user)]

# Защищённый эндпоинт:
@app.get("/me")
def read_me(current_user: CurrentUser) -> UserResponse:
    return UserResponse(username=current_user.username, is_active=current_user.is_active)
```

### Генерация SECRET_KEY

```bash
# Генерация безопасного ключа:
python -c "import secrets; print(secrets.token_hex(32))"
# → 09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7

# В production — храните в переменной окружения, никогда в коде!
export SECRET_KEY="ваш_ключ_из_команды_выше"
```

**Когда использовать JWT:** для stateless API — сервер не хранит сессии, токен самодостаточен. Альтернатива для stateful приложений — сессии на стороне сервера (Django sessions).

> **Подробнее:** см. файл [`examples/02_jwt_tokens.py`](examples/02_jwt_tokens.py) — создание, декодирование, истёкшие и подделанные токены. И [`examples/03_auth_app/`](examples/03_auth_app/) — полное рабочее приложение: `auth.py`, `dependencies.py`, `routers/users.py`, `routers/protected.py`.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 3: JWT токены + защита роутов** (задания 3.1–3.2).

---

## Блок 4: Тестирование с TestClient + pytest (20 мин)

Автоматические тесты — единственный способ быть уверенным, что безопасность не сломалась после рефакторинга.

### TestClient: тестирование без запуска сервера

**Проблема:** тестировать API через `curl` — медленно и нельзя автоматизировать.  
**Решение:** `TestClient` от FastAPI — отправляет HTTP-запросы напрямую в ASGI-приложение.

```python
from fastapi.testclient import TestClient
from myapp.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
```

### Fixtures: DRY-тесты без дублирования

```python
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)  # autouse: применяется ко ВСЕМ тестам
def clean_db():
    fake_users_db.clear()  # изоляция тестов — очищаем перед каждым
    yield
    fake_users_db.clear()  # и после

@pytest.fixture
def auth_headers(client):
    """Зарегистрировать пользователя и получить заголовки авторизации."""
    client.post("/auth/register", json={"username": "u", "password": "pass123"})
    response = client.post("/auth/login", data={"username": "u", "password": "pass123"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

### Тестирование ошибочных сценариев

```python
def test_wrong_password(client):
    """Неверный пароль должен возвращать 401."""
    client.post("/auth/register", json={"username": "alice", "password": "secret"})
    response = client.post("/auth/login", data={"username": "alice", "password": "wrong"})
    assert response.status_code == 401

def test_no_token(client):
    """Без токена → 401."""
    response = client.get("/me")
    assert response.status_code == 401

def test_expired_token(client):
    """Истёкший токен → 401."""
    expired = create_access_token({"sub": "alice"}, expires_delta=timedelta(seconds=-1))
    response = client.get("/me", headers={"Authorization": f"Bearer {expired}"})
    assert response.status_code == 401
```

### Полный flow в одном тесте

```python
def test_full_auth_flow(client):
    """Интеграционный тест: регистрация → логин → защищённый ресурс."""
    # 1. Регистрация
    r = client.post("/auth/register", json={"username": "alice", "password": "secret123"})
    assert r.status_code == 201

    # 2. Логин
    r = client.post("/auth/login", data={"username": "alice", "password": "secret123"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    # 3. Защищённый ресурс
    r = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["username"] == "alice"
```

**Когда использовать TestClient:** для интеграционных тестов FastAPI эндпоинтов — быстро, не требует запуска сервера. Для unit-тестов отдельных функций — используйте обычный `pytest` без TestClient.

> **Подробнее:** см. файл [`examples/04_testing/test_auth.py`](examples/04_testing/test_auth.py) — полный набор тестов с классами, fixtures и тестом истёкшего токена. И [`examples/04_testing/conftest.py`](examples/04_testing/conftest.py) — конфигурация fixtures.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 4: Тестирование** (задания 4.1–4.2).

---

## Подведение итогов

### Шпаргалка

| Концепция | Ключевое |
|-----------|---------|
| **Аутентификация** | *Кто ты?* → выдаём токен по логину/паролю |
| **Авторизация** | *Что можно?* → фильтруем данные по пользователю |
| `OAuth2PasswordBearer(tokenUrl=...)` | Схема: читает `Authorization: Bearer <token>` |
| `CryptContext(schemes=["bcrypt"])` | Инициализация passlib один раз при старте |
| `pwd_context.hash(plain)` | Хешировать пароль (bcrypt, случайная соль) |
| `pwd_context.verify(plain, hash)` | Проверить пароль против хеша |
| `jwt.encode(payload, SECRET_KEY, algorithm)` | Создать подписанный JWT |
| `jwt.decode(token, SECRET_KEY, algorithms)` | Верифицировать и декодировать JWT |
| `payload["exp"]` | Время истечения токена (datetime → unix timestamp) |
| `Depends(get_current_user)` | DI: FastAPI проверяет токен перед каждым запросом |
| `JWTError` | Невалидный токен (включая `ExpiredSignatureError`) |
| `TestClient(app)` | HTTP-клиент для тестов без запуска сервера |
| `@pytest.fixture(autouse=True)` | Fixture применяется ко всем тестам автоматически |
| `client.post("/login", data={...})` | form-data (не JSON!) для OAuth2PasswordRequestForm |
| `secrets.token_hex(32)` | Генерация безопасного SECRET_KEY |

### Ключевые выводы

1. **Пароли — только хешами, токены — только подписанными.** Никогда не храните пароли в открытом виде. Никогда не принимайте токены без проверки подписи и времени жизни.

2. **`Depends(get_current_user)` — сердце защиты.** Один dependency отвечает за весь security lifecycle: извлечение токена из заголовка, верификацию, поиск пользователя в БД. Добавляйте его в любой защищённый эндпоинт через `CurrentUser`.

3. **Тесты — страховка безопасности.** Без автотестов любой рефакторинг может случайно «открыть» защищённый роут. Тестируйте не только happy path, но и ошибочные сценарии: неверный пароль, истёкший токен, отсутствующий токен.

---

## Файлы семинара

```
seminar_11_fastapi_security_testing/
├── README.md                              # Этот файл
├── examples/
│   ├── 01_password_hashing.py             # passlib + bcrypt: хеш, verify, регистрация
│   ├── 02_jwt_tokens.py                   # python-jose: создание, декодирование, атаки
│   ├── 03_auth_app/                       # Полное FastAPI приложение с JWT-аутентификацией
│   │   ├── main.py                        # FastAPI app, роутеры
│   │   ├── models.py                      # UserCreate, UserInDB, Token, ...
│   │   ├── auth.py                        # hash_password, verify_password, create/decode JWT
│   │   ├── dependencies.py                # OAuth2PasswordBearer, get_current_user, CurrentUser
│   │   └── routers/
│   │       ├── users.py                   # POST /auth/register, POST /auth/login
│   │       └── protected.py               # GET /me, GET /items (только с токеном)
│   └── 04_testing/                        # Pytest тесты
│       ├── conftest.py                    # Fixtures: client, clean_db, auth_headers
│       └── test_auth.py                   # 16 тестов по 5 классам
└── exercises/
    └── exercises.md                       # Практические задания (4 части + бонус)
```

---

## Дополнительные материалы

- [FastAPI — Security](https://fastapi.tiangolo.com/tutorial/security/) — официальный туториал: OAuth2, JWT, scopes
- [FastAPI — Testing](https://fastapi.tiangolo.com/tutorial/testing/) — TestClient, pytest, fixtures
- [python-jose — документация](https://python-jose.readthedocs.io/en/latest/) — JWT, JWS, JWE с Python
- [passlib — документация](https://passlib.readthedocs.io/en/stable/) — контексты, bcrypt, argon2
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) — лучшие практики аутентификации
