"""Реальный веб-скрапинг: парсинг quotes.toscrape.com.

Сайт quotes.toscrape.com создан специально для практики скрапинга —
никаких этических проблем, robots.txt разрешает обход.

Запуск:
    python seminars/seminar_15_beautifulsoup_apis/examples/02_web_scraping.py
"""

import time
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup, Tag
from requests.exceptions import RequestException

BASE_URL = "https://quotes.toscrape.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; MIPTBot/1.0; educational)"}


# ============================================================
# Раздел 1: Структура данных для цитаты
# ============================================================


@dataclass
class Quote:
    """Цитата с сайта quotes.toscrape.com."""

    text: str
    author: str
    tags: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        tags_str = ", ".join(self.tags) if self.tags else "—"
        return f'"{self.text}"\n  — {self.author} | теги: {tags_str}'


# ============================================================
# Раздел 2: Загрузка страницы
# ============================================================


def fetch_page(url: str, delay: float = 1.0) -> str | None:
    """Загружает HTML-страницу по URL.

    Args:
        url: адрес страницы
        delay: пауза перед запросом (вежливость к серверу)

    Returns:
        HTML-текст или None при ошибке
    """
    time.sleep(delay)  # пауза между запросами — хороший тон
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        print(f"  Ошибка загрузки {url}: {e}")
        return None


# ============================================================
# Раздел 3: Парсинг одной страницы
# ============================================================


def parse_quotes_page(html: str) -> list[Quote]:
    """Извлекает цитаты из HTML одной страницы.

    Args:
        html: HTML-текст страницы

    Returns:
        Список объектов Quote
    """
    soup = BeautifulSoup(html, "lxml")
    quotes: list[Quote] = []

    # Каждая цитата — div.quote
    for div in soup.select("div.quote"):
        if not isinstance(div, Tag):
            continue

        # Текст цитаты: span.text
        text_tag = div.select_one("span.text")
        text = text_tag.get_text(strip=True) if text_tag else ""
        # Убираем типографские кавычки «» которые сайт добавляет
        text = text.strip("\u201c\u201d")

        # Автор: small.author
        author_tag = div.select_one("small.author")
        author = author_tag.get_text(strip=True) if author_tag else "Неизвестен"

        # Теги: a.tag внутри div.tags
        tag_links = div.select("div.tags a.tag")
        tags = [t.get_text(strip=True) for t in tag_links]

        quotes.append(Quote(text=text, author=author, tags=tags))

    return quotes


# ============================================================
# Раздел 4: Определение следующей страницы (пагинация)
# ============================================================


def get_next_page_url(html: str) -> str | None:
    """Находит URL следующей страницы пагинации.

    Args:
        html: HTML-текст текущей страницы

    Returns:
        Полный URL следующей страницы или None
    """
    soup = BeautifulSoup(html, "lxml")
    # Кнопка "Next" — li.next > a
    next_btn = soup.select_one("li.next a")
    if next_btn and isinstance(next_btn, Tag):
        href = next_btn.get("href")
        if href:
            return BASE_URL + str(href)
    return None


# ============================================================
# Раздел 5: Сбор нескольких страниц
# ============================================================


def scrape_quotes(max_pages: int = 3) -> list[Quote]:
    """Собирает цитаты с нескольких страниц.

    Args:
        max_pages: максимальное количество страниц для обхода

    Returns:
        Список всех собранных цитат
    """
    all_quotes: list[Quote] = []
    url: str | None = BASE_URL
    page_num = 0

    while url and page_num < max_pages:
        page_num += 1
        print(f"  Страница {page_num}: {url}")

        html = fetch_page(url)
        if html is None:
            break

        page_quotes = parse_quotes_page(html)
        all_quotes.extend(page_quotes)
        print(f"    Найдено цитат: {len(page_quotes)}")

        url = get_next_page_url(html)

    return all_quotes


# ============================================================
# Раздел 6: Анализ собранных данных
# ============================================================


def analyze_quotes(quotes: list[Quote]) -> None:
    """Выводит статистику по собранным цитатам.

    Args:
        quotes: список цитат
    """
    print(f"\nВсего цитат: {len(quotes)}")

    # Топ авторов
    author_counts: dict[str, int] = {}
    for q in quotes:
        author_counts[q.author] = author_counts.get(q.author, 0) + 1

    top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\nТоп-5 авторов:")
    for author, count in top_authors:
        print(f"  {author}: {count} цитат")

    # Топ тегов
    tag_counts: dict[str, int] = {}
    for q in quotes:
        for tag in q.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\nТоп-5 тегов:")
    for tag, count in top_tags:
        print(f"  #{tag}: {count}")


def main() -> None:
    """Демонстрация полного цикла веб-скрапинга."""
    print("=" * 60)
    print("Веб-скрапинг: quotes.toscrape.com")
    print("=" * 60)

    print("\nСобираем цитаты (3 страницы)...")
    quotes = scrape_quotes(max_pages=3)

    print("\n--- Первые 3 цитаты ---")
    for q in quotes[:3]:
        print(f"\n{q}")

    analyze_quotes(quotes)

    print("\n" + "=" * 60)
    print("Скрапинг завершён!")
    print("=" * 60)


if __name__ == "__main__":
    main()
