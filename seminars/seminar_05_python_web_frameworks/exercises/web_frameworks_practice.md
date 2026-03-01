# Практические задания: Python и веб-фреймворки

## Подготовка

```bash
# Активируйте виртуальное окружение
source .venv/bin/activate  # Linux/Mac

# Убедитесь, что Django установлен
python -c "import django; print(django.get_version())"

# Запустите примеры для ознакомления
python seminars/seminar_05_python_web_frameworks/examples/01_backend_frontend_api.py
python seminars/seminar_05_python_web_frameworks/examples/02_frameworks_comparison.py
python seminars/seminar_05_python_web_frameworks/examples/03_django_structure.py
python seminars/seminar_05_python_web_frameworks/examples/04_django_mvt_basics.py
```

> **Как работать с заданиями:** прочитайте условие, попробуйте решить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: Бэкенд, фронтенд и API

> **Теория:** [README.md — Блок 1](../README.md#блок-1-бэкенд-фронтенд-и-api-10-мин) | **Примеры:** [`examples/01_backend_frontend_api.py`](../examples/01_backend_frontend_api.py)

### Задание 1.1

Для каждого действия определите, на какой стороне оно выполняется — **фронтенд** или **бэкенд**:

| Действие | Фронтенд / Бэкенд? |
|----------|---------------------|
| Отображение кнопки «Купить» | ? |
| Проверка пароля пользователя в базе данных | ? |
| Анимация появления меню | ? |
| Отправка email после регистрации | ? |
| Проверка формата email в поле ввода | ? |
| Запись заказа в базу данных | ? |

<details>
<summary>Решение</summary>

| Действие | Сторона |
|----------|---------|
| Отображение кнопки «Купить» | **Фронтенд** — отображение UI-элементов |
| Проверка пароля в БД | **Бэкенд** — работа с базой данных |
| Анимация появления меню | **Фронтенд** — визуальные эффекты |
| Отправка email после регистрации | **Бэкенд** — серверная операция |
| Проверка формата email в поле ввода | **Фронтенд** — клиентская валидация (но бэкенд тоже должен проверять!) |
| Запись заказа в базу данных | **Бэкенд** — работа с БД |

</details>

---

### Задание 1.2

Спроектируйте REST API для приложения **«Библиотека»**. Для сущности «Книга» (Book) напишите таблицу с маршрутами: HTTP-метод, URL, описание действия.

<details>
<summary>Подсказка</summary>

Вспомните CRUD-операции: Create, Read (список и одна запись), Update, Delete. Для каждой операции подберите HTTP-метод и URL.

</details>

<details>
<summary>Решение</summary>

| Метод | URL | Действие |
|-------|-----|----------|
| GET | `/api/books` | Получить список всех книг |
| GET | `/api/books/1` | Получить книгу с ID=1 |
| POST | `/api/books` | Добавить новую книгу |
| PUT | `/api/books/1` | Обновить книгу с ID=1 |
| DELETE | `/api/books/1` | Удалить книгу с ID=1 |

Дополнительно можно добавить:

| Метод | URL | Действие |
|-------|-----|----------|
| GET | `/api/books?author=Пушкин` | Поиск книг по автору |
| GET | `/api/books/1/reviews` | Отзывы на книгу |
| POST | `/api/books/1/reviews` | Добавить отзыв |

</details>

---

## Часть 2: Обзор веб-фреймворков Python

> **Теория:** [README.md — Блок 2](../README.md#блок-2-обзор-веб-фреймворков-python-15-мин) | **Примеры:** [`examples/02_frameworks_comparison.py`](../examples/02_frameworks_comparison.py)

### Задание 2.1

Для каждой ситуации выберите наиболее подходящий фреймворк (Flask, Django или FastAPI) и объясните почему:

1. Нужно создать REST API для мобильного приложения с автоматической документацией
2. Нужен сайт интернет-магазина с каталогом товаров, корзиной, личным кабинетом и админкой
3. Нужен простой одностраничный сайт-визитка для запуска за пару часов
4. Нужен высокопроизводительный API для обработки данных в реальном времени

<details>
<summary>Решение</summary>

1. **FastAPI** — автоматическая документация (Swagger), валидация данных через Pydantic, хорошо подходит для API-сервисов.

2. **Django** — встроенная ORM для каталога товаров, система авторизации для личного кабинета, админ-панель для управления контентом.

3. **Flask** — минимальная настройка, быстрый старт, для простого проекта не нужны «батарейки» Django.

4. **FastAPI** — нативная поддержка async/await, высокая производительность, идеален для обработки в реальном времени.

</details>

---

### Задание 2.2

Заполните таблицу, отметив, какой функционал есть «из коробки» в каждом фреймворке:

| Функционал | Flask | Django | FastAPI |
|------------|-------|--------|---------|
| ORM (работа с БД) | ? | ? | ? |
| Админ-панель | ? | ? | ? |
| Авторизация пользователей | ? | ? | ? |
| Автодокументация API | ? | ? | ? |
| HTML-шаблоны | ? | ? | ? |
| Валидация данных | ? | ? | ? |

<details>
<summary>Решение</summary>

| Функционал | Flask | Django | FastAPI |
|------------|-------|--------|---------|
| ORM (работа с БД) | Нет (SQLAlchemy отдельно) | **Да** (Django ORM) | Нет (SQLAlchemy отдельно) |
| Админ-панель | Нет | **Да** | Нет |
| Авторизация пользователей | Нет (расширения) | **Да** | Нет (библиотеки) |
| Автодокументация API | Нет (расширения) | Нет (DRF отдельно) | **Да** (Swagger + ReDoc) |
| HTML-шаблоны | **Да** (Jinja2) | **Да** (DTL) | Нет (не предназначен) |
| Валидация данных | Нет (расширения) | **Да** (формы) | **Да** (Pydantic) |

</details>

---

## Часть 3: Структура Django-проекта

> **Теория:** [README.md — Блок 3](../README.md#блок-3-структура-django-проекта-25-мин) | **Примеры:** [`examples/03_django_structure.py`](../examples/03_django_structure.py)

### Задание 3.1

Создайте Django-проект и приложение. Выполните следующие шаги в терминале:

1. Перейдите во временную директорию (например, `/tmp` или рабочий стол)
2. Создайте проект с именем `mysite`
3. Создайте приложение с именем `blog`
4. Запустите сервер разработки
5. Откройте в браузере `http://127.0.0.1:8000/` и убедитесь, что видите стартовую страницу Django

<details>
<summary>Подсказка</summary>

Используйте команды: `django-admin startproject`, `python manage.py startapp`, `python manage.py runserver`.

</details>

<details>
<summary>Решение</summary>

```bash
# 1. Перейдите в подходящую директорию
cd /tmp

# 2. Создайте проект
django-admin startproject mysite
cd mysite

# 3. Создайте приложение
python manage.py startapp blog

# 4. Запустите сервер разработки
python manage.py runserver

# 5. Откройте в браузере: http://127.0.0.1:8000/
# Вы увидите страницу "The install worked successfully!"
```

Для остановки сервера нажмите `Ctrl+C`.

</details>

---

### Задание 3.2

Для каждого файла Django-проекта укажите его назначение:

| Файл | Назначение |
|------|------------|
| `manage.py` | ? |
| `settings.py` | ? |
| `urls.py` | ? |
| `models.py` | ? |
| `views.py` | ? |
| `admin.py` | ? |
| `migrations/` | ? |

<details>
<summary>Решение</summary>

| Файл | Назначение |
|------|------------|
| `manage.py` | Утилита управления проектом (запуск сервера, миграции и т.д.) |
| `settings.py` | Настройки проекта (БД, приложения, язык, пути) |
| `urls.py` | Маршрутизация — связь URL-путей с функциями-обработчиками |
| `models.py` | Описание моделей данных (таблиц БД) |
| `views.py` | Представления — обработчики HTTP-запросов |
| `admin.py` | Регистрация моделей в админ-панели |
| `migrations/` | Автогенерируемые файлы миграций БД |

</details>

---

## Часть 4: Основы Django — модель, view, шаблон

> **Теория:** [README.md — Блок 4](../README.md#блок-4-основы-django--модель-view-шаблон-30-мин) | **Примеры:** [`examples/04_django_mvt_basics.py`](../examples/04_django_mvt_basics.py)

### Задание 4.1

Создайте модель `Post` для блога (продолжая проект из задания 3.3):

1. Определите модель `Post` в `blog/models.py` с полями:
   - `title` — заголовок (строка до 200 символов)
   - `text` — текст поста (текстовое поле)
   - `author` — автор (строка до 100 символов)
   - `created_date` — дата создания (автоматическая)
2. Создайте и примените миграции
3. Зарегистрируйте модель в админ-панели (`admin.py`)
4. Создайте суперпользователя и добавьте через админку 2-3 поста

<details>
<summary>Подсказка</summary>

Используйте `models.CharField`, `models.TextField`, `models.DateTimeField(auto_now_add=True)`. Для миграций: `python manage.py makemigrations` и `python manage.py migrate`.

</details>

<details>
<summary>Решение</summary>

```python
# blog/models.py
from django.db import models


class Post(models.Model):
    """Модель поста блога."""

    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

```python
# blog/admin.py
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

```bash
# Создать и применить миграции
python manage.py makemigrations
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер и перейти в http://127.0.0.1:8000/admin/
python manage.py runserver
```

</details>

---

### Задание 4.2

Создайте view и шаблон для отображения списка постов:

1. Создайте view-функцию `post_list` в `blog/views.py`
2. Создайте шаблон `blog/templates/blog/post_list.html`
3. Обновите `blog/urls.py`, чтобы маршрут `/blog/` вызывал `post_list`
4. Откройте в браузере и убедитесь, что посты отображаются

<details>
<summary>Подсказка</summary>

View должен получить посты через `Post.objects.all()` и передать их в шаблон через `render()`. В шаблоне используйте цикл `{% for post in posts %}`.

</details>

<details>
<summary>Решение</summary>

```python
# blog/views.py
from django.shortcuts import render
from .models import Post


def post_list(request):
    """Список всех постов."""
    posts = Post.objects.all().order_by("-created_date")
    return render(request, "blog/post_list.html", {"posts": posts})
```

Создайте директорию `blog/templates/blog/` и файл `post_list.html`:

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
            <p><small>Автор: {{ post.author }} | {{ post.created_date|date:"d.m.Y H:i" }}</small></p>
            <p>{{ post.text|truncatewords:30 }}</p>
        </div>
        <hr>
    {% empty %}
        <p>Постов пока нет.</p>
    {% endfor %}
</body>
</html>
```

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
]
```

```bash
# Запустить сервер и проверить http://127.0.0.1:8000/blog/
python manage.py runserver
```

</details>

---

### Задание 4.3

Создайте страницу детального просмотра поста:

1. Создайте view-функцию `post_detail` в `blog/views.py`
2. Создайте шаблон `blog/templates/blog/post_detail.html`
3. Добавьте маршрут в `blog/urls.py` для URL вида `/blog/1/`
4. В шаблоне списка постов добавьте ссылки на детальные страницы

<details>
<summary>Подсказка</summary>

Используйте `get_object_or_404(Post, pk=pk)` для получения поста. В `urls.py` используйте `<int:pk>/` для захвата ID. Для ссылок в шаблоне: `{% url 'post_detail' pk=post.pk %}`.

</details>

<details>
<summary>Решение</summary>

```python
# blog/views.py (добавить функцию)
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

```html
<!-- blog/templates/blog/post_detail.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ post.title }}</title>
</head>
<body>
    <h1>{{ post.title }}</h1>
    <p><small>Автор: {{ post.author }} | {{ post.created_date|date:"d.m.Y H:i" }}</small></p>
    <div>{{ post.text|linebreaks }}</div>
    <hr>
    <a href="{% url 'post_list' %}">← Назад к списку</a>
</body>
</html>
```

Обновите шаблон списка, добавив ссылки:

```html
<!-- В post_list.html замените <h2> на: -->
<h2><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h2>
```

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
]
```

</details>

---

## Бонусные задания

### Бонус 1: API для постов

Добавьте в приложение `blog` view-функцию `api_posts`, которая возвращает список постов в формате JSON. Маршрут: `/blog/api/`.

<details>
<summary>Подсказка</summary>

Используйте `JsonResponse` из `django.http`. Метод `.values()` у QuerySet позволяет выбрать конкретные поля.

</details>

<details>
<summary>Решение</summary>

```python
# blog/views.py (добавить)
from django.http import JsonResponse


def api_posts(request):
    """API: список постов в формате JSON."""
    posts = Post.objects.all().order_by("-created_date").values(
        "id", "title", "author", "created_date"
    )
    return JsonResponse(list(posts), safe=False)
```

```python
# blog/urls.py (добавить маршрут)
urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("api/", views.api_posts, name="api_posts"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
]
```

Проверьте в браузере: `http://127.0.0.1:8000/blog/api/` — должен вернуться JSON.

</details>

---

### Бонус 2: Счётчик постов в шаблоне

Добавьте в шаблон списка постов:
- Общее количество постов
- Нумерацию постов в цикле (1, 2, 3...)

<details>
<summary>Подсказка</summary>

Для подсчёта используйте фильтр `{{ posts|length }}`. Для нумерации в цикле — переменную `{{ forloop.counter }}`.

</details>

<details>
<summary>Решение</summary>

```html
<!-- blog/templates/blog/post_list.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Блог</title>
</head>
<body>
    <h1>Мой блог</h1>
    <p>Всего постов: {{ posts|length }}</p>

    {% for post in posts %}
        <div>
            <h2>{{ forloop.counter }}. <a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h2>
            <p><small>Автор: {{ post.author }} | {{ post.created_date|date:"d.m.Y H:i" }}</small></p>
            <p>{{ post.text|truncatewords:30 }}</p>
        </div>
        <hr>
    {% empty %}
        <p>Постов пока нет.</p>
    {% endfor %}
</body>
</html>
```

</details>

---

## Полезные ресурсы

- [Django Documentation](https://docs.djangoproject.com/) — официальная документация Django
- [Django Tutorial](https://docs.djangoproject.com/en/5.0/intro/tutorial01/) — пошаговый туториал
- [FastAPI Documentation](https://fastapi.tiangolo.com/) — документация FastAPI
- [Django Girls Tutorial](https://tutorial.djangogirls.org/ru/) — отличный туториал на русском
- [REST API Tutorial](https://restfulapi.net/) — что такое REST
