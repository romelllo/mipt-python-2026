# Семинар 15: BeautifulSoup и Web API

**Модуль:** 4 — Анализ данных в Python  
**Дата:** 13.05.2026  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1_hmfIh9AX8RHzHikGaq1CfC87Tx0H83wM5ryb8rZy68/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:

- **Парсить** HTML-документы с помощью BeautifulSoup: создавать объект `soup`, находить теги через `find`/`find_all` и CSS-селекторы
- **Извлекать** текст, атрибуты и структурированные данные из реальных веб-страниц
- **Объяснять** концепцию Web API: чем API отличается от веб-скрапинга, что такое JSON, rate limiting и пагинация
- **Отправлять** запросы к публичным API (погода, новости) и обрабатывать JSON-ответы
- **Агрегировать** данные из нескольких источников и обрабатывать типичные ошибки (таймаут, 4xx/5xx, отсутствующие поля)

---

## Подготовка

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# beautifulsoup4 и requests уже есть в pyproject.toml
# Проверьте установку:
python -c "from bs4 import BeautifulSoup; import requests; print('OK')"

# Запустите примеры для проверки:
python seminars/seminar_15_beautifulsoup_apis/examples/01_beautifulsoup_basics.py
python seminars/seminar_15_beautifulsoup_apis/examples/03_web_apis.py
```

---

## План семинара

| Время | Тема | Практика |
|-------|------|----------|
| 20 мин | Блок 1: BeautifulSoup — основы парсинга HTML | → Упражнения: Часть 1 |
| 20 мин | Блок 2: Навигация и извлечение данных | → Упражнения: Часть 2 |
| 20 мин | Блок 3: Web API — концепция и работа с JSON | → Упражнения: Часть 3 |
| 20 мин | Блок 4: Практические примеры — агрегация данных | → Упражнения: Часть 4 |
| 10 мин | Блок 5: Подведение итогов + Chat Polls | — |

**Итого:** ~90 минут

---

## Блок 1: BeautifulSoup — основы парсинга HTML (20 мин)

### Зачем нужен BeautifulSoup?

В [семинаре 14](../seminar_14_external_data_collection/README.md) мы извлекали данные из HTML
с помощью регулярных выражений. Это работает для простых случаев, но у регулярок есть предел:
HTML — это дерево, а не плоский текст. **BeautifulSoup** понимает структуру HTML и позволяет
искать элементы так же, как это делает браузер.

```
Регулярки:  r'<span class="price">([^<]+)</span>'  — хрупко, ломается при изменении HTML
BeautifulSoup: soup.find("span", class_="price").text  — надёжно, читаемо
```

### Создание объекта BeautifulSoup

```python
from bs4 import BeautifulSoup

html = "<h1 class='title'>Привет</h1><p>Текст</p>"

# Первый аргумент — HTML-строка, второй — парсер
soup = BeautifulSoup(html, "lxml")   # lxml — быстрый C-парсер (рекомендуется)
# soup = BeautifulSoup(html, "html.parser")  # встроенный, без зависимостей
```

**Когда использовать:** `lxml` — для продакшн-кода (быстрее, терпимее к битому HTML);
`html.parser` — если нет возможности установить lxml.

### find() и find_all()

```python
# find() — возвращает ПЕРВЫЙ подходящий тег (или None)
tag = soup.find("h1")                          # по имени тега
tag = soup.find("span", class_="price")        # по имени + классу
tag = soup.find("div", attrs={"data-id": "5"}) # по произвольному атрибуту

# find_all() — возвращает СПИСОК всех подходящих тегов
items = soup.find_all("li")                    # все <li>
items = soup.find_all("a", limit=5)            # первые 5 ссылок
```

**Использование:**

```python
html = """
<ul>
  <li class="item">Яблоко</li>
  <li class="item">Груша</li>
  <li class="item sale">Банан (скидка)</li>
</ul>
"""
soup = BeautifulSoup(html, "lxml")

items = soup.find_all("li", class_="item")
print(len(items))   # 3 — class_="item" находит все li, содержащие класс "item"

first = soup.find("li")
print(first.text)   # Яблоко
```

### CSS-селекторы: select() и select_one()

CSS-селекторы — мощная альтернатива `find`/`find_all`. Если вы знакомы с CSS,
они покажутся интуитивными:

```python
# select_one() — первый элемент (аналог find)
title = soup.select_one("h1.main-title")       # тег h1 с классом main-title
intro = soup.select_one("#intro")              # элемент с id="intro"

# select() — все элементы (аналог find_all)
links = soup.select(".catalog a.link")         # ссылки с классом link внутри .catalog
book_links = soup.select('a[href^="/books/"]') # ссылки, href начинается с /books/
```

| Синтаксис | Что выбирает |
|-----------|-------------|
| `tag` | все теги с этим именем |
| `.class` | элементы с этим классом |
| `#id` | элемент с этим id |
| `parent child` | потомки (любой уровень) |
| `parent > child` | прямые потомки |
| `[attr^="val"]` | атрибут начинается с val |
| `[attr$="val"]` | атрибут заканчивается на val |
| `[attr*="val"]` | атрибут содержит val |

> **Подробнее:** см. файл [`examples/01_beautifulsoup_basics.py`](examples/01_beautifulsoup_basics.py) —
> полные примеры парсинга, find/find_all, CSS-селекторов, навигации по дереву.

### Практика

Перейдите к файлу [`exercises/beautifulsoup_apis_practice.md`](exercises/beautifulsoup_apis_practice.md)
и выполните **Часть 1: Основы BeautifulSoup** (задания 1.1–1.2).

---

## Блок 2: Навигация и извлечение данных (20 мин)

### Извлечение текста и атрибутов

После того как тег найден, нужно извлечь из него данные:

```python
from bs4 import BeautifulSoup, Tag

html = """
<article class="book" data-id="42">
  <h2 class="title">Чистый код</h2>
  <a href="/books/clean-code" target="_blank">Читать</a>
  <span class="price">1 200 ₽</span>
</article>
"""
soup = BeautifulSoup(html, "lxml")
article = soup.find("article")

# .text — весь текст внутри тега (включая вложенные)
print(article.text)  # '\nЧистый код\nЧитать\n1 200 ₽\n'

# .get_text(strip=True) — без лишних пробелов и переносов
print(article.get_text(separator=" | ", strip=True))
# 'Чистый код | Читать | 1 200 ₽'

# .get("attr") — безопасное получение атрибута (не выбросит KeyError)
link = soup.find("a")
print(link.get("href"))           # /books/clean-code
print(link.get("class", []))      # [] — атрибут отсутствует, возвращаем дефолт

# .attrs — словарь всех атрибутов
if isinstance(article, Tag):
    print(article.attrs)          # {'class': ['book'], 'data-id': '42'}
    print(article["data-id"])     # '42' — прямой доступ как к словарю
```

### Навигация по дереву

```python
span = soup.find("span", class_="price")

# Родитель
print(span.parent.name)           # article

# Следующий/предыдущий сосед (тег на том же уровне)
prev = span.find_previous_sibling("a")
print(prev.text)                  # Читать

# Дочерние элементы (итератор, включает NavigableString — пробелы!)
from bs4 import Tag
for child in article.children:
    if isinstance(child, Tag):    # фильтруем только теги
        print(child.name, child.text.strip())
```

### Реальный пример: скрапинг quotes.toscrape.com

```python
import requests
from bs4 import BeautifulSoup, Tag

url = "https://quotes.toscrape.com"
headers = {"User-Agent": "Mozilla/5.0 (compatible; MIPTBot/1.0)"}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

for div in soup.select("div.quote"):
    text = div.select_one("span.text")
    author = div.select_one("small.author")
    tags = div.select("a.tag")

    print(f'"{text.get_text(strip=True)}"')
    print(f"  — {author.get_text(strip=True)}")
    print(f"  Теги: {', '.join(t.text for t in tags)}\n")
```

**Этика скрапинга:**
- Всегда проверяйте `robots.txt` (`https://site.com/robots.txt`)
- Делайте паузы между запросами (`time.sleep(1)`)
- Устанавливайте понятный `User-Agent`
- Используйте сайты, созданные для практики: `quotes.toscrape.com`, `books.toscrape.com`

> **Подробнее:** см. файл [`examples/02_web_scraping.py`](examples/02_web_scraping.py) —
> полный цикл скрапинга quotes.toscrape.com: загрузка, парсинг, пагинация, анализ данных.

### Практика

Перейдите к файлу [`exercises/beautifulsoup_apis_practice.md`](exercises/beautifulsoup_apis_practice.md)
и выполните **Часть 2: Веб-скрапинг** (задания 2.1–2.2).

---

## Блок 3: Web API — концепция и работа с JSON (20 мин)

### Что такое Web API?

**Web API** (Application Programming Interface) — это интерфейс, через который программы
общаются друг с другом по HTTP. В отличие от веб-скрапинга, API возвращает
**структурированные данные** (обычно JSON), специально предназначенные для программной обработки.

```
Веб-скрапинг:  GET /products  →  HTML (для людей)  →  парсим BeautifulSoup
Web API:       GET /api/products  →  JSON (для программ)  →  response.json()
```

### JSON и requests

Вы уже умеете делать HTTP-запросы (семинар 4). Для API добавляется один шаг — парсинг JSON:

```python
import requests

# Запрос к API погоды (open-meteo.com — бесплатно, без ключа)
response = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": 55.7558,
        "longitude": 37.6173,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "Europe/Moscow",
    },
    timeout=10,
)
response.raise_for_status()  # HTTPError для 4xx/5xx

# Парсим JSON → Python dict
data = response.json()

# Структура ответа:
# {
#   "current": {
#     "temperature_2m": 18.5,
#     "wind_speed_10m": 12.3
#   },
#   "current_units": {"temperature_2m": "°C", ...}
# }
temp = data["current"]["temperature_2m"]
unit = data["current_units"]["temperature_2m"]
print(f"Температура: {temp}{unit}")  # Температура: 18.5°C
```

### API-ключи и аутентификация

Многие API требуют ключ для идентификации клиента:

```python
# Вариант 1: ключ в параметрах запроса
response = requests.get(url, params={"api_key": "your_key", ...})

# Вариант 2: ключ в заголовке Authorization
headers = {"Authorization": "Bearer your_token"}
response = requests.get(url, headers=headers)

# Вариант 3: ключ в заголовке X-API-Key
headers = {"X-API-Key": "your_key"}
response = requests.get(url, headers=headers)
```

**Правило:** никогда не храните ключи в коде — используйте переменные окружения:

```python
import os
api_key = os.environ.get("WEATHER_API_KEY", "")
```

### Rate Limiting и пагинация

**Rate limiting** — ограничение частоты запросов. Сервер возвращает `429 Too Many Requests`.

```python
import time

for city in cities:
    response = requests.get(url, params={...}, timeout=10)
    # ...
    time.sleep(0.5)  # пауза 500мс между запросами — хороший тон
```

**Пагинация** — данные разбиты на страницы. Два основных подхода:

```python
# Подход 1: параметр page
for page in range(1, 6):
    response = requests.get(url, params={"page": page, "per_page": 20})
    data = response.json()
    if not data["results"]:  # нет данных — конец
        break

# Подход 2: cursor / next_url
next_url = "https://api.example.com/items"
while next_url:
    response = requests.get(next_url, timeout=10)
    data = response.json()
    process(data["items"])
    next_url = data.get("next")  # None если последняя страница
```

> **Подробнее:** см. файл [`examples/03_web_apis.py`](examples/03_web_apis.py) —
> запросы к open-meteo.com, прогноз на неделю, rate limiting, обработка ошибок API.

### Практика

Перейдите к файлу [`exercises/beautifulsoup_apis_practice.md`](exercises/beautifulsoup_apis_practice.md)
и выполните **Часть 3: Web API** (задания 3.1–3.2).

---

## Блок 4: Практические примеры — агрегация данных (20 мин)

### Hacker News API

Hacker News предоставляет полностью открытый API без ключа:

```python
import time
import requests

HN_BASE = "https://hacker-news.firebaseio.com/v0"

# Список ID топ-новостей (до 500)
resp = requests.get(f"{HN_BASE}/topstories.json", timeout=10)
top_ids = resp.json()[:10]  # берём первые 10

# Данные каждой новости
for story_id in top_ids:
    item = requests.get(f"{HN_BASE}/item/{story_id}.json", timeout=10).json()

    # Обработка отсутствующих полей — реальные данные бывают неполными!
    title = item.get("title", "(без заголовка)")
    score = item.get("score", 0)
    url = item.get("url", "")  # Ask HN не имеют URL

    print(f"[{score}★] {title}")
    time.sleep(0.1)  # вежливая пауза
```

### Агрегация: сбор статистики

```python
from dataclasses import dataclass

@dataclass
class Story:
    title: str
    score: int
    author: str
    comments: int

stories: list[Story] = [...]  # загруженные новости

# Средний рейтинг
avg_score = sum(s.score for s in stories) / len(stories)

# Топ авторов
from collections import Counter
top_authors = Counter(s.author for s in stories).most_common(5)

# Фильтрация по ключевому слову
python_news = [s for s in stories if "python" in s.title.lower()]
```

### Обработка реальных проблем

В реальных данных всегда есть "грязь":

```python
def parse_story(data: dict) -> Story | None:
    # Удалённые/мёртвые записи
    if data.get("deleted") or data.get("dead"):
        return None

    # Неожиданный тип (комментарий вместо новости)
    if data.get("type") != "story":
        return None

    # Отсутствующие поля — используем .get() с дефолтом
    return Story(
        title=data.get("title", "(без заголовка)"),
        score=data.get("score", 0),
        author=data.get("by", "anonymous"),
        comments=data.get("descendants", 0),
    )
```

> **Подробнее:** см. файл [`examples/04_news_and_aggregation.py`](examples/04_news_and_aggregation.py) —
> полный пример: загрузка топ-новостей HN, агрегация, фильтрация, пагинация.

### Практика

Перейдите к файлу [`exercises/beautifulsoup_apis_practice.md`](exercises/beautifulsoup_apis_practice.md)
и выполните **Часть 4: Агрегация данных** (задания 4.1–4.2).

---

## Блок 5: Подведение итогов (10 мин)

### Шпаргалка

| Задача | Инструмент | Пример |
|--------|-----------|--------|
| Создать soup | `BeautifulSoup(html, "lxml")` | — |
| Найти первый тег | `soup.find("div", class_="x")` | → `Tag \| None` |
| Найти все теги | `soup.find_all("li")` | → `list[Tag]` |
| CSS-селектор (один) | `soup.select_one(".price")` | → `Tag \| None` |
| CSS-селектор (все) | `soup.select("ul li a")` | → `list[Tag]` |
| Получить текст | `tag.get_text(strip=True)` | → `str` |
| Получить атрибут | `tag.get("href", "")` | → `str` |
| Все атрибуты | `tag.attrs` | → `dict` |
| Запрос к API | `requests.get(url, params={...})` | — |
| Парсинг JSON | `response.json()` | → `dict \| list` |
| Проверить статус | `response.raise_for_status()` | → `HTTPError` |
| Пауза | `time.sleep(0.5)` | — |

### Ключевые выводы

1. **BeautifulSoup > регулярки для HTML.** Регулярки хрупкие — они ломаются при малейшем
   изменении разметки. BeautifulSoup понимает структуру дерева и устойчив к вариациям HTML.

2. **API > скрапинг, когда есть выбор.** API возвращает чистые структурированные данные,
   не ломается при редизайне сайта и обычно имеет стабильный контракт.

3. **Реальные данные грязные.** Всегда используйте `.get()` с дефолтом, проверяйте
   `deleted`/`dead` поля, обрабатывайте исключения — сеть ненадёжна.

---

## Файлы семинара

```
seminar_15_beautifulsoup_apis/
├── README.md                          # Этот файл
├── examples/
│   ├── 01_beautifulsoup_basics.py     # Парсинг HTML: find, find_all, CSS-селекторы, атрибуты
│   ├── 02_web_scraping.py             # Скрапинг quotes.toscrape.com: пагинация, анализ
│   ├── 03_web_apis.py                 # Web API: open-meteo.com, JSON, rate limiting
│   └── 04_news_and_aggregation.py     # Hacker News API: агрегация, фильтрация, пагинация
└── exercises/
    └── beautifulsoup_apis_practice.md # Задания (4 части + Chat Polls + 2 бонуса)
```

---

## Дополнительные материалы

- [BeautifulSoup документация](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) — официальная документация с примерами
- [open-meteo.com](https://open-meteo.com/en/docs) — бесплатный API погоды, документация параметров
- [Hacker News API](https://github.com/HackerNews/API) — документация Firebase API
- [Real Python — Web Scraping with BeautifulSoup](https://realpython.com/beautiful-soup-web-scraper-python/) — подробное руководство
- [MDN — CSS Selectors](https://developer.mozilla.org/ru/docs/Web/CSS/CSS_selectors) — справочник по CSS-селекторам
