"""
Блок 2: HTML и DOM — структура веб-страницы.

Перед тем как извлекать данные, нужно понять, как устроена
HTML-страница и как найти нужный элемент.

В этом файле мы работаем с HTML как с текстом, используя
регулярные выражения — без сторонних парсеров.
"""

import re
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Что такое HTML-документ
# ---------------------------------------------------------------------------

# HTML (HyperText Markup Language) — язык разметки веб-страниц.
# Документ состоит из вложенных тегов:
#
#   <тег атрибут="значение">содержимое</тег>
#   <одиночный-тег />
#
# Структура (DOM — Document Object Model):
#
#   <html>
#     <head>
#       <title>Заголовок вкладки</title>
#     </head>
#     <body>
#       <h1>Заголовок страницы</h1>
#       <p class="intro">Параграф текста</p>
#       <a href="/page.html">Ссылка</a>
#     </body>
#   </html>

SAMPLE_HTML = """
<html>
<head><title>Пример страницы</title></head>
<body>
  <h1 id="main-title">Добро пожаловать</h1>
  <p class="intro">Это вводный параграф.</p>
  <p class="content">Здесь основной текст. Email: info@example.com</p>
  <ul>
    <li><a href="/page1.html">Страница 1</a></li>
    <li><a href="/page2.html">Страница 2</a></li>
    <li><a href="https://external.com/page3.html">Внешняя ссылка</a></li>
  </ul>
  <div class="footer">
    <p>Контакт: admin@example.com | Тел: +7-999-123-45-67</p>
  </div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# 2. Как находить элементы: CSS-селекторы и XPath (концепции)
# ---------------------------------------------------------------------------

# CSS-селекторы — язык выборки элементов, используемый в браузерах и
# парсерах (например, BeautifulSoup, который мы рассмотрим в следующем
# семинаре).
#
# Примеры CSS-селекторов:
#   tag            — все элементы с этим тегом:      p, h1, a
#   .class         — элементы с классом:             .intro, .post-title
#   #id            — элемент с идентификатором:      #main-title
#   tag.class      — тег с классом:                  p.content
#   parent > child — прямой потомок:                 div > p
#   ancestor desc  — любой потомок:                  article a
#   [attr]         — элементы с атрибутом:           a[href]
#   [attr=value]   — атрибут равен значению:         input[type="text"]
#
# XPath — более мощный язык запросов к XML/HTML:
#   //tag          — все теги в документе:           //p
#   //tag[@attr]   — теги с атрибутом:               //a[@href]
#   //tag/text()   — текстовое содержимое тега:      //h2/text()
#   //tag[@class="x"]/text() — текст тега с классом
#
# В этом семинаре мы используем регулярные выражения для той же задачи.
# В следующем семинаре (BeautifulSoup) CSS-селекторы заработают напрямую.


# ---------------------------------------------------------------------------
# 3. Извлечение данных из HTML с помощью регулярных выражений
# ---------------------------------------------------------------------------

def extract_tag_text(html: str, tag: str) -> list[str]:
    """Извлекает текстовое содержимое всех тегов с заданным именем.

    Args:
        html: HTML-строка
        tag: имя тега (например, 'h1', 'p', 'title')

    Returns:
        Список строк с текстом внутри каждого тега
    """
    # <tag ...>содержимое</tag>
    # re.DOTALL нужен, чтобы . совпадал с переносами строк
    pattern = rf"<{tag}[^>]*>(.*?)</{tag}>"
    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
    # Убираем вложенные теги из найденного текста
    result = []
    for match in matches:
        clean = re.sub(r"<[^>]+>", "", match).strip()
        if clean:
            result.append(clean)
    return result


def extract_links(html: str) -> list[dict[str, str]]:
    """Извлекает все ссылки (<a href=...>) из HTML.

    Args:
        html: HTML-строка

    Returns:
        Список словарей {"href": ..., "text": ...}
    """
    # Ищем: <a ... href="URL" ...>текст</a>
    # Группа 1: значение href  Группа 2: текст ссылки
    pattern = r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>'
    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
    links = []
    for href, raw_text in matches:
        text = re.sub(r"<[^>]+>", "", raw_text).strip()
        links.append({"href": href, "text": text})
    return links


def extract_attribute(html: str, tag: str, attr: str) -> list[str]:
    """Извлекает значения заданного атрибута у всех тегов.

    Args:
        html: HTML-строка
        tag: имя тега
        attr: имя атрибута

    Returns:
        Список значений атрибута
    """
    pattern = rf'<{tag}\s+[^>]*{attr}=["\']([^"\']+)["\']'
    return re.findall(pattern, html, re.IGNORECASE)


# ---------------------------------------------------------------------------
# 4. Работа с реальным файлом sample_page.html
# ---------------------------------------------------------------------------

def load_local_html(filename: str) -> str:
    """Загружает HTML из локального файла в папке data/.

    Args:
        filename: имя файла (без пути)

    Returns:
        Текст HTML
    """
    data_dir = Path(__file__).parent.parent / "data"
    filepath = data_dir / filename
    return filepath.read_text(encoding="utf-8")


def main() -> None:
    """Демонстрирует разбор HTML с помощью регулярных выражений."""

    print("=" * 60)
    print("1. Разбор встроенного примера")
    print("=" * 60)

    titles = extract_tag_text(SAMPLE_HTML, "h1")
    print(f"Заголовки h1: {titles}")

    paragraphs = extract_tag_text(SAMPLE_HTML, "p")
    print(f"Параграфы p: {paragraphs}")

    links = extract_links(SAMPLE_HTML)
    print("Ссылки:")
    for link in links:
        print(f"  {link['text']!r:30s} -> {link['href']}")

    print()
    print("=" * 60)
    print("2. Разбор sample_page.html")
    print("=" * 60)

    html = load_local_html("sample_page.html")
    print(f"Загружено {len(html)} символов\n")

    # Все заголовки статей
    post_titles = extract_tag_text(html, "h2")
    print("Заголовки статей:")
    for title in post_titles:
        print(f"  - {title}")

    print()
    # Все ссылки
    all_links = extract_links(html)
    print(f"Всего ссылок: {len(all_links)}")
    print("Первые 5:")
    for link in all_links[:5]:
        print(f"  {link['text']!r:30s} -> {link['href']}")

    print()
    # Значения атрибута id у article
    ids = extract_attribute(html, "article", "id")
    print(f"ID статей: {ids}")


if __name__ == "__main__":
    main()
