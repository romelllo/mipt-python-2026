# Примеры Django приложений

Эта директория содержит примеры Django проектов.

## Быстрый старт

### Создание Django проекта

```bash
# Установить Django
pip install django

# Создать новый проект
django-admin startproject myproject

# Перейти в директорию проекта
cd myproject

# Создать приложение
python manage.py startapp myapp

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер разработки
python manage.py runserver
```

Приложение будет доступно по адресу: http://localhost:8000
Админ-панель: http://localhost:8000/admin

## Структура Django проекта

```
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── myapp/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── tests.py
    └── migrations/
```

## Основные концепции

### Models (Модели)
Определяют структуру базы данных.

```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Views (Представления)
Обрабатывают запросы и возвращают ответы.

```python
from django.shortcuts import render

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles.html', {'articles': articles})
```

### URLs (Маршруты)
Определяют соответствие URL и представлений.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
]
```

## Ресурсы

- [Официальный туториал Django](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
