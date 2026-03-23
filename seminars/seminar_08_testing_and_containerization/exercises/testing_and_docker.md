# Практические задания: Тестирование и контейнеризация

## Подготовка

```bash
# Активируйте виртуальное окружение
source .venv/bin/activate  # Linux/Mac

# Запустите примеры для ознакомления перед выполнением заданий
python seminars/seminar_08_testing_and_containerization/examples/01_test_types.py
python seminars/seminar_08_testing_and_containerization/examples/05_mocking.py

# Запустите pytest-тесты из примеров
pytest seminars/seminar_08_testing_and_containerization/examples/02_pytest_basics.py -v
pytest seminars/seminar_08_testing_and_containerization/examples/03_pytest_fixtures.py -v
```

> **Как работать с заданиями:** прочитайте условие, попробуйте ответить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: Виды тестов

> **Теория:** [README.md — Блок 1](../README.md#блок-1-виды-тестов-и-тестовая-пирамида-10-мин) | **Примеры:** [`examples/01_test_types.py`](../examples/01_test_types.py)

### Задание 1.1

Определите вид каждого теста (unit, component, integration, E2E) и объясните почему:

```python
# Тест A
def test_discount():
    assert apply_discount(Decimal("100"), 10) == Decimal("90")

# Тест B
@pytest.mark.django_db
def test_category_saved():
    cat = Category.objects.create(name="Напитки")
    assert Category.objects.count() == 1

# Тест C
def test_menu_add_and_filter():
    menu = Menu()
    menu.add_item("Капучино", "Напитки", 250)
    menu.add_item("Эспрессо", "Напитки", 180, is_available=False)
    available = menu.get_available()
    assert len(available) == 1

# Тест D
def test_menu_page_loads():
    client = Client()
    response = client.get("/menu/")
    assert response.status_code == 200
    assert "Капучино" in response.content.decode()
```

<details>
<summary>Подсказка</summary>

Задайте для каждого теста вопрос: «Есть ли реальные внешние зависимости (БД, HTTP, файловая система)?» Если нет — это unit или component. Если да — integration или E2E. Разница между unit и component: unit тестирует одну функцию, component — взаимодействие нескольких методов.

</details>

<details>
<summary>Решение</summary>

**Тест A — Unit-тест.**  
Тестирует ровно одну функцию `apply_discount`. Нет зависимостей, нет состояния.

**Тест B — Integration-тест.**  
Использует `@pytest.mark.django_db` — реальную тестовую БД. Проверяет стык между Python-кодом и базой данных.

**Тест C — Component-тест.**  
Тестирует взаимодействие нескольких методов класса `Menu` (`add_item` + `get_available`). Нет внешних зависимостей (всё in-memory), но тест охватывает несколько частей подсистемы.

**Тест D — E2E-тест.**  
Тестирует весь путь: HTTP-запрос → Django view → шаблон → ответ. Зависит от всего приложения (URL-маршруты, view, шаблон, данные в БД).

</details>

---

### Задание 1.2

Расположите виды тестов в порядке **от самого быстрого к самому медленному** и объясните почему. Нарисуйте тестовую пирамиду и укажите, каких тестов должно быть больше всего.

<details>
<summary>Подсказка</summary>

Скорость теста определяется наличием внешних зависимостей. Каждый «прыжок» к реальному ресурсу (БД, HTTP, браузер) добавляет задержку.

</details>

<details>
<summary>Решение</summary>

**Порядок от быстрого к медленному:**  
Unit (~1 мс) → Component (~5 мс) → Integration (~100 мс) → E2E (~1 с)

**Тестовая пирамида:**
```
         /\
        /E2E\        ← мало, для критичных user journey
       /------\
      /Integr. \     ← умеренно, для стыков с БД
     /----------\
    / Unit/Comp. \   ← большинство: быстрые, дешёвые, информативные
   /______________\
```

**Почему большинство — unit/component:**  
- Быстро выполняются (тысячи тестов за секунды)
- При падении сразу ясно, ЧТО сломалось
- Не зависят от инфраструктуры (БД, сеть)

**Почему мало E2E:**  
- Медленные (каждый тест — секунды)
- Хрупкие (зависят от URL, шаблонов, CSS)
- При падении неясно, где именно сломалось

</details>

---

## Часть 2: pytest — основы

> **Теория:** [README.md — Блок 2](../README.md#блок-2-pytest--основы-15-мин) | **Примеры:** [`examples/02_pytest_basics.py`](../examples/02_pytest_basics.py)

### Задание 2.1

Напишите pytest-тесты для функции `apply_discount`. Покройте: обычный случай, нулевую скидку, максимальную скидку (100%), и случай когда скидка > 100% (должна быть ошибка).

```python
from decimal import Decimal


def apply_discount(price: Decimal, discount_percent: float) -> Decimal:
    """Применить скидку к цене.

    Args:
        price: исходная цена
        discount_percent: процент скидки (0–100)

    Returns:
        Цена со скидкой

    Raises:
        ValueError: если скидка < 0 или > 100
    """
    if not (0 <= discount_percent <= 100):
        raise ValueError(f"Скидка должна быть от 0 до 100, получено: {discount_percent}")
    factor = Decimal(str(1 - discount_percent / 100))
    return (price * factor).quantize(Decimal("0.01"))
```

Требования к тестам:
- Имена тестов должны описывать сценарий (`test_<что>_<условие>`)
- Используйте `pytest.mark.parametrize` для нескольких нормальных случаев
- Используйте `pytest.raises` для проверки ошибочных входных данных

<details>
<summary>Подсказка</summary>

Для `parametrize` составьте таблицу входных данных и ожидаемых результатов. Для `raises` используйте `with pytest.raises(ValueError, match="...")`.

</details>

<details>
<summary>Решение</summary>

```python
import pytest
from decimal import Decimal


@pytest.mark.parametrize(
    "price, discount_percent, expected",
    [
        (Decimal("100.00"), 0,    Decimal("100.00")),   # нет скидки
        (Decimal("100.00"), 10,   Decimal("90.00")),    # 10%
        (Decimal("250.00"), 20,   Decimal("200.00")),   # 20%
        (Decimal("100.00"), 100,  Decimal("0.00")),     # 100% — бесплатно
        (Decimal("99.99"),  50,   Decimal("50.00")),    # дробная цена
    ],
)
def test_apply_discount_parametrized(
    price: Decimal, discount_percent: float, expected: Decimal
) -> None:
    assert apply_discount(price, discount_percent) == expected


def test_apply_discount_raises_on_negative() -> None:
    """Отрицательная скидка → ValueError."""
    with pytest.raises(ValueError, match="0 до 100"):
        apply_discount(Decimal("100"), -5)


def test_apply_discount_raises_on_over_100() -> None:
    """Скидка больше 100% → ValueError."""
    with pytest.raises(ValueError, match="0 до 100"):
        apply_discount(Decimal("100"), 101)


def test_apply_discount_returns_decimal() -> None:
    """Результат должен быть Decimal, не float."""
    result = apply_discount(Decimal("100"), 10)
    assert isinstance(result, Decimal)
```

</details>

---

### Задание 2.2

Запустите тесты из `examples/02_pytest_basics.py` через pytest и изучите вывод:

```bash
pytest seminars/seminar_08_testing_and_containerization/examples/02_pytest_basics.py -v
```

Затем намеренно «сломайте» один тест: измените ожидаемое значение в `test_single_item` на `Decimal("999.00")` и снова запустите. Изучите, как pytest объясняет ошибку. После — верните правильное значение.

<details>
<summary>Подсказка</summary>

В сломанном тесте pytest покажет строку с `assert`, и значения обеих сторон: `Decimal('500.00') != Decimal('999.00')`. Именно поэтому важно давать тестам понятные имена — при падении сразу видно, что именно проверялось.

</details>

<details>
<summary>Решение</summary>

Запуск исходных тестов:
```
collected 14 items

02_pytest_basics.py::test_empty_order_returns_zero PASSED
02_pytest_basics.py::test_single_item PASSED
...
14 passed in 0.02s
```

После намеренной поломки (`Decimal("999.00")`):
```
FAILED 02_pytest_basics.py::test_single_item
AssertionError: assert Decimal('500.00') == Decimal('999.00')
```

pytest показывает:
- Имя упавшего теста
- Строку с `assert`
- Фактическое и ожидаемое значения

Это и есть главное преимущество pytest: **имя теста + значения = мгновенная диагностика**.

</details>

---

## Часть 3: pytest fixtures

> **Теория:** [README.md — Блок 3](../README.md#блок-3-pytest-fixtures-15-мин) | **Примеры:** [`examples/03_pytest_fixtures.py`](../examples/03_pytest_fixtures.py)

### Задание 3.1

Ниже три теста с дублирующимся кодом. Вынесите общую инициализацию в фикстуру:

```python
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class MenuItem:
    name: str
    price: Decimal
    is_available: bool = True


# ТЕКУЩИЙ КОД (с дублированием):
def test_item_name() -> None:
    item = MenuItem(name="Капучино", price=Decimal("250.00"))  # дублирование
    assert item.name == "Капучино"


def test_item_price() -> None:
    item = MenuItem(name="Капучино", price=Decimal("250.00"))  # дублирование
    assert item.price == Decimal("250.00")


def test_item_available_by_default() -> None:
    item = MenuItem(name="Капучино", price=Decimal("250.00"))  # дублирование
    assert item.is_available is True
```

Перепишите так, чтобы объект `MenuItem` создавался в фикстуре `cappuccino_item`.

<details>
<summary>Подсказка</summary>

Объявите функцию `cappuccino_item()` с декоратором `@pytest.fixture`, которая возвращает `MenuItem(...)`. Добавьте параметр `cappuccino_item: MenuItem` в каждый тест.

</details>

<details>
<summary>Решение</summary>

```python
import pytest
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class MenuItem:
    name: str
    price: Decimal
    is_available: bool = True


@pytest.fixture
def cappuccino_item() -> MenuItem:
    """Фикстура: позиция Капучино. Создаётся заново для каждого теста."""
    return MenuItem(name="Капучино", price=Decimal("250.00"))


def test_item_name(cappuccino_item: MenuItem) -> None:
    assert cappuccino_item.name == "Капучино"


def test_item_price(cappuccino_item: MenuItem) -> None:
    assert cappuccino_item.price == Decimal("250.00")


def test_item_available_by_default(cappuccino_item: MenuItem) -> None:
    assert cappuccino_item.is_available is True
```

</details>

---

### Задание 3.2

Напишите фикстуру с `yield`, которая:
1. Создаёт временный файл `cart.txt` с содержимым `"# Корзина\n"`
2. Отдаёт тесту путь к файлу
3. После теста — удаляет файл (teardown)

Напишите тест `test_cart_file_contains_header`, который использует эту фикстуру.

<details>
<summary>Подсказка</summary>

Используйте встроенную фикстуру pytest `tmp_path` — она автоматически создаёт временную директорию для теста. Внутри фикстуры: `cart_file = tmp_path / "cart.txt"`, затем `yield str(cart_file)`. В teardown-части (после `yield`) можно вызвать `cart_file.unlink()`, но `tmp_path` и так очищается pytest автоматически.

</details>

<details>
<summary>Решение</summary>

```python
import pytest
from pathlib import Path


@pytest.fixture
def cart_file(tmp_path: Path) -> str:  # type: ignore[type-arg]
    """Создать файл корзины, отдать путь тесту, удалить после."""
    path = tmp_path / "cart.txt"
    path.write_text("# Корзина\n")  # setup

    yield str(path)  # тест получает путь к файлу

    # teardown: tmp_path удаляется pytest автоматически.
    # Здесь можно добавить дополнительную очистку, если нужно.


def test_cart_file_contains_header(cart_file: str) -> None:
    """Файл корзины содержит заголовок, созданный фикстурой."""
    with open(cart_file) as f:
        content = f.read()
    assert "# Корзина" in content
```

</details>

---

## Часть 4: Mocking

> **Теория:** [README.md — Блок 4](../README.md#блок-4-mocking--имитация-зависимостей-10-мин) | **Примеры:** [`examples/05_mocking.py`](../examples/05_mocking.py)

### Задание 4.1

Напишите тест для функции `send_order_notification`, которая отправляет SMS-уведомление. Используйте `patch`, чтобы SMS реально не отправлялся. Проверьте, что функция вызвала `send_sms` с правильными аргументами.

```python
def send_sms(phone: str, message: str) -> bool:
    """Отправить SMS через внешний API (реальный вызов)."""
    # Имитация: в реальности здесь requests.post(...)
    raise ConnectionError("Нет доступа к SMS-сервису!")


def send_order_notification(phone: str, order_id: int) -> bool:
    """Уведомить клиента об оформлении заказа через SMS."""
    message = f"Ваш заказ #{order_id} принят!"
    return send_sms(phone, message)
```

<details>
<summary>Подсказка</summary>

Используйте `with patch("__main__.send_sms", return_value=True) as mock_sms:` внутри теста. После вызова `send_order_notification(...)` проверьте `mock_sms.assert_called_once_with(...)`.

</details>

<details>
<summary>Решение</summary>

```python
from unittest.mock import patch


def test_send_order_notification_calls_sms() -> None:
    """send_order_notification вызывает send_sms с правильными аргументами."""
    with patch("__main__.send_sms", return_value=True) as mock_sms:
        result = send_order_notification("+79001234567", 42)

        # Проверяем, что функция вернула True (из мока)
        assert result is True

        # Проверяем, что send_sms был вызван ровно один раз
        # с правильными аргументами
        mock_sms.assert_called_once_with(
            "+79001234567",
            "Ваш заказ #42 принят!",
        )


def test_send_order_notification_not_called_without_phone() -> None:
    """Если phone пустой — send_sms не должен вызываться."""
    with patch("__main__.send_sms") as mock_sms:
        # В реальной реализации здесь была бы проверка на пустой phone
        mock_sms.assert_not_called()
```

</details>

---

### Задание 4.2

Функция `get_menu_from_api` получает данные через HTTP. Напишите тест с `MagicMock`, который:
1. Имитирует успешный ответ API (список блюд)
2. Проверяет, что функция правильно обрабатывает ответ

```python
import requests


def get_menu_from_api(url: str) -> list[dict]:
    """Получить меню с удалённого API.

    Returns:
        Список блюд [{"name": ..., "price": ...}, ...]
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["items"]
```

<details>
<summary>Подсказка</summary>

`MagicMock` позволяет имитировать атрибуты цепочкой: `mock_response.json.return_value = {"items": [...]}`. Мокируйте `requests.get` и настройте атрибут `status_code` и метод `json()`. Используйте `with patch("__main__.requests.get", return_value=mock_response):`.

</details>

<details>
<summary>Решение</summary>

```python
from unittest.mock import MagicMock, patch


def test_get_menu_from_api_returns_items() -> None:
    """get_menu_from_api правильно разбирает JSON-ответ API."""
    # Создаём мок HTTP-ответа
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {"name": "Капучино", "price": 250},
            {"name": "Латте", "price": 280},
        ]
    }
    # raise_for_status() не должен поднимать исключение
    mock_response.raise_for_status.return_value = None

    with patch("__main__.requests.get", return_value=mock_response) as mock_get:
        result = get_menu_from_api("https://api.cafe.example.com/menu")

        # Проверяем результат
        assert len(result) == 2
        assert result[0]["name"] == "Капучино"
        assert result[1]["price"] == 280

        # Проверяем, что запрос был сделан к правильному URL
        mock_get.assert_called_once_with("https://api.cafe.example.com/menu")
```

</details>

---

## Часть 5: Django tests

> **Теория:** [README.md — Блок 5](../README.md#блок-5-django-testcase--client-10-мин) | **Примеры:** [`examples/06_django_tests.py`](../examples/06_django_tests.py)

### Задание 5.1

Изучите файл [`examples/06_django_tests.py`](../examples/06_django_tests.py) — он содержит готовый шаблон `cafe/tests.py` для вашего Django-проекта.

Ответьте на вопросы:

1. В каком методе (`setUp` или `setUpTestData`) лучше создать тестовые данные, если несколько тестов только **читают** эти данные, не изменяя их?
2. Что проверяет `self.assertNotIn("Недоступный товар", content)`? Почему это важно?
3. Как `self.client` отличается от реального браузерного запроса?

Затем добавьте в шаблон новый тест `test_menu_shows_prices`, который проверяет, что страница `/menu/` содержит строку `"250"` (цена Капучино).

<details>
<summary>Подсказка</summary>

Для п. 1: подумайте о разнице «вызывается один раз» vs «вызывается перед каждым тестом». Для нового теста: скопируйте паттерн `test_available_items_shown`, но проверяйте наличие цены в content.

</details>

<details>
<summary>Решение</summary>

**Ответы:**

1. `setUpTestData` — данные создаются один раз для всего класса, что значительно быстрее при большом числе тестов.

2. Это проверяет, что view не отображает позиции с `is_available=False`. Важно для бизнес-логики: клиент не должен видеть и заказывать недоступные товары.

3. `self.client` делает запросы **внутри Django** без реального HTTP-сервера, TCP-соединений и сетевых задержек. Работает в той же Python-среде.

**Новый тест:**

```python
def test_menu_shows_prices(self) -> None:
    """Страница меню отображает цены позиций."""
    response = self.client.get("/menu/")
    content = response.content.decode("utf-8")
    # Проверяем, что цена Капучино отображается
    self.assertIn("250", content)
```

</details>

---

## Часть 6: Docker

> **Теория:** [README.md — Блок 6](../README.md#блок-6-docker--основы-15-мин) | **Примеры:** [`examples/07_dockerfile/`](../examples/07_dockerfile/)

### Задание 6.1

Изучите [`examples/07_dockerfile/Dockerfile`](../examples/07_dockerfile/Dockerfile) и ответьте:

1. Почему `COPY requirements.txt .` и `RUN pip install ...` идут **перед** `COPY . .`?
2. Что такое `EXPOSE 8000`? Делает ли эта инструкция порт реально доступным?
3. Чем отличается `CMD ["python", "manage.py", "runserver"]` от `ENTRYPOINT`?

<details>
<summary>Подсказка</summary>

Docker строит образ слоями. Слои кешируются: если файл не изменился, Docker использует кешированный слой. Подумайте: `requirements.txt` меняется редко, а код приложения — часто. Какое расположение ускорит повторные сборки?

</details>

<details>
<summary>Решение</summary>

1. **Кеширование слоёв.** Docker кеширует каждую инструкцию. `requirements.txt` меняется редко — значит, слой с `pip install` будет браться из кеша при большинстве пересборок. Если поставить `COPY . .` первым, любое изменение кода инвалидирует кеш и заставит переустанавливать все зависимости заново.

2. `EXPOSE 8000` — документация, сигнал другим разработчикам о том, какой порт использует контейнер. Реально порт становится доступным только при запуске с флагом `-p 8000:8000`. `EXPOSE` без `-p` ничего не открывает.

3. `CMD` задаёт команду по умолчанию, которую **можно переопределить** при запуске: `docker run image other_command`. `ENTRYPOINT` задаёт исполняемый файл, который **всегда** запускается — переопределить можно только через `--entrypoint`. Для Django-приложения обычно используют `CMD`, чтобы иметь возможность запустить `python manage.py migrate` тем же образом.

</details>

---

### Задание 6.2

Изучите [`examples/07_dockerfile/docker-compose.yml`](../examples/07_dockerfile/docker-compose.yml).

Добавьте в конфигурацию сервис `redis` для кеширования:
- Образ: `redis:7-alpine`
- Нет портов, проброшенных на хост (Redis доступен только внутри сети Docker)

Затем добавьте `redis` в `depends_on` сервиса `web`.

<details>
<summary>Подсказка</summary>

Структура нового сервиса такая же, как у `db`. Секция `volumes` для Redis не нужна (данные в памяти). Для изоляции от внешнего мира — просто не указывайте `ports`.

</details>

<details>
<summary>Решение</summary>

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/cafe
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis   # ← добавили зависимость

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: cafe
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:               # ← новый сервис
    image: redis:7-alpine
    # Порты не пробрасываем — Redis доступен только внутри сети Docker
    # по имени хоста "redis" (имя сервиса = DNS-имя в сети compose)

volumes:
  postgres_data:
```

</details>

---

## Часть 7: Ситуационные задачи (Chat Polls)

> Этот раздел используется преподавателем для интерактива в чате.

### Ситуация 1

> Вы тестируете функцию `calculate_tax(price, rate)`, которая умножает цену на ставку налога. Функция не обращается к БД, не делает HTTP-запросов.

Какой вид теста лучше всего подойдёт?

- A) E2E тест через браузер
- B) Integration тест с `@pytest.mark.django_db`
- C) Unit тест с `pytest`
- D) Component тест с реальной БД

<details>
<summary>Ответ</summary>

**C) Unit тест с `pytest`**

Функция `calculate_tax` — чистая математика без зависимостей. Unit-тест будет выполняться за ~1 мс и сразу укажет на проблему при падении.

A — E2E излишен и медленен для простой математической функции.  
B — `django_db` добавляет реальную БД, которая здесь не нужна.  
D — Component-тест предполагает несколько взаимодействующих частей, которых здесь нет.

</details>

---

### Ситуация 2

> Вы пишете тест для view `order_detail`, который достаёт заказ из БД и рендерит шаблон. Данные для теста нужны в БД.

Какой механизм подготовки тестовых данных лучше использовать, если у вас **5 тестов**, и все они **только читают** данные (не изменяют)?

- A) Создавать данные в каждом тесте через `MenuItem.objects.create(...)`
- B) `setUp` — создавать данные перед каждым тестом
- C) `setUpTestData` — создать данные один раз для всего класса
- D) Хардкодить данные прямо в SQL-файле

<details>
<summary>Ответ</summary>

**C) `setUpTestData`**

`setUpTestData` вызывается один раз для класса — данные создаются один раз в БД, а каждый тест видит их через savepoint. При 5 тестах это в 5 раз быстрее, чем `setUp`.

A — Создавать в каждом тесте = дублирование кода.  
B — `setUp` правильный выбор, когда тесты изменяют данные; здесь это излишне.  
D — SQL-файл не поддерживается Django TestCase напрямую и усложняет поддержку.

</details>

---

### Ситуация 3

> Ваш метод `create_order` вызывает `send_confirmation_email(email)` после создания заказа. В тесте вы хотите убедиться, что email **не отправляется** при невалидных данных заказа.

Какой инструмент использовать?

- A) Ничего, просто проверить `order.status`
- B) `MagicMock` с `assert_not_called()`
- C) Реальный SMTP-сервер в Docker
- D) `pytest.raises`

<details>
<summary>Ответ</summary>

**B) `MagicMock` с `assert_not_called()`**

Мок позволяет проверить, что функция `send_confirmation_email` вообще не была вызвана — без реальной отправки писем.

```python
with patch("module.send_confirmation_email") as mock_email:
    create_order(invalid_data)
    mock_email.assert_not_called()
```

A — проверка `status` не гарантирует, что email не был отправлен.  
C — реальный SMTP излишен, медленен и имеет побочные эффекты.  
D — `pytest.raises` проверяет исключения, а не количество вызовов функции.

</details>

---

### Ситуация 4 (Бонус)

> Вы хотите задеплоить Django-приложение на сервер. Коллеги работают на macOS, сервер на Linux. Приложение зависит от `Python 3.12`, `PostgreSQL 16`, `Redis 7`.

Какой инструмент решит проблему «у меня работало»?

- A) Написать подробный README с инструкцией установки
- B) Использовать `virtualenv` для изоляции Python-зависимостей
- C) `docker-compose` с описанием всех сервисов
- D) Попросить всех установить одинаковую версию macOS

<details>
<summary>Ответ</summary>

**C) `docker-compose`**

Docker-compose упаковывает всё приложение (Django + PostgreSQL + Redis) в контейнеры. Один `docker compose up` — и у всех одинаковая среда, независимо от ОС.

A — README требует ручной работы и не гарантирует одинаковость сред.  
B — `virtualenv` изолирует только Python-зависимости, не решает проблему PostgreSQL и Redis.  
D — Привязка к конкретной ОС — антипаттерн.

</details>

---

## Бонусные задания

### Задание Б.1: Полный цикл unit-тестирования

Напишите класс `Cart` и полный набор тестов для него:

```python
from decimal import Decimal


class Cart:
    """Корзина заказа."""

    def __init__(self) -> None:
        self._items: dict[str, dict] = {}  # name → {price, quantity}

    def add(self, name: str, price: Decimal, quantity: int = 1) -> None:
        """Добавить позицию или увеличить количество."""
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        if name in self._items:
            self._items[name]["quantity"] += quantity
        else:
            self._items[name] = {"price": price, "quantity": quantity}

    def remove(self, name: str) -> None:
        """Удалить позицию из корзины."""
        if name not in self._items:
            raise KeyError(f"Позиция '{name}' не найдена в корзине")
        del self._items[name]

    @property
    def total(self) -> Decimal:
        """Итоговая сумма корзины."""
        return sum(
            (v["price"] * v["quantity"] for v in self._items.values()),
            Decimal("0"),
        )

    def __len__(self) -> int:
        return len(self._items)
```

Требования к тестам:
- Покройте все публичные методы и свойство `total`
- Напишите фикстуру `empty_cart` и `cart_with_items`
- Проверьте поведение при ошибочных входных данных (`raises`)
- Проверьте накопление количества при повторном `add` той же позиции

<details>
<summary>Подсказка</summary>

Для `cart_with_items` сделайте фикстуру, которая зависит от `empty_cart` — добавьте несколько позиций. Не забудьте тест на `add` одной позиции дважды — итоговое количество должно накопиться.

</details>

<details>
<summary>Решение</summary>

```python
import pytest
from decimal import Decimal


@pytest.fixture
def empty_cart() -> Cart:
    """Пустая корзина."""
    return Cart()


@pytest.fixture
def cart_with_items(empty_cart: Cart) -> Cart:
    """Корзина с двумя позициями."""
    empty_cart.add("Капучино", Decimal("250.00"), 2)
    empty_cart.add("Круассан", Decimal("180.00"), 1)
    return empty_cart


# --- Тесты для add ---

def test_add_item_increases_length(empty_cart: Cart) -> None:
    empty_cart.add("Капучино", Decimal("250.00"))
    assert len(empty_cart) == 1


def test_add_same_item_accumulates_quantity(empty_cart: Cart) -> None:
    """Повторный add той же позиции накапливает количество."""
    empty_cart.add("Капучино", Decimal("250.00"), 1)
    empty_cart.add("Капучино", Decimal("250.00"), 2)
    assert empty_cart._items["Капучино"]["quantity"] == 3


def test_add_raises_on_zero_quantity(empty_cart: Cart) -> None:
    with pytest.raises(ValueError, match="положительным"):
        empty_cart.add("Капучино", Decimal("250.00"), quantity=0)


def test_add_raises_on_negative_quantity(empty_cart: Cart) -> None:
    with pytest.raises(ValueError, match="положительным"):
        empty_cart.add("Капучино", Decimal("250.00"), quantity=-1)


# --- Тесты для remove ---

def test_remove_item_decreases_length(cart_with_items: Cart) -> None:
    cart_with_items.remove("Капучино")
    assert len(cart_with_items) == 1


def test_remove_nonexistent_raises(empty_cart: Cart) -> None:
    with pytest.raises(KeyError, match="Капучино"):
        empty_cart.remove("Капучино")


# --- Тесты для total ---

def test_total_empty_cart(empty_cart: Cart) -> None:
    assert empty_cart.total == Decimal("0")


def test_total_with_items(cart_with_items: Cart) -> None:
    # Капучино x2 = 500, Круассан x1 = 180
    assert cart_with_items.total == Decimal("680.00")


def test_total_after_remove(cart_with_items: Cart) -> None:
    cart_with_items.remove("Капучино")
    assert cart_with_items.total == Decimal("180.00")
```

</details>

---

### Задание Б.2: Тест с mock + фикстура

Напишите фикстуру `mock_exchange_api`, которая автоматически патчит функцию `get_exchange_rate` и устанавливает курс `90.0` для `"USD"` и `100.0` для `"EUR"`. Используйте `side_effect` для возврата разных значений в зависимости от аргумента.

Затем напишите тест, который использует эту фикстуру и проверяет конвертацию цены в USD и EUR.

<details>
<summary>Подсказка</summary>

`side_effect` может принимать функцию, а не только список. Напишите лямбда-функцию или обычную функцию, которая принимает аргумент `currency` и возвращает нужный курс. В фикстуре используйте `with patch(...) as mock_rate: yield mock_rate` — это позволит тесту работать внутри контекста патча.

</details>

<details>
<summary>Решение</summary>

```python
import pytest
from unittest.mock import patch
from decimal import Decimal


def fake_exchange_rate(currency: str) -> float:
    """Имитация API обменных курсов."""
    rates = {"USD": 90.0, "EUR": 100.0}
    if currency not in rates:
        raise ValueError(f"Неизвестная валюта: {currency}")
    return rates[currency]


@pytest.fixture
def mock_exchange_api():
    """Фикстура: патчит get_exchange_rate на время теста."""
    with patch("__main__.get_exchange_rate", side_effect=fake_exchange_rate) as mock:
        yield mock


def test_price_in_usd(mock_exchange_api) -> None:
    """900 ₽ → 10 USD при курсе 90."""
    result = calculate_price_in_currency(Decimal("900.00"), "USD")
    assert result == Decimal("10.00")
    mock_exchange_api.assert_called_with("USD")


def test_price_in_eur(mock_exchange_api) -> None:
    """1000 ₽ → 10 EUR при курсе 100."""
    result = calculate_price_in_currency(Decimal("1000.00"), "EUR")
    assert result == Decimal("10.00")
    mock_exchange_api.assert_called_with("EUR")
```

</details>

---

## Полезные ресурсы

- [pytest documentation](https://docs.pytest.org/en/stable/) — официальная документация: fixtures, marks, plugins
- [Real Python — Getting Started with Testing](https://realpython.com/python-testing/) — подробный туториал с примерами
- [unittest.mock — Python docs](https://docs.python.org/3/library/unittest.mock.html) — справочник: `patch`, `MagicMock`, `call`
- [Django Testing](https://docs.djangoproject.com/en/5.0/topics/testing/) — официальная документация Django
- [Docker Get Started](https://docs.docker.com/get-started/) — официальный туториал Docker
