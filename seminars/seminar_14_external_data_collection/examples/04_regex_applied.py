"""
Блок 4: Практическое применение регулярных выражений.

Реальные задачи веб-скрапинга: извлечение структурированных данных
из HTML-страниц — emails, телефонов, имён авторов, дат, заголовков.
"""

import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Загрузка тестовой страницы
# ---------------------------------------------------------------------------

def load_sample_page() -> str:
    """Загружает sample_page.html из папки data/."""
    data_dir = Path(__file__).parent.parent / "data"
    return (data_dir / "sample_page.html").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Извлечение email-адресов
# ---------------------------------------------------------------------------

# Паттерн email:
#   [a-zA-Z0-9._%+\-]+   — локальная часть (до @): буквы, цифры, . _ % + -
#   @                     — символ @
#   [a-zA-Z0-9.\-]+       — домен: буквы, цифры, точка, тире
#   \.                    — обязательная точка перед зоной
#   [a-zA-Z]{2,}          — доменная зона: минимум 2 буквы (ru, com, org, ...)

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")


def extract_emails(text: str) -> list[str]:
    """Извлекает все email-адреса из текста.

    Args:
        text: произвольный текст или HTML

    Returns:
        Список уникальных email-адресов (в нижнем регистре)
    """
    found = EMAIL_RE.findall(text)
    # Убираем дубли, приводим к нижнему регистру
    return sorted(set(email.lower() for email in found))


# ---------------------------------------------------------------------------
# 2. Извлечение телефонных номеров
# ---------------------------------------------------------------------------

# Российские номера встречаются в разных форматах:
#   +7 (495) 123-45-67
#   +7-495-987-65-43
#   8-916-222-33-44
#   +7 (812) 555-00-11
#
# Паттерн разбирается поэтапно:
#   (?:\+7|8)             — страновой код: +7 или 8
#   [\s\-]?               — необязательный разделитель
#   \(?                   — необязательная открывающая скобка
#   \d{3}                 — код города/оператора (3 цифры)
#   \)?                   — необязательная закрывающая скобка
#   [\s\-]?               — разделитель
#   \d{3}                 — первые 3 цифры номера
#   [\s\-]                — разделитель
#   \d{2}                 — следующие 2 цифры
#   [\s\-]                — разделитель
#   \d{2}                 — последние 2 цифры

PHONE_RE = re.compile(
    r"(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]\d{2}[\s\-]\d{2}"
)


def extract_phones(text: str) -> list[str]:
    """Извлекает телефонные номера в российском формате.

    Args:
        text: произвольный текст или HTML

    Returns:
        Список найденных номеров
    """
    return PHONE_RE.findall(text)


# ---------------------------------------------------------------------------
# 3. Извлечение имён авторов
# ---------------------------------------------------------------------------

# На нашей тестовой странице авторы обёрнуты в:
#   <span class="author">Автор: Имя Фамилия</span>
#
# Стратегия:
#   1. Найти тег с классом "author"
#   2. Извлечь текст из него
#   3. Убрать префикс "Автор: "

AUTHOR_TAG_RE = re.compile(
    r'<span\s+class="author">Автор:\s*([^<]+)</span>',
    re.IGNORECASE,
)


def extract_authors(html: str) -> list[str]:
    """Извлекает имена авторов из HTML-разметки страницы.

    Args:
        html: HTML-текст страницы

    Returns:
        Список имён авторов
    """
    return AUTHOR_TAG_RE.findall(html)


# ---------------------------------------------------------------------------
# 4. Извлечение дат публикаций
# ---------------------------------------------------------------------------

# Даты на странице в формате YYYY-MM-DD внутри тега:
#   <span class="date">Дата: 2026-04-28</span>

DATE_TAG_RE = re.compile(
    r'<span\s+class="date">Дата:\s*(\d{4}-\d{2}-\d{2})</span>',
    re.IGNORECASE,
)

# Паттерн для поиска любой даты формата YYYY-MM-DD в произвольном тексте
DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")


def extract_dates(html: str) -> list[str]:
    """Извлекает даты публикаций из HTML.

    Args:
        html: HTML-текст страницы

    Returns:
        Список дат в формате YYYY-MM-DD
    """
    return DATE_TAG_RE.findall(html)


# ---------------------------------------------------------------------------
# 5. Комплексная функция: сбор метаданных всех статей
# ---------------------------------------------------------------------------

def extract_articles(html: str) -> list[dict[str, str]]:
    """Извлекает метаданные всех статей со страницы.

    Для каждой статьи собирает:
    - id статьи
    - заголовок
    - автора
    - дату
    - количество комментариев

    Args:
        html: HTML-текст страницы

    Returns:
        Список словарей с данными статей
    """
    # Разбиваем HTML на блоки <article>...</article>
    article_blocks = re.findall(
        r'<article\s+id="([^"]+)"[^>]*>(.*?)</article>',
        html,
        re.DOTALL | re.IGNORECASE,
    )

    articles = []
    for article_id, block in article_blocks:
        # Заголовок — текст внутри <h2 class="post-title"><a ...>TEXT</a></h2>
        title_match = re.search(
            r'<h2[^>]*>.*?<a[^>]*>(.*?)</a>.*?</h2>',
            block, re.DOTALL | re.IGNORECASE,
        )
        title = title_match.group(1).strip() if title_match else ""

        # Автор
        author_match = re.search(
            r'<span\s+class="author">Автор:\s*([^<]+)</span>',
            block, re.IGNORECASE,
        )
        author = author_match.group(1).strip() if author_match else ""

        # Дата
        date_match = re.search(
            r'<span\s+class="date">Дата:\s*(\d{4}-\d{2}-\d{2})</span>',
            block, re.IGNORECASE,
        )
        date = date_match.group(1) if date_match else ""

        # Количество комментариев
        comments_match = re.search(r"Комментарии:\s*(\d+)", block)
        comments = comments_match.group(1) if comments_match else "0"

        articles.append({
            "id": article_id,
            "title": title,
            "author": author,
            "date": date,
            "comments": comments,
        })

    return articles


# ---------------------------------------------------------------------------
# 6. Очистка текста — удаление HTML-тегов и нормализация пробелов
# ---------------------------------------------------------------------------

def strip_html(html: str) -> str:
    """Удаляет все HTML-теги и нормализует пробелы.

    Args:
        html: текст с HTML-разметкой

    Returns:
        Чистый текст
    """
    # Убираем все теги вида <...>
    text = re.sub(r"<[^>]+>", " ", html)
    # Заменяем множественные пробелы/переносы строк одним пробелом
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Демонстрация
# ---------------------------------------------------------------------------

def main() -> None:
    """Запускает все примеры на реальном HTML-файле."""
    html = load_sample_page()
    print(f"Загружена страница: {len(html)} символов\n")

    print("=" * 60)
    print("1. Email-адреса")
    print("=" * 60)
    emails = extract_emails(html)
    for email in emails:
        print(f"  {email}")

    print()
    print("=" * 60)
    print("2. Телефонные номера")
    print("=" * 60)
    phones = extract_phones(html)
    for phone in phones:
        print(f"  {phone}")

    print()
    print("=" * 60)
    print("3. Авторы статей")
    print("=" * 60)
    authors = extract_authors(html)
    for author in authors:
        print(f"  {author}")

    print()
    print("=" * 60)
    print("4. Даты публикаций")
    print("=" * 60)
    dates = extract_dates(html)
    for date in dates:
        print(f"  {date}")

    print()
    print("=" * 60)
    print("5. Метаданные всех статей")
    print("=" * 60)
    articles = extract_articles(html)
    for article in articles:
        print(
            f"  [{article['id']}] {article['title'][:45]!r:47s}"
            f"  {article['author']:20s}  {article['date']}  ({article['comments']} коммент.)"
        )

    print()
    print("=" * 60)
    print("6. Очистка текста первой статьи")
    print("=" * 60)
    first_article_match = re.search(
        r'<article[^>]*>(.*?)</article>', html, re.DOTALL
    )
    if first_article_match:
        clean = strip_html(first_article_match.group(1))
        print(clean[:300])


if __name__ == "__main__":
    main()
