"""Основы BeautifulSoup: парсинг HTML, поиск элементов, извлечение данных.

Запуск:
    python seminars/seminar_15_beautifulsoup_apis/examples/01_beautifulsoup_basics.py
"""

from bs4 import BeautifulSoup, Tag

# ============================================================
# Раздел 1: Создание объекта BeautifulSoup
# ============================================================

# Тестовый HTML-документ
SAMPLE_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Книжный магазин</title>
</head>
<body>
    <h1 class="store-title">Лучшие книги 2026</h1>
    <p id="intro">Добро пожаловать в наш каталог.</p>

    <div class="catalog">
        <article class="book" data-id="1">
            <h2 class="title">Чистый код</h2>
            <span class="author">Роберт Мартин</span>
            <span class="price">1200 ₽</span>
            <a href="/books/clean-code" class="link">Подробнее</a>
        </article>

        <article class="book" data-id="2">
            <h2 class="title">Паттерны проектирования</h2>
            <span class="author">Банда четырёх</span>
            <span class="price">1500 ₽</span>
            <a href="/books/design-patterns" class="link">Подробнее</a>
        </article>

        <article class="book" data-id="3">
            <h2 class="title">Python Tricks</h2>
            <span class="author">Дэн Бейдер</span>
            <span class="price">900 ₽</span>
            <a href="/books/python-tricks" class="link">Подробнее</a>
        </article>
    </div>

    <footer>
        <p>Контакт: <a href="mailto:shop@example.com">shop@example.com</a></p>
    </footer>
</body>
</html>
"""


def demo_parsing() -> None:
    """Демонстрация создания объекта BeautifulSoup и базовых свойств."""
    print("=" * 60)
    print("1. Создание объекта BeautifulSoup")
    print("=" * 60)

    # Парсим HTML-строку с помощью lxml (быстрый C-парсер)
    soup = BeautifulSoup(SAMPLE_HTML, "lxml")

    # Тип объекта
    print(f"Тип soup: {type(soup)}")

    # Заголовок страницы
    print(f"Заголовок страницы: {soup.title}")
    print(f"Текст заголовка: {soup.title.string}")  # type: ignore[union-attr]

    # Первый тег h1 (быстрый доступ через атрибут)
    h1 = soup.h1
    print(f"\nПервый <h1>: {h1}")
    print(f"Текст h1: {h1.text}")  # type: ignore[union-attr]
    print(f"Класс h1: {h1['class']}")  # type: ignore[union-attr]


# ============================================================
# Раздел 2: find() и find_all()
# ============================================================


def demo_find_methods() -> None:
    """Демонстрация методов find() и find_all()."""
    print("\n" + "=" * 60)
    print("2. Методы find() и find_all()")
    print("=" * 60)

    soup = BeautifulSoup(SAMPLE_HTML, "lxml")

    # find() — возвращает ПЕРВЫЙ подходящий тег (или None)
    first_book = soup.find("article", class_="book")
    print(f"Первая книга (find): {type(first_book)}")
    if isinstance(first_book, Tag):
        print(f"  data-id: {first_book.get('data-id')}")

    # find_all() — возвращает СПИСОК всех подходящих тегов
    all_books = soup.find_all("article", class_="book")
    print(f"\nВсего книг (find_all): {len(all_books)}")

    # Извлекаем данные из каждой книги
    print("\nСписок книг:")
    for book in all_books:
        if not isinstance(book, Tag):
            continue
        title = book.find("h2", class_="title")
        author = book.find("span", class_="author")
        price = book.find("span", class_="price")
        print(
            f"  [{book.get('data-id')}] "
            f"{title.text if title else '?'} — "
            f"{author.text if author else '?'} — "
            f"{price.text if price else '?'}"
        )

    # find_all() с ограничением количества
    two_books = soup.find_all("article", limit=2)
    print(f"\nТолько первые 2 книги: {len(two_books)}")

    # Поиск по атрибуту data-id
    book_2 = soup.find("article", attrs={"data-id": "2"})
    if isinstance(book_2, Tag):
        title_tag = book_2.find("h2")
        print(f"\nКнига с data-id=2: {title_tag.text if title_tag else '?'}")


# ============================================================
# Раздел 3: CSS-селекторы через select() и select_one()
# ============================================================


def demo_css_selectors() -> None:
    """Демонстрация CSS-селекторов через select() и select_one()."""
    print("\n" + "=" * 60)
    print("3. CSS-селекторы: select() и select_one()")
    print("=" * 60)

    soup = BeautifulSoup(SAMPLE_HTML, "lxml")

    # select_one() — аналог find(), возвращает первый элемент
    intro = soup.select_one("#intro")
    print(f"Элемент #intro: {intro.text if intro else None}")

    # select() — аналог find_all(), возвращает список
    # Все заголовки книг: тег h2 с классом title внутри article.book
    titles = soup.select("article.book h2.title")
    print("\nЗаголовки книг (article.book h2.title):")
    for t in titles:
        print(f"  {t.text}")

    # Все ссылки внутри каталога
    links = soup.select(".catalog a.link")
    print("\nСсылки в каталоге (.catalog a.link):")
    for link in links:
        print(f"  {link.text} → {link.get('href')}")

    # Атрибутный селектор: ссылки с href, начинающимся на /books/
    book_links = soup.select('a[href^="/books/"]')
    print(f"\nСсылки на книги (a[href^='/books/']): {len(book_links)}")


# ============================================================
# Раздел 4: Извлечение текста и атрибутов
# ============================================================


def demo_text_and_attrs() -> None:
    """Демонстрация .text, .get_text(), .get(), .attrs."""
    print("\n" + "=" * 60)
    print("4. Извлечение текста и атрибутов")
    print("=" * 60)

    soup = BeautifulSoup(SAMPLE_HTML, "lxml")

    # .text vs .get_text()
    # .text — свойство, возвращает весь текст внутри тега (включая вложенные)
    # .get_text(separator, strip) — метод с параметрами
    first_article = soup.find("article")
    if isinstance(first_article, Tag):
        print(f".text (сырой):\n{repr(first_article.text[:80])}")
        print(
            f"\n.get_text(strip=True):\n"
            f"{repr(first_article.get_text(separator=' | ', strip=True))}"
        )

    # .get() — безопасное получение атрибута (не выбросит KeyError)
    link = soup.find("a", class_="link")
    if isinstance(link, Tag):
        print(f"\nАтрибут href: {link.get('href')}")
        print(f"Несуществующий атрибут: {link.get('target', 'не задан')}")

    # .attrs — словарь всех атрибутов тега
    h1 = soup.find("h1")
    if isinstance(h1, Tag):
        print(f"\nВсе атрибуты <h1>: {h1.attrs}")

    # Многозначные атрибуты (class) возвращаются как список
    book = soup.find("article", class_="book")
    if isinstance(book, Tag):
        print(f"Классы article: {book['class']}")  # ['book']


# ============================================================
# Раздел 5: NavigableString и навигация по дереву
# ============================================================


def demo_navigation() -> None:
    """Демонстрация навигации по дереву: parent, children, siblings."""
    print("\n" + "=" * 60)
    print("5. Навигация по дереву")
    print("=" * 60)

    soup = BeautifulSoup(SAMPLE_HTML, "lxml")

    # Найдём автора первой книги и поднимемся к родителю
    author_span = soup.find("span", class_="author")
    if isinstance(author_span, Tag):
        print(f"Автор: {author_span.text}")
        print(f"Родитель: {author_span.parent.name if author_span.parent else None}")

        # Следующий сосед (sibling) — тег на том же уровне
        next_sib = author_span.find_next_sibling("span")
        print(f"Следующий <span>: {next_sib.text if next_sib else None}")

    # Дочерние элементы через .children (итератор)
    catalog = soup.find("div", class_="catalog")
    if isinstance(catalog, Tag):
        # children включает NavigableString (пробелы/переносы) — фильтруем
        child_tags = [c for c in catalog.children if isinstance(c, Tag)]
        print(f"\nДочерние теги каталога: {len(child_tags)} article")


def main() -> None:
    """Запуск всех демонстраций."""
    demo_parsing()
    demo_find_methods()
    demo_css_selectors()
    demo_text_and_attrs()
    demo_navigation()

    print("\n" + "=" * 60)
    print("Готово! Изучите код выше и перейдите к упражнениям.")
    print("=" * 60)


if __name__ == "__main__":
    main()
