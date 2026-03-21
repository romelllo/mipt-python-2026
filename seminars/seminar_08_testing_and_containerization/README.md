# Семинар 8: Тестирование и контейнеризация

**Модуль:** 3 — Создание Web-сервисов на Python  
**Дата:** 23.03.2026  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1D6hnIwlu8qcd4xtZC0lMaVZ_du1XKVWyCkkZZYBNTXI/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:

- **Называть** виды тестов (unit, component, integration, E2E) и объяснять, когда применять каждый
- **Писать** тесты с pytest: простые тест-функции, `parametrize`, `raises`, фикстуры
- **Использовать** `unittest.mock.patch` и `MagicMock` для изоляции внешних зависимостей
- **Читать** шаблоны Django TestCase и тестировать views через `self.client`
- **Объяснять** концепцию Docker: образ, контейнер, реестр — и читать `Dockerfile`

---

## Подготовка

```bash
# Активируйте виртуальное окружение
source .venv/bin/activate  # Linux/Mac

# Убедитесь, что pytest установлен
pytest --version

# Запустите примеры для ознакомления
python seminars/seminar_08_advanced_django/examples/01_test_types.py
python seminars/seminar_08_advanced_django/examples/02_pytest_basics.py
python seminars/seminar_08_advanced_django/examples/05_mocking.py

# Запустите тесты из примеров через pytest
pytest seminars/seminar_08_advanced_django/examples/02_pytest_basics.py -v
pytest seminars/seminar_08_advanced_django/examples/03_pytest_fixtures.py -v

# Для Docker-части (опционально): установите Docker Desktop
# https://docs.docker.com/get-docker/
docker --version  # проверить установку
```

---

## План семинара

Семинар построен по принципу **«теория → практика»**: после каждого блока теории переходите к соответствующим упражнениям в файле [`exercises/testing_and_docker.md`](exercises/testing_and_docker.md).

| Время | Тема | Практика |
|-------|------|----------|
| 10 мин | Блок 1: Виды тестов и тестовая пирамида | → Упражнения: Часть 1 |
| 15 мин | Блок 2: pytest — основы | → Упражнения: Часть 2 |
| 15 мин | Блок 3: pytest fixtures | → Упражнения: Часть 3 |
| 10 мин | Блок 4: Mocking — имитация зависимостей | → Упражнения: Часть 4 |
| 10 мин | Блок 5: Django TestCase + Client | → Упражнения: Часть 5 |
| 15 мин | Блок 6: Docker — основы | → Упражнения: Часть 6 |
| 15 мин | Интерактив: ситуационные задачи (Chat Polls) | → Упражнения: Часть 7 |
| 10 мин | Подведение итогов | — |

**Итого:** ~80 мин теории + практика + 10 мин итоги = ~90 минут

---

## Блок 1: Виды тестов и тестовая пирамида (10 мин)

Тест — это код, который проверяет, что другой код работает правильно. Но не все тесты одинаковы: они различаются по **скорости**, **изолированности** и тому, **что именно** проверяют.

### Четыре вида тестов

| Вид | Что тестирует | Скорость | Зависимости |
|-----|--------------|----------|-------------|
| **Unit** | Одна функция или метод | ⚡ ~1 мс | Нет |
| **Component** | Небольшая подсистема (класс) | ⚡ ~5 мс | Нет (in-memory) |
| **Integration** | Стыки компонентов с реальной БД/API | 🐢 ~100 мс | Реальная БД |
| **E2E** | Весь путь «браузер → сервер → БД → ответ» | 🐢🐢 ~1 с | Всё приложение |

### Тестовая пирамида

```
         /\
        /E2E\        ← мало, но обязательно для ключевых сценариев
       /------\
      /Integr. \     ← умеренно, для критичных стыков с БД
     /----------\
    / Unit/Comp. \   ← большинство тестов: быстрые и дешёвые
   /______________\
```

**Правило:** большинство тестов — unit-тесты (быстрые, дешёвые). Немного integration-тестов для проверки «стыков». Минимум E2E для ключевых пользовательских сценариев.

```python
from decimal import Decimal


def calculate_order_total(items: list[dict]) -> Decimal:
    """Подсчитать итоговую сумму заказа."""
    total = Decimal("0")
    for item in items:
        total += Decimal(str(item["price"])) * int(item["quantity"])
    return total


# Unit-тест: тестируем ровно одну функцию
def test_order_total() -> None:
    items = [{"price": "250", "quantity": 2}, {"price": "180", "quantity": 1}]
    assert calculate_order_total(items) == Decimal("680")
```

**Когда использовать:** Unit-тесты — всегда, для любой функции с логикой. Integration и E2E — только для критичных сценариев.

> **Подробнее:** см. файл [`examples/01_test_types.py`](examples/01_test_types.py) — демонстрация всех четырёх видов тестов на примере приложения кафе, включая таблицу сравнения и тестовую пирамиду.

### Практика

Перейдите к файлу [`exercises/testing_and_docker.md`](exercises/testing_and_docker.md) и выполните **Часть 1: Виды тестов** (задания 1.1–1.2).

---

## Блок 2: pytest — основы (15 мин)

pytest — стандарт тестирования в Python. Его главное преимущество перед стандартным `unittest` — простота: не нужны классы, не нужен `self`, информативные сообщения об ошибках.

### Простые тест-функции

**Проблема:** `unittest.TestCase` требует классы, `self.assertEqual(...)` — избыточный синтаксис.
**Решение:** в pytest достаточно функции с именем `test_`, и обычного `assert`.

```python
# Хорошее имя теста — как документация:
# test_<что_тестируем>_<условие>_<ожидаемый результат>
def test_empty_order_returns_zero() -> None:
    """Пустой список → итоговая сумма 0."""
    assert calculate_order_total([]) == Decimal("0")


def test_single_item() -> None:
    items = [{"price": "250.00", "quantity": 2}]
    assert calculate_order_total(items) == Decimal("500.00")
```

### `pytest.mark.parametrize` — несколько случаев одним тестом

```python
import pytest
from decimal import Decimal

@pytest.mark.parametrize(
    "items, expected",
    [
        ([], Decimal("0")),
        ([{"price": "100", "quantity": 3}], Decimal("300")),
        ([{"price": "99.99", "quantity": 2}], Decimal("199.98")),
    ],
)
def test_calculate_order_total(items: list[dict], expected: Decimal) -> None:
    assert calculate_order_total(items) == expected
```

### `pytest.raises` — проверка исключений

```python
def test_raises_on_negative_quantity() -> None:
    """Отрицательное количество → ValueError."""
    items = [{"price": "250", "quantity": -1}]
    with pytest.raises(ValueError, match="отрицательным"):
        calculate_order_total(items)
```

**Когда использовать:** `parametrize` — когда одна логика проверяется на 3+ наборах данных. `raises` — всегда когда функция должна поднимать исключение в определённых условиях.

> **Подробнее:** см. файл [`examples/02_pytest_basics.py`](examples/02_pytest_basics.py) — 14 тестов с `parametrize`, `raises`, проверкой типов результата. Запуск: `pytest examples/02_pytest_basics.py -v`.

### Практика

Перейдите к файлу [`exercises/testing_and_docker.md`](exercises/testing_and_docker.md) и выполните **Часть 2: pytest — основы** (задания 2.1–2.2).

---

## Блок 3: pytest fixtures (15 мин)

Фикстуры решают проблему **дублирования кода инициализации** в тестах. Вместо того чтобы в каждом тесте заново создавать объекты, мы описываем их один раз в фикстуре.

### Объявление и использование фикстуры

```python
import pytest
from decimal import Decimal

@pytest.fixture
def category_drinks() -> Category:
    """Фикстура: категория Напитки. Создаётся заново для каждого теста."""
    return Category(id=1, name="Напитки")

@pytest.fixture
def menu_item_cappuccino(category_drinks: Category) -> MenuItem:
    """Фикстура зависит от другой фикстуры — pytest разрешает цепочки."""
    return MenuItem(id=1, name="Капучино", category=category_drinks,
                    price=Decimal("250.00"))

# Использование: pytest передаёт фикстуру по имени параметра
def test_item_price(menu_item_cappuccino: MenuItem) -> None:
    assert menu_item_cappuccino.price == Decimal("250.00")
```

### `scope` — когда пересоздавать фикстуру

| scope | Когда создаётся | Когда использовать |
|-------|-----------------|--------------------|
| `"function"` (default) | Перед каждым тестом | Обычные объекты, изоляция |
| `"module"` | Один раз на файл | Дорогие операции (загрузка конфига) |
| `"session"` | Один раз на запуск pytest | Подключение к БД, внешний сервис |

### `yield` — setup + teardown в одной фикстуре

```python
@pytest.fixture
def temp_order_log(tmp_path: pytest.TempPathFactory) -> str:  # type: ignore[type-arg]
    """Всё до yield — setup. Всё после yield — teardown."""
    log_file = tmp_path / "orders.log"  # type: ignore[operator]
    log_file.write_text("# Лог заказов\n")  # type: ignore[union-attr]
    yield str(log_file)           # ← тест получает путь к файлу
    # teardown выполняется ПОСЛЕ теста, даже если тест упал
```

### `conftest.py` — общие фикстуры для всего пакета

Файл `conftest.py` — специальный файл pytest. Фикстуры, объявленные в нём, автоматически доступны всем тестам в директории и подпапках. Не нужно ничего импортировать.

```
tests/
├── conftest.py          ← фикстуры category_drinks, sample_order
├── test_models.py       ← использует фикстуры из conftest.py
└── test_views.py        ← тоже использует фикстуры из conftest.py
```

> **Подробнее:** см. файл [`examples/03_pytest_fixtures.py`](examples/03_pytest_fixtures.py) — 7 pytest-тестов с зависимостями фикстур, `scope='module'`, `yield`. Также [`examples/conftest.py`](examples/conftest.py) — пример общего conftest.

### Практика

Перейдите к файлу [`exercises/testing_and_docker.md`](exercises/testing_and_docker.md) и выполните **Часть 3: pytest fixtures** (задания 3.1–3.2).

---

## Блок 4: Mocking — имитация зависимостей (10 мин)

Мокирование — замена реальных зависимостей (HTTP-запросов, БД, email) на управляемые заглушки во время тестов.

**Проблема:** тесты, вызывающие внешние сервисы — медленные, ненадёжные и дорогие.
**Решение:** `unittest.mock.patch` заменяет объект на `MagicMock` на время теста.

### `patch` — замена функции или объекта

```python
from unittest.mock import patch
from decimal import Decimal

# Замена функции get_exchange_rate на время теста
with patch("__main__.get_exchange_rate", return_value=90.0) as mock_rate:
    result = calculate_price_in_currency(Decimal("900.00"), "USD")
    assert result == Decimal("10.00")
    mock_rate.assert_called_once_with("USD")  # проверяем аргументы вызова
```

**Правило:** `patch` принимает путь к объекту **там, где он используется**, а не там, где он определён.

### `MagicMock` — объект-заглушка

```python
from unittest.mock import MagicMock

mock_notifier = MagicMock(spec=OrderNotifier)
mock_notifier.send_confirmation.return_value = True

result = mock_notifier.send_confirmation("alice@example.com", 42)
assert result is True
mock_notifier.send_confirmation.assert_called_once_with("alice@example.com", 42)
```

| Атрибут/метод | Что делает |
|---------------|------------|
| `return_value = X` | Мок возвращает `X` при вызове |
| `side_effect = [a, b, c]` | Возвращает `a`, `b`, `c` при последовательных вызовах |
| `side_effect = Exception()` | Поднимает исключение при вызове |
| `assert_called_once_with(...)` | Проверяет, что вызван ровно один раз с этими аргументами |
| `assert_not_called()` | Проверяет, что не был вызван вообще |

**Когда использовать:** мокируйте на **границе** вашего кода с внешним миром: HTTP-клиенты, SMTP, платёжные системы.

> **Подробнее:** см. файл [`examples/05_mocking.py`](examples/05_mocking.py) — `patch` как декоратор и контекстный менеджер, `MagicMock` с `side_effect`, `assert_has_calls`.

### Практика

Перейдите к файлу [`exercises/testing_and_docker.md`](exercises/testing_and_docker.md) и выполните **Часть 4: Mocking** (задания 4.1–4.2).

---

## Блок 5: Django TestCase + Client (10 мин)

Для тестирования Django-приложений используется `django.test.TestCase` — подкласс `unittest.TestCase`, который автоматически оборачивает каждый тест в транзакцию и откатывает изменения после.

### setUp vs setUpTestData

```python
from django.test import TestCase
from decimal import Decimal
from cafe.models import Category, MenuItem


class MenuViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Вызывается ОДИН РАЗ для класса — быстрее.
        # Тесты должны только читать cls.*, не изменять.
        cls.drinks = Category.objects.create(name="Напитки")
        cls.cappuccino = MenuItem.objects.create(
            name="Капучино", category=cls.drinks, price=Decimal("250.00")
        )

    def test_menu_page_returns_200(self) -> None:
        response = self.client.get("/menu/")  # HTTP-запрос без реального сервера
        self.assertEqual(response.status_code, 200)

    def test_available_items_shown(self) -> None:
        response = self.client.get("/menu/")
        self.assertIn("Капучино", response.content.decode("utf-8"))
```

### Django test client

`self.client` — встроенный тестовый HTTP-клиент. Делает запросы к Django-приложению **без реального сервера**:

```python
response = self.client.get("/menu/")
response = self.client.get("/menu/?category=1")
response = self.client.post("/orders/", data={"name": "Алиса"})

# Что проверять:
response.status_code            # 200, 404, 302, ...
response.content.decode("utf-8")  # HTML-содержимое
response.context["items"]        # переменные контекста шаблона
```

**Когда использовать:** `setUpTestData` — когда тесты только читают данные (быстрее). `setUp` — когда тесты изменяют данные (`item.save()`, `item.delete()`).

> **Подробнее:** см. файл [`examples/06_django_tests.py`](examples/06_django_tests.py) — полный шаблон `cafe/tests.py`: тесты для `menu_list` view, `order_detail` view, модели `MenuItem`. Скопируйте в свой `cafe_project`.

### Практика

Перейдите к файлу [`exercises/testing_and_docker.md`](exercises/testing_and_docker.md) и выполните **Часть 5: Django tests** (задание 5.1).

---

## Блок 6: Docker — основы (15 мин)

Docker позволяет упаковать приложение со всеми зависимостями в **контейнер** — изолированную среду, которая одинаково работает на любой машине.

### Три ключевые концепции

```
Dockerfile  →  docker build  →  Image  →  docker run  →  Container
(инструкция)                   (снимок)                  (процесс)
```

| Концепция | Аналогия | Описание |
|-----------|----------|----------|
| **Image** | Рецепт блюда | Неизменяемый снимок файловой системы |
| **Container** | Готовое блюдо | Запущенный процесс из образа |
| **Registry** | Книга рецептов | Хранилище образов (Docker Hub, GHCR) |

### Основные команды Docker

```bash
# Сборка образа из Dockerfile в текущей директории
docker build -t cafe-app:1.0 .

# Запуск контейнера (порт 8000 хоста → 8000 контейнера)
docker run -p 8000:8000 cafe-app:1.0

# Запуск в фоне (detach)
docker run -d -p 8000:8000 cafe-app:1.0

# Список запущенных контейнеров
docker ps

# Остановить контейнер
docker stop <container_id>

# Список скачанных образов
docker images
```

### Dockerfile для Django

```dockerfile
# Базовый образ: официальный Python 3.12
FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Сначала копируем зависимости (кеш слоёв!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Порт, который слушает контейнер
EXPOSE 8000

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### docker-compose — несколько сервисов вместе

В реальных проектах Django работает вместе с базой данных. `docker-compose` описывает эту связку:

```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/cafe
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: cafe
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```bash
# Запустить все сервисы
docker compose up

# Запустить в фоне
docker compose up -d

# Остановить все сервисы
docker compose down
```

**Когда использовать:** Docker — для любого проекта, который нужно деплоить или запускать в команде. `docker-compose` — для проектов с несколькими сервисами (Django + PostgreSQL + Redis).

> **Подробнее:** см. файлы [`examples/07_dockerfile/Dockerfile`](examples/07_dockerfile/Dockerfile), [`examples/07_dockerfile/docker-compose.yml`](examples/07_dockerfile/docker-compose.yml) и [`examples/07_dockerfile/.dockerignore`](examples/07_dockerfile/.dockerignore) — готовые файлы для Django-проекта с комментариями.

### Практика

Перейдите к файлу [`exercises/testing_and_docker.md`](exercises/testing_and_docker.md) и выполните **Часть 6: Docker** (задания 6.1–6.2).

---

## Подведение итогов

### Шпаргалка

| Концепция | Ключевое |
|-----------|----------|
| **Unit-тест** | Одна функция, нет зависимостей, ⚡ быстрый |
| **Integration-тест** | Реальная БД, `@pytest.mark.django_db` |
| **E2E-тест** | Весь путь через HTTP, `self.client.get(...)` |
| `@pytest.fixture` | Объявить переиспользуемые данные для тестов |
| `scope="function"` | Пересоздавать фикстуру для каждого теста (default) |
| `scope="module"` | Создать фикстуру один раз на файл |
| `yield` в фикстуре | До yield = setup, после yield = teardown |
| `conftest.py` | Общие фикстуры для всех тестов в директории |
| `patch(path)` | Заменить объект на `MagicMock` на время теста |
| `return_value` | Что возвращает мок при вызове |
| `assert_called_with(...)` | Проверить аргументы вызова мока |
| `setUpTestData` | Данные один раз на класс тестов (быстрее) |
| `setUp` | Данные перед каждым тестом (полная изоляция) |
| `self.client.get(url)` | HTTP-запрос без реального сервера |
| **Image** | Неизменяемый снимок файловой системы |
| **Container** | Запущенный процесс из образа |
| `docker build -t name .` | Собрать образ из Dockerfile |
| `docker run -p 8000:8000` | Запустить контейнер с пробросом порта |
| `docker compose up` | Запустить все сервисы из docker-compose.yml |

### Ключевые выводы

1. **Тесты — это инвестиция, а не трата времени.** Хорошо покрытый тестами код можно рефакторить уверенно. Без тестов каждое изменение — это риск.

2. **Пирамида тестирования — ориентир.** Много быстрых unit-тестов, немного integration-тестов для стыков с БД, минимум E2E для критичных сценариев.

3. **Docker решает проблему «у меня работало».** Контейнер несёт с собой все зависимости — один и тот же образ работает одинаково на ноутбуке разработчика и на сервере.

> **Главное правило:** тесты — это код. Плохо написанные тесты — хуже, чем их отсутствие: они дают ложное ощущение безопасности. Пишите тесты вдумчиво, давайте им понятные имена, и они станут лучшей документацией вашего кода.

---

## Файлы семинара

```
seminar_08_advanced_django/
├── README.md                              # Этот файл
├── examples/
│   ├── 01_test_types.py                   # Виды тестов: unit, component, integration, E2E
│   ├── 02_pytest_basics.py                # pytest: тест-функции, parametrize, raises
│   ├── 03_pytest_fixtures.py              # pytest fixtures: scope, yield, зависимости
│   ├── 04_test_coverage.md                # Покрытие кода: pytest-cov, интерпретация отчёта
│   ├── 05_mocking.py                      # Mocking: patch, MagicMock, side_effect
│   ├── 06_django_tests.py                 # Django TestCase: setUpTestData, self.client
│   ├── 07_dockerfile/
│   │   ├── Dockerfile                     # Dockerfile для Django-приложения
│   │   ├── docker-compose.yml             # Сервисы: Django + PostgreSQL
│   │   └── .dockerignore                  # Исключения при копировании в образ
│   └── conftest.py                        # Общие фикстуры (пример)
└── exercises/
    └── testing_and_docker.md              # Практические задания
```

---

## Дополнительные материалы

- [pytest documentation](https://docs.pytest.org/en/stable/) — официальная документация: fixtures, markers, plugins
- [Real Python — Getting Started with Testing in Python](https://realpython.com/python-testing/) — подробный туториал по unit-тестам, mock, pytest
- [unittest.mock — Python docs](https://docs.python.org/3/library/unittest.mock.html) — справочник по `patch`, `MagicMock`, `call`
- [Django Testing](https://docs.djangoproject.com/en/5.0/topics/testing/) — официальная документация Django по тестированию
- [Docker Get Started](https://docs.docker.com/get-started/) — официальный туториал Docker: образы, контейнеры, compose
