# Программирование на Python - 2 семестр (МФТИ, 2026)

Добро пожаловать в репозиторий курса "Программирование на Python" для студентов МФТИ!

## О курсе

Этот курс охватывает продвинутые темы программирования на Python и включает практические занятия по современным технологиям разработки. Курс состоит из 17 семинаров, разделённых на три модуля.

## Структура курса

### Модуль 2: Объектно-ориентированное программирование и основы работы с базами данных в Python

| # | Семинар | Описание |
|---|---------|----------|
| 1 | [ Введение в базы данных. Знакомство с SQL](./seminars/seminar_01_intro_to_sql/) | CREATE, INSERT, UPDATE, DELETE, простые SELECT |
| 2 | [Проектирование базы данных](./seminars/seminar_02_db_design/) | JOIN, агрегация, GROUP BY, подзапросы, нормализация |
| 3 | [Паттерны ООП на Python для разработки приложения](./seminars/seminar_03_oop_patterns/) | Singleton, Factory, SOLID |

### Модуль 3: Создание Web-сервисов на Python

| # | Семинар | Описание |
|---|---------|----------|
| 4 | [Общее представление о WEB](./seminars/seminar_04_web_fundamentals/) | HTTP, REST, JSON |
| 5 | [Python и WEB-фреймворки](./seminars/seminar_05_python_web_frameworks/) | Django, Flask, FastAPI |
| 6 | [Взаимодействие с базами данных с помощью Django](./seminars/seminar_06_django_db_integration/) | Django ORM, миграции |
| 7 | [Основы Frontend-разработки](./seminars/seminar_07_frontend_basics/) | HTML, CSS, JavaScript |
| 8 | [Продвинутые возможности Django](./seminars/seminar_08_advanced_django/) | DRF, CBV, аутентификация |
| 9 | [Введение в FastAPI и REST-сервисы](./seminars/seminar_09_fastapi_rest/) | Async, Pydantic, OpenAPI |
| 10 | [Работа с данными в FastAPI](./seminars/seminar_10_fastapi_data_handling/) | SQLAlchemy, Alembic |
| 11 | [Безопасность и тестирование приложений на FastAPI](./seminars/seminar_11_fastapi_security_testing/) | JWT, pytest |
| 12 | [Контейнеризация FastAPI-приложения](./seminars/seminar_12_fastapi_containerization/) | Docker, Docker Compose |

### Модуль 4: Анализ данных на Python

| # | Семинар | Описание |
|---|---------|----------|
| 13 | [Введение в анализ данных](./seminars/seminar_13_data_analysis_basics/) | NumPy, Pandas, Jupyter |
| 14 | [Сбор данных со сторонних сайтов](./seminars/seminar_14_external_data_collection/) | requests, aiohttp |
| 15 | [Beautiful Soup и работа с API](./seminars/seminar_15_beautifulsoup_apis/) | Парсинг HTML, работа с API |
| 16 | [Описательные статистики. Статистика вывода](./seminars/seminar_16_statistics/) | Описательная и инференциальная статистика |
| 17 | [Методы визуализации](./seminars/seminar_17_data_visualization/) | Matplotlib, Seaborn, Plotly |

## Требования

- Python 3.10 или выше
- Git
- SQLite3
- [uv](https://docs.astral.sh/uv/) — современный менеджер пакетов Python

## Установка

### Установка SQLite3

**macOS (через Homebrew):**
```bash
# Если Homebrew не установлен:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установить SQLite3
brew install sqlite3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install sqlite3
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install sqlite
```

**Windows:**
1. Скачайте предкомпилированный бинарник с [официального сайта SQLite](https://www.sqlite.org/download.html)
2. Найдите раздел "Precompiled Binaries for Windows" и скачайте `sqlite-tools-win32-x86-3*.zip`
3. Распакуйте архив
4. Добавьте папку с `sqlite3.exe` в переменную окружения PATH:
   - Откройте "Система" → "Переменные окружения"
   - Нажмите "Изменить переменные среды пользователя"
   - Отредактируйте переменную `PATH` и добавьте путь к папке с sqlite3
5. Откройте новый терминал и проверьте: `sqlite3 --version`

### Установка проекта
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

# Установить все зависимости включая dev-зависимости (ruff, pytest, ty и т.д.)
uv sync --all-extras

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
| [uv](https://docs.astral.sh/uv/) | Менеджер пакетов | `uv sync`, `uv add <pkg>` |
| [ruff](https://docs.astral.sh/ruff/) | Линтер и форматтер | `ruff check .`, `ruff format .` |
| [pytest](https://pytest.org/) | Тестирование | `pytest` |
| [ty](https://docs.astral.sh/ty/) | Проверка типов | `ty check` |

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
ty check
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
│   ├── seminar_02_db_design/
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
