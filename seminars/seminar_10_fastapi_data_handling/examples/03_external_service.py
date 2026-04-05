"""
Семинар 10, Блок 3: Вызов внешних HTTP-сервисов с httpx.AsyncClient.

Демонстрирует:
- async with httpx.AsyncClient() as client — контекстный менеджер
- await client.get(url) — асинхронный GET-запрос
- response.json() — десериализация JSON-ответа
- response.raise_for_status() — генерация исключения при HTTP-ошибке
- Паттерн "fire-and-forget" через asyncio.create_task()
- Параллельные запросы через asyncio.gather()

Использует https://jsonplaceholder.typicode.com — публичный тестовый API.

Запуск (из корня репозитория):
    python seminars/seminar_10_fastapi_data_handling/examples/03_external_service.py
"""

import asyncio
import time

import httpx

# ============================================================
# Базовый URL публичного тестового API
# ============================================================
BASE_URL = "https://jsonplaceholder.typicode.com"


# ============================================================
# 1. Простой async GET-запрос
# ============================================================


async def fetch_todo(todo_id: int) -> dict:
    """Получить одну задачу с внешнего API.

    Args:
        todo_id: идентификатор задачи (1–200)

    Returns:
        словарь с данными задачи
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/todos/{todo_id}")
        response.raise_for_status()  # бросит исключение при 4xx/5xx
        return dict(response.json())


# ============================================================
# 2. Параллельные запросы через asyncio.gather()
# ============================================================


async def fetch_multiple_todos(ids: list[int]) -> list[dict]:
    """Получить несколько задач параллельно.

    asyncio.gather() запускает корутины одновременно —
    суммарное время ≈ время самого медленного запроса.

    Args:
        ids: список идентификаторов задач

    Returns:
        список словарей с данными задач
    """
    async with httpx.AsyncClient() as client:
        # Создаём корутины для каждого запроса
        tasks = [client.get(f"{BASE_URL}/todos/{id_}") for id_ in ids]
        # Запускаем все параллельно
        responses = await asyncio.gather(*tasks)
        # Парсим JSON из каждого ответа
        return [dict(r.json()) for r in responses]


# ============================================================
# 3. Паттерн в FastAPI-эндпоинте (демо-функция)
# ============================================================


async def enrich_note_with_external_data(note_title: str) -> dict:
    """Пример: обогащение заметки данными из внешнего API.

    В реальном FastAPI-эндпоинте:
        @router.get("/notes/{id}/enriched")
        async def get_enriched_note(id: int, session: SessionDep):
            note = await session.get(Note, id)           # запрос к БД
            extra = await fetch_todo(1)                  # запрос к внешнему API
            return {"note": note, "related_todo": extra} # объединяем

    Ключевое: оба await выполняются без блокировки event loop.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/posts/1")
        response.raise_for_status()
        external_data = response.json()

    return {
        "note_title": note_title,
        "related_post_title": external_data["title"],
        "user_id": external_data["userId"],
    }


# ============================================================
# 4. Обработка ошибок
# ============================================================


async def fetch_with_error_handling(url: str) -> dict | None:
    """Запрос с обработкой HTTP-ошибок.

    Returns:
        данные ответа или None при ошибке
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return dict(response.json())
    except httpx.HTTPStatusError as e:
        print(f"  HTTP ошибка: {e.response.status_code} — {e.request.url}")
        return None
    except httpx.RequestError as e:
        print(f"  Сетевая ошибка: {e}")
        return None


# ============================================================
# 5. Демонстрация
# ============================================================


async def demo() -> None:
    """Демонстрация httpx.AsyncClient."""
    print("=" * 60)
    print("СЕМИНАР 10, БЛОК 3: httpx.AsyncClient — внешние сервисы")
    print("=" * 60)
    print()

    # Простой запрос
    print("1. Простой async GET-запрос:")
    todo = await fetch_todo(1)
    print(f"   id={todo['id']}, title={todo['title']!r}, completed={todo['completed']}")
    print()

    # Параллельные запросы
    print("2. Параллельные запросы (asyncio.gather):")
    start = time.perf_counter()
    todos = await fetch_multiple_todos([1, 2, 3, 4, 5])
    elapsed = time.perf_counter() - start
    print(f"   Получено {len(todos)} задач за {elapsed:.2f}с (параллельно)")
    for t in todos:
        print(f"   [{t['id']}] {t['title'][:40]!r}")
    print()

    # Обогащение данными
    print("3. Обогащение заметки внешними данными:")
    enriched = await enrich_note_with_external_data("Моя заметка")
    print(f"   note_title: {enriched['note_title']!r}")
    print(f"   related_post_title: {enriched['related_post_title'][:40]!r}")
    print()

    # Обработка ошибок
    print("4. Обработка HTTP-ошибок:")
    ok = await fetch_with_error_handling(f"{BASE_URL}/todos/1")
    print(f"   Успешный запрос: {ok is not None}")
    err = await fetch_with_error_handling(f"{BASE_URL}/nonexistent-endpoint")
    print(f"   Ошибочный запрос вернул None: {err is None}")
    print()

    print("Ключевые выводы:")
    print("  - async with httpx.AsyncClient() as client → автозакрытие соединений")
    print("  - response.raise_for_status() → исключение при 4xx/5xx")
    print("  - asyncio.gather(*tasks) → параллельные запросы без лишнего времени")
    print("  - timeout=10.0 → защита от зависших соединений")


def main() -> None:
    """Точка входа."""
    asyncio.run(demo())


if __name__ == "__main__":
    main()
