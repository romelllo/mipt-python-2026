# Практические задания: Основы Frontend-разработки

## Подготовка

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate  # Linux/Mac

# Проверьте, что Django установлен
python -c "import django; print(django.get_version())"

# Убедитесь, что у вас есть Django-проект из семинара 6.
# Если нет — создайте быстрый стартовый проект:
django-admin startproject cafe_project
cd cafe_project
python manage.py startapp cafe
# Затем добавьте модели из семинара 6 в cafe/models.py и выполните миграции.

# Откройте примеры в браузере (просто двойной клик на файле):
#   seminars/seminar_07_frontend_basics/examples/01_html_basics.html
#   seminars/seminar_07_frontend_basics/examples/02_css_styling.html
#   seminars/seminar_07_frontend_basics/examples/03_javascript_basics.html
```

> **Как работать с заданиями:** прочитайте условие, попробуйте решить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: HTML-структура

> **Теория:** [README.md — Блок 1](../README.md#блок-1-html-структура-и-теги-10-мин) | **Примеры:** [`examples/01_html_basics.html`](../examples/01_html_basics.html)

### Задание 1.1

Создайте файл `my_menu.html` с корректной HTML-структурой, который отображает список из 3 блюд вашего кафе. Требования:
- Обязательные теги: `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`
- Тег `<title>` с названием вашего кафе
- Один заголовок `<h1>` с названием кафе
- Подзаголовок `<h2>` «Наше меню»
- Ненумерованный список `<ul>` с 3 блюдами (используйте `<li>`)
- Ссылка `<a>` на любой сайт

<details>
<summary>Подсказка</summary>

Минимальная структура HTML-документа:
```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Название</title>
</head>
<body>
  <!-- Ваш контент здесь -->
</body>
</html>
```

</details>

<details>
<summary>Решение</summary>

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Кафе «Солнышко»</title>
</head>
<body>

  <h1>Кафе «Солнышко»</h1>
  <h2>Наше меню</h2>

  <ul>
    <li>Капучино — 250 ₽</li>
    <li>Круассан — 150 ₽</li>
    <li>Тирамису — 400 ₽</li>
  </ul>

  <p>
    Посмотрите наш <a href="https://example.com">полный сайт</a>.
  </p>

</body>
</html>
```

Откройте файл в браузере — вы увидите заголовок, список и ссылку.

</details>

---

### Задание 1.2

Добавьте в `my_menu.html` карточку «Блюдо дня» с использованием тега `<div>`. Карточка должна содержать:
- Подзаголовок `<h3>` «Блюдо дня»
- Название блюда в теге `<p>` с атрибутом `style="font-weight: bold;"`
- Цену блюда
- Картинку через `<img>` (можете использовать `https://via.placeholder.com/200x120`)

<details>
<summary>Подсказка</summary>

`<div>` — это блочный контейнер без собственных стилей. Оберните в него все элементы карточки. Для картинки: `<img src="URL" alt="Описание" width="200" />`.

</details>

<details>
<summary>Решение</summary>

```html
<!-- Добавьте в <body>, после списка меню -->
<div style="border: 1px solid #ccc; padding: 16px; margin-top: 20px; border-radius: 8px;">
  <h3>Блюдо дня</h3>
  <p style="font-weight: bold;">Паста карбонара</p>
  <p>Цена: 450 ₽</p>
  <img
    src="https://via.placeholder.com/200x120?text=Pasta"
    alt="Паста карбонара"
    width="200"
  />
</div>
```

</details>

---

## Часть 2: CSS-стилизация

> **Теория:** [README.md — Блок 2](../README.md#блок-2-css-стилизация-15-мин) | **Примеры:** [`examples/02_css_styling.html`](../examples/02_css_styling.html) | [`examples/02_styles.css`](../examples/02_styles.css)

### Задание 2.1

Добавьте к вашему `my_menu.html` встроенный блок `<style>` в `<head>`. Требования:
- Установите `font-family: Arial, sans-serif` для всей страницы через селектор `body`
- Задайте цвет фона страницы через `background-color`
- Ограничьте ширину содержимого до `600px` и центрируйте через `margin: 0 auto`
- Задайте `<h1>` синий цвет и выравнивание по центру

<details>
<summary>Подсказка</summary>

Вставьте в `<head>`:
```html
<style>
  body {
    font-family: Arial, sans-serif;
    /* ваши стили */
  }
  h1 {
    /* ваши стили */
  }
</style>
```

`margin: 0 auto` центрирует блочный элемент с фиксированной шириной.

</details>

<details>
<summary>Решение</summary>

```html
<head>
  <meta charset="UTF-8" />
  <title>Кафе «Солнышко»</title>

  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f5f5f5;
      color: #333;
      max-width: 600px;
      margin: 0 auto;       /* Центрировать контейнер */
      padding: 20px;
    }

    h1 {
      color: #2980b9;
      text-align: center;
    }

    h2 {
      color: #555;
      margin-top: 24px;
    }

    ul {
      list-style: none;     /* Убрать маркеры */
      padding: 0;
    }

    li {
      padding: 8px 0;
      border-bottom: 1px solid #ddd;
    }
  </style>
</head>
```

</details>

---

### Задание 2.2

Создайте отдельный файл `my_styles.css` и подключите его к `my_menu.html` через `<link>`. В CSS-файле:
- Добавьте стили для карточки «Блюдо дня»: белый фон, скруглённые углы (`border-radius`), тень (`box-shadow`), отступы
- Создайте класс `.price` с красным жирным шрифтом
- Примените класс `.price` к тегу с ценой в HTML

<details>
<summary>Подсказка</summary>

Подключение: `<link rel="stylesheet" href="my_styles.css" />` в `<head>`.  
Класс в CSS: `.price { color: red; font-weight: bold; }`.  
Применение в HTML: `<p class="price">450 ₽</p>`.

</details>

<details>
<summary>Решение</summary>

`my_styles.css`:
```css
/* Стили для карточки блюда дня */
.day-card {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 16px 20px;
  margin-top: 24px;
}

.day-card h3 {
  color: #e67e22;
  margin-bottom: 8px;
}

/* Класс для цены */
.price {
  color: #e74c3c;
  font-weight: bold;
  font-size: 1.15rem;
}
```

`my_menu.html` (в `<head>`):
```html
<link rel="stylesheet" href="my_styles.css" />
```

В HTML-карточке замените `<div style="...">` на:
```html
<div class="day-card">
  <h3>Блюдо дня</h3>
  <p style="font-weight: bold;">Паста карбонара</p>
  <p class="price">450 ₽</p>
  <img src="https://via.placeholder.com/200x120?text=Pasta" alt="Паста" width="200" />
</div>
```

</details>

---

### Задание 2.3

Используя Flexbox, расположите 3 карточки меню в строку. Добавьте в HTML три `<div class="menu-card">` и напишите CSS:
- `.menu-grid` — контейнер с `display: flex`, `gap: 16px`
- `.menu-card` — фиксированная ширина `180px`, белый фон, скруглённые углы, отступ
- При наведении (`hover`) карточка должна немного подниматься (`transform: translateY(...)`)

<details>
<summary>Подсказка</summary>

Flexbox включается на контейнере: `display: flex`. Дочерние элементы становятся «flex-элементами».  
Эффект при наведении: `.menu-card:hover { transform: translateY(-4px); transition: transform 0.2s; }`.

</details>

<details>
<summary>Решение</summary>

HTML:
```html
<div class="menu-grid">
  <div class="menu-card">
    <h3>Капучино</h3>
    <p class="price">250 ₽</p>
  </div>
  <div class="menu-card">
    <h3>Круассан</h3>
    <p class="price">150 ₽</p>
  </div>
  <div class="menu-card">
    <h3>Тирамису</h3>
    <p class="price">400 ₽</p>
  </div>
</div>
```

CSS (`my_styles.css`):
```css
.menu-grid {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;     /* Перенос на новую строку на маленьких экранах */
  margin-top: 20px;
}

.menu-card {
  background-color: #fff;
  border-radius: 10px;
  padding: 16px;
  width: 180px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.menu-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}
```

</details>

---

## Часть 3: JavaScript — основы

> **Теория:** [README.md — Блок 3](../README.md#блок-3-javascript-основы-10-мин) | **Примеры:** [`examples/03_javascript_basics.html`](../examples/03_javascript_basics.html) | [`examples/03_script.js`](../examples/03_script.js)

### Задание 3.1

Добавьте в `my_menu.html` кнопку и встроенный `<script>`:
- Кнопка «Показать приветствие» с `id="btn-hello"`
- В скрипте: по клику на кнопку выводите `console.log("Привет!")` и меняйте текст кнопки на «Привет! 👋»

Откройте DevTools (F12 → Console), чтобы увидеть вывод `console.log`.

<details>
<summary>Подсказка</summary>

`document.getElementById("btn-hello")` — найти кнопку.  
`.addEventListener("click", function() { ... })` — подписаться на клик.  
`.textContent = "..."` — изменить текст элемента.

</details>

<details>
<summary>Решение</summary>

В `<body>`:
```html
<button id="btn-hello">Показать приветствие</button>

<!-- script должен быть ПОСЛЕ кнопки в HTML, чтобы кнопка уже существовала -->
<script>
  const btn = document.getElementById("btn-hello");

  btn.addEventListener("click", function () {
    console.log("Привет!");
    btn.textContent = "Привет! 👋";
  });
</script>
```

</details>

---

### Задание 3.2

Вынесите JavaScript из предыдущего задания в отдельный файл `my_script.js`. Подключите его через `<script src="my_script.js" defer></script>`.

Дополнительно: добавьте кнопку «Сбросить» — при клике возвращает текст первой кнопки обратно в «Показать приветствие».

<details>
<summary>Подсказка</summary>

`defer` — скрипт выполняется после загрузки всего HTML, поэтому `document.getElementById(...)` найдёт элемент даже если `<script>` в `<head>`.  
В `my_script.js` используйте `document.getElementById` так же, как в inline-скрипте.

</details>

<details>
<summary>Решение</summary>

`my_script.js`:
```javascript
const btnHello = document.getElementById("btn-hello");
const btnReset = document.getElementById("btn-reset");

btnHello.addEventListener("click", function () {
  console.log("Привет!");
  btnHello.textContent = "Привет! 👋";
});

btnReset.addEventListener("click", function () {
  btnHello.textContent = "Показать приветствие";
  console.log("Сброшено.");
});
```

`my_menu.html` — в `<head>`:
```html
<script src="my_script.js" defer></script>
```

В `<body>` (inline-script убрать):
```html
<button id="btn-hello">Показать приветствие</button>
<button id="btn-reset">Сбросить</button>
```

</details>

---

## Часть 4: Django Templates

> **Теория:** [README.md — Блок 4](../README.md#блок-4-django-templates-20-мин) | **Примеры:** [`examples/04_django_templates/`](../examples/04_django_templates/)

### Задание 4.1

В вашем Django-проекте (кафе из семинара 6) создайте директорию шаблонов и базовый шаблон:

1. Создайте папку `cafe_project/templates/`
2. В `settings.py` в `TEMPLATES` добавьте `BASE_DIR / "templates"` в `DIRS`
3. Создайте `templates/base.html` с:
   - Полной HTML-структурой (`<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`)
   - Блоком `{% block title %}Кафе{% endblock %}` в `<title>`
   - Блоком `{% block content %}{% endblock %}` в `<body>`

<details>
<summary>Подсказка</summary>

В `settings.py` найдите список `TEMPLATES` и измените:
```python
"DIRS": [BASE_DIR / "templates"],
```

В шаблоне используйте `{% block имя %}контент_по_умолчанию{% endblock %}`.

</details>

<details>
<summary>Решение</summary>

`cafe_project/settings.py`:
```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],   # ← Добавили
        "APP_DIRS": True,
        # ...
    }
]
```

`templates/base.html`:
```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <title>{% block title %}Кафе «Питоновая кружка»{% endblock %}</title>
</head>
<body>

  <header>
    <h1><a href="/">☕ Питоновая кружка</a></h1>
  </header>

  <main>
    {% block content %}{% endblock %}
  </main>

  <footer>
    <p>© 2026 Кафе «Питоновая кружка»</p>
  </footer>

</body>
</html>
```

</details>

---

### Задание 4.2

Создайте view `menu_list` и шаблон `cafe/templates/cafe/menu_list.html`:

1. В `cafe/views.py` создайте view, который передаёт в шаблон список объектов `MenuItem`
2. В шаблоне используйте `{% extends "base.html" %}`, `{% for item in menu_items %}`, `{% if item.is_available %}`
3. Подключите view к URL `/menu/` в `cafe/urls.py` и включите `cafe.urls` в `cafe_project/urls.py`
4. Запустите сервер: `python manage.py runserver` и откройте `http://localhost:8000/menu/`

<details>
<summary>Подсказка</summary>

View минимальный: `return render(request, "cafe/menu_list.html", {"menu_items": MenuItem.objects.all()})`.  
Шаблон: создайте папку `cafe/templates/cafe/` (Django ищет шаблоны именно в `templates/<app>/`).

</details>

<details>
<summary>Решение</summary>

`cafe/views.py`:
```python
from django.shortcuts import render
from cafe.models import MenuItem


def menu_list(request):
    """Список всех позиций меню."""
    menu_items = MenuItem.objects.all().select_related("category")
    return render(request, "cafe/menu_list.html", {"menu_items": menu_items})
```

`cafe/templates/cafe/menu_list.html`:
```html
{% extends "base.html" %}

{% block title %}Меню{% endblock %}

{% block content %}
  <h2>Меню кафе</h2>

  {% if menu_items %}
    <ul>
      {% for item in menu_items %}
        <li>
          <strong>{{ item.name }}</strong> — {{ item.price }} ₽
          ({{ item.category.name }})
          {% if not item.is_available %}
            <em>— нет в наличии</em>
          {% endif %}
        </li>
      {% endfor %}
    </ul>
  {% else %}
    <p>Меню пустое.</p>
  {% endif %}
{% endblock %}
```

`cafe/urls.py`:
```python
from django.urls import path
from cafe.views import menu_list

app_name = "cafe"
urlpatterns = [
    path("menu/", menu_list, name="menu_list"),
]
```

`cafe_project/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cafe.urls")),
]
```

</details>

---

### Задание 4.3

Добавьте в Django-проект статические файлы:

1. В `settings.py` убедитесь, что `STATIC_URL = "static/"` задан (он там по умолчанию)
2. Создайте файл `cafe/static/cafe/css/style.css` с минимальными стилями (фон, шрифт, цвет ссылок)
3. Подключите CSS в `base.html` через `{% load static %}` и `{% static 'cafe/css/style.css' %}`

<details>
<summary>Подсказка</summary>

Структура статики: `<app>/static/<app>/css/style.css` (двойное имя приложения — намеренно, чтобы избежать коллизий при `collectstatic`).  
Тег в шаблоне: `<link rel="stylesheet" href="{% static 'cafe/css/style.css' %}">` — но нужно сначала добавить `{% load static %}` в начало файла.

</details>

<details>
<summary>Решение</summary>

`cafe/static/cafe/css/style.css`:
```css
body {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

a { color: #2980b9; }

header {
  background: #3498db;
  color: #fff;
  padding: 12px 20px;
  border-radius: 8px;
  margin-bottom: 24px;
}

header a { color: #fff; text-decoration: none; }
```

`templates/base.html` (обновлённый):
```html
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <title>{% block title %}Кафе{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'cafe/css/style.css' %}" />
</head>
<body>
  <header>
    <h1><a href="/">☕ Питоновая кружка</a></h1>
  </header>
  <main>
    {% block content %}{% endblock %}
  </main>
  <footer><p>© 2026</p></footer>
</body>
</html>
```

</details>

---

## Часть 5: Собираем всё вместе

> **Теория:** [README.md — Блок 5](../README.md#блок-5-собираем-всё-вместе-15-мин) | **Примеры:** [`examples/05_cafe_menu_complete/`](../examples/05_cafe_menu_complete/)

### Задание 5.1

Улучшите шаблон `menu_list.html`: замените список `<ul>` на сетку карточек с CSS:
- Используйте Flexbox-сетку `.menu-grid` с карточками `.menu-card`
- В каждой карточке: название, категория (бейдж), цена, кнопка «В корзину» (или «Нет в наличии»)
- Создайте или дополните `cafe/static/cafe/css/style.css` стилями для сетки и карточек

<details>
<summary>Подсказка</summary>

Возьмите за основу стили из [`examples/02_styles.css`](../examples/02_styles.css) или из [`examples/05_cafe_menu_complete/static/cafe/css/style.css`](../examples/05_cafe_menu_complete/static/cafe/css/style.css). Скопируйте классы `.menu-grid`, `.menu-card`, `.btn`.

</details>

<details>
<summary>Решение</summary>

`cafe/templates/cafe/menu_list.html`:
```html
{% extends "base.html" %}
{% load static %}

{% block title %}Меню{% endblock %}

{% block content %}
  <h2 class="page-title">Меню кафе</h2>

  {% if menu_items %}
    <div class="menu-grid">
      {% for item in menu_items %}
        <div class="menu-card {% if not item.is_available %}menu-card--unavailable{% endif %}">
          <span class="menu-card__badge">{{ item.category.name }}</span>
          <h3 class="menu-card__title">{{ item.name }}</h3>
          <p class="menu-card__price">{{ item.price }} ₽</p>
          {% if item.is_available %}
            <button class="btn btn--primary">В корзину</button>
          {% else %}
            <button class="btn btn--disabled" disabled>Нет в наличии</button>
          {% endif %}
        </div>
      {% endfor %}
    </div>
  {% else %}
    <p>Меню пустое. <a href="/admin/">Добавить через админку</a>.</p>
  {% endif %}
{% endblock %}
```

Добавьте в `cafe/static/cafe/css/style.css` (минимум):
```css
.page-title { font-size: 1.8rem; margin-bottom: 20px; }

.menu-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.menu-card {
  background: #fff;
  border-radius: 10px;
  padding: 18px;
  width: 200px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.09);
}

.menu-card--unavailable { opacity: 0.5; }

.menu-card__badge {
  background: #e8f4fd;
  color: #2980b9;
  font-size: 0.75rem;
  padding: 2px 10px;
  border-radius: 999px;
}

.menu-card__title { margin: 10px 0 6px; }

.menu-card__price { color: #e74c3c; font-weight: bold; margin-bottom: 12px; }

.btn { padding: 8px 14px; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; width: 100%; }
.btn--primary { background: #3498db; color: #fff; }
.btn--primary:hover { background: #2980b9; }
.btn--disabled { background: #ddd; color: #999; cursor: not-allowed; }
```

</details>

---

### Задание 5.2

Добавьте JavaScript-фильтрацию по категориям:

1. В view передайте в контекст список всех категорий: `"categories": Category.objects.all()`
2. В шаблоне добавьте кнопки-фильтры с `data-category="{{ category.id }}"` и у каждой карточки — `data-category="{{ item.category.id }}"`
3. Создайте файл `cafe/static/cafe/js/menu.js` с JavaScript, который при клике на кнопку скрывает/показывает карточки нужной категории
4. Подключите JS в `base.html` через `{% static 'cafe/js/menu.js' %}`

<details>
<summary>Подсказка</summary>

В JS: `document.querySelectorAll(".filter-btn")` — все кнопки. При клике: `btn.dataset.category` — значение `data-category`. Карточки скрывать/показывать через `card.style.display = "none"` или `card.style.display = ""`.

</details>

<details>
<summary>Решение</summary>

`cafe/views.py` (обновлённый):
```python
from cafe.models import Category, MenuItem

def menu_list(request):
    menu_items = MenuItem.objects.all().select_related("category")
    categories = Category.objects.all()
    return render(request, "cafe/menu_list.html", {
        "menu_items": menu_items,
        "categories": categories,
    })
```

В `menu_list.html` — добавьте перед `.menu-grid`:
```html
<div class="category-filter" id="category-filter">
  <button class="filter-btn filter-btn--active" data-category="all">Все</button>
  {% for category in categories %}
    <button class="filter-btn" data-category="{{ category.id }}">
      {{ category.name }}
    </button>
  {% endfor %}
</div>
```

У каждой карточки добавьте атрибут:
```html
<div class="menu-card ..." data-category="{{ item.category.id }}">
```

`cafe/static/cafe/js/menu.js`:
```javascript
document.addEventListener("DOMContentLoaded", function () {
  const filterBtns = document.querySelectorAll(".filter-btn");
  const cards = document.querySelectorAll(".menu-card");

  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      // Активная кнопка
      filterBtns.forEach(function (b) {
        b.classList.remove("filter-btn--active");
      });
      btn.classList.add("filter-btn--active");

      const selected = btn.dataset.category;

      // Показать/скрыть карточки
      cards.forEach(function (card) {
        if (selected === "all" || card.dataset.category === selected) {
          card.style.display = "";
        } else {
          card.style.display = "none";
        }
      });
    });
  });
});
```

В `base.html` перед `</body>`:
```html
{% load static %}
<script src="{% static 'cafe/js/menu.js' %}"></script>
```

</details>

---

## Бонусные задания

Эти задания объединяют несколько тем семинара. Попробуйте решить самостоятельно!

### Задание Б.1: Поиск по названию блюда

Добавьте на страницу меню поле поиска, которое в реальном времени фильтрует карточки по названию блюда. Требования:
- `<input type="text" id="menu-search" placeholder="Поиск...">` в шаблоне
- У каждой карточки атрибут `data-name="{{ item.name|lower }}"` (Jinja-фильтр `lower` приводит к нижнему регистру)
- JavaScript: при событии `input` скрывать карточки, название которых не содержит введённую строку
- Поиск и фильтр по категории должны работать **вместе** (оба условия должны быть выполнены)

<details>
<summary>Подсказка</summary>

Храните текущую категорию в переменной `activeCategory`, а текущий запрос в `searchQuery`. Применяйте оба фильтра в единой функции `applyFilters()`. Вызывайте её и из обработчика кнопок, и из обработчика поля ввода.

</details>

<details>
<summary>Решение</summary>

`menu_list.html` — добавьте поле ввода перед кнопками фильтра:
```html
<div class="menu-controls">
  <input type="text" id="menu-search" placeholder="🔍 Поиск по названию..." />
  <div class="category-filter" id="category-filter">
    <button class="filter-btn filter-btn--active" data-category="all">Все</button>
    {% for category in categories %}
      <button class="filter-btn" data-category="{{ category.id }}">{{ category.name }}</button>
    {% endfor %}
  </div>
</div>
```

У карточек добавьте:
```html
<div class="menu-card ..." data-category="{{ item.category.id }}" data-name="{{ item.name|lower }}">
```

`cafe/static/cafe/js/menu.js` (расширенная версия):
```javascript
document.addEventListener("DOMContentLoaded", function () {
  const filterBtns = document.querySelectorAll(".filter-btn");
  const cards = document.querySelectorAll(".menu-card");
  const searchInput = document.getElementById("menu-search");

  let activeCategory = "all";
  let searchQuery = "";

  function applyFilters() {
    cards.forEach(function (card) {
      const categoryMatch =
        activeCategory === "all" || card.dataset.category === activeCategory;
      const nameMatch = card.dataset.name.includes(searchQuery);
      card.style.display = categoryMatch && nameMatch ? "" : "none";
    });
  }

  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      filterBtns.forEach(function (b) { b.classList.remove("filter-btn--active"); });
      btn.classList.add("filter-btn--active");
      activeCategory = btn.dataset.category;
      applyFilters();
    });
  });

  if (searchInput) {
    searchInput.addEventListener("input", function () {
      searchQuery = searchInput.value.toLowerCase().trim();
      applyFilters();
    });
  }
});
```

</details>

---

### Задание Б.2: Страница детали блюда

Добавьте страницу с подробным описанием блюда, которая открывается по клику на карточку:

1. Создайте view `menu_detail(request, pk)`, который получает объект `MenuItem.objects.get(pk=pk)`
2. Обработайте случай «блюдо не найдено» через `get_object_or_404`
3. Создайте шаблон `cafe/menu_detail.html` с подробной информацией
4. Добавьте URL `menu/<int:pk>/` → `menu_detail`
5. В `menu_list.html` оберните название блюда в ссылку `<a href="{% url 'cafe:menu_detail' item.pk %}">`

<details>
<summary>Подсказка</summary>

`get_object_or_404(MenuItem, pk=pk)` — если объект не найден, Django автоматически вернёт ответ 404.  
URL с параметром: `path("menu/<int:pk>/", menu_detail, name="menu_detail")`.  
В шаблоне: `{% url 'cafe:menu_detail' item.pk %}`.

</details>

<details>
<summary>Решение</summary>

`cafe/views.py`:
```python
from django.shortcuts import get_object_or_404, render
from cafe.models import Category, MenuItem


def menu_list(request):
    menu_items = MenuItem.objects.all().select_related("category")
    categories = Category.objects.all()
    return render(request, "cafe/menu_list.html", {
        "menu_items": menu_items,
        "categories": categories,
    })


def menu_detail(request, pk: int):
    """Детальная страница позиции меню."""
    item = get_object_or_404(MenuItem, pk=pk)
    return render(request, "cafe/menu_detail.html", {"item": item})
```

`cafe/urls.py`:
```python
from django.urls import path
from cafe.views import menu_list, menu_detail

app_name = "cafe"
urlpatterns = [
    path("menu/", menu_list, name="menu_list"),
    path("menu/<int:pk>/", menu_detail, name="menu_detail"),
]
```

`cafe/templates/cafe/menu_detail.html`:
```html
{% extends "base.html" %}

{% block title %}{{ item.name }} — Кафе{% endblock %}

{% block content %}
  <a href="{% url 'cafe:menu_list' %}">← Назад к меню</a>

  <h2>{{ item.name }}</h2>
  <p>Категория: <strong>{{ item.category.name }}</strong></p>
  <p>Цена: <strong>{{ item.price }} ₽</strong></p>
  <p>
    Статус:
    {% if item.is_available %}
      <span style="color: green;">✓ В наличии</span>
    {% else %}
      <span style="color: red;">✗ Нет в наличии</span>
    {% endif %}
  </p>
{% endblock %}
```

В `menu_list.html` замените `<h3>{{ item.name }}</h3>` на:
```html
<h3><a href="{% url 'cafe:menu_detail' item.pk %}">{{ item.name }}</a></h3>
```

</details>

---

## Полезные ресурсы

- [MDN Web Docs — HTML](https://developer.mozilla.org/ru/docs/Web/HTML) — справочник по HTML-тегам на русском
- [MDN Web Docs — CSS](https://developer.mozilla.org/ru/docs/Web/CSS) — справочник по CSS с примерами
- [MDN Flexbox Guide](https://developer.mozilla.org/ru/docs/Learn/CSS/CSS_layout/Flexbox) — руководство по Flexbox
- [Django Templates](https://docs.djangoproject.com/en/5.0/topics/templates/) — официальная документация по шаблонам
- [Django Static Files](https://docs.djangoproject.com/en/5.0/howto/static-files/) — работа со статическими файлами в Django
