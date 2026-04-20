# Практические задания: Контейнеризация FastAPI-приложения

## Подготовка

```bash
# Убедитесь, что Docker установлен и запущен
docker --version
docker compose version

# Перейдите в директорию с примерами
cd seminars/seminar_12_fastapi_containerization/examples

# Скопируйте .env.example в .env
cp .env.example .env

# Соберите образ и запустите стек
docker compose up --build -d

# Проверьте, что всё работает
curl http://localhost:8000/health
# → {"status":"ok"}

# Остановить стек после работы
docker compose down
```

> **Как работать с заданиями:** прочитайте условие, попробуйте ответить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: Dockerfile для FastAPI

> **Теория:** [README.md — Блок 1](../README.md#блок-1-dockerfile-для-fastapi-20-мин) | **Примеры:** [`examples/Dockerfile`](../examples/Dockerfile)

### Задание 1.1

Изучите файл [`examples/Dockerfile`](../examples/Dockerfile). Ответьте на вопросы:

1. Почему `COPY requirements.txt .` стоит **до** `COPY . .`? Что произойдёт, если поменять их местами?
2. Зачем нужна инструкция `USER appuser`? Что случится, если её убрать?
3. Чем `uvicorn` отличается от `gunicorn`? Почему для FastAPI используется `uvicorn`?

<details>
<summary>Подсказка</summary>

Подумайте о том, как Docker кеширует слои. Каждая инструкция `COPY` и `RUN` создаёт новый слой. Если слой не изменился — Docker берёт его из кеша. Что меняется чаще: `requirements.txt` или код приложения?

Для вопроса про `USER`: подумайте, что произойдёт, если процесс внутри контейнера получит возможность выйти за его пределы.

</details>

<details>
<summary>Решение</summary>

1. **Порядок COPY и кеш слоёв:**
   - `requirements.txt` меняется редко (только при добавлении новых пакетов)
   - Код приложения меняется часто (при каждой правке)
   - Если сначала `COPY requirements.txt .` → `RUN pip install` → `COPY . .`:
     - При изменении кода Docker берёт `pip install` из кеша ✓
   - Если поменять местами: при каждом изменении кода Docker будет заново запускать `pip install` — это медленно (30-120 секунд)

2. **`USER appuser`:**
   - По умолчанию процессы в контейнере запускаются от `root`
   - Если атакующий найдёт уязвимость в приложении и выйдет из контейнера — он получит root-доступ к хосту
   - `USER appuser` запускает процесс от непривилегированного пользователя — минимизирует ущерб при взломе

3. **uvicorn vs gunicorn:**
   - `gunicorn` — WSGI-сервер (синхронный), подходит для Django
   - `uvicorn` — ASGI-сервер (асинхронный), нужен для FastAPI
   - FastAPI использует `async def` и `await` — это ASGI. WSGI-сервер не умеет обрабатывать асинхронные запросы

</details>

---

### Задание 1.2

Соберите образ из [`examples/Dockerfile`](../examples/Dockerfile) и запустите контейнер **без docker-compose** (только с SQLite, без PostgreSQL):

```bash
cd seminars/seminar_12_fastapi_containerization/examples

# Соберите образ
docker build -t tasks-api:dev .

# Запустите контейнер
docker run -p 8000:8000 tasks-api:dev
```

Что произойдёт? Почему? Как это исправить?

<details>
<summary>Подсказка</summary>

Посмотрите на `CMD` в Dockerfile — он запускает `uvicorn` напрямую, без `alembic upgrade head`. Что это означает для таблиц в БД?

Также обратите внимание: `DATABASE_URL` не задан → используется SQLite fallback. Но `alembic upgrade head` не запускается в `CMD`...

</details>

<details>
<summary>Решение</summary>

При запуске без docker-compose:
- `DATABASE_URL` не задан → `database.py` использует `sqlite:///./tasks.db`
- `CMD` запускает только `uvicorn`, без `alembic upgrade head`
- Таблицы в БД не созданы → запросы к `/tasks` упадут с ошибкой

**Исправление 1:** передать команду с миграциями через `docker run`:
```bash
docker run -p 8000:8000 tasks-api:dev \
  sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

**Исправление 2:** передать `DATABASE_URL` через `-e`:
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./tasks.db \
  tasks-api:dev \
  sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

**Вывод:** Dockerfile описывает образ, docker-compose описывает запуск. Миграции — часть запуска, не сборки.

</details>

---

## Часть 2: Двухконтейнерный стек

> **Теория:** [README.md — Блок 2](../README.md#блок-2-двухконтейнерный-стек-db--web-20-мин) | **Примеры:** [`examples/docker-compose.yml`](../examples/docker-compose.yml)

### Задание 2.1

Запустите стек и исследуйте его:

```bash
cd seminars/seminar_12_fastapi_containerization/examples
docker compose up --build -d
```

Выполните следующие команды и объясните вывод каждой:

```bash
# 1. Список запущенных контейнеров
docker compose ps

# 2. Логи web-сервиса
docker compose logs web

# 3. Войдите в контейнер web и проверьте переменные окружения
docker compose exec web env | grep -E "DATABASE|POSTGRES|SECRET"

# 4. Проверьте сетевую связность: web видит db по имени?
docker compose exec web python -c "import socket; print(socket.gethostbyname('db'))"

# 5. Создайте задачу через API
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Изучить Docker", "description": "Семинар 12"}'
```

<details>
<summary>Подсказка</summary>

Обратите внимание на вывод `docker compose ps` — у каждого контейнера есть статус `healthy` или `running`. Что означает разница?

В выводе `docker compose logs web` найдите строку с `alembic upgrade head` — это подтверждение, что миграции применились.

</details>

<details>
<summary>Решение</summary>

1. `docker compose ps` — показывает два контейнера: `db` (postgres) и `web` (fastapi). `db` имеет статус `healthy` (прошёл healthcheck), `web` — `running`.

2. `docker compose logs web` — в начале логов видно:
   ```
   INFO  [alembic.runtime.migration] Running upgrade  -> xxxx, create tasks table
   INFO:     Application startup complete.
   ```
   Это подтверждает: сначала миграции, потом uvicorn.

3. `docker compose exec web env | grep ...` — видны переменные из `.env` файла. `DATABASE_URL` содержит `@db:5432` — хост `db`, не `localhost`.

4. `socket.gethostbyname('db')` — возвращает IP-адрес контейнера `db` (например, `172.18.0.2`). Docker DNS разрешает имя сервиса в IP.

5. `curl -X POST ...` — возвращает созданную задачу с `id=1`.

</details>

---

### Задание 2.2

**Проверьте persistence данных:**

```bash
# Создайте несколько задач
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Задача 1"}'

curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Задача 2"}'

# Остановите и удалите контейнеры (БЕЗ флага -v)
docker compose down

# Запустите снова
docker compose up -d

# Проверьте: данные сохранились?
curl http://localhost:8000/tasks
```

Теперь повторите, но с флагом `-v`:

```bash
docker compose down -v
docker compose up -d
curl http://localhost:8000/tasks
```

Объясните разницу.

<details>
<summary>Подсказка</summary>

Флаг `-v` в `docker compose down -v` удаляет не только контейнеры, но и именованные volumes. Где хранятся данные PostgreSQL?

</details>

<details>
<summary>Решение</summary>

**Без `-v`:**
- `docker compose down` удаляет контейнеры, но **не volumes**
- Volume `seminar_12_postgres_data` сохраняется на хосте
- При повторном `docker compose up` PostgreSQL находит данные в volume
- `curl http://localhost:8000/tasks` возвращает ранее созданные задачи ✓

**С `-v`:**
- `docker compose down -v` удаляет контейнеры **и все volumes**
- Volume `seminar_12_postgres_data` удалён
- При повторном `docker compose up` PostgreSQL создаёт пустую БД
- Alembic применяет миграции заново (создаёт таблицы)
- `curl http://localhost:8000/tasks` возвращает пустой список `[]`

**Вывод:** `docker compose down -v` — деструктивная операция. Используйте только когда хотите сбросить БД до чистого состояния.

</details>

---

### Задание 2.3 ⭐

Измените [`examples/docker-compose.yml`](../examples/docker-compose.yml) так, чтобы порт PostgreSQL `5432` был доступен с хоста (для подключения через pgAdmin или DBeaver). Добавьте проброс порта только для сервиса `db`.

После изменения проверьте подключение:
```bash
docker compose up -d
# Подключитесь через psql (если установлен):
psql -h localhost -p 5432 -U taskuser -d tasks_db
```

Почему в production это делать **не рекомендуется**?

<details>
<summary>Подсказка</summary>

Добавьте секцию `ports:` к сервису `db`. Формат: `"хост:контейнер"`.

</details>

<details>
<summary>Решение</summary>

```yaml
services:
  db:
    image: postgres:15-alpine
    env_file: .env
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"   # ← добавить эту строку
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 10s
    networks:
      - app_network
```

**Почему не рекомендуется в production:**
- Открытый порт 5432 доступен всем, кто может достучаться до сервера
- Атакующий может попытаться подобрать пароль (brute force)
- В production БД должна быть доступна только изнутри сети (через имя сервиса)
- Для администрирования используйте `docker compose exec db psql ...` или VPN

</details>

---

## Часть 3: Alembic-миграции

> **Теория:** [README.md — Блок 3](../README.md#блок-3-alembic-миграции-в-docker-compose-20-мин) | **Примеры:** [`examples/app/alembic/env.py`](../examples/app/alembic/env.py)

### Задание 3.1

Изучите файл [`examples/app/alembic/env.py`](../examples/app/alembic/env.py). Ответьте на вопросы:

1. Зачем в `env.py` импортируется `from app.models import Task`? Что будет, если убрать этот импорт?
2. Почему `sqlalchemy.url` в `alembic.ini` оставлен пустым?
3. Что такое `target_metadata = Base.metadata` и зачем оно нужно?

<details>
<summary>Подсказка</summary>

Alembic при автогенерации (`--autogenerate`) сравнивает два состояния:
- Текущее состояние БД (читает из реальной БД)
- Целевое состояние (читает из `target_metadata`)

Откуда Alembic знает о таблице `tasks`?

</details>

<details>
<summary>Решение</summary>

1. **Импорт `Task`:**
   - `Base.metadata` содержит информацию о таблицах только тех моделей, которые **импортированы**
   - Если убрать `from app.models import Task`, Alembic при `--autogenerate` не увидит таблицу `tasks`
   - Он решит, что таблица лишняя, и сгенерирует миграцию с `op.drop_table('tasks')`!
   - Комментарий `# noqa: F401` говорит линтеру: "этот импорт нужен, не удаляй его"

2. **Пустой `sqlalchemy.url` в `alembic.ini`:**
   - `alembic.ini` коммитится в git — нельзя хранить там пароли
   - `env.py` читает `DATABASE_URL` из переменной окружения и передаёт в конфиг: `config.set_main_option("sqlalchemy.url", database_url)`
   - Это позволяет использовать один `alembic.ini` для dev/staging/production

3. **`target_metadata = Base.metadata`:**
   - `Base.metadata` — объект SQLAlchemy, содержащий описание всех таблиц (из всех импортированных моделей)
   - Alembic использует его как "целевое состояние" при `--autogenerate`
   - Сравнивает с реальной БД и генерирует `upgrade()` / `downgrade()`

</details>

---

### Задание 3.2

Добавьте новое поле `priority` (целое число, по умолчанию 0) в модель `Task` в файле [`examples/app/models.py`](../examples/app/models.py) и создайте миграцию.

```bash
# Запустите стек
docker compose up -d

# Отредактируйте models.py (добавьте поле priority)
# Затем создайте миграцию:
docker compose exec web alembic revision --autogenerate -m "add priority to tasks"

# Посмотрите сгенерированный файл
ls app/alembic/versions/

# Примените миграцию
docker compose exec web alembic upgrade head

# Проверьте текущую ревизию
docker compose exec web alembic current
```

<details>
<summary>Подсказка</summary>

В `models.py` добавьте поле после `is_done`:

```python
priority: Mapped[int] = mapped_column(Integer, default=0, nullable=False, server_default="0")
```

`server_default="0"` важен для существующих строк в БД — без него PostgreSQL не сможет добавить NOT NULL колонку к таблице с данными.

</details>

<details>
<summary>Решение</summary>

**Изменение в `models.py`:**

```python
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    priority: Mapped[int] = mapped_column(  # ← новое поле
        Integer,
        default=0,
        nullable=False,
        server_default="0",  # значение для существующих строк
    )
    created_at: Mapped[datetime] = mapped_column(...)
    updated_at: Mapped[datetime] = mapped_column(...)
```

**Сгенерированная миграция будет содержать:**

```python
def upgrade() -> None:
    op.add_column(
        'tasks',
        sa.Column('priority', sa.Integer(), server_default='0', nullable=False)
    )

def downgrade() -> None:
    op.drop_column('tasks', 'priority')
```

**Проверка:**
```bash
docker compose exec web alembic current
# → xxxx (head)  ← текущая ревизия совпадает с head

docker compose exec db psql -U taskuser tasks_db -c "\d tasks"
# → в таблице появилась колонка priority integer not null default 0
```

</details>

---

## Часть 4: Переменные окружения и секреты

> **Теория:** [README.md — Блок 4](../README.md#блок-4-переменные-окружения-и-секреты-15-мин) | **Примеры:** [`examples/.env.example`](../examples/.env.example)

### Задание 4.1

Изучите файл [`examples/.env.example`](../examples/.env.example). Найдите и исправьте потенциальные проблемы безопасности в следующем `docker-compose.yml`:

```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
      - POSTGRES_DB=myapp
    ports:
      - "5432:5432"

  web:
    build: .
    environment:
      - DATABASE_URL=postgresql://admin:admin123@db:5432/myapp
      - SECRET_KEY=mysecretkey
      - DEBUG=1
    ports:
      - "8000:8000"
```

Перечислите все проблемы и предложите исправленную версию.

<details>
<summary>Подсказка</summary>

Найдите минимум 5 проблем. Подсказки:
- Где хранятся секреты?
- Какой порт не должен быть открыт наружу?
- Что означает `DEBUG=1` в production?
- Насколько надёжен пароль `admin123`?
- Есть ли healthcheck для db?

</details>

<details>
<summary>Решение</summary>

**Проблемы:**

1. **Секреты в `docker-compose.yml`** — `POSTGRES_PASSWORD=admin123` и `SECRET_KEY=mysecretkey` попадут в git-историю. Использовать `env_file: .env`.

2. **Слабый пароль** — `admin123` легко подбирается. Использовать сгенерированный пароль: `openssl rand -hex 32`.

3. **Слабый SECRET_KEY** — `mysecretkey` предсказуем. Использовать `python -c "import secrets; print(secrets.token_hex(32))"`.

4. **`DEBUG=1` в production** — включает подробные сообщения об ошибках (стек трейсы) в HTTP-ответах. Атакующий получает информацию о структуре кода.

5. **Открытый порт PostgreSQL** — `"5432:5432"` делает БД доступной снаружи. Убрать проброс порта для `db`.

6. **Нет healthcheck для db** — `web` может стартовать раньше, чем PostgreSQL готов.

7. **Нет `depends_on`** — нет гарантии порядка запуска.

**Исправленная версия:**

```yaml
services:
  db:
    image: postgres:15-alpine
    env_file: .env          # секреты из файла, не inline
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 10
    networks:
      - app_network
    # НЕТ ports: — db не доступен снаружи

  web:
    build: .
    env_file: .env          # секреты из файла
    ports:
      - "8000:8000"         # только web доступен снаружи
    command: >
      sh -c "alembic upgrade head &&
             uvicorn app.main:app --host 0.0.0.0 --port 8000"
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app_network

volumes:
  postgres_data:

networks:
  app_network:
    driver: bridge
```

```bash
# .env (НЕ в git!)
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=a3f8b2c1d4e5f6a7b8c9d0e1f2a3b4c5  # openssl rand -hex 16
POSTGRES_DB=tasks_db
DATABASE_URL=postgresql://taskuser:a3f8b2c1d4e5f6a7b8c9d0e1f2a3b4c5@db:5432/tasks_db
SECRET_KEY=d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7
DEBUG=0
```

</details>

---

### Задание 4.2 ⭐

Добавьте в [`examples/app/database.py`](../examples/app/database.py) валидацию переменной окружения `DATABASE_URL`: если переменная не задана и приложение запущено **не в режиме разработки** (`DEBUG != "1"`), выбросить `RuntimeError` с понятным сообщением.

```python
# Ожидаемое поведение:
# DEBUG=1, DATABASE_URL не задан → использовать SQLite (для разработки)
# DEBUG=0, DATABASE_URL не задан → RuntimeError с инструкцией
# DATABASE_URL задан → использовать его
```

<details>
<summary>Подсказка</summary>

Используйте `os.getenv("DEBUG", "0")` для чтения режима. Добавьте проверку после чтения `DATABASE_URL`.

</details>

<details>
<summary>Решение</summary>

```python
"""Настройка подключения к базе данных через SQLAlchemy."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Читаем режим отладки
DEBUG: bool = os.getenv("DEBUG", "0") == "1"

# Читаем строку подключения
_database_url: str | None = os.getenv("DATABASE_URL")

if _database_url is None:
    if DEBUG:
        # В режиме разработки — SQLite fallback
        _database_url = "sqlite:///./tasks.db"
    else:
        raise RuntimeError(
            "Переменная окружения DATABASE_URL не задана.\n"
            "Для запуска в production задайте DATABASE_URL:\n"
            "  export DATABASE_URL=postgresql://user:pass@host:5432/dbname\n"
            "Для локальной разработки установите DEBUG=1."
        )

DATABASE_URL: str = _database_url

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей."""
    pass


def get_db() -> Session:  # type: ignore[return]
    """Dependency: создать сессию БД и закрыть её после запроса."""
    db = SessionLocal()
    try:
        yield db  # type: ignore[misc]
    finally:
        db.close()
```

**Проверка:**
```bash
# Без DATABASE_URL и без DEBUG=1 → RuntimeError
docker run --rm tasks-api:dev python -c "from app.database import DATABASE_URL"
# RuntimeError: Переменная окружения DATABASE_URL не задана...

# С DEBUG=1 → SQLite fallback
docker run --rm -e DEBUG=1 tasks-api:dev python -c \
  "from app.database import DATABASE_URL; print(DATABASE_URL)"
# sqlite:///./tasks.db
```

</details>

---

## Часть 5: Ситуационные задачи (Chat Polls)

> Этот раздел используется преподавателем для интерактива в чате.

### Ситуация 1

> Вы запускаете `docker compose up` и видите в логах:
> ```
> web_1  | sqlalchemy.exc.OperationalError: could not connect to server: Connection refused
> web_1  |   Is the server running on host "db" (172.18.0.2) and accepting TCP/IP connections on port 5432?
> ```
> Контейнер `db` запущен и работает.

Какова наиболее вероятная причина?

- A) Неверный пароль в `DATABASE_URL`
- B) `web` стартовал раньше, чем PostgreSQL успел инициализироваться
- C) Порт 5432 не пробрасывается в `docker-compose.yml`
- D) Неверное имя хоста — нужно `localhost` вместо `db`

<details>
<summary>Ответ</summary>

**B) `web` стартовал раньше, чем PostgreSQL успел инициализироваться**

PostgreSQL при первом запуске инициализирует кластер данных — это занимает несколько секунд. Если `web` стартует в это время, соединение отклоняется.

**Решение:** добавить healthcheck для `db` и `depends_on: condition: service_healthy` для `web`:

```yaml
db:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
    interval: 5s
    retries: 10

web:
  depends_on:
    db:
      condition: service_healthy
```

**Почему не другие варианты:**
- A) Неверный пароль дал бы `authentication failed`, не `Connection refused`
- C) Порт 5432 не нужно пробрасывать — `web` обращается к `db` внутри сети
- D) `db` — правильное имя хоста в Docker Compose; `localhost` указывал бы на сам контейнер `web`

</details>

---

### Ситуация 2

> Коллега говорит: «Я добавил поле `email` в модель `User`, запустил `docker compose up --build` — но в БД колонки нет!»

Что пошло не так?

- A) Нужно было запустить `docker compose down -v` перед `up --build`
- B) `--build` пересобирает образ, но не применяет новые миграции автоматически
- C) Alembic не поддерживает автогенерацию для новых полей
- D) Нужно добавить поле вручную через `ALTER TABLE`

<details>
<summary>Ответ</summary>

**B) `--build` пересобирает образ, но не применяет новые миграции автоматически**

`docker compose up --build` пересобирает Docker-образ с новым кодом. Но Alembic применяет только **существующие файлы миграций**. Новое поле в модели — это ещё не миграция.

**Правильный workflow:**
```bash
# 1. Изменить модель (models.py)
# 2. Создать файл миграции
docker compose exec web alembic revision --autogenerate -m "add email to users"
# 3. Применить миграцию
docker compose exec web alembic upgrade head
# 4. Пересобрать образ (чтобы файл миграции попал в образ)
docker compose up --build -d
```

**Почему не другие варианты:**
- A) `down -v` удалит все данные — это не решение
- C) Alembic отлично поддерживает `--autogenerate` для новых полей
- D) `ALTER TABLE` вручную — это обход системы миграций, создаёт рассинхронизацию

</details>

---

### Ситуация 3

> Вы деплоите приложение на сервер. В `docker-compose.yml` написано:
> ```yaml
> environment:
>   - SECRET_KEY=abc123
>   - DATABASE_URL=postgresql://admin:password@db:5432/prod_db
> ```
> Тимлид говорит: «Это критическая проблема безопасности». Почему?

- A) `abc123` — слишком короткий SECRET_KEY
- B) Секреты в `docker-compose.yml` попадают в git-историю и видны всем, у кого есть доступ к репозиторию
- C) PostgreSQL не принимает пароли в URL
- D) Нужно использовать HTTPS для DATABASE_URL

<details>
<summary>Ответ</summary>

**B) Секреты в `docker-compose.yml` попадают в git-историю и видны всем, у кого есть доступ к репозиторию**

`docker-compose.yml` обычно коммитится в git. Если в нём хардкодить секреты:
- Все разработчики видят production-пароли
- Секреты остаются в git-истории навсегда (даже после удаления из файла)
- При утечке репозитория — утекают все секреты

**Правильное решение:**
```yaml
# docker-compose.yml (в git)
services:
  web:
    env_file: .env  # читаем из файла

# .env (НЕ в git, в .gitignore)
SECRET_KEY=реальный_секрет
DATABASE_URL=реальный_url
```

**Почему A тоже верно, но не главная проблема:**
- Да, `abc123` слишком короткий — но это вторичная проблема
- Главная проблема — хранение в git, а не длина ключа

</details>

---

### Бонусная ситуация: Комбинированный вопрос

> Вы получили задание: «Задеплоить FastAPI + PostgreSQL в Docker. Требования: данные не должны теряться при перезапуске, web не должен стартовать раньше db, секреты не должны быть в git».

Какой минимальный набор изменений нужен в `docker-compose.yml`?

- A) Добавить `volumes:` для db, `depends_on: condition: service_healthy` для web, использовать `env_file:`
- B) Добавить `restart: always` для обоих сервисов
- C) Добавить `networks:` и пробросить порт 5432
- D) Добавить `healthcheck:` только для web

<details>
<summary>Ответ</summary>

**A) Добавить `volumes:` для db, `depends_on: condition: service_healthy` для web, использовать `env_file:`**

Каждое требование решается конкретным инструментом:
- **Данные не теряются** → `volumes: postgres_data:/var/lib/postgresql/data`
- **Web ждёт db** → `healthcheck:` для db + `depends_on: condition: service_healthy` для web
- **Секреты не в git** → `env_file: .env` + `.env` в `.gitignore`

**Почему не другие варианты:**
- B) `restart: always` — перезапускает при сбоях, но не решает ни одно из трёх требований
- C) `networks:` полезна для изоляции, но не обязательна (compose создаёт сеть по умолчанию); порт 5432 наружу — это антипаттерн
- D) `healthcheck` только для web не решает проблему порядка запуска

</details>

---

## Бонусные задания

### Бонус 1: Multi-stage Dockerfile

Перепишите [`examples/Dockerfile`](../examples/Dockerfile) с использованием **multi-stage build**. Цель: уменьшить размер финального образа, исключив из него `gcc` и `libpq-dev` (нужны только для сборки, не для запуска).

```dockerfile
# Stage 1: builder — устанавливаем зависимости
FROM python:3.11-slim AS builder
# ... установка gcc, libpq-dev, pip install ...

# Stage 2: runtime — только то, что нужно для запуска
FROM python:3.11-slim AS runtime
# ... копируем только установленные пакеты из builder ...
```

Сравните размеры образов:
```bash
docker build -t tasks-api:single .           # однослойный
docker build -t tasks-api:multistage .       # многоступенчатый
docker images | grep tasks-api
```

<details>
<summary>Подсказка</summary>

В multi-stage build используйте `COPY --from=builder` для копирования установленных Python-пакетов из `/usr/local/lib/python3.11/site-packages` и бинарников из `/usr/local/bin`.

</details>

<details>
<summary>Решение</summary>

```dockerfile
# ============================================================
# Stage 1: builder — сборка зависимостей
# ============================================================
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Системные зависимости нужны только для сборки psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

# ============================================================
# Stage 2: runtime — минимальный образ для запуска
# ============================================================
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Только runtime-зависимость: libpq (не libpq-dev!)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем установленные пакеты из builder
COPY --from=builder /install /usr/local

# Копируем код приложения
COPY . .

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser \
    && chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c \
    "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" \
    || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

Multi-stage build уменьшает размер образа на ~100-200 МБ, исключая компилятор и заголовочные файлы.

</details>

---

### Бонус 2: Отдельный сервис для миграций

Вместо запуска `alembic upgrade head` в `command:` сервиса `web`, создайте **отдельный сервис `migrate`**, который применяет миграции и завершается. Сервис `web` должен ждать завершения `migrate`.

```yaml
services:
  db: ...

  migrate:
    build: .
    command: alembic upgrade head
    depends_on:
      db:
        condition: service_healthy
    # migrate должен завершиться успешно перед стартом web

  web:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    depends_on:
      migrate:
        condition: service_completed_successfully  # ← ключевое
```

Реализуйте это и проверьте: `docker compose up --build`. Убедитесь, что `migrate` завершается с кодом 0, а `web` стартует после него.

<details>
<summary>Подсказка</summary>

`condition: service_completed_successfully` — специальное условие, которое ждёт, пока сервис завершится с кодом выхода 0 (успешно). Это отличается от `service_healthy` (ждёт healthcheck).

</details>

<details>
<summary>Решение</summary>

```yaml
services:
  db:
    image: postgres:15-alpine
    env_file: .env
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 10s
    networks:
      - app_network

  migrate:
    build: .
    command: alembic upgrade head
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app_network
    # Нет restart: — сервис должен завершиться, а не перезапускаться

  web:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      migrate:
        condition: service_completed_successfully  # ждём успешного завершения migrate
    networks:
      - app_network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  app_network:
    driver: bridge
```

**Преимущества отдельного сервиса `migrate`:**
- Чёткое разделение ответственности
- Если миграция упала — `web` не стартует (явная ошибка)
- Можно запустить только миграции: `docker compose run migrate`
- Логи миграций отделены от логов приложения

</details>

---

## Полезные ресурсы

- [FastAPI — Deployment with Docker](https://fastapi.tiangolo.com/deployment/docker/) — официальное руководство FastAPI
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) — создание и применение миграций
- [Docker Compose — Startup Order](https://docs.docker.com/compose/how-tos/startup-order/) — `depends_on` и healthcheck
- [12 Factor App](https://12factor.net/) — методология для cloud-native приложений
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/) — официальные рекомендации по безопасности
