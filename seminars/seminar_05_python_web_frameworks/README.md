# Семинар 5: Python и веб-фреймворки

**Модуль:** 3 — Создание Web-сервисов на Python  
**Дата:** 02.03.2026  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/195l5wB501Xb2Ct6RFZtgNMpptgr4cYPPZ0RiT5MkxI4/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:
- Объяснять разницу между бэкендом и фронтендом
- Понимать, что такое API и зачем оно нужно
- Сравнивать веб-фреймворки Python (Flask, Django, FastAPI) и понимать, когда какой выбрать
- Создавать Django-проект и понимать его структуру
- Описывать модели, представления (views), шаблоны (templates) и маршрутизацию в Django

---

## Подготовка

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# Установите зависимости (если ещё не установлены)
uv sync

# Проверьте, что Django установлен
python -c "import django; print(django.get_version())"
```

---

## План семинара

| Время | Тема | Практика |
|-------|------|----------|
| 10 мин | Блок 1: Бэкенд, фронтенд и API | → Упражнения: Часть 1 |
| 15 мин | Блок 2: Обзор веб-фреймворков Python | → Упражнения: Часть 2 |
| 25 мин | Блок 3: Структура Django-проекта | → Упражнения: Часть 3 |
| 30 мин | Блок 4: Основы Django — модель, view, шаблон | → Упражнения: Часть 4 |
| 10 мин | Подведение итогов | — |

**Итого:** ~90 минут

> Семинар построен по принципу **«теория → практика»**: после каждого блока теории студенты переходят к соответствующим упражнениям.

---

## Блок 1: Бэкенд, фронтенд и API (10 мин)

### Что такое фронтенд и бэкенд?

Веб-приложение состоит из двух частей:

```
┌──────────────────────────────────────────────────────────┐
│                    Веб-приложение                         │
│                                                          │
│  ┌─────────────────┐        ┌─────────────────────────┐  │
│  │    Фронтенд     │  HTTP  │       Бэкенд            │  │
│  │   (клиент)      │ ◄────► │      (сервер)           │  │
│  │                 │        │                         │  │
│  │ - HTML/CSS/JS   │        │ - Бизнес-логика         │  │
│  │ - Интерфейс     │        │ - Работа с БД           │  │
│  │ - Отображение   │        │ - Авторизация           │  │
│  │   данных        │        │ - Обработка запросов    │  │
│  └─────────────────┘        └─────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**Фронтенд** — то, что видит пользователь в браузере: кнопки, формы, анимации. Технологии: HTML, CSS, JavaScript, React, Vue.

**Бэкенд** — серверная часть, которая обрабатывает запросы, хранит данные и выполняет бизнес-логику. Технологии: Python, Java, Go, Node.js и др.

### Что такое API?

**API** (Application Programming Interface) — набор правил, по которым программы общаются друг с другом.

**Web API** — API, доступный по сети через HTTP. Клиент отправляет HTTP-запрос, сервер возвращает ответ (обычно в формате JSON).

```
Клиент                              Сервер
  │                                    │
  │  GET /api/users HTTP/1.1           │
  │ ──────────────────────────────►    │
  │                                    │
  │  HTTP/1.1 200 OK                   │
  │  [{"id": 1, "name": "Alice"}]      │
  │ ◄──────────────────────────────    │
  │                                    │
```

**REST API** — самый популярный стиль проектирования API:
- Ресурсы имеют URL: `/api/users`, `/api/orders/42`
- HTTP-методы определяют действие: GET (читать), POST (создать), PUT (обновить), DELETE (удалить)
- Ответы обычно в формате JSON

Пример REST API для магазина:

| Метод | URL | Действие |
|-------|-----|----------|
| GET | `/api/products` | Получить список товаров |
| GET | `/api/products/1` | Получить товар с ID=1 |
| POST | `/api/products` | Создать новый товар |
| PUT | `/api/products/1` | Обновить товар с ID=1 |
| DELETE | `/api/products/1` | Удалить товар с ID=1 |

> **Подробнее:** см. файл [`examples/01_backend_frontend_api.py`](examples/01_backend_frontend_api.py) — примеры запросов к публичным API.

### Практика

Перейдите к файлу [`exercises/web_frameworks_practice.md`](exercises/web_frameworks_practice.md) и выполните **Часть 1: Бэкенд, фронтенд и API** (задания 1.1–1.2).

---

## Блок 2: Обзор веб-фреймворков Python (15 мин)

### Основные фреймворки

В экосистеме Python есть три главных веб-фреймворка:

#### Flask — микрофреймворк

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
```

**Характеристики Flask:**
- Минималистичный: только маршрутизация + шаблоны «из коробки»
- Всё остальное — через расширения (ORM, формы, авторизация)
- Хорошо подходит для небольших проектов и микросервисов
- Синхронный (есть async-поддержка с Flask 2.0, но ограниченная)

#### Django — «батарейки в комплекте»

```python
# views.py
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, World!")
```

**Характеристики Django:**
- Полноценный фреймворк: ORM, админ-панель, формы, авторизация, миграции
- Подход «batteries included» — всё нужное уже есть
- Идеален для больших проектов с базой данных
- Синхронный (async-поддержка с Django 4.1, развивается)

#### FastAPI — современный асинхронный фреймворк

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, World!"}
```

**Характеристики FastAPI:**
- Автоматическая валидация данных через Pydantic
- Автогенерация документации (Swagger UI, ReDoc)
- Нативная поддержка async/await
- Высокая производительность
- Идеален для API-сервисов

### Сравнение фреймворков

| Критерий | Flask | Django | FastAPI |
|----------|-------|--------|---------|
| Тип | Микрофреймворк | Полный фреймворк | API-фреймворк |
| ORM | Нет (SQLAlchemy) | Встроенный | Нет (SQLAlchemy) |
| Админ-панель | Нет | Встроенная | Нет |
| Валидация | Расширения | Встроенная | Pydantic |
| Документация API | Расширения | DRF (расширение) | Автоматическая |
| Async | Ограниченный | Развивается | Нативный |
| Шаблоны (HTML) | Jinja2 | Встроенные (DTL) | Не предназначен |
| Сложность изучения | Низкая | Средняя | Низкая |
| Подходит для | Небольшие проекты | Большие проекты | API-сервисы |

### Что используем в курсе?

В нашем курсе мы изучим **Django** и **FastAPI** — два наиболее востребованных фреймворка:

- **Django** — для полноценных веб-приложений с HTML-страницами, базой данных и админ-панелью (семинары 5–8)
- **FastAPI** — для создания REST API сервисов (семинары 9–12)

Flask мы не используем, но он полезен для понимания общих принципов — и если вы знаете Django и FastAPI, освоить Flask не составит труда.

> **Подробнее:** см. файл [`examples/02_frameworks_comparison.py`](examples/02_frameworks_comparison.py) — минимальные примеры на каждом фреймворке.

### Практика

Перейдите к файлу [`exercises/web_frameworks_practice.md`](exercises/web_frameworks_practice.md) и выполните **Часть 2: Обзор веб-фреймворков Python** (задания 2.1–2.2).

---

## Блок 3: Структура Django-проекта (25 мин)

### Создание проекта

Django предоставляет утилиту `django-admin` для генерации проекта:

```bash
# Создание проекта
django-admin startproject mysite

# Структура после создания:
mysite/
├── manage.py               # Утилита управления проектом
└── mysite/                 # Пакет настроек проекта
    ├── __init__.py
    ├── settings.py         # Настройки проекта
    ├── urls.py             # Корневой файл маршрутов
    ├── asgi.py             # Точка входа для ASGI-серверов
    └── wsgi.py             # Точка входа для WSGI-серверов
```

### Создание приложения

Django-проект состоит из **приложений** (apps). Каждое приложение отвечает за свою часть функциональности:

```bash
# Создание приложения
python manage.py startapp blog

# Структура приложения:
blog/
├── __init__.py
├── admin.py              # Регистрация моделей в админ-панели
├── apps.py               # Конфигурация приложения
├── migrations/           # Миграции базы данных
│   └── __init__.py
├── models.py             # Модели (таблицы БД)
├── tests.py              # Тесты
└── views.py              # Представления (обработка запросов)
```

### Ключевые файлы проекта

#### `settings.py` — настройки

```python
# Список установленных приложений
INSTALLED_APPS = [
    "django.contrib.admin",       # Админ-панель
    "django.contrib.auth",        # Система авторизации
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles", # Статические файлы (CSS, JS)
    "blog",                       # Наше приложение
]

# База данных (по умолчанию — SQLite)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

#### `urls.py` — маршрутизация

```python
# mysite/urls.py (корневой)
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),      # Админ-панель
    path("blog/", include("blog.urls")),  # Маршруты приложения blog
]
```

```python
# blog/urls.py (приложение)
from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),           # /blog/
    path("<int:pk>/", views.post_detail, name="post_detail"),  # /blog/1/
]
```

### Запуск сервера разработки

```bash
# Применить миграции (создать таблицы в БД)
python manage.py migrate

# Запустить сервер разработки
python manage.py runserver

# Сервер доступен по адресу: http://127.0.0.1:8000/
```

### Архитектура Django: MVT

Django использует паттерн **MVT** (Model-View-Template):

```
                 ┌──────────────────────────────────────────┐
  HTTP-запрос    │              Django                       │
  ──────────►    │                                          │
                 │  urls.py ──► View ──► Model ──► БД       │
                 │              │                 │         │
                 │              ▼                 │         │
  HTTP-ответ     │          Template ◄────────────┘         │
  ◄──────────    │              │                           │
                 │              ▼                           │
                 │           HTML-ответ                     │
                 └──────────────────────────────────────────┘
```

- **Model** — описание данных (таблицы в БД)
- **View** — логика обработки запроса (что делать?)
- **Template** — HTML-шаблон (как отобразить?)

> **Подробнее:** см. файл [`examples/03_django_structure.py`](examples/03_django_structure.py) — скрипт, демонстрирующий создание и структуру Django-проекта.

### Практика

Перейдите к файлу [`exercises/web_frameworks_practice.md`](exercises/web_frameworks_practice.md) и выполните **Часть 3: Структура Django-проекта** (задания 3.1–3.2).

---

## Блок 4: Основы Django — модель, view, шаблон (30 мин)

### Модель (Model)

Модель описывает структуру данных. Django автоматически создаёт таблицу в БД по описанию модели.

```python
# blog/models.py
from django.db import models


class Post(models.Model):
    """Модель поста блога."""
    title = models.CharField(max_length=200)          # Заголовок
    text = models.TextField()                          # Текст поста
    author = models.CharField(max_length=100)          # Автор
    created_date = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return self.title
```

**Основные типы полей:**

| Тип поля | Описание | Пример |
|----------|----------|--------|
| `CharField` | Строка (ограниченной длины) | Заголовок, имя |
| `TextField` | Текст (без ограничения) | Описание, статья |
| `IntegerField` | Целое число | Возраст, количество |
| `BooleanField` | True/False | Опубликован? |
| `DateTimeField` | Дата и время | Дата создания |
| `ForeignKey` | Связь с другой моделью | Автор поста |

После создания модели нужно создать и применить миграции:

```bash
# Создать миграцию (файл с инструкциями по изменению БД)
python manage.py makemigrations

# Применить миграцию (выполнить изменения в БД)
python manage.py migrate
```

### Представление (View)

View — это функция (или класс), которая принимает HTTP-запрос и возвращает HTTP-ответ.

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    """Список всех постов."""
    posts = Post.objects.all().order_by("-created_date")
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    """Детальная страница поста."""
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})
```

Ключевые моменты:
- `request` — объект HTTP-запроса (содержит метод, заголовки, тело и т.д.)
- `render()` — создаёт HTML-ответ из шаблона + данных (контекст)
- `get_object_or_404()` — получает объект или возвращает 404

### Шаблон (Template)

Шаблон — это HTML-файл с плейсхолдерами для данных. Django использует свой язык шаблонов (Django Template Language, DTL).

```
blog/
└── templates/
    └── blog/
        ├── post_list.html
        └── post_detail.html
```

**Плейсхолдеры и теги шаблонов:**

```html
<!-- blog/templates/blog/post_list.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Блог</title>
</head>
<body>
    <h1>Мой блог</h1>

    {% for post in posts %}
        <div>
            <h2>{{ post.title }}</h2>
            <p>Автор: {{ post.author }}</p>
            <p>{{ post.text|truncatewords:30 }}</p>
            <a href="{% url 'post_detail' pk=post.pk %}">Читать далее</a>
        </div>
    {% empty %}
        <p>Постов пока нет.</p>
    {% endfor %}
</body>
</html>
```

**Синтаксис шаблонов Django:**

| Синтаксис | Описание | Пример |
|-----------|----------|--------|
| `{{ переменная }}` | Вывод значения | `{{ post.title }}` |
| `{% тег %}` | Управляющая конструкция | `{% for item in list %}` |
| `{{ var\|фильтр }}` | Фильтр (преобразование) | `{{ text\|truncatewords:30 }}` |
| `{# комментарий #}` | Комментарий | `{# Это комментарий #}` |

**Основные теги:**

```html
<!-- Условие -->
{% if posts %}
    <p>Найдено {{ posts|length }} постов</p>
{% else %}
    <p>Постов нет</p>
{% endif %}

<!-- Цикл -->
{% for post in posts %}
    <p>{{ forloop.counter }}. {{ post.title }}</p>
{% endfor %}

<!-- Ссылка по имени маршрута -->
<a href="{% url 'post_detail' pk=post.pk %}">Читать</a>
```

### Связь всех компонентов

Полный цикл обработки запроса `GET /blog/`:

```
1. Пользователь запрашивает /blog/
2. urls.py находит маршрут → вызывает views.post_list
3. View запрашивает данные из модели Post → получает записи из БД
4. View передаёт данные в шаблон post_list.html
5. Django рендерит шаблон (подставляет данные вместо плейсхолдеров)
6. Готовый HTML возвращается пользователю
```

> **Подробнее:** см. файл [`examples/04_django_mvt_basics.py`](examples/04_django_mvt_basics.py) — полные примеры модели, view и шаблонов.

### Практика

Перейдите к файлу [`exercises/web_frameworks_practice.md`](exercises/web_frameworks_practice.md) и выполните **Часть 4: Основы Django — модель, view, шаблон** (задания 4.1–4.3).

---

## Подведение итогов

### Шпаргалка

| Концепция | Ключевое |
|-----------|----------|
| Фронтенд | Интерфейс, то что видит пользователь (HTML, CSS, JS) |
| Бэкенд | Серверная логика, работа с БД (Python, Django) |
| API | Набор правил общения между программами |
| REST API | API через HTTP: ресурсы + методы (GET, POST, PUT, DELETE) |
| Django | «Батарейки в комплекте»: ORM, админка, шаблоны |
| FastAPI | Современный async-фреймворк для API |
| Model | Описание данных (таблица в БД) |
| View | Обработка запроса (бизнес-логика) |
| Template | HTML-шаблон с плейсхолдерами |
| `manage.py` | Утилита управления Django-проектом |

### Ключевые выводы

1. **Веб-приложение = фронтенд + бэкенд**, связанные через HTTP/API.

2. **Django** — полноценный фреймворк с ORM, админкой и шаблонами. **FastAPI** — для REST API. Оба будем использовать в курсе.

3. **MVT-паттерн Django**: Model (данные) → View (логика) → Template (отображение).

---

## Файлы семинара

```
seminar_05_python_web_frameworks/
├── README.md                              # Этот файл
├── examples/
│   ├── 01_backend_frontend_api.py         # Примеры запросов к публичным API
│   ├── 02_frameworks_comparison.py        # Минимальные примеры на каждом фреймворке
│   ├── 03_django_structure.py             # Структура Django-проекта
│   └── 04_django_mvt_basics.py            # Модель, View, Template в Django
└── exercises/
    └── web_frameworks_practice.md         # Практические задания
```

---

## Дополнительные материалы

- [Django Documentation](https://docs.djangoproject.com/) — официальная документация Django
- [Django Tutorial](https://docs.djangoproject.com/en/5.0/intro/tutorial01/) — официальный туториал
- [FastAPI Documentation](https://fastapi.tiangolo.com/) — официальная документация FastAPI
- [Flask Documentation](https://flask.palletsprojects.com/) — официальная документация Flask
- [REST API Tutorial](https://restfulapi.net/) — что такое REST
- [MDN Web Docs — HTTP](https://developer.mozilla.org/ru/docs/Web/HTTP) — подробно об HTTP
