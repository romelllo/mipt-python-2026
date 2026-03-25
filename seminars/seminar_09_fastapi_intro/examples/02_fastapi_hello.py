"""
Семинар 9: Первое приложение FastAPI + сравнение с Django.

Демонстрирует:
- Минимальное FastAPI-приложение
- Сравнение с аналогичным Django-кодом
- Синхронные и асинхронные эндпоинты
- Автоматическая документация (Swagger UI, ReDoc)

Запуск (из корня репозитория):
    python seminars/seminar_09_fastapi_intro/examples/02_fastapi_hello.py

Или через uvicorn (для открытия в браузере):
    uvicorn seminars.seminar_09_fastapi_intro.examples.02_fastapi_hello:app --reload
    → Swagger UI: http://127.0.0.1:8000/docs
    → ReDoc:      http://127.0.0.1:8000/redoc
    → OpenAPI:    http://127.0.0.1:8000/openapi.json
"""

import asyncio
import time

from fastapi import FastAPI

# ============================================================
# 1. Минимальное FastAPI-приложение
# ============================================================
# Три строки — и у вас работающий API с документацией.

app = FastAPI()


@app.get("/")
def root() -> dict:
    """Корневой эндпоинт — возвращает приветствие."""
    return {"message": "Привет от FastAPI!"}


# ============================================================
# 2. Синхронные vs асинхронные эндпоинты
# ============================================================
# FastAPI поддерживает оба варианта.
# async def → эндпоинт асинхронный (использует event loop)
# def       → FastAPI запускает в threadpool, не блокируя event loop


@app.get("/sync-endpoint")
def sync_example() -> dict:
    """Синхронный эндпоинт.

    Используйте, когда:
    - Нет I/O-операций (вычисления, работа с памятью)
    - Используете библиотеки без async-поддержки
    """
    # Имитируем работу без I/O
    result = sum(range(1000))
    return {"type": "sync", "result": result}


@app.get("/async-endpoint")
async def async_example() -> dict:
    """Асинхронный эндпоинт.

    Используйте, когда:
    - Есть I/O-операции: запросы к БД, HTTP-запросы, файлы
    - Хотите обрабатывать много запросов одновременно
    """
    # Имитируем async I/O (например, запрос к БД)
    await asyncio.sleep(0)  # не блокирует event loop
    return {"type": "async", "message": "Асинхронный эндпоинт"}


# ============================================================
# 3. Path-параметры и Query-параметры
# ============================================================


@app.get("/items/{item_id}")
def get_item(item_id: int, verbose: bool = False) -> dict:
    """Пример path-параметра и query-параметра.

    - `item_id` — path-параметр (часть URL: /items/42)
    - `verbose` — query-параметр (в строке запроса: ?verbose=true)

    FastAPI автоматически:
    - Преобразует item_id из строки в int
    - Возвращает 422, если item_id не число
    """
    response: dict = {"id": item_id}
    if verbose:
        response["description"] = f"Подробная информация о товаре {item_id}"
    return response


# ============================================================
# 4. Сравнение FastAPI и Django (комментарии)
# ============================================================
#
# Django:
# ────────────────────────────────────
# # urls.py
# urlpatterns = [path("items/<int:pk>/", views.item_detail)]
#
# # views.py
# def item_detail(request, pk):
#     return JsonResponse({"id": pk})
#
# FastAPI:
# ────────────────────────────────────
# @app.get("/items/{item_id}")
# def get_item(item_id: int):
#     return {"id": item_id}
#
# Ключевые отличия:
# ┌─────────────────────┬─────────────────────┬──────────────────────┐
# │ Критерий            │ Django              │ FastAPI              │
# ├─────────────────────┼─────────────────────┼──────────────────────┤
# │ Маршрутизация       │ urls.py + views.py  │ Декоратор над функц. │
# │ Валидация данных    │ Forms / Serializers │ Pydantic (авто)      │
# │ Документация API    │ DRF (расширение)    │ Встроенная (авто)    │
# │ Async               │ Частичная           │ Нативная             │
# │ ORM                 │ Встроенный          │ Нет (SQLAlchemy)     │
# │ Админ-панель        │ Встроенная          │ Нет                  │
# │ Назначение          │ Полный сайт + API   │ API-сервисы          │
# └─────────────────────┴─────────────────────┴──────────────────────┘


# ============================================================
# 5. Демонстрационный запуск (без реального сервера)
# ============================================================


def demo_without_server() -> None:
    """Показать структуру приложения без запуска сервера."""
    print("=" * 60)
    print("СЕМИНАР 9: ПЕРВОЕ ПРИЛОЖЕНИЕ FASTAPI")
    print("=" * 60)
    print()

    print("Зарегистрированные маршруты:")
    print("-" * 50)
    for route in app.routes:
        # Показываем только наши эндпоинты (не служебные)
        if hasattr(route, "methods"):
            methods = ", ".join(sorted(route.methods or []))  # type: ignore[union-attr]
            print(f"  {methods:<8} {route.path}")  # type: ignore[union-attr]
    print()

    print("Автоматическая документация (при запуске сервера):")
    print("  Swagger UI → http://127.0.0.1:8000/docs")
    print("  ReDoc      → http://127.0.0.1:8000/redoc")
    print("  OpenAPI    → http://127.0.0.1:8000/openapi.json")
    print()

    print("Сравнение FastAPI и Django:")
    print("-" * 50)
    comparisons = [
        ("Маршрутизация", "urls.py + views.py", "Декоратор @app.get(...)"),
        ("Валидация", "Forms / Serializers", "Pydantic (автоматически)"),
        ("Документация", "DRF (расширение)", "Swagger UI (встроено)"),
        ("Async", "Частичная", "Нативная (async def)"),
        ("ORM", "Встроенный", "Нет (SQLAlchemy / др.)"),
        ("Назначение", "Сайт + API", "API-сервисы"),
    ]
    print(f"  {'Критерий':<20} {'Django':<25} {'FastAPI'}")
    print("  " + "-" * 65)
    for criterion, django_val, fastapi_val in comparisons:
        print(f"  {criterion:<20} {django_val:<25} {fastapi_val}")
    print()

    print("Запустите сервер командой:")
    print(
        "  uvicorn seminars.seminar_09_fastapi_intro.examples.02_fastapi_hello:app --reload"
    )
    print()

    # Демонстрируем синхронный вызов напрямую
    print("Тест синхронного эндпоинта (вызов без сервера):")
    t0 = time.perf_counter()
    result = sync_example()
    elapsed = time.perf_counter() - t0
    print(f"  sync_example() → {result} (за {elapsed:.4f}с)")
    print()

    # Демонстрируем асинхронный вызов напрямую
    print("Тест асинхронного эндпоинта (вызов без сервера):")

    async def run_async() -> dict:
        return await async_example()

    result_async = asyncio.run(run_async())
    print(f"  async_example() → {result_async}")
    print()


def main() -> None:
    """Точка входа."""
    demo_without_server()


if __name__ == "__main__":
    main()
