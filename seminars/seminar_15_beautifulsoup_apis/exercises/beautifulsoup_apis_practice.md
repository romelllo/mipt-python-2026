# Практические задания: BeautifulSoup и Web API

## Подготовка

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate  # Linux/Mac

# Зависимости уже установлены в проекте, но на всякий случай:
python -c "from bs4 import BeautifulSoup; import requests; print('OK')"

# Запустите примеры, чтобы убедиться, что всё работает:
python seminars/seminar_15_beautifulsoup_apis/examples/01_beautifulsoup_basics.py
python seminars/seminar_15_beautifulsoup_apis/examples/02_web_scraping.py
python seminars/seminar_15_beautifulsoup_apis/examples/03_web_apis.py
python seminars/seminar_15_beautifulsoup_apis/examples/04_news_and_aggregation.py
```

> **Как работать с заданиями:** прочитайте условие, попробуйте решить самостоятельно,
> и только после этого раскройте подсказку или решение для проверки.

---

## Часть 1: Основы BeautifulSoup

> **Теория:** [README.md — Блок 1](../README.md#блок-1-beautifulsoup--основы-парсинга-html-20-мин) |
> **Примеры:** [`examples/01_beautifulsoup_basics.py`](../examples/01_beautifulsoup_basics.py)

### Задание 1.1 — Первый парсинг

Дан HTML-фрагмент. Распарсите его и выведите:
1. Текст тега `<h1>`
2. Значение атрибута `href` у первой ссылки `<a>`
3. Количество тегов `<li>` на странице

```python
html = """
<html>
<body>
  <h1 class="main-title">Курсы МФТИ</h1>
  <ul id="courses">
    <li><a href="/python">Python</a></li>
    <li><a href="/ml">Machine Learning</a></li>
    <li><a href="/algo">Алгоритмы</a></li>
  </ul>
</body>
</html>
"""
```

<details>
<summary>Подсказка</summary>

- Создайте `BeautifulSoup(html, "lxml")`
- Для текста используйте `.text` или `.get_text(strip=True)`
- Для атрибута — `.get("href")` или `tag["href"]`
- Для подсчёта — `len(soup.find_all("li"))`

</details>

<details>
<summary>Решение</summary>

```python
from bs4 import BeautifulSoup

html = """
<html>
<body>
  <h1 class="main-title">Курсы МФТИ</h1>
  <ul id="courses">
    <li><a href="/python">Python</a></li>
    <li><a href="/ml">Machine Learning</a></li>
    <li><a href="/algo">Алгоритмы</a></li>
  </ul>
</body>
</html>
"""

soup = BeautifulSoup(html, "lxml")

# 1. Текст h1
h1 = soup.find("h1")
print(h1.text)  # Курсы МФТИ

# 2. href первой ссылки
first_link = soup.find("a")
print(first_link.get("href"))  # /python

# 3. Количество li
items = soup.find_all("li")
print(len(items))  # 3
```

</details>

---

### Задание 1.2 — Извлечение структурированных данных

Дан HTML с карточками товаров. Напишите функцию `parse_products(html: str) -> list[dict]`,
которая возвращает список словарей с ключами `name`, `price`, `in_stock`.

```python
html = """
<div class="shop">
  <div class="product" data-sku="A001">
    <h3 class="name">Ноутбук Pro</h3>
    <span class="price">89990</span>
    <span class="stock available">В наличии</span>
  </div>
  <div class="product" data-sku="A002">
    <h3 class="name">Мышь беспроводная</h3>
    <span class="price">2490</span>
    <span class="stock unavailable">Нет в наличии</span>
  </div>
  <div class="product" data-sku="A003">
    <h3 class="name">Клавиатура механическая</h3>
    <span class="price">7800</span>
    <span class="stock available">В наличии</span>
  </div>
</div>
"""
```

Ожидаемый результат:
```python
[
    {"name": "Ноутбук Pro", "price": 89990, "in_stock": True},
    {"name": "Мышь беспроводная", "price": 2490, "in_stock": False},
    {"name": "Клавиатура механическая", "price": 7800, "in_stock": True},
]
```

<details>
<summary>Подсказка</summary>

- Найдите все `div.product` через `find_all()`
- Для каждого: извлеките `.name`, `.price`, проверьте класс `.stock`
- `"available" in tag["class"]` — проверка наличия класса
- `int(price_tag.text)` — конвертация цены в число

</details>

<details>
<summary>Решение</summary>

```python
from bs4 import BeautifulSoup, Tag


def parse_products(html: str) -> list[dict]:
    """Извлекает список товаров из HTML."""
    soup = BeautifulSoup(html, "lxml")
    products = []

    for div in soup.find_all("div", class_="product"):
        if not isinstance(div, Tag):
            continue

        name_tag = div.find("h3", class_="name")
        price_tag = div.find("span", class_="price")
        stock_tag = div.find("span", class_="stock")

        name = name_tag.get_text(strip=True) if name_tag else ""
        price = int(price_tag.get_text(strip=True)) if price_tag else 0

        # Проверяем наличие класса "available"
        in_stock = False
        if isinstance(stock_tag, Tag):
            classes = stock_tag.get("class", [])
            in_stock = "available" in classes

        products.append({"name": name, "price": price, "in_stock": in_stock})

    return products


result = parse_products(html)
for p in result:
    status = "✓" if p["in_stock"] else "✗"
    print(f"  {status} {p['name']}: {p['price']} ₽")
```

</details>

---

## Часть 2: Веб-скрапинг

> **Теория:** [README.md — Блок 2](../README.md#блок-2-навигация-и-извлечение-данных-20-мин) |
> **Примеры:** [`examples/02_web_scraping.py`](../examples/02_web_scraping.py)

### Задание 2.1 — Скрапинг цитат

Напишите функцию `get_quotes_by_author(author_name: str) -> list[str]`,
которая загружает страницу `https://quotes.toscrape.com` и возвращает
все цитаты указанного автора.

<details>
<summary>Подсказка</summary>

- Загрузите страницу через `requests.get()`
- Найдите все `div.quote`
- Для каждой проверьте `small.author` — совпадает ли с `author_name`
- Текст цитаты — в `span.text`

</details>

<details>
<summary>Решение</summary>

```python
import requests
from bs4 import BeautifulSoup, Tag


def get_quotes_by_author(author_name: str) -> list[str]:
    """Возвращает цитаты указанного автора с первой страницы."""
    url = "https://quotes.toscrape.com"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MIPTBot/1.0)"}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    quotes = []

    for div in soup.select("div.quote"):
        if not isinstance(div, Tag):
            continue
        author_tag = div.select_one("small.author")
        if author_tag and author_tag.get_text(strip=True) == author_name:
            text_tag = div.select_one("span.text")
            if text_tag:
                quotes.append(text_tag.get_text(strip=True).strip("\u201c\u201d"))

    return quotes


# Тест
quotes = get_quotes_by_author("Albert Einstein")
print(f"Цитаты Эйнштейна: {len(quotes)}")
for q in quotes:
    print(f"  — {q[:80]}...")
```

</details>

---

### Задание 2.2 — Скрапинг с пагинацией

Напишите функцию `collect_all_tags() -> dict[str, int]`, которая обходит
**все страницы** `quotes.toscrape.com` и возвращает словарь `{тег: количество}`.

<details>
<summary>Подсказка</summary>

- Начните с `url = "https://quotes.toscrape.com"`
- После парсинга каждой страницы ищите `li.next a` для получения следующей страницы
- Если `li.next` не найден — вы на последней странице
- Теги — `a.tag` внутри `div.tags`

</details>

<details>
<summary>Решение</summary>

```python
import time
import requests
from bs4 import BeautifulSoup, Tag


def collect_all_tags() -> dict[str, int]:
    """Собирает все теги со всех страниц quotes.toscrape.com."""
    base_url = "https://quotes.toscrape.com"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MIPTBot/1.0)"}
    tag_counts: dict[str, int] = {}
    url: str | None = base_url

    while url:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        # Собираем теги
        for tag_link in soup.select("div.tags a.tag"):
            tag = tag_link.get_text(strip=True)
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Следующая страница
        next_btn = soup.select_one("li.next a")
        if next_btn and isinstance(next_btn, Tag):
            href = next_btn.get("href")
            url = base_url + str(href) if href else None
        else:
            url = None

        time.sleep(0.5)  # вежливая пауза

    return tag_counts


tags = collect_all_tags()
top_10 = sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]
print("Топ-10 тегов:")
for tag, count in top_10:
    print(f"  #{tag}: {count}")
```

</details>

---

## Часть 3: Web API

> **Теория:** [README.md — Блок 3](../README.md#блок-3-web-api--концепция-и-работа-с-json-20-мин) |
> **Примеры:** [`examples/03_web_apis.py`](../examples/03_web_apis.py)

### Задание 3.1 — Первый запрос к API

Используя open-meteo.com, получите текущую температуру в Москве (широта 55.7558, долгота 37.6173).
Выведите температуру и единицу измерения.

API URL: `https://api.open-meteo.com/v1/forecast`

Параметры:
- `latitude=55.7558`
- `longitude=37.6173`
- `current=temperature_2m`
- `timezone=Europe/Moscow`

<details>
<summary>Подсказка</summary>

- Используйте `requests.get(url, params={...})`
- Ответ — JSON: `response.json()`
- Температура: `data["current"]["temperature_2m"]`
- Единица: `data["current_units"]["temperature_2m"]`

</details>

<details>
<summary>Решение</summary>

```python
import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 55.7558,
    "longitude": 37.6173,
    "current": "temperature_2m",
    "timezone": "Europe/Moscow",
}

response = requests.get(url, params=params, timeout=10)
response.raise_for_status()
data = response.json()

temp = data["current"]["temperature_2m"]
unit = data["current_units"]["temperature_2m"]
print(f"Текущая температура в Москве: {temp}{unit}")
```

</details>

---

### Задание 3.2 — Обработка ошибок API

Напишите функцию `robust_api_call(url: str, params: dict, max_retries: int = 3) -> dict | None`,
которая повторяет запрос при временных ошибках (таймаут, 5xx) с экспоненциальной задержкой,
но сразу возвращает `None` при клиентских ошибках (4xx).

<details>
<summary>Подсказка</summary>

- Экспоненциальная задержка: `time.sleep(2 ** attempt)`
- `e.response.status_code` — код ошибки у `HTTPError`
- 4xx (400-499) — ошибка клиента, повторять бессмысленно
- 5xx (500-599) — ошибка сервера, можно повторить

</details>

<details>
<summary>Решение</summary>

```python
import time
import requests
from requests.exceptions import HTTPError, RequestException


def robust_api_call(
    url: str, params: dict, max_retries: int = 3
) -> dict | None:
    """Запрос к API с повторными попытками при временных ошибках."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except HTTPError as e:
            status = e.response.status_code if e.response is not None else 0
            if 400 <= status < 500:
                # Клиентская ошибка — повторять бессмысленно
                print(f"Клиентская ошибка {status}, прекращаем")
                return None
            # Серверная ошибка — повторим
            delay = 2**attempt
            print(f"Серверная ошибка {status}, повтор через {delay}с...")
            time.sleep(delay)

        except RequestException as e:
            delay = 2**attempt
            print(f"Ошибка сети ({e}), повтор через {delay}с...")
            time.sleep(delay)

    print(f"Все {max_retries} попытки исчерпаны")
    return None
```

</details>

---

## Часть 4: Агрегация данных

> **Теория:** [README.md — Блок 4](../README.md#блок-4-практические-примеры--агрегация-данных-20-мин) |
> **Примеры:** [`examples/04_news_and_aggregation.py`](../examples/04_news_and_aggregation.py)

### Задание 4.1 — Топ новостей HN

Напишите скрипт, который загружает топ-20 новостей с Hacker News и выводит
только те, у которых рейтинг выше среднего.

API: `https://hacker-news.firebaseio.com/v0/topstories.json`
Новость: `https://hacker-news.firebaseio.com/v0/item/{id}.json`

<details>
<summary>Подсказка</summary>

- Сначала загрузите все 20 новостей
- Посчитайте средний рейтинг: `sum(scores) / len(scores)`
- Отфильтруйте и выведите

</details>

<details>
<summary>Решение</summary>

```python
import time
import requests


def get_top_stories_above_average(n: int = 20) -> None:
    """Выводит новости HN с рейтингом выше среднего."""
    # Получаем список ID
    ids_resp = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10
    )
    ids_resp.raise_for_status()
    top_ids = ids_resp.json()[:n]

    # Загружаем каждую новость
    stories = []
    for story_id in top_ids:
        resp = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
            timeout=10,
        )
        data = resp.json()
        if data and data.get("type") == "story" and not data.get("dead"):
            stories.append(data)
        time.sleep(0.1)

    if not stories:
        print("Нет данных")
        return

    avg_score = sum(s.get("score", 0) for s in stories) / len(stories)
    print(f"Средний рейтинг: {avg_score:.1f}")
    print("\nНовости выше среднего:")

    above_avg = [s for s in stories if s.get("score", 0) > avg_score]
    above_avg.sort(key=lambda s: s.get("score", 0), reverse=True)

    for s in above_avg:
        print(f"  [{s['score']}★] {s.get('title', '?')[:70]}")


get_top_stories_above_average()
```

</details>

---

### Задание 4.2 — Погода + новости: комбинированный дашборд

Напишите функцию `morning_dashboard(city: str, lat: float, lon: float) -> None`,
которая выводит "утренний дайджест":
1. Текущая погода в городе (open-meteo.com)
2. Топ-5 новостей HN прямо сейчас

<details>
<summary>Подсказка</summary>

- Сначала погода, потом новости — два независимых блока
- Оберните каждый блок в отдельный `try/except` — если один источник недоступен, другой всё равно выводится

</details>

<details>
<summary>Решение</summary>

```python
import time
import requests
from requests.exceptions import RequestException


def morning_dashboard(city: str, lat: float, lon: float) -> None:
    """Утренний дайджест: погода + топ новостей."""
    print(f"{'=' * 50}")
    print(f"  Утренний дайджест: {city}")
    print(f"{'=' * 50}")

    # --- Погода ---
    print("\n🌤  Погода:")
    try:
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,weather_code,wind_speed_10m",
                "timezone": "auto",
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        current = data.get("current", {})
        print(
            f"  Температура: {current.get('temperature_2m')}°C, "
            f"ветер: {current.get('wind_speed_10m')} км/ч"
        )
    except RequestException as e:
        print(f"  Ошибка получения погоды: {e}")

    # --- Новости ---
    print("\n📰  Топ-5 новостей Hacker News:")
    try:
        ids_resp = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10
        )
        ids_resp.raise_for_status()
        top_ids = ids_resp.json()[:5]

        for i, story_id in enumerate(top_ids, 1):
            item_resp = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                timeout=10,
            )
            item = item_resp.json()
            if item:
                title = item.get("title", "?")[:65]
                score = item.get("score", 0)
                print(f"  {i}. [{score}★] {title}")
            time.sleep(0.1)
    except RequestException as e:
        print(f"  Ошибка получения новостей: {e}")

    print(f"\n{'=' * 50}")


morning_dashboard("Москва", 55.7558, 37.6173)
```

</details>

---

## Часть 5: Ситуационные задачи (Chat Polls)

> Этот раздел используется преподавателем для интерактива в чате.

### Ситуация 1

> Вы парсите интернет-магазин. Нужно извлечь цену товара из такого HTML:
> `<span class="price current-price">1 299 ₽</span>`

Какой код правильно извлечёт текст цены?

- A) `soup.find("span")["price"]`
- B) `soup.find("span", class_="price").text`
- C) `soup.find("span", class_="price current-price").get_text(strip=True)`
- D) `soup.select(".price.current-price")[0].attrs`

<details>
<summary>Ответ</summary>

**C) `soup.find("span", class_="price current-price").get_text(strip=True)`**

- **A** — неверно: `["price"]` обращается к атрибуту тега, а не к тексту
- **B** — частично верно, но `class_="price"` найдёт первый span с классом `price`,
  а у нас два класса. В BeautifulSoup `class_="price"` ищет элементы, **содержащие** класс `price`,
  так что B тоже сработает — но C надёжнее и убирает лишние пробелы через `strip=True`
- **C** — правильно: явно указываем оба класса, `get_text(strip=True)` убирает пробелы
- **D** — вернёт словарь атрибутов, а не текст

</details>

---

### Ситуация 2

> Вы делаете запрос к API погоды и получаете ответ. Как правильно извлечь данные?
>
> ```python
> response = requests.get(url, params=params, timeout=10)
> ```

Что нужно сделать **следующим** шагом перед обращением к `response.json()`?

- A) `response.encoding = "utf-8"`
- B) `response.raise_for_status()`
- C) `assert response.ok`
- D) `json.loads(response.text)`

<details>
<summary>Ответ</summary>

**B) `response.raise_for_status()`**

- **A** — установка кодировки не нужна для JSON (он всегда UTF-8) и не проверяет ошибки
- **B** — правильно: выбрасывает `HTTPError` для кодов 4xx/5xx, позволяя поймать ошибку в `except`
- **C** — `assert` — плохая практика для обработки ошибок: в production-коде `assert` может быть отключён
- **D** — `response.json()` уже делает это внутри; дублировать не нужно

</details>

---

### Ситуация 3

> Вы пишете скрапер, который обходит 100 страниц сайта. После ~20 запросов
> сервер начинает возвращать код 429 (Too Many Requests).

Что нужно сделать?

- A) Игнорировать ошибку и продолжать
- B) Добавить `time.sleep(2)` между запросами
- C) Поменять User-Agent на каждом запросе
- D) Использовать `response.raise_for_status()` и остановить скрапер

<details>
<summary>Ответ</summary>

**B) Добавить `time.sleep(2)` между запросами**

- **A** — неверно: игнорирование 429 приведёт к блокировке IP
- **B** — правильно: пауза между запросами — основной способ соблюдать rate limit.
  Также стоит проверить заголовок `Retry-After` в ответе 429
- **C** — смена User-Agent не решает проблему rate limiting (сервер видит IP, а не User-Agent)
- **D** — остановить скрапер полностью — слишком радикально; лучше замедлиться

</details>

---

### Ситуация 4

> Нужно найти все ссылки на статьи в таком HTML:
> ```html
> <div class="articles">
>   <a href="/article/1" class="article-link">Статья 1</a>
>   <a href="https://external.com" class="ext-link">Внешняя</a>
>   <a href="/article/2" class="article-link">Статья 2</a>
> </div>
> ```

Какой CSS-селектор выберет **только** ссылки на статьи (начинающиеся с `/article/`)?

- A) `soup.select("a")`
- B) `soup.select(".articles a.article-link")`
- C) `soup.select('a[href^="/article/"]')`
- D) `soup.find_all("a", href=True)`

<details>
<summary>Ответ</summary>

**C) `soup.select('a[href^="/article/"]')`**

- **A** — выберет все ссылки, включая внешнюю
- **B** — выберет ссылки с классом `article-link` — тоже правильно в данном примере,
  но менее универсально (класс может измениться)
- **C** — правильно: атрибутный селектор `[href^="/article/"]` выбирает ссылки,
  у которых `href` **начинается** с `/article/` — точно и надёжно
- **D** — выберет все ссылки с любым `href`

</details>

---

## Бонусные задания

### Бонус 1 — Мини-агрегатор новостей

Напишите скрипт `news_aggregator.py`, который:
1. Загружает топ-30 новостей с Hacker News
2. Фильтрует новости, содержащие ключевые слова из списка `["Python", "AI", "ML", "data"]`
3. Для каждой найденной новости выводит заголовок, рейтинг, дату и ссылку
4. Сохраняет результат в JSON-файл `news_digest.json`

<details>
<summary>Подсказка</summary>

- Используйте функции из `04_news_and_aggregation.py`
- `datetime.fromtimestamp(story.time).isoformat()` — дата в ISO формате
- `json.dumps(data, ensure_ascii=False, indent=2)` — красивый JSON
- `Path("news_digest.json").write_text(...)` — сохранение файла

</details>

<details>
<summary>Решение</summary>

```python
import json
import time
from datetime import datetime
from pathlib import Path

import requests


def fetch_story(story_id: int) -> dict | None:
    """Загружает одну новость по ID."""
    try:
        resp = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        return None


def news_aggregator(
    keywords: list[str],
    top_n: int = 30,
    output_file: str = "news_digest.json",
) -> None:
    """Агрегирует новости HN по ключевым словам."""
    resp = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10
    )
    resp.raise_for_status()
    top_ids = resp.json()[:top_n]

    print(f"Загружаем {top_n} новостей...")
    stories = []
    for i, story_id in enumerate(top_ids, 1):
        print(f"  [{i}/{top_n}]", end="\r")
        data = fetch_story(story_id)
        if data and data.get("type") == "story" and not data.get("dead"):
            stories.append(data)
        time.sleep(0.1)

    print(f"\nЗагружено: {len(stories)}")

    kw_lower = [kw.lower() for kw in keywords]
    matched = [
        s for s in stories
        if any(kw in s.get("title", "").lower() for kw in kw_lower)
    ]
    print(f"Найдено по ключевым словам {keywords}: {len(matched)}")

    digest = []
    for s in matched:
        digest.append({
            "title": s.get("title", ""),
            "score": s.get("score", 0),
            "url": s.get("url", ""),
            "author": s.get("by", ""),
            "published_at": datetime.fromtimestamp(s.get("time", 0)).isoformat(),
            "comments": s.get("descendants", 0),
        })

    digest.sort(key=lambda x: x["score"], reverse=True)

    for item in digest:
        print(f"\n[{item['score']}★] {item['title']}")
        print(f"  {item['published_at']} | {item['comments']} комментариев")
        print(f"  {item['url'] or '(без ссылки)'}")

    Path(output_file).write_text(
        json.dumps(digest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nСохранено в {output_file}")


news_aggregator(keywords=["Python", "AI", "ML", "data"])
```

</details>

---

### Бонус 2 — Скрапинг + API: обогащение данных

Напишите скрипт, который:
1. Парсит список книг с `https://books.toscrape.com` (первые 2 страницы)
2. Для каждой книги извлекает: название, цену, рейтинг (звёзды), наличие
3. Добавляет к каждой книге текущий курс GBP→RUB (используйте
   `https://open.er-api.com/v6/latest/GBP` — бесплатный API без ключа)
4. Выводит цену в рублях

<details>
<summary>Подсказка</summary>

- Рейтинг на books.toscrape.com задан классом: `class="star-rating Three"` → 3 звезды
- Словарь для перевода: `{"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}`
- Цена: `£51.77` → `float("51.77")`
- Курс: `data["rates"]["RUB"]`

</details>

<details>
<summary>Решение</summary>

```python
import time
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

STAR_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


@dataclass
class Book:
    """Книга с books.toscrape.com."""
    title: str
    price_gbp: float
    rating: int
    available: bool


def get_gbp_to_rub_rate() -> float:
    """Получает курс GBP к RUB."""
    try:
        resp = requests.get("https://open.er-api.com/v6/latest/GBP", timeout=10)
        resp.raise_for_status()
        return float(resp.json()["rates"]["RUB"])
    except Exception:
        return 115.0  # запасной курс


def parse_books_page(html: str) -> list[Book]:
    """Парсит страницу books.toscrape.com."""
    soup = BeautifulSoup(html, "lxml")
    books = []

    for article in soup.select("article.product_pod"):
        if not isinstance(article, Tag):
            continue

        title_tag = article.select_one("h3 a")
        title = title_tag.get("title", "") if title_tag else ""

        price_tag = article.select_one("p.price_color")
        price_text = (
            price_tag.get_text(strip=True).replace("£", "").replace("Â", "")
            if price_tag
            else "0"
        )
        try:
            price = float(price_text)
        except ValueError:
            price = 0.0

        rating_tag = article.select_one("p.star-rating")
        rating = 0
        if isinstance(rating_tag, Tag):
            for cls in rating_tag.get("class", []):
                if cls in STAR_MAP:
                    rating = STAR_MAP[cls]

        avail_tag = article.select_one("p.availability")
        available = "In stock" in (avail_tag.get_text() if avail_tag else "")

        books.append(Book(title=str(title), price_gbp=price, rating=rating, available=available))

    return books


def scrape_books_with_prices(pages: int = 2) -> None:
    """Скрапит книги и выводит цены в рублях."""
    print("Получаем курс GBP/RUB...")
    rate = get_gbp_to_rub_rate()
    print(f"Курс: 1 GBP = {rate:.2f} RUB\n")

    base_url = "https://books.toscrape.com"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MIPTBot/1.0)"}
    all_books: list[Book] = []

    for page in range(1, pages + 1):
        url = f"{base_url}/catalogue/page-{page}.html"
        print(f"Страница {page}: {url}")
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        all_books.extend(parse_books_page(resp.text))
        time.sleep(0.5)

    print(f"\nВсего книг: {len(all_books)}")
    print(f"\n{'Название':<45} {'GBP':>6} {'RUB':>8} {'★':>3}")
    print("-" * 70)

    for book in sorted(all_books, key=lambda b: b.price_gbp)[:10]:
        price_rub = book.price_gbp * rate
        status = "✓" if book.available else "✗"
        print(
            f"{status} {book.title[:43]:<43} "
            f"£{book.price_gbp:>5.2f} "
            f"{price_rub:>7.0f}₽ "
            f"{'★' * book.rating}"
        )


scrape_books_with_prices(pages=2)
```

</details>

---

## Полезные ресурсы

- [BeautifulSoup документация](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) — официальная документация
- [open-meteo.com](https://open-meteo.com/en/docs) — бесплатный API погоды без ключа
- [Hacker News API](https://github.com/HackerNews/API) — документация HN Firebase API
- [quotes.toscrape.com](https://quotes.toscrape.com) — сайт для практики скрапинга
- [Real Python — Web Scraping](https://realpython.com/beautiful-soup-web-scraper-python/) — подробное руководство
