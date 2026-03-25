"""
Семинар 9: Конфигурация FastAPI-приложения и Swagger UI.

Демонстрирует:
- Все параметры конструктора FastAPI()
- Кастомизация Swagger UI и ReDoc
- Метаданные тегов для группировки эндпоинтов
- Изменение URL документации
- Отключение документации для production

Запуск (из корня репозитория):
    python seminars/seminar_09_fastapi_intro/examples/04_app_config.py

Или через uvicorn:
    uvicorn seminars.seminar_09_fastapi_intro.examples.04_app_config:app --reload
    → Swagger UI: http://127.0.0.1:8000/docs
    → ReDoc:      http://127.0.0.1:8000/redoc
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

# ============================================================
# 1. Метаданные тегов
# ============================================================
# Теги группируют эндпоинты в Swagger UI.
# Здесь можно добавить описание и ссылку на внешнюю документацию.

tags_metadata = [
    {
        "name": "tasks",
        "description": "Операции с задачами: создание, чтение, обновление, удаление.",
    },
    {
        "name": "health",
        "description": "Проверка состояния сервиса.",
        "externalDocs": {
            "description": "Подробнее о health checks",
            "url": "https://microservices.io/patterns/observability/health-check-api.html",
        },
    },
]

# ============================================================
# 2. Создание приложения с полной конфигурацией
# ============================================================

app = FastAPI(
    # --- Основные метаданные ---
    title="TODO API",
    description="""
## TODO API — учебный пример FastAPI

Это простой API для управления задачами, демонстрирующий возможности FastAPI:

- **CRUD-операции** с задачами
- **Автоматическая валидация** через Pydantic
- **Документация** прямо в браузере

### Быстрый старт

1. Создайте задачу: `POST /tasks`
2. Посмотрите список: `GET /tasks`
3. Отметьте как выполненную: `PATCH /tasks/{id}`
""",
    version="2.0.0",
    # --- Контактная информация ---
    contact={
        "name": "MIPT Python Course",
        "url": "https://github.com/mipt-python",
        "email": "python@mipt.ru",
    },
    # --- Лицензия ---
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    # --- Метаданные тегов ---
    openapi_tags=tags_metadata,
    # --- URL документации ---
    # По умолчанию: docs_url="/docs", redoc_url="/redoc"
    # Можно изменить или отключить (docs_url=None)
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    # --- Для production: отключить документацию ---
    # docs_url=None,
    # redoc_url=None,
    # openapi_url=None,
)


# ============================================================
# 3. Примеры эндпоинтов с тегами и документацией
# ============================================================


@app.get("/health", tags=["health"], summary="Проверить работоспособность API")
def health_check() -> dict:
    """Возвращает статус сервиса.

    Используется системами мониторинга (Kubernetes liveness probe, etc.).
    """
    return {"status": "ok", "version": "2.0.0"}


@app.get(
    "/tasks",
    tags=["tasks"],
    summary="Получить список задач",
    description="Возвращает все задачи. Опционально фильтрует по статусу `done`.",
)
def list_tasks(done: bool | None = None) -> list[dict]:
    """Список задач с опциональной фильтрацией."""
    tasks = [
        {"id": 1, "title": "Купить продукты", "done": False},
        {"id": 2, "title": "Прочитать книгу", "done": True},
    ]
    if done is not None:
        tasks = [t for t in tasks if t["done"] == done]
    return tasks


# ============================================================
# 4. Кастомизация OpenAPI-схемы (продвинутый уровень)
# ============================================================
# Можно полностью заменить генерируемую OpenAPI-схему.
# Полезно, когда нужно добавить серверы, security-схемы и т.д.


def custom_openapi() -> dict:
    """Кастомная OpenAPI-схема с дополнительными серверами."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=tags_metadata,
    )

    # Добавляем информацию о серверах (dev / prod)
    openapi_schema["servers"] = [
        {"url": "http://localhost:8000", "description": "Локальный сервер разработки"},
        {"url": "https://api.example.com", "description": "Production-сервер"},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore[method-assign]


# ============================================================
# 5. Демонстрационный запуск
# ============================================================


def main() -> None:
    """Показать конфигурацию приложения без запуска сервера."""
    print("=" * 60)
    print("СЕМИНАР 9: КОНФИГУРАЦИЯ FASTAPI + SWAGGER UI")
    print("=" * 60)
    print()

    print("Конфигурация приложения:")
    print(f"  title:       {app.title}")
    print(f"  version:     {app.version}")
    print(f"  docs_url:    {app.docs_url}")
    print(f"  redoc_url:   {app.redoc_url}")
    print(f"  openapi_url: {app.openapi_url}")
    print()

    print("Зарегистрированные маршруты:")
    print("-" * 50)
    for route in app.routes:
        if hasattr(route, "methods"):
            methods = ", ".join(sorted(route.methods or []))  # type: ignore[union-attr]
            tags = getattr(route, "tags", [])
            tag_str = f"[{', '.join(tags)}]" if tags else ""
            print(f"  {methods:<8} {route.path:<20} {tag_str}")  # type: ignore[union-attr]
    print()

    print("Параметры конструктора FastAPI():")
    print("-" * 50)
    params = [
        ("title", "Название API (отображается в Swagger UI)"),
        ("description", "Описание API (поддерживает Markdown)"),
        ("version", "Версия API (например, '1.0.0')"),
        ("contact", "Контактная информация разработчика"),
        ("license_info", "Лицензия API"),
        ("openapi_tags", "Метаданные тегов для группировки"),
        ("docs_url", "URL Swagger UI (None — отключить)"),
        ("redoc_url", "URL ReDoc (None — отключить)"),
        ("openapi_url", "URL OpenAPI JSON-схемы"),
    ]
    for param, desc in params:
        print(f"  {param:<15} — {desc}")
    print()

    print("Запустите сервер для просмотра документации:")
    print(
        "  uvicorn seminars.seminar_09_fastapi_intro.examples.04_app_config:app --reload"
    )
    print("  → Swagger UI: http://127.0.0.1:8000/docs")
    print("  → ReDoc:      http://127.0.0.1:8000/redoc")


if __name__ == "__main__":
    main()
