"""
Семинар 9: HTTP, REST и CRUD — повторение.

Демонстрирует ключевые концепции:
- HTTP-методы и их соответствие CRUD-операциям
- Структура HTTP-запроса и ответа
- Статус-коды и их смысл
- REST-соглашения об именовании маршрутов

Запуск (из корня репозитория):
    python seminars/seminar_09_fastapi_intro/examples/01_http_rest_recap.py
"""

# ============================================================
# 1. CRUD ↔ HTTP: таблица соответствия
# ============================================================
# CRUD — четыре базовые операции с данными:
#   Create → POST
#   Read   → GET
#   Update → PUT / PATCH
#   Delete → DELETE

CRUD_HTTP_TABLE = [
    # (CRUD, HTTP-метод, типичный URL, смысл)
    ("Create", "POST", "/tasks", "Создать новую задачу"),
    ("Read (list)", "GET", "/tasks", "Получить список задач"),
    ("Read (one)", "GET", "/tasks/{id}", "Получить одну задачу по ID"),
    ("Update (full)", "PUT", "/tasks/{id}", "Полностью заменить задачу"),
    ("Update (partial)", "PATCH", "/tasks/{id}", "Частично обновить задачу"),
    ("Delete", "DELETE", "/tasks/{id}", "Удалить задачу"),
]


def print_crud_table() -> None:
    """Вывести таблицу соответствия CRUD ↔ HTTP."""
    print("CRUD ↔ HTTP: соответствие операций")
    print("-" * 72)
    print(f"{'CRUD':<18} {'HTTP':<8} {'URL':<22} {'Смысл'}")
    print("-" * 72)
    for crud, method, url, desc in CRUD_HTTP_TABLE:
        print(f"{crud:<18} {method:<8} {url:<22} {desc}")
    print()


# ============================================================
# 2. Структура HTTP-запроса и ответа
# ============================================================


def print_http_request_example() -> None:
    """Показать структуру типичного HTTP-запроса (создание задачи)."""
    print("Структура HTTP-запроса (POST /tasks)")
    print("-" * 50)
    request_example = """\
POST /tasks HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer <token>

{
    "title": "Купить продукты",
    "description": "Молоко, хлеб, яйца",
    "done": false
}
"""
    print(request_example)

    print("Структура HTTP-ответа (201 Created)")
    print("-" * 50)
    response_example = """\
HTTP/1.1 201 Created
Content-Type: application/json
Location: /tasks/42

{
    "id": 42,
    "title": "Купить продукты",
    "description": "Молоко, хлеб, яйца",
    "done": false
}
"""
    print(response_example)


# ============================================================
# 3. Статус-коды HTTP
# ============================================================

STATUS_CODES: list[tuple[int, str, str]] = [
    # (код, название, когда использовать)
    (200, "OK", "Запрос выполнен успешно (GET, PUT, PATCH)"),
    (201, "Created", "Ресурс успешно создан (POST)"),
    (204, "No Content", "Успешно, но тело ответа пустое (DELETE)"),
    (400, "Bad Request", "Ошибка в запросе — неверные данные от клиента"),
    (401, "Unauthorized", "Нужна авторизация (нет или невалидный токен)"),
    (403, "Forbidden", "Авторизован, но нет прав на действие"),
    (404, "Not Found", "Ресурс не найден"),
    (422, "Unprocessable Entity", "Данные получены, но не прошли валидацию"),
    (500, "Internal Server Error", "Ошибка на стороне сервера"),
]


def print_status_codes() -> None:
    """Вывести важнейшие HTTP статус-коды."""
    print("Важные HTTP статус-коды")
    print("-" * 70)
    print(f"{'Код':<6} {'Название':<26} {'Когда использовать'}")
    print("-" * 70)
    for code, name, usage in STATUS_CODES:
        # Группируем по диапазону: 2xx → OK, 4xx → ошибка клиента, 5xx → сервер
        prefix = "✅" if code < 300 else ("⚠️ " if code < 500 else "❌")
        print(f"{prefix} {code:<4} {name:<26} {usage}")
    print()


# ============================================================
# 4. REST-соглашения: правильные и неправильные URL
# ============================================================

REST_CONVENTIONS: list[tuple[str, str, str, str]] = [
    # (метод, хороший URL, плохой URL, пояснение)
    ("GET", "/tasks", "/getTasks", "Существительное, не глагол"),
    ("GET", "/tasks/42", "/tasks/get/42", "ID в пути, не в сегменте /get/"),
    ("POST", "/tasks", "/createTask", "Метод POST уже означает создание"),
    ("DELETE", "/tasks/42", "/tasks/42/delete", "DELETE означает удаление"),
    ("GET", "/users/5/tasks", "/getUserTasks?id=5", "Вложенные ресурсы через /"),
]


def print_rest_conventions() -> None:
    """Вывести примеры правильного и неправильного REST-именования."""
    print("REST-соглашения об именовании URL")
    print("-" * 72)
    print(f"{'Метод':<8} {'✅ Правильно':<28} {'❌ Неправильно':<25} {'Почему'}")
    print("-" * 72)
    for method, good, bad, reason in REST_CONVENTIONS:
        print(f"{method:<8} {good:<28} {bad:<25} {reason}")
    print()


# ============================================================
# 5. Симуляция REST-клиента (без реального HTTP-сервера)
# ============================================================


class FakeTask:
    """Модель задачи для демонстрации REST-операций."""

    def __init__(
        self, task_id: int, title: str, description: str = "", done: bool = False
    ) -> None:
        self.id = task_id
        self.title = title
        self.description = description
        self.done = done

    def to_dict(self) -> dict:
        """Сериализовать в словарь (как JSON-ответ API)."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
        }

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title!r}, done={self.done})"


class FakeTasksAPI:
    """Имитация REST API для задач (без реального сервера)."""

    def __init__(self) -> None:
        self._tasks: dict[int, FakeTask] = {}
        self._next_id = 1

    # POST /tasks
    def create(self, title: str, description: str = "") -> tuple[int, dict]:
        """Создать задачу → 201 Created."""
        task = FakeTask(self._next_id, title, description)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return 201, task.to_dict()

    # GET /tasks
    def list_all(self) -> tuple[int, list[dict]]:
        """Получить все задачи → 200 OK."""
        return 200, [t.to_dict() for t in self._tasks.values()]

    # GET /tasks/{id}
    def get(self, task_id: int) -> tuple[int, dict]:
        """Получить задачу по ID → 200 или 404."""
        if task_id not in self._tasks:
            return 404, {"detail": f"Task {task_id} not found"}
        return 200, self._tasks[task_id].to_dict()

    # PATCH /tasks/{id}
    def update(self, task_id: int, **fields: object) -> tuple[int, dict]:
        """Частично обновить задачу → 200 или 404."""
        if task_id not in self._tasks:
            return 404, {"detail": f"Task {task_id} not found"}
        task = self._tasks[task_id]
        for key, value in fields.items():
            if hasattr(task, key):
                setattr(task, key, value)
        return 200, task.to_dict()

    # DELETE /tasks/{id}
    def delete(self, task_id: int) -> tuple[int, dict]:
        """Удалить задачу → 204 или 404."""
        if task_id not in self._tasks:
            return 404, {"detail": f"Task {task_id} not found"}
        del self._tasks[task_id]
        return 204, {}


def demo_rest_api() -> None:
    """Демонстрация CRUD-операций через симуляцию REST API."""
    print("Симуляция REST API для задач (TODO)")
    print("=" * 50)
    api = FakeTasksAPI()

    # POST /tasks — создать
    status, body = api.create("Купить продукты", "Молоко, хлеб")
    print(f"POST /tasks → {status}: {body}")

    status, body = api.create("Прочитать книгу", "Clean Code")
    print(f"POST /tasks → {status}: {body}")

    # GET /tasks — список
    status, body = api.list_all()
    print(f"\nGET /tasks → {status}: {body}")

    # GET /tasks/1 — одна задача
    status, body = api.get(1)
    print(f"\nGET /tasks/1 → {status}: {body}")

    # PATCH /tasks/1 — обновить поле done
    status, body = api.update(1, done=True)
    print(f"\nPATCH /tasks/1 (done=True) → {status}: {body}")

    # DELETE /tasks/2 — удалить
    status, body = api.delete(2)
    print(f"\nDELETE /tasks/2 → {status} (No Content)")

    # GET /tasks/99 — не найдено
    status, body = api.get(99)
    print(f"\nGET /tasks/99 → {status}: {body}")

    print()


# ============================================================
# Точка входа
# ============================================================


def main() -> None:
    """Запустить все демонстрации."""
    print("=" * 60)
    print("СЕМИНАР 9: HTTP, REST И CRUD — ПОВТОРЕНИЕ")
    print("=" * 60)
    print()

    print_crud_table()
    print_http_request_example()
    print_status_codes()
    print_rest_conventions()
    demo_rest_api()

    print("Итог: REST — это соглашение, а не стандарт.")
    print("Ключевые правила:")
    print("  1. URL — это существительные (ресурсы), не глаголы")
    print("  2. HTTP-метод — это глагол (действие)")
    print("  3. Статус-коды несут смысл — используйте их правильно")


if __name__ == "__main__":
    main()
