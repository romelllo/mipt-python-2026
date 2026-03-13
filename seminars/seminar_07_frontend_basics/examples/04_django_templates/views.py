"""
Семинар 7: Пример Django-view для отображения меню.

Этот файл — фрагмент cafe/views.py.
View получает данные из БД и передаёт их в шаблон menu_list.html.

Ключевые концепции:
- render() — рендерит шаблон с контекстом и возвращает HttpResponse
- context — словарь переменных, доступных в шаблоне
- request.GET — параметры GET-запроса (?category=1)
"""

# Импортируем модели из нашего приложения
from cafe.models import Category, MenuItem
from django.shortcuts import render


def menu_list(request):
    """Отобразить список позиций меню с фильтрацией по категориям.

    GET-параметры:
        category (int, optional): ID категории для фильтрации

    Шаблон: cafe/templates/cafe/menu_list.html

    Контекст:
        menu_items: QuerySet позиций меню
        categories: QuerySet всех категорий
        selected_category: ID выбранной категории (или None)
    """
    # Получаем все категории для кнопок фильтра
    categories = Category.objects.all()

    # Получаем параметр ?category= из URL, если есть
    # request.GET — словарь QueryDict с GET-параметрами
    category_id = request.GET.get("category")

    # Фильтруем позиции меню
    if category_id:
        menu_items = MenuItem.objects.filter(category_id=category_id).select_related(
            "category"
        )
        # select_related("category") — загружает категорию одним JOIN-запросом
        # (без него каждое обращение к item.category делает отдельный SQL-запрос)
        selected_category = int(category_id)
    else:
        menu_items = MenuItem.objects.all().select_related("category")
        selected_category = None

    # render(request, template_name, context) — главная функция для рендеринга
    # context — словарь: ключи становятся переменными в шаблоне
    return render(
        request,
        "cafe/menu_list.html",
        {
            "menu_items": menu_items,  # {{ menu_items }} в шаблоне
            "categories": categories,  # {{ categories }} в шаблоне
            "selected_category": selected_category,  # {{ selected_category }}
        },
    )
