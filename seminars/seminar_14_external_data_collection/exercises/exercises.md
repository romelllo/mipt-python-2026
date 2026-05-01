# Практические задания: Сбор данных со сторонних сайтов

## Подготовка

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate  # Linux/Mac

# Установите зависимости
uv add requests

# Проверьте установку
python -c "import requests, re; print('OK')"

# Перейдите в папку семинара
cd seminars/seminar_14_external_data_collection
```

> **Как работать с заданиями:** прочитайте условие, попробуйте написать
> решение самостоятельно и только после этого раскройте подсказку или решение.
> Задания внутри каждой части идут от простых к сложным.

---

## Часть 1: HTTP-запросы для сбора данных

> **Теория:** [README.md — Блок 1](../README.md#блок-1-http-запросы-для-сбора-данных-20-мин) |
> **Примеры:** [`examples/01_http_requests.py`](../examples/01_http_requests.py)
>
> В семинаре 4 мы изучили основы HTTP и библиотеку `requests`.
> Здесь применяем эти знания для скрапинга: загружаем страницы,
> обрабатываем ошибки и сохраняем результаты.

### Задание 1.1 — Загрузка данных из API

Сервис `https://jsonplaceholder.typicode.com` предоставляет тестовый REST API.

Напишите функцию `get_users()`, которая:
1. Делает GET-запрос к `https://jsonplaceholder.typicode.com/users`
2. Возвращает список словарей `{"name": ..., "email": ..., "city": ...}`,
   извлекая `name`, `email` и вложенное поле `address.city` для каждого пользователя
3. Обрабатывает возможные ошибки (сеть, HTTP-статус): при ошибке возвращает пустой список

Проверьте: вызов `get_users()` должен вернуть список из 10 элементов.

<details>
<summary>Подсказка</summary>

Используйте `requests.get(..., timeout=10)` и `response.raise_for_status()`.
Данные API — это список объектов; каждый объект имеет ключ `address`, внутри которого `city`.
Оберните всё в `try/except RequestException`.

</details>

<details>
<summary>Решение</summary>

```python
import requests
from requests.exceptions import RequestException


def get_users() -> list[dict]:
    """Загружает список пользователей из JSONPlaceholder API."""
    try:
        response = requests.get(
            "https://jsonplaceholder.typicode.com/users",
            timeout=10,
        )
        response.raise_for_status()
        users = response.json()
        return [
            {
                "name": user["name"],
                "email": user["email"],
                "city": user["address"]["city"],
            }
            for user in users
        ]
    except RequestException as e:
        print(f"[ОШИБКА] {e}")
        return []


if __name__ == "__main__":
    users = get_users()
    print(f"Получено пользователей: {len(users)}")
    for user in users[:3]:
        print(f"  {user['name']:25s} | {user['email']:30s} | {user['city']}")
```

</details>

---

### Задание 1.2 — Загрузка HTML-страницы с сохранением

Напишите скрипт, который:
1. Загружает HTML-страницу по URL `https://httpbin.org/html`
2. Устанавливает заголовок `User-Agent: MIPT-Python-Seminar/1.0`
3. Выводит первые 5 строк полученного HTML
4. Сохраняет полный HTML в файл `data/httpbin_page.html`
5. При любой ошибке выводит сообщение и завершает работу без исключения

<details>
<summary>Подсказка</summary>

Используйте `response.text` для получения HTML как строки.
Для сохранения — `Path(...).write_text(html, encoding="utf-8")`.
Посмотрите на функцию `fetch_page` и `save_html` в `examples/01_http_requests.py`.

</details>

<details>
<summary>Решение</summary>

```python
from pathlib import Path

import requests
from requests.exceptions import RequestException


def fetch_and_save(url: str, save_path: Path) -> None:
    """Загружает HTML и сохраняет в файл."""
    headers = {"User-Agent": "MIPT-Python-Seminar/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text

        # Первые 5 строк
        print("=== Первые 5 строк HTML ===")
        for line in html.splitlines()[:5]:
            print(line)

        # Сохранение
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(html, encoding="utf-8")
        print(f"\n[СОХРАНЕНО] {save_path} ({len(html)} символов)")

    except RequestException as e:
        print(f"[ОШИБКА] {e}")


if __name__ == "__main__":
    fetch_and_save(
        url="https://httpbin.org/html",
        save_path=Path("data/httpbin_page.html"),
    )
```

</details>

---

## Часть 2: HTML и DOM — поиск элементов через регулярные выражения

> **Теория:** [README.md — Блок 2](../README.md#блок-2-html-и-dom-15-мин) |
> **Примеры:** [`examples/02_html_structure.py`](../examples/02_html_structure.py)

### Задание 2.1 — Извлечение ссылок из HTML

Загрузите файл `data/sample_page.html` и с помощью регулярного выражения извлеките
**все внешние ссылки** — те, у которых `href` начинается с `https://`.

Выведите результат в формате:
```
Внешние ссылки:
  https://github.com/technews    — GitHub
  https://t.me/technews_ru       — Telegram
```

<details>
<summary>Подсказка</summary>

Используйте паттерн `<a\s+[^>]*href=["'](https://[^"']+)["'][^>]*>(.*?)</a>` с флагом `re.DOTALL`.
Чтобы убрать вложенные теги из текста ссылки, примените `re.sub(r"<[^>]+>", "", text)`.

</details>

<details>
<summary>Решение</summary>

```python
import re
from pathlib import Path


def extract_external_links(html: str) -> list[dict[str, str]]:
    """Извлекает ссылки с href, начинающимся на https://."""
    pattern = r'<a\s+[^>]*href=["\']( https://[^"\']+)["\'][^>]*>(.*?)</a>'
    # Упрощённый вариант: ищем href="https://..."
    pattern = r'href=["\'](https://[^"\']+)["\'][^>]*>(.*?)</a>'
    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
    result = []
    for href, raw_text in matches:
        text = re.sub(r"<[^>]+>", "", raw_text).strip()
        result.append({"href": href, "text": text})
    return result


if __name__ == "__main__":
    html = Path("data/sample_page.html").read_text(encoding="utf-8")
    links = extract_external_links(html)
    print("Внешние ссылки:")
    for link in links:
        print(f"  {link['href']:40s} — {link['text']}")
```

</details>

---

## Часть 3: Регулярные выражения — синтаксис

> **Теория:** [README.md — Блок 3](../README.md#блок-3-регулярные-выражения-25-мин) |
> **Примеры:** [`examples/03_regex_basics.py`](../examples/03_regex_basics.py)

### Задание 3.1 — Валидация и нормализация дат

Дан список строк. Для каждой строки:
1. Определите, содержит ли она дату в формате `YYYY-MM-DD`
2. Если содержит — выведите дату в российском формате `DD.MM.YYYY`
3. Если не содержит — выведите `"дата не найдена"`

```python
test_strings = [
    "Опубликовано: 2026-04-28",
    "Версия 3.12 вышла 2023-10-02",
    "Нет даты в этой строке",
    "Два события: 2025-01-15 и 2025-06-30",
    "Некорректно: 26-4-5",
]
```

<details>
<summary>Подсказка</summary>

Используйте `re.search(r"(\d{4})-(\d{2})-(\d{2})", s)` для поиска.
Группы захвата `(\d{4})`, `(\d{2})`, `(\d{2})` дают год, месяц, день.
Для строк с несколькими датами используйте `re.findall`.

</details>

<details>
<summary>Решение</summary>

```python
import re

test_strings = [
    "Опубликовано: 2026-04-28",
    "Версия 3.12 вышла 2023-10-02",
    "Нет даты в этой строке",
    "Два события: 2025-01-15 и 2025-06-30",
    "Некорректно: 26-4-5",
]

DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")

for s in test_strings:
    matches = DATE_RE.findall(s)
    if matches:
        dates_ru = [f"{day}.{month}.{year}" for year, month, day in matches]
        print(f"  {s!r:45s} -> {', '.join(dates_ru)}")
    else:
        print(f"  {s!r:45s} -> дата не найдена")
```

</details>

---

### Задание 3.2 — Замена и очистка текста

Дан текст с артикулами товаров в формате `SKU-XXXXX` (5 цифр).
Напишите функцию `anonymize_skus(text: str) -> str`, которая заменяет
все артикулы на строку `SKU-XXXXX` (маскировка для публикации).

Дополнительно: посчитайте, сколько уникальных артикулов было заменено.

```python
catalog_text = """
Товар SKU-10234 — ноутбук, SKU-99871 — мышь, SKU-10234 — снова ноутбук.
Новинка: SKU-55500. Уценка: SKU-00001 и SKU-10234.
"""
```

Ожидаемый результат: все `SKU-NNNNN` заменены, 4 уникальных артикула найдено.

<details>
<summary>Подсказка</summary>

Используйте `re.findall(r"SKU-\d{5}", text)` для подсчёта уникальных.
Для замены — `re.sub(r"SKU-\d{5}", "SKU-XXXXX", text)`.

</details>

<details>
<summary>Решение</summary>

```python
import re

catalog_text = """
Товар SKU-10234 — ноутбук, SKU-99871 — мышь, SKU-10234 — снова ноутбук.
Новинка: SKU-55500. Уценка: SKU-00001 и SKU-10234.
"""

SKU_RE = re.compile(r"SKU-\d{5}")


def anonymize_skus(text: str) -> str:
    """Заменяет все артикулы SKU на маску SKU-XXXXX."""
    found = SKU_RE.findall(text)
    unique_count = len(set(found))
    print(f"Уникальных артикулов: {unique_count}")
    return SKU_RE.sub("SKU-XXXXX", text)


result = anonymize_skus(catalog_text)
print(result)
```

</details>

---

## Часть 4: Применение регулярных выражений к реальным данным

> **Теория:** [README.md — Блок 4](../README.md#блок-4-извлечение-данных-практика-20-мин) |
> **Примеры:** [`examples/04_regex_applied.py`](../examples/04_regex_applied.py)

### Задание 4.1 — Извлечение контактных данных

Загрузите `data/sample_page.html` и извлеките **все** email-адреса и телефоны.
Выведите результат в виде сводной таблицы:

```
Контактные данные на странице:
  Emails (7):
    ads@technews.ru
    a.novikov@technews.ru
    ...
  Телефоны (5):
    +7 (495) 123-45-67
    ...
```

Используйте паттерны из `examples/04_regex_applied.py`.

<details>
<summary>Подсказка</summary>

Для email используйте паттерн `[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}`.
Для телефонов — `(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]\d{2}[\s\-]\d{2}`.
Убирайте дубли через `set()`.

</details>

<details>
<summary>Решение</summary>

```python
import re
from pathlib import Path

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(
    r"(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]\d{2}[\s\-]\d{2}"
)

html = Path("data/sample_page.html").read_text(encoding="utf-8")

emails = sorted(set(e.lower() for e in EMAIL_RE.findall(html)))
phones = list(dict.fromkeys(PHONE_RE.findall(html)))  # уникальные, порядок сохранён

print("Контактные данные на странице:")
print(f"  Emails ({len(emails)}):")
for email in emails:
    print(f"    {email}")
print(f"  Телефоны ({len(phones)}):")
for phone in phones:
    print(f"    {phone}")
```

</details>

---

### Задание 4.2 — Сбор метаданных статей в CSV

Напишите скрипт, который:
1. Загружает `data/sample_page.html`
2. Извлекает метаданные каждой статьи: `id`, `title`, `author`, `date`, `comments`
3. Сохраняет результат в файл `data/articles.csv`

Формат CSV (разделитель `;`):
```
id;title;author;date;comments
article-1;Python остаётся лидером...;Иван Петров;2026-04-28;42
...
```

<details>
<summary>Подсказка</summary>

Разбейте HTML на блоки `<article>...</article>` с помощью `re.findall`.
Для каждого блока применяйте `re.search` для извлечения каждого поля.
Для записи CSV используйте стандартный модуль `csv` или просто запись строк с `join`.

</details>

<details>
<summary>Решение</summary>

```python
import csv
import re
from pathlib import Path


def extract_articles(html: str) -> list[dict[str, str]]:
    """Извлекает метаданные всех статей из HTML."""
    blocks = re.findall(
        r'<article\s+id="([^"]+)"[^>]*>(.*?)</article>',
        html, re.DOTALL | re.IGNORECASE,
    )
    articles = []
    for article_id, block in blocks:
        title_m = re.search(r'<h2[^>]*>.*?<a[^>]*>(.*?)</a>', block, re.DOTALL)
        author_m = re.search(r'<span\s+class="author">Автор:\s*([^<]+)</span>', block)
        date_m = re.search(r'<span\s+class="date">Дата:\s*(\d{4}-\d{2}-\d{2})</span>', block)
        comments_m = re.search(r"Комментарии:\s*(\d+)", block)

        articles.append({
            "id": article_id,
            "title": re.sub(r"<[^>]+>", "", title_m.group(1)).strip() if title_m else "",
            "author": author_m.group(1).strip() if author_m else "",
            "date": date_m.group(1) if date_m else "",
            "comments": comments_m.group(1) if comments_m else "0",
        })
    return articles


if __name__ == "__main__":
    html = Path("data/sample_page.html").read_text(encoding="utf-8")
    articles = extract_articles(html)

    output_path = Path("data/articles.csv")
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "author", "date", "comments"],
                                delimiter=";")
        writer.writeheader()
        writer.writerows(articles)

    print(f"Сохранено {len(articles)} статей в {output_path}")
    for a in articles:
        print(f"  {a['id']:12s} | {a['author']:20s} | {a['date']} | {a['comments']} коммент.")
```

</details>

---

## Бонусные задания

### Бонус 1 — Анализ структуры страницы

Напишите функцию `page_stats(html: str) -> dict`, которая возвращает статистику
HTML-страницы:
- `tags` — словарь `{тег: количество}` для всех тегов (`<p>`, `<a>`, `<div>`, ...)
- `internal_links` — количество внутренних ссылок (href начинается с `/`)
- `external_links` — количество внешних ссылок (href начинается с `http`)
- `images` — количество тегов `<img>`
- `words` — примерное количество слов в тексте страницы (после удаления тегов)

<details>
<summary>Подсказка</summary>

Для подсчёта тегов: `re.findall(r"<(\w+)", html)` — находит имена открывающих тегов.
Используйте `collections.Counter` для подсчёта.
Для слов — удалите теги и разбейте по пробелам.

</details>

<details>
<summary>Решение</summary>

```python
import re
from collections import Counter
from pathlib import Path


def page_stats(html: str) -> dict:
    """Возвращает статистику HTML-страницы."""
    # Все теги
    all_tags = re.findall(r"<(\w+)", html, re.IGNORECASE)
    tag_counts = dict(Counter(t.lower() for t in all_tags))

    # Ссылки
    all_hrefs = re.findall(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE)
    internal = sum(1 for h in all_hrefs if h.startswith("/"))
    external = sum(1 for h in all_hrefs if h.startswith("http"))

    # Изображения
    images = len(re.findall(r"<img\b", html, re.IGNORECASE))

    # Слова в тексте
    clean = re.sub(r"<[^>]+>", " ", html)
    clean = re.sub(r"\s+", " ", clean).strip()
    words = len([w for w in clean.split() if re.search(r"\w", w)])

    return {
        "tags": tag_counts,
        "internal_links": internal,
        "external_links": external,
        "images": images,
        "words": words,
    }


if __name__ == "__main__":
    html = Path("data/sample_page.html").read_text(encoding="utf-8")
    stats = page_stats(html)
    print(f"Внутренних ссылок: {stats['internal_links']}")
    print(f"Внешних ссылок:    {stats['external_links']}")
    print(f"Изображений:       {stats['images']}")
    print(f"Слов в тексте:     {stats['words']}")
    print("Топ-10 тегов:")
    top_tags = sorted(stats["tags"].items(), key=lambda x: x[1], reverse=True)[:10]
    for tag, count in top_tags:
        print(f"  <{tag}>: {count}")
```

</details>

---

### Бонус 2 — Скрапинг реального API с пагинацией

Сервис `https://jsonplaceholder.typicode.com/posts` возвращает 100 постов.
Напишите функцию `scrape_posts_by_user(user_id: int) -> list[dict]`, которая:
1. Загружает все посты для конкретного пользователя (параметр `userId`)
2. Для каждого поста загружает его комментарии (`/posts/{id}/comments`)
3. Возвращает список словарей `{"title": ..., "body": ..., "comments_count": ...}`
4. Добавляет паузу 0.5 секунды между запросами (rate limiting)

<details>
<summary>Подсказка</summary>

Используйте параметр `params={"userId": user_id}` в первом запросе.
Для каждого поста делайте отдельный запрос к `/posts/{post_id}/comments`.
`time.sleep(0.5)` — пауза между запросами.

</details>

<details>
<summary>Решение</summary>

```python
import time

import requests
from requests.exceptions import RequestException


BASE_URL = "https://jsonplaceholder.typicode.com"


def fetch_json(url: str, params: dict | None = None) -> list | dict | None:
    """Загружает JSON по URL."""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"[ОШИБКА] {e}")
        return None


def scrape_posts_by_user(user_id: int) -> list[dict]:
    """Загружает посты пользователя с количеством комментариев."""
    posts = fetch_json(f"{BASE_URL}/posts", params={"userId": user_id})
    if not posts:
        return []

    result = []
    for post in posts:
        time.sleep(0.5)  # уважаем сервер
        comments = fetch_json(f"{BASE_URL}/posts/{post['id']}/comments")
        result.append({
            "title": post["title"],
            "body": post["body"][:80] + "...",
            "comments_count": len(comments) if comments else 0,
        })

    return result


if __name__ == "__main__":
    posts = scrape_posts_by_user(user_id=1)
    print(f"Постов пользователя 1: {len(posts)}")
    for p in posts:
        print(f"  [{p['comments_count']} коммент.] {p['title'][:50]}")
```

</details>
