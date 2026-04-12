# Практические задания: Безопасность и тестирование FastAPI

## Подготовка

```bash
# 1. Активируйте виртуальное окружение
source .venv/bin/activate  # Linux/Mac

# 2. Убедитесь, что зависимости установлены
uv add "python-jose[cryptography]" "passlib[bcrypt]" python-multipart
python -c "from jose import jwt; from passlib.context import CryptContext; print('OK')"

# 3. Запустите standalone-примеры (полезно перед заданиями)
python seminars/seminar_11_fastapi_security_testing/examples/01_password_hashing.py
python seminars/seminar_11_fastapi_security_testing/examples/02_jwt_tokens.py

# 4. Запустите тесты из примеров (должны все пройти — это эталон)
pytest seminars/seminar_11_fastapi_security_testing/examples/04_testing/ -v
```

> **Как работать с заданиями:** прочитайте условие, попробуйте ответить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: Аутентификация vs Авторизация

> **Теория:** [README.md — Блок 1](../README.md#блок-1-аутентификация-vs-авторизация--oauth2-20-мин) | **Примеры:** [`examples/03_auth_app/dependencies.py`](../examples/03_auth_app/dependencies.py)

### Задание 1.1

Изучите файл `examples/03_auth_app/dependencies.py` и ответьте на вопросы:

1. Что произойдёт, если клиент отправит запрос на `GET /me` **без** заголовка `Authorization`?
2. Что произойдёт, если клиент отправит заголовок `Authorization: Basic alice:secret` (Basic Auth вместо Bearer)?
3. Какую роль играет параметр `tokenUrl="/auth/login"` в `OAuth2PasswordBearer`? Влияет ли он на реальную проверку токена?

<details>
<summary>Подсказка</summary>

- `OAuth2PasswordBearer` — это `Depends`, который извлекает токен из заголовка. Если заголовка нет — он сам поднимает исключение.
- `tokenUrl` — только метаданные для Swagger UI (кнопка «Authorize»). На логику проверки токена не влияет.
- Откройте `http://127.0.0.1:8000/docs` и попробуйте вызвать `/me` без авторизации.

</details>

<details>
<summary>Решение</summary>

1. **Без заголовка `Authorization`:** FastAPI вернёт `403 Forbidden` с телом `{"detail": "Not authenticated"}`. Это делает сам `OAuth2PasswordBearer` — он обязателен по умолчанию (`auto_error=True`).

2. **`Authorization: Basic ...`:** FastAPI ожидает схему `Bearer`. Заголовок с `Basic` не соответствует формату, поэтому `OAuth2PasswordBearer` вернёт `403 Forbidden` — токен не будет извлечён.

3. **`tokenUrl`** используется **только** Swagger UI: когда пользователь нажимает кнопку «Authorize», Swagger делает `POST /auth/login` с username и password. На фактическую проверку JWT в `get_current_user` этот параметр не влияет никак.

</details>

---

### Задание 1.2

Запустите полное auth API и выполните следующий сценарий через Swagger UI (`http://127.0.0.1:8000/docs`):

```bash
uvicorn seminars.seminar_11_fastapi_security_testing.examples.03_auth_app.main:app --reload
```

1. Зарегистрируйте двух пользователей: `alice` (пароль: `alice_pass`) и `bob` (пароль: `bob_pass`)
2. Нажмите «Authorize», войдите как `alice`
3. Вызовите `GET /items` — что вернул сервер?
4. Выйдите из «Authorize», войдите как `bob`
5. Вызовите `GET /items` — изменился ли набор элементов?

Объясните, почему результаты разные. Это аутентификация или авторизация?

<details>
<summary>Подсказка</summary>

Посмотрите на код `GET /items` в `routers/protected.py`. Обратите внимание на строку с фильтрацией `user_items = [item for item in fake_items_db if item["owner"] == ...]`.

</details>

<details>
<summary>Решение</summary>

**Alice** увидит элементы с `owner == "alice"` (документы #1 и #2).  
**Bob** увидит элемент с `owner == "bob"` (личные заметки).

Это **авторизация** — оба пользователя аутентифицированы (система знает, кто они), но каждый видит только свои ресурсы. Фильтрация выполняется в коде:

```python
user_items = [
    item for item in fake_items_db if item["owner"] == current_user.username
]
```

`current_user` приходит из `Depends(get_current_user)` — он декодирует токен и возвращает объект с `username`. Именно это поле используется для авторизации (фильтрации).

**Итог:**
- Аутентификация: токен → система знает, что запрос от alice
- Авторизация: alice видит только элементы с `owner == "alice"`

</details>

---

## Часть 2: Хеширование паролей

> **Теория:** [README.md — Блок 2](../README.md#блок-2-хеширование-паролей-15-мин) | **Примеры:** [`examples/01_password_hashing.py`](../examples/01_password_hashing.py)

### Задание 2.1

Запустите скрипт и ответьте на вопросы:

```bash
python seminars/seminar_11_fastapi_security_testing/examples/01_password_hashing.py
```

1. Почему два хеша одного и того же пароля разные? Как тогда `verify_password` понимает, что пароль правильный?
2. Что такое timing attack? Как passlib защищает от него?
3. Что произойдёт, если пароль пользователя изменится? Надо ли пересчитывать хеш?

<details>
<summary>Подсказка</summary>

- bcrypt встраивает **случайную соль** прямо в хеш (в строку `$2b$12$...`). При `verify()` passlib сначала извлекает соль из хеша, хеширует введённый пароль с той же солью и сравнивает результат.
- Timing attack: злоумышленник измеряет время ответа — если «неправильный пароль» отвечает быстрее, можно угадать правильный. `verify()` всегда работает одинаковое время.

</details>

<details>
<summary>Решение</summary>

1. **Разные хеши, один пароль:** bcrypt использует **случайную соль** — случайные байты, которые добавляются к паролю перед хешированием. Соль встроена в сам хеш (символы после `$2b$12$`). При `verify_password(plain, hash)` passlib:
   - Извлекает соль из `hash`
   - Хеширует `plain + salt`
   - Сравнивает с ожидаемым хешем
   
   Именно поэтому `verify()` корректен, даже когда два хеша одного пароля разные.

2. **Timing attack:** без защиты сервер может возвращать «неправильный пароль» быстрее (например, если пользователь не найден — сразу `return False`). Злоумышленник замеряет время сотен запросов и угадывает правильный логин. passlib использует `hmac.compare_digest()` — константное время сравнения, независимо от результата.

3. **При смене пароля:** да, нужно пересчитать хеш: `new_hash = hash_password(new_password)` и сохранить его в БД. Старый хеш становится невалидным автоматически, потому что `verify_password(new_password, old_hash)` вернёт `False`.

</details>

---

### Задание 2.2

Реализуйте функцию безопасной смены пароля:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def change_password(
    username: str,
    old_password: str,
    new_password: str,
    fake_db: dict[str, str],  # {username: hashed_password}
) -> bool:
    """Сменить пароль пользователя.

    Требования:
    1. Проверить, что old_password верный
    2. Убедиться, что new_password != old_password
    3. Захешировать new_password и обновить fake_db
    4. Вернуть True при успехе, False при ошибке
    """
    ...
```

Проверьте: что происходит при передаче неверного старого пароля?

<details>
<summary>Подсказка</summary>

Используйте `pwd_context.verify(plain, hash)` для проверки старого пароля.  
Для проверки `new != old` — нельзя сравнивать хеши напрямую (они разные каждый раз!). Используйте `pwd_context.verify(new_password, old_hash)`.

</details>

<details>
<summary>Решение</summary>

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def change_password(
    username: str,
    old_password: str,
    new_password: str,
    fake_db: dict[str, str],
) -> bool:
    """Сменить пароль пользователя.

    Returns:
        True если пароль успешно изменён, False иначе
    """
    # Проверяем, что пользователь существует
    current_hash = fake_db.get(username)
    if current_hash is None:
        return False

    # Проверяем старый пароль
    if not pwd_context.verify(old_password, current_hash):
        return False  # неверный старый пароль

    # Убеждаемся, что новый пароль отличается от старого
    if pwd_context.verify(new_password, current_hash):
        return False  # новый пароль совпадает со старым

    # Обновляем хеш в "БД"
    fake_db[username] = pwd_context.hash(new_password)
    return True


# Проверка:
db: dict[str, str] = {}
db["alice"] = pwd_context.hash("old_pass")

result = change_password("alice", "old_pass", "new_pass_123", db)
print(result)  # True — пароль изменён

result = change_password("alice", "old_pass", "another", db)
print(result)  # False — старый пароль уже неверный

result = change_password("alice", "new_pass_123", "new_pass_123", db)
print(result)  # False — новый == старый
```

</details>

---

## Часть 3: JWT токены + защита роутов

> **Теория:** [README.md — Блок 3](../README.md#блок-3-jwt-токены--защита-роутов-25-мин) | **Примеры:** [`examples/02_jwt_tokens.py`](../examples/02_jwt_tokens.py), [`examples/03_auth_app/auth.py`](../examples/03_auth_app/auth.py)

### Задание 3.1

Запустите скрипт и ответьте на вопросы:

```bash
python seminars/seminar_11_fastapi_security_testing/examples/02_jwt_tokens.py
```

1. Декодируйте payload токена вручную (без SECRET_KEY), используя только `base64`:
   ```bash
   python -c "
   import base64, json
   token = 'вставьте_ваш_токен'
   payload_b64 = token.split('.')[1]
   padded = payload_b64 + '=' * (4 - len(payload_b64) % 4)
   print(json.loads(base64.urlsafe_b64decode(padded)))
   "
   ```
   Что вы видите? Что это означает для данных в токене?

2. Что произойдёт, если изменить `exp` на будущее прямо в payload и отправить токен на сервер? Почему?

<details>
<summary>Подсказка</summary>

- Payload JWT — это просто base64url. Любой может его прочитать без ключа.
- Но изменить payload и пересчитать подпись без `SECRET_KEY` — невозможно. Сервер отклонит такой токен с `JWTError: Signature verification failed`.

</details>

<details>
<summary>Решение</summary>

1. **Декодирование payload без ключа:** вы увидите что-то вроде `{"sub": "alice", "exp": 1775756994}`. Это означает, что payload **не зашифрован** — любой может прочитать данные в токене без секрета. Именно поэтому JWT не подходит для хранения секретных данных (паролей, номеров карт и т.д.).

2. **Изменение `exp` в payload:** если изменить `exp` на будущее время и отправить токен с изменённым payload (но оригинальной подписью), сервер вернёт `JWTError: Signature verification failed`. Это происходит потому что подпись покрывает весь токен (`header.payload`) — изменение payload делает подпись невалидной. Без `SECRET_KEY` вы не можете пересчитать корректную подпись.

</details>

---

### Задание 3.2

Добавьте к приложению `03_auth_app` эндпоинт `POST /auth/refresh`, который принимает действующий токен и возвращает новый токен с обновлённым временем жизни. Это полезно для «продления сессии» без повторного ввода пароля.

```python
@router.post("/auth/refresh", response_model=Token)
def refresh_token(current_user: CurrentUser) -> Token:
    """Обновить access token (продлить сессию)."""
    ...
```

<details>
<summary>Подсказка</summary>

`CurrentUser` — это уже проверенный пользователь из токена. Для создания нового токена используйте `create_access_token(data={"sub": current_user.username})`.

</details>

<details>
<summary>Решение</summary>

```python
# Добавить в routers/users.py:
from ..auth import create_access_token
from ..dependencies import CurrentUser
from ..models import Token

@router.post("/auth/refresh", response_model=Token)
def refresh_token(current_user: CurrentUser) -> Token:
    """Выдать новый access token для аутентифицированного пользователя.

    Клиент отправляет действующий токен → получает новый с обновлённым exp.
    Полезно для «keep-me-logged-in» функциональности.
    """
    # Создаём новый токен с тем же username
    new_token = create_access_token(data={"sub": current_user.username})
    return Token(access_token=new_token, token_type="bearer")
```

**Почему это безопасно:** эндпоинт защищён через `CurrentUser` — только пользователь с валидным (не истёкшим) токеном может получить новый токен. Истёкший токен не даёт доступа к `/auth/refresh`.

**Тест:**
```python
def test_refresh_token(client, auth_headers):
    old_token = auth_headers["Authorization"].split(" ")[1]
    response = client.post("/auth/refresh", headers=auth_headers)
    assert response.status_code == 200
    new_token = response.json()["access_token"]
    # Новый токен должен отличаться (разное время создания → разный exp)
    assert new_token != old_token
```

</details>

---

## Часть 4: Тестирование с TestClient + pytest

> **Теория:** [README.md — Блок 4](../README.md#блок-4-тестирование-с-testclient--pytest-20-мин) | **Примеры:** [`examples/04_testing/conftest.py`](../examples/04_testing/conftest.py), [`examples/04_testing/test_auth.py`](../examples/04_testing/test_auth.py)

### Задание 4.1

Изучите `examples/04_testing/conftest.py` и ответьте на вопросы:

1. Зачем нужен `fake_users_db.clear()` в fixture `clean_users_db`? Что произойдёт без него?
2. Почему `clean_users_db` помечен `autouse=True`? Что это означает?
3. Почему для `POST /auth/login` используется `data={...}`, а не `json={...}` как для регистрации?

<details>
<summary>Подсказка</summary>

- Без очистки состояние «базы данных» переходит от одного теста к другому — это нарушает **изоляцию тестов**.
- `OAuth2PasswordRequestForm` ожидает `Content-Type: application/x-www-form-urlencoded`, а не JSON. FastAPI/httpx: `data={}` → form, `json={}` → JSON.

</details>

<details>
<summary>Решение</summary>

1. **`fake_users_db.clear()`:** без очистки тест A может зарегистрировать пользователя «alice», а тест B — упасть с ошибкой «Username already registered», хотя тест B не ожидал существования пользователя. Тесты должны быть **изолированными**: каждый начинает с чистого состояния.

2. **`autouse=True`:** fixture применяется ко **всем** тестам в модуле (и подпакетах) автоматически, без явного указания в параметрах теста. Без `autouse=True` нужно было бы добавлять `clean_users_db` в параметры каждого теста — легко забыть.

3. **`data={}` vs `json={}`:** `OAuth2PasswordRequestForm` — это FastAPI-зависимость, которая читает тело запроса как `application/x-www-form-urlencoded` (HTML-форма). При `client.post("/login", data={"username": "alice", "password": "secret"})` httpx устанавливает правильный `Content-Type`. При `json={}` тело — JSON, FastAPI не сможет распарсить форму и вернёт `422 Unprocessable Entity`.

</details>

---

### Задание 4.2

Напишите собственный тест, который проверяет, что **два разных пользователя** видят только свои элементы (`GET /items`). Структура теста:

```python
def test_items_isolation(client: TestClient) -> None:
    """Alice видит свои элементы, Bob видит свои — и не чужие."""
    # 1. Зарегистрировать alice и bob
    # 2. Получить токены для обоих
    # 3. Вызвать GET /items с токеном alice
    # 4. Вызвать GET /items с токеном bob
    # 5. Убедиться, что наборы элементов разные
    ...
```

<details>
<summary>Подсказка</summary>

Регистрация через `client.post("/auth/register", json={...})`, логин через `client.post("/auth/login", data={...})`.  
Вспомните структуру `fake_items_db` в `routers/protected.py` — там уже есть данные для alice и bob.

</details>

<details>
<summary>Решение</summary>

```python
from fastapi.testclient import TestClient


def test_items_isolation(client: TestClient) -> None:
    """Пользователи видят только свои элементы (авторизация)."""

    def get_token(username: str, password: str) -> str:
        """Зарегистрировать и получить токен."""
        client.post("/auth/register", json={"username": username, "password": password})
        response = client.post(
            "/auth/login", data={"username": username, "password": password}
        )
        assert response.status_code == 200
        return str(response.json()["access_token"])

    alice_token = get_token("alice", "alice_pass123")
    bob_token = get_token("bob", "bob_pass123")

    # GET /items для alice
    alice_response = client.get(
        "/items", headers={"Authorization": f"Bearer {alice_token}"}
    )
    assert alice_response.status_code == 200
    alice_items = alice_response.json()

    # GET /items для bob
    bob_response = client.get(
        "/items", headers={"Authorization": f"Bearer {bob_token}"}
    )
    assert bob_response.status_code == 200
    bob_items = bob_response.json()

    # Элементы должны быть разными
    alice_titles = {item["title"] for item in alice_items}
    bob_titles = {item["title"] for item in bob_items}

    # У alice и bob нет общих элементов
    assert alice_titles.isdisjoint(bob_titles), (
        "У alice и bob не должно быть общих элементов!"
    )

    # Все элементы принадлежат правильным владельцам
    assert all(item["owner"] == "alice" for item in alice_items)
    assert all(item["owner"] == "bob" for item in bob_items)
```

</details>

---

## Бонусное задание

### Бонус: Ограничение количества попыток входа (Rate Limiting)

Расширьте приложение `03_auth_app` защитой от брутфорса: если пользователь ввёл неверный пароль **3 раза подряд**, его аккаунт должен быть заблокирован на 60 секунд.

Требования:
1. Добавьте счётчик неудачных попыток в `fake_users_db` (или отдельный словарь)
2. При успешном входе — сбросьте счётчик
3. При 3-й неудачной попытке — верните `429 Too Many Requests` с временем разблокировки
4. Напишите тест, который проверяет блокировку

<details>
<summary>Подсказка</summary>

Используйте отдельный словарь `failed_attempts: dict[str, int]` и `lockout_until: dict[str, datetime]`.  
В эндпоинте `/login` — проверяйте `lockout_until.get(username)` перед проверкой пароля.  
HTTP статус `429` — `status.HTTP_429_TOO_MANY_REQUESTS`.

</details>

<details>
<summary>Решение</summary>

```python
# routers/users.py — расширенная версия с rate limiting

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import create_access_token, hash_password, verify_password
from ..dependencies import fake_users_db
from ..models import Token, UserCreate, UserInDB, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# In-memory хранилище для rate limiting (в production — Redis)
failed_attempts: dict[str, int] = {}
lockout_until: dict[str, datetime] = {}

MAX_ATTEMPTS = 3
LOCKOUT_SECONDS = 60


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user_data: UserCreate) -> UserResponse:
    """Зарегистрировать нового пользователя."""
    if user_data.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed = hash_password(user_data.password)
    new_user = UserInDB(username=user_data.username, hashed_password=hashed)
    fake_users_db[user_data.username] = new_user
    return UserResponse(username=new_user.username, is_active=new_user.is_active)


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Логин с защитой от брутфорса."""
    username = form_data.username

    # Проверяем блокировку
    locked_until = lockout_until.get(username)
    if locked_until and datetime.now(timezone.utc) < locked_until:
        remaining = int((locked_until - datetime.now(timezone.utc)).total_seconds())
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Account locked. Try again in {remaining} seconds.",
        )

    user = fake_users_db.get(username)
    if user is None or not verify_password(form_data.password, user.hashed_password):
        # Неудачная попытка
        attempts = failed_attempts.get(username, 0) + 1
        failed_attempts[username] = attempts

        if attempts >= MAX_ATTEMPTS:
            lockout_until[username] = datetime.now(timezone.utc) + timedelta(
                seconds=LOCKOUT_SECONDS
            )
            failed_attempts[username] = 0
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Account locked for {LOCKOUT_SECONDS} seconds after too many failed attempts.",
            )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect username or password. Attempts: {attempts}/{MAX_ATTEMPTS}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Успех — сбрасываем счётчик
    failed_attempts.pop(username, None)
    lockout_until.pop(username, None)

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


# Тест:
# def test_rate_limiting(client: TestClient) -> None:
#     client.post("/auth/register", json={"username": "alice", "password": "secret123"})
#
#     # 3 неудачные попытки
#     for _ in range(MAX_ATTEMPTS):
#         r = client.post("/auth/login", data={"username": "alice", "password": "wrong"})
#
#     # После блокировки — 429
#     r = client.post("/auth/login", data={"username": "alice", "password": "secret123"})
#     assert r.status_code == 429
#     assert "locked" in r.json()["detail"]
```

</details>

---

## Полезные ресурсы

- [FastAPI — Security](https://fastapi.tiangolo.com/tutorial/security/) — официальный туториал по OAuth2, JWT, scopes
- [FastAPI — Testing](https://fastapi.tiangolo.com/tutorial/testing/) — TestClient, fixtures, mocking
- [python-jose — документация](https://python-jose.readthedocs.io/en/latest/) — JWT encode/decode, алгоритмы
- [passlib — bcrypt](https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html) — параметры bcrypt, work factor
- [OWASP — Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) — лучшие практики аутентификации
