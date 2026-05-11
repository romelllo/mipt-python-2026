"""Агрегация данных через Hacker News Firebase API.

Hacker News API: https://hacker-news.firebaseio.com/v0/
Полностью бесплатный, без API-ключа, без регистрации.

Документация: https://github.com/HackerNews/API

Запуск:
    python seminars/seminar_15_beautifulsoup_apis/examples/04_news_and_aggregation.py
"""

import time
from dataclasses import dataclass
from datetime import datetime

import requests
from requests.exceptions import RequestException

HN_BASE = "https://hacker-news.firebaseio.com/v0"

# ============================================================
# Раздел 1: Структура данных
# ============================================================


@dataclass
class HNStory:
    """Новость с Hacker News."""

    id: int
    title: str
    url: str
    score: int
    by: str  # автор
    time: int  # Unix timestamp
    descendants: int = 0  # количество комментариев

    @property
    def published_at(self) -> str:
        """Дата публикации в читаемом формате."""
        return datetime.fromtimestamp(self.time).strftime("%Y-%m-%d %H:%M")

    def __str__(self) -> str:
        return (
            f"[{self.score}★] {self.title}\n"
            f"  Автор: {self.by} | {self.published_at} | "
            f"{self.descendants} комментариев\n"
            f"  {self.url or '(без ссылки)'}"
        )


# ============================================================
# Раздел 2: Получение одной новости
# ============================================================


def fetch_item(item_id: int) -> dict | None:
    """Получает данные одного элемента HN по ID.

    Args:
        item_id: числовой ID новости/комментария

    Returns:
        Словарь с данными или None при ошибке
    """
    url = f"{HN_BASE}/item/{item_id}.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"  Ошибка получения item {item_id}: {e}")
        return None


def parse_story(data: dict) -> HNStory | None:
    """Преобразует словарь API в объект HNStory.

    Args:
        data: сырые данные от API

    Returns:
        HNStory или None, если это не новость
    """
    # Обработка отсутствующих полей — реальные данные бывают неполными!
    if data.get("type") != "story":
        return None
    if data.get("deleted") or data.get("dead"):
        return None

    return HNStory(
        id=data.get("id", 0),
        title=data.get("title", "(без заголовка)"),
        url=data.get("url", ""),  # Ask HN / Show HN могут не иметь URL
        score=data.get("score", 0),
        by=data.get("by", "anonymous"),
        time=data.get("time", 0),
        descendants=data.get("descendants", 0),
    )


# ============================================================
# Раздел 3: Получение списка топ-новостей
# ============================================================


def fetch_top_story_ids(limit: int = 30) -> list[int]:
    """Получает список ID топ-новостей.

    Args:
        limit: сколько ID вернуть (максимум 500)

    Returns:
        Список числовых ID
    """
    url = f"{HN_BASE}/topstories.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        all_ids: list[int] = response.json()
        return all_ids[:limit]
    except RequestException as e:
        print(f"Ошибка получения топ-новостей: {e}")
        return []


def fetch_stories_batch(story_ids: list[int], delay: float = 0.1) -> list[HNStory]:
    """Загружает несколько новостей последовательно.

    Args:
        story_ids: список ID для загрузки
        delay: пауза между запросами (секунды)

    Returns:
        Список успешно загруженных новостей
    """
    stories: list[HNStory] = []

    for i, story_id in enumerate(story_ids, 1):
        print(f"  [{i}/{len(story_ids)}] Загружаем ID {story_id}...", end="\r")
        data = fetch_item(story_id)
        if data:
            story = parse_story(data)
            if story:
                stories.append(story)
        time.sleep(delay)  # вежливая пауза

    print()  # перенос строки после \r
    return stories


# ============================================================
# Раздел 4: Агрегация и анализ
# ============================================================


def aggregate_stories(stories: list[HNStory]) -> dict:
    """Вычисляет агрегированную статистику по новостям.

    Args:
        stories: список новостей

    Returns:
        Словарь со статистикой
    """
    if not stories:
        return {}

    scores = [s.score for s in stories]
    comments = [s.descendants for s in stories]

    # Топ авторов по количеству новостей
    author_counts: dict[str, int] = {}
    for s in stories:
        author_counts[s.by] = author_counts.get(s.by, 0) + 1

    top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        "total": len(stories),
        "avg_score": sum(scores) / len(scores),
        "max_score": max(scores),
        "avg_comments": sum(comments) / len(comments),
        "top_story": max(stories, key=lambda s: s.score),
        "most_discussed": max(stories, key=lambda s: s.descendants),
        "top_authors": top_authors,
    }


def filter_stories(
    stories: list[HNStory],
    min_score: int = 0,
    keyword: str = "",
) -> list[HNStory]:
    """Фильтрует новости по критериям.

    Args:
        stories: исходный список
        min_score: минимальный рейтинг
        keyword: ключевое слово в заголовке (регистронезависимо)

    Returns:
        Отфильтрованный список
    """
    result = stories

    if min_score > 0:
        result = [s for s in result if s.score >= min_score]

    if keyword:
        kw_lower = keyword.lower()
        result = [s for s in result if kw_lower in s.title.lower()]

    return result


# ============================================================
# Раздел 5: Пагинация — концепция
# ============================================================


def demo_pagination_concept() -> None:
    """Объясняет концепцию пагинации на примере HN API."""
    print("\n" + "=" * 60)
    print("5. Пагинация — загрузка данных по частям")
    print("=" * 60)

    # HN API возвращает до 500 ID за раз — это уже "страница"
    # Для постраничной загрузки мы сами нарезаем список:
    all_ids = fetch_top_story_ids(limit=20)
    print(f"Всего ID получено: {len(all_ids)}")

    # Разбиваем на страницы по 5 элементов
    page_size = 5
    total_pages = (len(all_ids) + page_size - 1) // page_size

    print(f"Размер страницы: {page_size}, всего страниц: {total_pages}")

    # Загружаем только первую страницу
    page_1_ids = all_ids[:page_size]
    print(f"\nЗагружаем страницу 1 (ID: {page_1_ids})...")
    page_1_stories = fetch_stories_batch(page_1_ids, delay=0.2)
    print(f"Загружено новостей: {len(page_1_stories)}")

    for story in page_1_stories:
        print(f"  [{story.score}★] {story.title[:60]}...")


def main() -> None:
    """Демонстрация агрегации данных через Hacker News API."""
    print("=" * 60)
    print("Hacker News API: агрегация новостей")
    print("=" * 60)

    # 1. Загружаем топ-15 новостей
    print("\nШаг 1: Получаем список топ-новостей...")
    top_ids = fetch_top_story_ids(limit=15)
    print(f"Получено ID: {len(top_ids)}")

    print("\nШаг 2: Загружаем данные каждой новости...")
    stories = fetch_stories_batch(top_ids, delay=0.15)
    print(f"Успешно загружено: {len(stories)} новостей")

    # 2. Показываем топ-3
    print("\n--- Топ-3 по рейтингу ---")
    top_3 = sorted(stories, key=lambda s: s.score, reverse=True)[:3]
    for i, story in enumerate(top_3, 1):
        print(f"\n{i}. {story}")

    # 3. Агрегация
    print("\n--- Статистика ---")
    stats = aggregate_stories(stories)
    if stats:
        print(f"Всего новостей: {stats['total']}")
        print(f"Средний рейтинг: {stats['avg_score']:.1f}")
        print(f"Максимальный рейтинг: {stats['max_score']}")
        print(f"Среднее кол-во комментариев: {stats['avg_comments']:.1f}")
        print("\nСамая обсуждаемая:")
        print(f"  {stats['most_discussed']}")
        print(f"\nТоп авторов: {stats['top_authors']}")

    # 4. Фильтрация
    print("\n--- Фильтрация: новости про Python ---")
    python_stories = filter_stories(stories, keyword="python")
    if python_stories:
        for s in python_stories:
            print(f"  [{s.score}★] {s.title}")
    else:
        print("  (в текущем топе нет новостей про Python)")

    # 5. Пагинация
    demo_pagination_concept()

    print("\n" + "=" * 60)
    print("Готово!")
    print("=" * 60)


if __name__ == "__main__":
    main()
