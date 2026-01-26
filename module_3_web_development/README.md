# Модуль 3: Сбор данных и разработка веб-приложений

## Описание

Третий модуль курса посвящен разработке веб-приложений с использованием Django и FastAPI, а также методам сбора данных из различных источников.

## Темы

### 1. Основы веб-разработки
- HTTP протокол (методы, заголовки, коды ответа)
- REST API принципы
- Client-Server архитектура
- Асинхронное программирование в Python
- `asyncio` и `async/await`

### 2. Django Framework
- Установка и настройка Django
- Модели (Models) и ORM
- Представления (Views)
- Шаблоны (Templates)
- URL маршрутизация
- Django Admin
- Формы и валидация
- Миграции базы данных
- Django REST Framework (DRF)
- Аутентификация и авторизация

### 3. FastAPI Framework
- Установка и настройка FastAPI
- Определение эндпоинтов
- Path и Query параметры
- Request и Response модели (Pydantic)
- Валидация данных
- Асинхронные операции
- Документация API (Swagger/OpenAPI)
- Dependency Injection
- Middleware

### 4. Работа с базами данных
- SQL основы
- SQLite, PostgreSQL
- ORM (SQLAlchemy, Django ORM)
- Миграции
- NoSQL базы данных (MongoDB)
- Redis для кэширования

### 5. Веб-скрапинг и сбор данных
- Requests библиотека
- BeautifulSoup
- Selenium для динамических сайтов
- Scrapy framework
- API клиенты
- Этика веб-скрапинга
- Rate limiting и robots.txt

### 6. Работа с API
- Создание REST API
- Документирование API
- Версионирование API
- Тестирование API
- GraphQL (введение)

### 7. Deployment и Production
- Docker контейнеризация
- Environment variables
- Logging
- CORS
- Безопасность (CSRF, XSS, SQL Injection)

## Структура модуля

```
module_3_web_development/
├── README.md (этот файл)
├── django_app/        # Примеры Django приложений
├── fastapi_app/       # Примеры FastAPI приложений
├── examples/          # Дополнительные примеры
└── homework/          # Домашние задания
```

## Практические задания

### Django проекты
- Создание блога
- REST API для управления задачами
- Система аутентификации

### FastAPI проекты
- REST API для микросервиса
- Асинхронная обработка данных
- Интеграция с внешними API

### Веб-скрапинг
- Сбор данных с новостных сайтов
- Парсинг прогноза погоды
- Автоматизация сбора данных

## Домашние задания

Домашние задания включают:
- Полноценное веб-приложение на Django
- REST API на FastAPI
- Проект по сбору и обработке данных

## Ресурсы

### Django
- [Официальная документация Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)

### FastAPI
- [Официальная документация FastAPI](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### Веб-скрапинг
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Scrapy Documentation](https://docs.scrapy.org/)
- [Requests Documentation](https://requests.readthedocs.io/)

## Требования для выполнения

- Python 3.10+
- PostgreSQL (опционально)
- Docker (опционально, но рекомендуется)
- Postman или аналог для тестирования API

## Установка зависимостей

```bash
# Django
pip install django djangorestframework

# FastAPI
pip install fastapi uvicorn pydantic

# Веб-скрапинг
pip install requests beautifulsoup4 selenium scrapy

# База данных
pip install psycopg2-binary sqlalchemy
```

## Дополнительно

Рекомендуется изучить:
- RESTful API Design
- Асинхронное программирование
- Docker и контейнеризация
