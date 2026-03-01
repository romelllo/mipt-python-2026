"""
Семинар 5: Сравнение веб-фреймворков Python.

Этот модуль демонстрирует:
- Минимальные примеры приложений на Flask, Django и FastAPI
- Ключевые отличия между фреймворками
- Критерии выбора фреймворка для проекта

Примечание: этот файл содержит код-примеры для чтения и обсуждения.
Для запуска каждого фреймворка требуется отдельная настройка
(см. комментарии в коде).
"""

# ============================================================
# 1. Flask — минимальный пример
# ============================================================

# Для запуска:
#   pip install flask
#   python 02_frameworks_comparison.py
# Но мы не запускаем Flask в этом курсе — только изучаем синтаксис.

FLASK_EXAMPLE = """
# flask_app.py
from flask import Flask, jsonify

app = Flask(__name__)

# Список задач (в памяти)
tasks = [
    {"id": 1, "title": "Купить молоко", "done": False},
    {"id": 2, "title": "Написать код", "done": True},
]


@app.route("/")
def index():
    return "<h1>Привет от Flask!</h1>"


@app.route("/api/tasks")
def get_tasks():
    return jsonify(tasks)


@app.route("/api/tasks/<int:task_id>")
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

# Запуск: python flask_app.py
# Открыть: http://localhost:5000/
# API:     http://localhost:5000/api/tasks
"""

# ============================================================
# 2. Django — минимальный пример
# ============================================================

DJANGO_EXAMPLE = """
# === views.py (обработчики запросов) ===
from django.http import JsonResponse, HttpResponse

# Список задач (в памяти, в реальном проекте — из БД)
tasks = [
    {"id": 1, "title": "Купить молоко", "done": False},
    {"id": 2, "title": "Написать код", "done": True},
]


def index(request):
    return HttpResponse("<h1>Привет от Django!</h1>")


def get_tasks(request):
    return JsonResponse(tasks, safe=False)


def get_task(request, task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return JsonResponse({"error": "Task not found"}, status=404)
    return JsonResponse(task)


# === urls.py (маршруты) ===
from django.urls import path

urlpatterns = [
    path("", index),
    path("api/tasks/", get_tasks),
    path("api/tasks/<int:task_id>/", get_task),
]

# Запуск: python manage.py runserver
# Открыть: http://localhost:8000/
# API:     http://localhost:8000/api/tasks/
"""

# ============================================================
# 3. FastAPI — минимальный пример
# ============================================================

FASTAPI_EXAMPLE = """
# fastapi_app.py
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Список задач (в памяти)
tasks = [
    {"id": 1, "title": "Купить молоко", "done": False},
    {"id": 2, "title": "Написать код", "done": True},
]


@app.get("/")
def index():
    return {"message": "Привет от FastAPI!"}


@app.get("/api/tasks")
def get_tasks():
    return tasks


@app.get("/api/tasks/{task_id}")
def get_task(task_id: int):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Запуск: uvicorn fastapi_app:app --reload --port 8000
# Открыть: http://localhost:8000/
# Документация: http://localhost:8000/docs  (автоматически!)
"""


# ============================================================
# 4. Сравнение фреймворков
# ============================================================


def show_comparison() -> None:
    """Выводит сравнительную таблицу фреймворков."""
    print("=" * 60)
    print("СРАВНЕНИЕ ВЕБ-ФРЕЙМВОРКОВ PYTHON")
    print("=" * 60)

    comparison = {
        "Тип": {
            "Flask": "Микрофреймворк",
            "Django": "Полный фреймворк",
            "FastAPI": "API-фреймворк",
        },
        "ORM": {
            "Flask": "Нет (подключается отдельно)",
            "Django": "Встроенный Django ORM",
            "FastAPI": "Нет (подключается отдельно)",
        },
        "Админ-панель": {
            "Flask": "Нет",
            "Django": "Встроенная",
            "FastAPI": "Нет",
        },
        "Документация API": {
            "Flask": "Через расширения",
            "Django": "Через DRF",
            "FastAPI": "Автоматическая (Swagger)",
        },
        "Async": {
            "Flask": "Ограниченный",
            "Django": "Развивается (с v4.1)",
            "FastAPI": "Нативный",
        },
        "Шаблоны HTML": {
            "Flask": "Jinja2",
            "Django": "Django Template Language",
            "FastAPI": "Не предназначен",
        },
        "Когда использовать": {
            "Flask": "Небольшие проекты, прототипы",
            "Django": "Большие проекты с БД и админкой",
            "FastAPI": "REST API, микросервисы",
        },
    }

    for criterion, frameworks in comparison.items():
        print(f"\n  {criterion}:")
        for framework, value in frameworks.items():
            print(f"    {framework:8s} — {value}")


def show_examples() -> None:
    """Выводит минимальные примеры кода для каждого фреймворка."""
    print("\n" + "=" * 60)
    print("МИНИМАЛЬНЫЕ ПРИМЕРЫ КОДА")
    print("=" * 60)

    print("\n--- Flask ---")
    print(FLASK_EXAMPLE)

    print("\n--- Django ---")
    print(DJANGO_EXAMPLE)

    print("\n--- FastAPI ---")
    print(FASTAPI_EXAMPLE)


def show_choice_guide() -> None:
    """Выводит руководство по выбору фреймворка."""
    print("\n" + "=" * 60)
    print("КАК ВЫБРАТЬ ФРЕЙМВОРК?")
    print("=" * 60)

    print("""
  Нужна админ-панель и работа с БД?
    → Django

  Нужен только REST API?
    → FastAPI

  Нужен минимальный прототип?
    → Flask

  Нужна высокая производительность и async?
    → FastAPI

  Нужна полноценная система авторизации?
    → Django

  В нашем курсе:
    Семинары 5-8: Django (полноценные веб-приложения)
    Семинары 9-12: FastAPI (REST API сервисы)
    """)


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 5: СРАВНЕНИЕ ВЕБ-ФРЕЙМВОРКОВ PYTHON")
    print("=" * 60)

    show_comparison()
    show_examples()
    show_choice_guide()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
