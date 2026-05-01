"""
Блок 1: HTTP-запросы для сбора данных с веб-страниц.

Этот файл демонстрирует, как использовать библиотеку requests
для получения HTML-страниц и данных из API.

Предполагается, что базы HTTP вы уже знаете из семинара 4.
Здесь акцент на применении requests для веб-скрапинга:
загрузка HTML, обработка ошибок, сохранение результата.
"""

import time
from pathlib import Path

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

# ---------------------------------------------------------------------------
# 1. Загрузка HTML-страницы
# ---------------------------------------------------------------------------

def fetch_page(url: str, timeout: int = 10) -> str | None:
    """Загружает HTML-страницу по URL и возвращает текст.

    Args:
        url: адрес страницы
        timeout: максимальное время ожидания ответа (секунды)

    Returns:
        HTML-текст страницы или None при ошибке
    """
    # Заголовок User-Agent — некоторые серверы блокируют запросы без него
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; PythonScraper/1.0)",
        "Accept-Language": "ru-RU,ru;q=0.9",
    }
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # выбросит HTTPError для 4xx/5xx
        return response.text
    except Timeout:
        print(f"[ОШИБКА] Превышено время ожидания: {url}")
    except ConnectionError:
        print(f"[ОШИБКА] Не удалось подключиться: {url}")
    except HTTPError as e:
        print(f"[ОШИБКА] HTTP {e.response.status_code}: {url}")
    except RequestException as e:
        print(f"[ОШИБКА] {e}")
    return None


# ---------------------------------------------------------------------------
# 2. Получение данных из публичного API (JSON)
# ---------------------------------------------------------------------------

def fetch_json(url: str, params: dict | None = None, timeout: int = 10) -> dict | list | None:
    """Загружает JSON-ответ из API.

    Args:
        url: адрес эндпоинта
        params: query-параметры (опционально)
        timeout: таймаут в секундах

    Returns:
        Разобранный JSON (dict или list) или None при ошибке
    """
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        print(f"[ОШИБКА] HTTP {e.response.status_code}")
    except RequestException as e:
        print(f"[ОШИБКА] {e}")
    return None


# ---------------------------------------------------------------------------
# 3. Сохранение результата в файл
# ---------------------------------------------------------------------------

def save_html(html: str, filepath: Path) -> None:
    """Сохраняет HTML-строку в файл на диске.

    Args:
        html: текст страницы
        filepath: путь для сохранения
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(html, encoding="utf-8")
    print(f"[СОХРАНЕНО] {filepath} ({len(html)} символов)")


# ---------------------------------------------------------------------------
# 4. Простой retry — повтор при ошибке
# ---------------------------------------------------------------------------

def fetch_with_retry(url: str, retries: int = 3, delay: float = 2.0) -> str | None:
    """Загружает страницу с повторными попытками при ошибке.

    Args:
        url: адрес страницы
        retries: количество попыток
        delay: пауза между попытками (секунды)

    Returns:
        HTML-текст или None если все попытки исчерпаны
    """
    for attempt in range(1, retries + 1):
        print(f"  Попытка {attempt}/{retries}...")
        html = fetch_page(url)
        if html is not None:
            return html
        if attempt < retries:
            time.sleep(delay)
    print(f"[ОШИБКА] Все {retries} попытки исчерпаны: {url}")
    return None


# ---------------------------------------------------------------------------
# 5. Проверка robots.txt — этика скрапинга
# ---------------------------------------------------------------------------

def check_robots_txt(base_url: str) -> None:
    """Загружает и выводит содержимое robots.txt сайта.

    robots.txt — файл, в котором сайт указывает, какие страницы
    разрешено или запрещено обходить автоматическим ботам.
    Перед скрапингом всегда проверяйте robots.txt!

    Args:
        base_url: корневой адрес сайта (например, https://example.com)
    """
    robots_url = base_url.rstrip("/") + "/robots.txt"
    html = fetch_page(robots_url)
    if html:
        print(f"=== robots.txt для {base_url} ===")
        # Показываем первые 20 строк
        lines = html.splitlines()[:20]
        for line in lines:
            print(line)
    else:
        print("robots.txt недоступен или не существует")


# ---------------------------------------------------------------------------
# Демонстрация
# ---------------------------------------------------------------------------

def main() -> None:
    """Запускает примеры из этого файла."""

    print("=" * 60)
    print("1. Загрузка публичного API — посты JSONPlaceholder")
    print("=" * 60)
    posts = fetch_json("https://jsonplaceholder.typicode.com/posts", params={"_limit": 3})
    if posts:
        for post in posts:
            print(f"  [{post['id']}] {post['title'][:50]}...")

    print()
    print("=" * 60)
    print("2. Загрузка HTML-страницы")
    print("=" * 60)
    html = fetch_page("https://httpbin.org/html")
    if html:
        print(f"  Получено {len(html)} символов HTML")
        # Сохраняем в папку data рядом с этим скриптом
        save_path = Path(__file__).parent.parent / "data" / "fetched_page.html"
        save_html(html, save_path)

    print()
    print("=" * 60)
    print("3. Проверка robots.txt")
    print("=" * 60)
    check_robots_txt("https://httpbin.org")

    print()
    print("=" * 60)
    print("4. Демонстрация обработки ошибок")
    print("=" * 60)
    # Намеренно запрашиваем несуществующий ресурс
    fetch_page("https://httpbin.org/status/404")
    fetch_page("https://httpbin.org/status/500")


if __name__ == "__main__":
    main()
