"""
Семинар 5: Основы Django — Model, View, Template.

Этот модуль демонстрирует:
- Как описываются модели (Model)
- Как создаются представления (View)
- Как работают шаблоны (Template)
- Связь между компонентами MVT

Примечание: этот файл содержит примеры кода Django для изучения.
Он выводит примеры на экран. Для запуска реального Django-приложения
используйте команды manage.py.
"""

# ============================================================
# 1. Модель (Model) — описание данных
# ============================================================

MODEL_EXAMPLE = """
# blog/models.py
from django.db import models


class Post(models.Model):
    \"\"\"Модель поста блога.\"\"\"

    title = models.CharField(max_length=200)          # Строка до 200 символов
    text = models.TextField()                          # Текст без ограничения
    author = models.CharField(max_length=100)          # Автор
    created_date = models.DateTimeField(auto_now_add=True)  # Авто-дата создания
    published = models.BooleanField(default=False)     # Опубликован?

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_date"]  # Сортировка по умолчанию


class Comment(models.Model):
    \"\"\"Модель комментария к посту.\"\"\"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author_name = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author_name} к '{self.post.title}'"
"""

# ============================================================
# 2. Работа с ORM — запросы к базе данных
# ============================================================

ORM_EXAMPLES = """
# Работа с Django ORM (в manage.py shell или в views.py)

# --- Создание объектов ---
post = Post.objects.create(
    title="Первый пост",
    text="Привет, мир!",
    author="Алиса",
    published=True,
)

# --- Чтение объектов ---
# Все посты
all_posts = Post.objects.all()

# Фильтрация
published = Post.objects.filter(published=True)
alice_posts = Post.objects.filter(author="Алиса")

# Один объект
post = Post.objects.get(pk=1)  # По первичному ключу

# Сортировка
recent = Post.objects.order_by("-created_date")

# Ограничение количества
top_5 = Post.objects.all()[:5]

# --- Обновление ---
post.title = "Обновлённый заголовок"
post.save()

# Массовое обновление
Post.objects.filter(author="Алиса").update(published=True)

# --- Удаление ---
post.delete()
Post.objects.filter(published=False).delete()
"""

# ============================================================
# 3. Представления (Views) — обработка запросов
# ============================================================

VIEWS_EXAMPLE = """
# blog/views.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post


# --- Простейший View ---
def hello(request):
    return HttpResponse("Привет, мир!")


# --- View со списком объектов ---
def post_list(request):
    \"\"\"Список всех опубликованных постов.\"\"\"
    posts = Post.objects.filter(published=True).order_by("-created_date")
    return render(request, "blog/post_list.html", {"posts": posts})


# --- View с одним объектом ---
def post_detail(request, pk):
    \"\"\"Детальная страница поста.\"\"\"
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


# --- View, возвращающий JSON ---
def api_posts(request):
    \"\"\"API: список постов в формате JSON.\"\"\"
    posts = Post.objects.filter(published=True).values(
        "id", "title", "author", "created_date"
    )
    return JsonResponse(list(posts), safe=False)
"""

# ============================================================
# 4. URL-маршрутизация
# ============================================================

URLS_EXAMPLE = """
# === mysite/urls.py (корневой) ===
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),          # Админ-панель: /admin/
    path("blog/", include("blog.urls")),      # Все URL блога: /blog/...
]


# === blog/urls.py (приложение) ===
from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    # GET /blog/ → views.post_list

    path("<int:pk>/", views.post_detail, name="post_detail"),
    # GET /blog/1/ → views.post_detail(request, pk=1)

    path("api/", views.api_posts, name="api_posts"),
    # GET /blog/api/ → views.api_posts
]
"""

# ============================================================
# 5. Шаблоны (Templates) — отображение данных
# ============================================================

TEMPLATE_LIST_EXAMPLE = """
<!-- blog/templates/blog/post_list.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Блог</title>
</head>
<body>
    <h1>Мой блог</h1>

    {% if posts %}
        {% for post in posts %}
            <article>
                <h2>
                    <a href="{% url 'post_detail' pk=post.pk %}">
                        {{ post.title }}
                    </a>
                </h2>
                <p class="meta">
                    Автор: {{ post.author }} |
                    Дата: {{ post.created_date|date:"d.m.Y H:i" }}
                </p>
                <p>{{ post.text|truncatewords:30 }}</p>
            </article>
            <hr>
        {% endfor %}
    {% else %}
        <p>Постов пока нет.</p>
    {% endif %}
</body>
</html>
"""

TEMPLATE_DETAIL_EXAMPLE = """
<!-- blog/templates/blog/post_detail.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ post.title }}</title>
</head>
<body>
    <article>
        <h1>{{ post.title }}</h1>
        <p class="meta">
            Автор: {{ post.author }} |
            Дата: {{ post.created_date|date:"d.m.Y H:i" }}
        </p>
        <div>{{ post.text|linebreaks }}</div>
    </article>

    <h3>Комментарии ({{ post.comments.count }}):</h3>
    {% for comment in post.comments.all %}
        <div>
            <strong>{{ comment.author_name }}</strong>
            <span>{{ comment.created_date|date:"d.m.Y" }}</span>
            <p>{{ comment.text }}</p>
        </div>
    {% empty %}
        <p>Комментариев пока нет.</p>
    {% endfor %}

    <a href="{% url 'post_list' %}">← Назад к списку</a>
</body>
</html>
"""

# ============================================================
# 6. Синтаксис шаблонов Django (DTL)
# ============================================================

TEMPLATE_SYNTAX = """
=== Основной синтаксис Django Template Language ===

--- Переменные ---
{{ variable }}                       # Вывод переменной
{{ user.name }}                      # Доступ к атрибуту
{{ items.0 }}                        # Доступ по индексу
{{ dict.key }}                       # Доступ по ключу

--- Фильтры ---
{{ name|upper }}                     # АЛИСА
{{ name|lower }}                     # алиса
{{ text|truncatewords:20 }}          # Обрезать до 20 слов
{{ text|linebreaks }}                # Перевод строк → <p> и <br>
{{ date|date:"d.m.Y" }}             # Формат даты: 02.03.2026
{{ list|length }}                    # Количество элементов
{{ value|default:"Не указано" }}     # Значение по умолчанию

--- Теги ---
{% if condition %}                   # Условие
    ...
{% elif other %}
    ...
{% else %}
    ...
{% endif %}

{% for item in list %}               # Цикл
    {{ forloop.counter }}. {{ item }}
{% empty %}                          # Если список пуст
    Нет элементов
{% endfor %}

{% url 'name' arg1 arg2 %}          # URL по имени маршрута
{% url 'post_detail' pk=post.pk %}   # URL с параметром

{# Это комментарий #}               # Комментарий в шаблоне
"""


# ============================================================
# 7. Регистрация модели в админке
# ============================================================

ADMIN_EXAMPLE = """
# blog/admin.py
from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_date", "published"]
    list_filter = ["published", "author"]
    search_fields = ["title", "text"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author_name", "post", "created_date"]
    list_filter = ["created_date"]
"""


# ============================================================
# Функции демонстрации
# ============================================================


def demonstrate_model() -> None:
    """Демонстрация модели Django."""
    print("=" * 60)
    print("1. Модель (Model) — описание данных")
    print("=" * 60)
    print(MODEL_EXAMPLE)

    print("\n  Типы полей Django:")
    fields = [
        ("CharField(max_length=N)", "Строка ограниченной длины"),
        ("TextField()", "Текст без ограничения"),
        ("IntegerField()", "Целое число"),
        ("FloatField()", "Число с плавающей точкой"),
        ("BooleanField()", "True / False"),
        ("DateTimeField()", "Дата и время"),
        ("DateField()", "Только дата"),
        ("EmailField()", "Email (с валидацией)"),
        ("URLField()", "URL (с валидацией)"),
        ("ForeignKey(Model)", "Связь «многие к одному»"),
        ("ManyToManyField(Model)", "Связь «многие ко многим»"),
    ]
    for field_type, description in fields:
        print(f"    {field_type:30s} — {description}")


def demonstrate_orm() -> None:
    """Демонстрация Django ORM."""
    print("\n" + "=" * 60)
    print("2. Django ORM — запросы к базе данных")
    print("=" * 60)
    print(ORM_EXAMPLES)


def demonstrate_views() -> None:
    """Демонстрация представлений Django."""
    print("\n" + "=" * 60)
    print("3. Представления (Views)")
    print("=" * 60)
    print(VIEWS_EXAMPLE)


def demonstrate_urls() -> None:
    """Демонстрация маршрутизации Django."""
    print("\n" + "=" * 60)
    print("4. URL-маршрутизация")
    print("=" * 60)
    print(URLS_EXAMPLE)


def demonstrate_templates() -> None:
    """Демонстрация шаблонов Django."""
    print("\n" + "=" * 60)
    print("5. Шаблоны (Templates)")
    print("=" * 60)

    print("\n--- Шаблон списка постов ---")
    print(TEMPLATE_LIST_EXAMPLE)

    print("\n--- Шаблон детальной страницы ---")
    print(TEMPLATE_DETAIL_EXAMPLE)

    print("\n--- Синтаксис шаблонов ---")
    print(TEMPLATE_SYNTAX)


def demonstrate_admin() -> None:
    """Демонстрация админ-панели Django."""
    print("\n" + "=" * 60)
    print("6. Админ-панель")
    print("=" * 60)
    print(ADMIN_EXAMPLE)

    print("  Для доступа к админ-панели:")
    print("    1. python manage.py createsuperuser")
    print("    2. python manage.py runserver")
    print("    3. Открыть http://127.0.0.1:8000/admin/")


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 5: ОСНОВЫ DJANGO — MODEL, VIEW, TEMPLATE")
    print("=" * 60)

    demonstrate_model()
    demonstrate_orm()
    demonstrate_views()
    demonstrate_urls()
    demonstrate_templates()
    demonstrate_admin()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
