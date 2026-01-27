# Программирование на Python - 2 семестр (МФТИ, 2026)

Добро пожаловать в репозиторий курса "Программирование на Python" для студентов МФТИ!

## О курсе

Этот курс охватывает продвинутые темы программирования на Python и включает практические занятия по современным технологиям разработки. Курс состоит из 17 семинаров, разделённых на три модуля.

## Структура курса

### Модуль 2: ООП и базы данных в Python

| # | Семинар | Описание |
|---|---------|----------|
| 1 | [Введение в SQL](./seminars/seminar_01_intro_to_sql/) | CREATE, INSERT, UPDATE, DELETE, простые SELECT |
| 2 | [Сложные SQL-запросы](./seminars/seminar_02_advanced_sql/) | JOIN, агрегация, GROUP BY, подзапросы, нормализация |
| 3 | [Паттерны проектирования ООП](./seminars/seminar_03_oop_patterns/) | Singleton, Factory, SOLID |

### Модуль 3: Веб-сервисы на Python

| # | Семинар | Описание |
|---|---------|----------|
| 4 | [Основы веб-технологий](./seminars/seminar_04_web_fundamentals/) | HTTP, REST, JSON |
| 5 | [Веб-фреймворки Python](./seminars/seminar_05_python_web_frameworks/) | Django, Flask, FastAPI |
| 6 | [Django и базы данных](./seminars/seminar_06_django_db_integration/) | Django ORM, миграции |
| 7 | [Основы фронтенда](./seminars/seminar_07_frontend_basics/) | HTML, CSS, JavaScript |
| 8 | [Продвинутый Django](./seminars/seminar_08_advanced_django/) | DRF, CBV, аутентификация |
| 9 | [FastAPI и REST](./seminars/seminar_09_fastapi_rest/) | Async, Pydantic, OpenAPI |
| 10 | [Работа с данными в FastAPI](./seminars/seminar_10_fastapi_data_handling/) | SQLAlchemy, Alembic |
| 11 | [Безопасность и тестирование](./seminars/seminar_11_fastapi_security_testing/) | JWT, pytest |
| 12 | [Контейнеризация FastAPI](./seminars/seminar_12_fastapi_containerization/) | Docker, Docker Compose |

### Модуль 4: Анализ данных на Python

| # | Семинар | Описание |
|---|---------|----------|
| 13 | [Основы анализа данных](./seminars/seminar_13_data_analysis_basics/) | NumPy, Pandas, Jupyter |
| 14 | [Сбор данных из внешних источников](./seminars/seminar_14_external_data_collection/) | requests, aiohttp |
| 15 | [Beautiful Soup и API](./seminars/seminar_15_beautifulsoup_apis/) | Парсинг HTML, работа с API |
| 16 | [Статистика](./seminars/seminar_16_statistics/) | Описательная и инференциальная статистика |
| 17 | [Визуализация данных](./seminars/seminar_17_data_visualization/) | Matplotlib, Seaborn, Plotly |

## Требования

- Python 3.10 или выше
- Git
- [uv](https://github.com/astral-sh/uv) — современный менеджер пакетов Python

## Установка

```bash
# Клонировать репозиторий
git clone https://github.com/romelllo/mipt-python-2026.git
cd mipt-python-2026

# Установить uv (если ещё не установлен)
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Создать виртуальное окружение и установить зависимости
uv sync

# Активировать виртуальное окружение
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows
```

### Альтернативная установка (pip)

```bash
# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate

# Установить зависимости
pip install -e ".[dev]"
```

## Инструменты разработки

Проект использует современные инструменты Python:

| Инструмент | Назначение | Команда |
|------------|------------|---------|
| [uv](https://github.com/astral-sh/uv) | Менеджер пакетов | `uv sync`, `uv add <pkg>` |
| [ruff](https://github.com/astral-sh/ruff) | Линтер и форматтер | `ruff check .`, `ruff format .` |
| [pytest](https://pytest.org/) | Тестирование | `pytest` |
| [mypy](https://mypy-lang.org/) | Проверка типов | `mypy .` |

### Быстрый старт с инструментами

```bash
# Форматирование кода
ruff format .

# Проверка на ошибки
ruff check .

# Автоисправление ошибок
ruff check --fix .

# Запуск тестов
pytest

# Проверка типов
mypy seminars/
```

## Структура репозитория

```
mipt-python-2026/
├── seminars/
│   ├── seminar_01_intro_to_sql/
│   │   ├── README.md
│   │   ├── examples/
│   │   ├── exercises/
│   │   └── data/
│   ├── seminar_02_advanced_sql/
│   │   ├── README.md
│   │   ├── examples/
│   │   ├── exercises/
│   │   └── data/
│   └── ... (seminar_03 - seminar_17)
├── pyproject.toml          # Конфигурация проекта (uv, ruff, pytest)
├── AGENTS.md               # Инструкции для AI-агентов
├── README.md               # Этот файл
└── RESOURCES.md            # Дополнительные ресурсы
```

## Использование

Каждый семинар содержит:
- `README.md` — описание темы, теория, инструкции
- `examples/` — примеры кода
- `exercises/` — практические задания
- `data/` — данные и скрипты (где применимо)

Для начала работы перейдите в директорию нужного семинара и следуйте инструкциям в README.

## Содействие

Если вы нашли ошибку или хотите предложить улучшение, пожалуйста, создайте issue или pull request.

## Лицензия

Этот проект предназначен для образовательных целей.

## Контакты

Для вопросов и предложений обращайтесь к преподавателям курса.
