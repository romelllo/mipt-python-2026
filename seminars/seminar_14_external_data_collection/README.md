# Семинар 14: Сбор данных со сторонних сайтов

**Модуль:** 4 — Анализ данных в Python  
**Дата:** 04.05.2026  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/10owuXUcUqvLdagmFSxVLLvMJtAaq7ds54eOm3G5Snfg/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:
- Загружать HTML-страницы и данные из API с помощью `requests`
- Понимать структуру HTML-документа (DOM) и принципы поиска элементов
- Описывать структуру регулярного выражения: символьные классы, квантификаторы, группы
- Использовать все основные функции модуля `re`: `search`, `findall`, `sub`, `split`
- Извлекать структурированные данные (email, телефоны, имена, даты) из HTML и текста
- Сохранять собранные данные в файлы (HTML, CSV)

---

## Подготовка

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# Установите зависимости
uv add requests

# Проверьте установку
python -c "import requests, re; print('OK')"
```

---

## План семинара

| Время | Тема | Практика |
|-------|------|----------|
| 5 мин | Введение: что такое веб-скрапинг | — |
| 20 мин | Блок 1: HTTP-запросы для сбора данных | → Упражнения: Часть 1 |
| 15 мин | Блок 2: HTML и DOM — структура страницы | → Упражнения: Часть 2 |
| 25 мин | Блок 3: Регулярные выражения — синтаксис | → Упражнения: Часть 3 |
| 20 мин | Блок 4: Извлечение данных — практика | → Упражнения: Часть 4 |
| 5 мин | Подведение итогов | — |

**Итого:** ~90 минут

---

## Блок 1: HTTP-запросы для сбора данных (20 мин)

### Напоминание из семинара 4

В [семинаре 4](../seminar_04_web_fundamentals/README.md) мы изучили:
- структуру HTTP-запроса и ответа
- методы GET, POST и коды статусов
- библиотеку `requests`: `get()`, `post()`, заголовки, `raise_for_status()`

Здесь мы применяем эти знания к задаче **сбора данных** — загружаем HTML-страницы
и ответы API для дальнейшей обработки.

### Ключевые практики для скрапинга

**1. Установите User-Agent** — некоторые серверы отклоняют запросы без него:

```python
headers = {"User-Agent": "Mozilla/5.0 (compatible; MyBot/1.0)"}
response = requests.get(url, headers=headers, timeout=10)
```

**2. Всегда используйте timeout** — без него запрос может зависнуть навсегда:

```python
response = requests.get(url, timeout=10)         # 10 секунд
response = requests.get(url, timeout=(3, 10))    # (connect, read)
```

**3. Обрабатывайте ошибки** — сеть ненадёжна:

```python
from requests.exceptions import RequestException, HTTPError, Timeout

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # HTTPError для 4xx/5xx
    return response.text
except Timeout:
    print("Превышен таймаут")
except HTTPError as e:
    print(f"HTTP {e.response.status_code}")
except RequestException as e:
    print(f"Ошибка сети: {e}")
```

**4. Соблюдайте этику** — проверяйте `robots.txt` и делайте паузы между запросами:

```python
import time

# robots.txt — правила обхода сайта для ботов
# https://site.com/robots.txt

time.sleep(1)  # пауза 1 секунда между запросами
```

### Сохранение результата

```python
from pathlib import Path

html = response.text
Path("data/page.html").write_text(html, encoding="utf-8")

# JSON — через стандартный модуль
import json
data = response.json()
Path("data/result.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
```

> **Подробнее:** см. файл [`examples/01_http_requests.py`](examples/01_http_requests.py) —
> функции загрузки с retry-логикой, проверка robots.txt, сохранение на диск.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните
**Часть 1: HTTP-запросы для сбора данных** (задания 1.1–1.2).

---

## Блок 2: HTML и DOM (15 мин)

### Структура HTML-документа

HTML-страница — это дерево вложенных тегов (**DOM**, Document Object Model):

```
<html>
 └── <head>
 │    └── <title>Заголовок</title>
 └── <body>
      ├── <h1>Главный заголовок</h1>
      ├── <article class="post" id="post-1">
      │    ├── <h2><a href="/url">Заголовок статьи</a></h2>
      │    ├── <p class="author">Автор: Иван</p>
      │    └── <p class="body">Текст...</p>
      └── <footer>...</footer>
```

Тег имеет:
- **имя**: `div`, `p`, `a`, `span`, ...
- **атрибуты**: `class="post"`, `id="post-1"`, `href="/url"`
- **содержимое**: текст или вложенные теги

### CSS-селекторы (концепция)

CSS-селекторы — язык для выборки элементов. В следующем семинаре
(BeautifulSoup) они заработают напрямую. Сейчас запомним нотацию:

| Селектор | Что выбирает | Пример |
|----------|-------------|--------|
| `tag` | все теги | `p`, `h2` |
| `.class` | элементы с классом | `.post-title` |
| `#id` | элемент с id | `#article-1` |
| `tag.class` | тег с классом | `span.author` |
| `[attr=val]` | атрибут равен значению | `a[href="/page"]` |
| `parent > child` | прямой потомок | `article > h2` |

### XPath (концепция)

XPath — альтернативный язык запросов, мощнее CSS:

```
//article               — все теги <article> в документе
//span[@class="author"] — все <span> с class="author"
//h2/a/text()           — текст ссылок внутри h2
```

### Поиск через регулярные выражения

Пока мы работаем с HTML как с текстом:

```python
import re

# Извлечь текст из всех тегов <h2>
titles = re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.DOTALL)

# Извлечь все href из тегов <a>
hrefs = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\']', html)

# Убрать все теги (получить чистый текст)
text = re.sub(r"<[^>]+>", " ", html)
```

> **Подробнее:** см. файл [`examples/02_html_structure.py`](examples/02_html_structure.py) —
> функции для извлечения тегов, ссылок и атрибутов из HTML.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните
**Часть 2: HTML и DOM** (задание 2.1).

---

## Блок 3: Регулярные выражения (25 мин)

### Синтаксис: метасимволы

```
.        — любой символ (кроме \n)
^        — начало строки
$        — конец строки
\        — экранирование: \. \* \?
```

### Символьные классы

```
\d       — цифра              [0-9]
\D       — не цифра
\w       — буква/цифра/_      [a-zA-Z0-9_]
\W       — не \w
\s       — пробельный символ
\S       — не пробельный
[abc]    — один из: a, b, c
[a-z]    — диапазон: строчные латинские
[А-Яа-я] — диапазон: русские буквы
[^abc]   — любой, КРОМЕ a, b, c
```

### Квантификаторы

```
*        — 0 или более (жадный)
+        — 1 или более (жадный)
?        — 0 или 1
{n}      — ровно n
{n,m}    — от n до m
*?  +?   — ленивые версии (как можно меньше)
```

**Жадность vs. ленивость:**

```python
html = "<b>первый</b> и <b>второй</b>"
re.findall(r"<b>.*</b>",   html)   # ['<b>первый</b> и <b>второй</b>']  — жадный
re.findall(r"<b>.*?</b>",  html)   # ['<b>первый</b>', '<b>второй</b>']  — ленивый
```

### Группы захвата

```python
# (pattern) — захватывает совпадение
match = re.search(r"(\d{4})-(\d{2})-(\d{2})", "Дата: 2026-04-28")
match.group(0)  # '2026-04-28'  — полное совпадение
match.group(1)  # '2026'        — первая группа (год)
match.group(2)  # '04'          — вторая группа (месяц)

# Именованные группы (?P<name>...)
match = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", s)
match.group("year")   # '2026'
match.group("month")  # '04'
```

### Основные функции модуля `re`

| Функция | Что делает | Возвращает |
|---------|-----------|-----------|
| `re.search(p, s)` | первое совпадение | `Match` или `None` |
| `re.match(p, s)` | совпадение с начала строки | `Match` или `None` |
| `re.findall(p, s)` | все совпадения | `list[str]` |
| `re.finditer(p, s)` | все совпадения с позициями | итератор `Match` |
| `re.sub(p, repl, s)` | замена совпадений | новая строка |
| `re.split(p, s)` | разбить по паттерну | `list[str]` |
| `re.compile(p)` | скомпилировать паттерн | `Pattern` |

### Флаги

```python
re.IGNORECASE   # re.I — регистронезависимый поиск
re.MULTILINE    # re.M — ^ и $ для каждой строки
re.DOTALL       # re.S — точка совпадает с \n
# комбинируются через |
re.findall(r"pattern", text, re.I | re.M)
```

> **Подробнее:** см. файл [`examples/03_regex_basics.py`](examples/03_regex_basics.py) —
> все синтаксические конструкции с примерами и комментариями.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните
**Часть 3: Регулярные выражения** (задания 3.1–3.2).

---

## Блок 4: Извлечение данных — практика (20 мин)

### Паттерны для типовых задач

**Email-адрес:**
```python
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
```

**Российский телефон** (форматы: `+7 (495) 123-45-67`, `8-916-222-33-44`):
```python
PHONE_RE = re.compile(
    r"(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]\d{2}[\s\-]\d{2}"
)
```

**Дата в формате `YYYY-MM-DD`:**
```python
DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
```

### Извлечение данных из HTML-тегов

Типичный шаблон — выделить блок по тегу, потом извлечь поля:

```python
# Шаг 1: Разбить на блоки-статьи
article_blocks = re.findall(
    r'<article\s+id="([^"]+)"[^>]*>(.*?)</article>',
    html, re.DOTALL
)

# Шаг 2: Для каждого блока извлечь нужное поле
for article_id, block in article_blocks:
    author_match = re.search(
        r'<span\s+class="author">Автор:\s*([^<]+)</span>', block
    )
    author = author_match.group(1).strip() if author_match else ""
```

### Очистка текста

```python
# Удалить все HTML-теги
clean_text = re.sub(r"<[^>]+>", " ", html)
# Нормализовать пробелы
clean_text = re.sub(r"\s+", " ", clean_text).strip()
```

> **Подробнее:** см. файл [`examples/04_regex_applied.py`](examples/04_regex_applied.py) —
> полный разбор паттернов для email, телефонов, авторов и дат на реальном HTML.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните
**Часть 4: Применение регулярных выражений** (задания 4.1–4.2).

---

## Подведение итогов

### Шпаргалка

| Задача | Инструмент |
|--------|-----------|
| Загрузить HTML | `requests.get(url, timeout=10).text` |
| Обработать ошибку | `raise_for_status()` + `except RequestException` |
| Найти первое совпадение | `re.search(pattern, text)` |
| Найти все совпадения | `re.findall(pattern, text)` |
| Заменить текст | `re.sub(pattern, replacement, text)` |
| Извлечь атрибут | `re.findall(r'attr=["\']([^"\']+)["\']', html)` |
| Убрать HTML-теги | `re.sub(r"<[^>]+>", " ", html)` |
| Лениво захватить | `.*?` вместо `.*` |
| Извлечь группы | `re.search(...).group(1)` |

---

## Файлы семинара

```
seminar_14_external_data_collection/
├── README.md                      # Этот файл
├── data/
│   └── sample_page.html           # Тестовая новостная страница TechNews
├── examples/
│   ├── 01_http_requests.py        # HTTP-запросы: загрузка, ошибки, retry, сохранение
│   ├── 02_html_structure.py       # Структура HTML, извлечение тегов/ссылок через re
│   ├── 03_regex_basics.py         # Синтаксис regex: классы, квантификаторы, группы, флаги
│   └── 04_regex_applied.py        # Практика: email, телефоны, авторы, даты, очистка текста
└── exercises/
    └── exercises.md               # Практические задания (4 части + 2 бонусных)
```

---

## Дополнительные материалы

- [Python `re` — официальная документация](https://docs.python.org/3/library/re.html)
- [regex101.com](https://regex101.com/) — интерактивный отладчик регулярных выражений (выберите Python)
- [requests — официальная документация](https://docs.python-requests.org/)
- [MDN — Введение в HTML](https://developer.mozilla.org/ru/docs/Learn/HTML/Introduction_to_HTML)
- [Real Python — Regular Expressions](https://realpython.com/regex-python/)
