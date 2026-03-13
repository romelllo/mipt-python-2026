"""
Семинар 7: URL-конфигурация для приложения cafe.

Этот файл — cafe/urls.py (файл URL-маршрутов приложения).

Чтобы подключить его к проекту, добавьте в cafe_project/urls.py:

    from django.urls import path, include

    urlpatterns = [
        path("admin/", admin.site.urls),
        path("", include("cafe.urls")),   # Подключаем URL-ы приложения cafe
    ]
"""

from cafe.views import menu_list
from django.urls import path

# app_name — пространство имён для тега {% url %}
# Позволяет писать {% url 'cafe:menu_list' %} вместо просто {% url 'menu_list' %}
app_name = "cafe"

urlpatterns = [
    # http://localhost:8000/ → вызвать view menu_list
    # name="menu_list" → имя маршрута для {% url 'cafe:menu_list' %} в шаблонах
    path("", menu_list, name="menu_list"),
]
