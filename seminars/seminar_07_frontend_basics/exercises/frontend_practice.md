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

### Проверка данных в БД

Для заданий 4.1 и 5.1 нужны данные в БД. Проверьте их наличие в `manage.py shell`:

```bash
python manage.py shell
```

```python
from cafe.models import Category, MenuItem
print(Category.objects.count())   # Должно быть > 0
print(MenuItem.objects.count())   # Должно быть > 0
```

Если данных нет — добавьте тестовые записи прямо в shell:

```python
from cafe.models import Category, MenuItem

# Категории
drinks = Category.objects.create(name="Напитки")
pastry = Category.objects.create(name="Выпечка")
breakfast = Category.objects.create(name="Завтраки")

# Блюда
MenuItem.objects.create(name="Капучино", category=drinks, price=250)
MenuItem.objects.create(name="Латте", category=drinks, price=280)
MenuItem.objects.create(name="Чай зелёный", category=drinks, price=150)
MenuItem.objects.create(name="Круассан", category=pastry, price=180)
MenuItem.objects.create(name="Чизкейк", category=pastry, price=350)
MenuItem.objects.create(name="Тирамису", category=pastry, price=380, is_available=False)
MenuItem.objects.create(name="Яичница с тостами", category=breakfast, price=320)
MenuItem.objects.create(name="Овсянка с ягодами", category=breakfast, price=280)
```

> **Как работать с заданиями:** прочитайте условие, попробуйте решить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: HTML-структура

> **Теория:** [README.md — Блок 1](../README.md#блок-1-html-структура-и-теги-10-мин) | **Примеры:** [`examples/01_html_basics.html`](../examples/01_html_basics.html)

### Задание 1.1

Создайте файл `my_menu.html` с корректной HTML-структурой, который отображает меню кафе. Требования:
- Обязательные теги: `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`
- Заголовок `<h1>` с названием кафе и подзаголовок `<h2>` «Наше меню»
- Ненумерованный список `<ul>` с 3 блюдами (`<li>`)
- Карточка «Блюдо дня» внутри `<div>` с: названием в `<p style="font-weight: bold;">`, ценой, картинкой через `<img src="https://via.placeholder.com/200x120" alt="...">`

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

`<div>` — это блочный контейнер без собственных стилей. Оберните в него все элементы карточки.

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

</body>
</html>
```

Откройте файл в браузере — вы увидите заголовок, список и карточку блюда дня.

</details>

---

## Часть 2: CSS-стилизация

> **Теория:** [README.md — Блок 2](../README.md#блок-2-css-стилизация-15-мин) | **Примеры:** [`examples/02_css_styling.html`](../examples/02_css_styling.html) | [`examples/02_styles.css`](../examples/02_styles.css)

### Задание 2.1

Добавьте стилизацию к `my_menu.html` в два шага:

**Шаг 1 — встроенные стили:** добавьте блок `<style>` в `<head>`:
- `body`: шрифт `Arial, sans-serif`, фон `#f5f5f5`, ширина `max-width: 600px`, центрирование `margin: 0 auto`
- `h1`: синий цвет, выравнивание по центру

**Шаг 2 — внешний CSS:** создайте файл `my_styles.css`, подключите его через `<link rel="stylesheet" href="my_styles.css" />` и перенесите стили туда. Добавьте класс `.price` с красным жирным шрифтом и примените его к тегу с ценой блюда дня.

<details>
<summary>Подсказка</summary>

Вставьте в `<head>`:
```html
<style>
  body { font-family: Arial, sans-serif; /* ... */ }
  h1   { color: #2980b9; text-align: center; }
</style>
```

Класс в CSS: `.price { color: #e74c3c; font-weight: bold; }`.
Применение в HTML: `<p class="price">450 ₽</p>`.

`margin: 0 auto` центрирует блочный элемент с фиксированной шириной.

</details>

<details>
<summary>Решение</summary>

`my_styles.css`:
```css
body {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  color: #333;
  max-width: 600px;
  margin: 0 auto;
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
  list-style: none;
  padding: 0;
}

li {
  padding: 8px 0;
  border-bottom: 1px solid #ddd;
}

/* Карточка блюда дня */
.day-card {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 16px 20px;
  margin-top: 24px;
}

/* Класс для цены */
.price {
  color: #e74c3c;
  font-weight: bold;
  font-size: 1.15rem;
}
```

`my_menu.html` — в `<head>` замените `<style>` на:
```html
<link rel="stylesheet" href="my_styles.css" />
```

В HTML-карточке замените `<div style="...">` и `<p>` с ценой на:
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

## Часть 3: JavaScript — основы

> **Теория:** [README.md — Блок 3](../README.md#блок-3-javascript-основы-10-мин) | **Примеры:** [`examples/03_javascript_basics.html`](../examples/03_javascript_basics.html) | [`examples/03_script.js`](../examples/03_script.js)

### Задание 3.1

Добавьте в `my_menu.html` интерактивность в два шага:

**Шаг 1 — встроенный скрипт:** добавьте кнопку «Показать приветствие» с `id="btn-hello"` и `<script>` в конце `<body>`. По клику: вывести `console.log("Привет!")` и изменить текст кнопки на «Привет! 👋». Откройте DevTools (F12 → Console), чтобы увидеть вывод.

**Шаг 2 — внешний файл:** вынесите JS в файл `my_script.js`, подключите через `<script src="my_script.js" defer></script>` в `<head>`, встроенный `<script>` удалите. Добавьте кнопку «Сбросить» (`id="btn-reset"`), которая возвращает текст первой кнопки обратно.

<details>
<summary>Подсказка</summary>

`document.getElementById("btn-hello")` — найти кнопку.
`.addEventListener("click", function() { ... })` — подписаться на клик.
`.textContent = "..."` — изменить текст элемента.

`defer` — скрипт выполняется после загрузки всего HTML, поэтому `document.getElementById(...)` найдёт элемент даже если `<script>` в `<head>`.

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

`my_menu.html` — в `<head>` добавьте (inline-script в `<body>` удалите):
```html
<script src="my_script.js" defer></script>
```

В `<body>`:
```html
<button id="btn-hello">Показать приветствие</button>
<button id="btn-reset">Сбросить</button>
```

</details>

---

## Часть 4: Django Templates

> **Теория:** [README.md — Блок 4](../README.md#блок-4-django-templates-20-мин) | **Примеры:** [`examples/04_django_templates/`](../examples/04_django_templates/)

### Задание 4.1

В Django-проекте кафе из семинара 6 создайте базовый шаблон и страницу меню:

1. Убедитесь, что `'cafe'` есть в `INSTALLED_APPS` в `settings.py`
2. В `settings.py` добавьте `BASE_DIR / "templates"` в `TEMPLATES → DIRS`
3. Создайте `templates/base.html` с полной HTML-структурой, блоками `{% block title %}` и `{% block content %}`
4. В `cafe/views.py` создайте view `menu_list`, который передаёт в шаблон все объекты `MenuItem` через `select_related("category")`
5. Создайте `cafe/templates/cafe/menu_list.html` c `{% extends "base.html" %}`, `{% for item in menu_items %}` и `{% if item.is_available %}`
6. Создайте `cafe/urls.py`, подключите его в `cafe_project/urls.py` и запустите сервер: `python manage.py runserver`

<details>
<summary>Подсказка</summary>

Без `'cafe'` в `INSTALLED_APPS` Django не найдёт шаблоны в `cafe/templates/` (даже при `APP_DIRS: True`) и не будет применять миграции приложения.

View минимальный:
```python
return render(request, "cafe/menu_list.html", {"menu_items": MenuItem.objects.all().select_related("category")})
```

Шаблоны приложения: создайте папку `cafe/templates/cafe/` — Django ищет их именно по пути `templates/<app_name>/`.
`cafe/urls.py` не создаётся автоматически командой `startapp` — его нужно создать вручную.

</details>

<details>
<summary>Решение</summary>

`cafe_project/settings.py`:
```python
INSTALLED_APPS = [
    # ... стандартные приложения Django ...
    "cafe",   # ← Добавили
]

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
  <title>{% block title %}Кафе{% endblock %}</title>
</head>
<body>
  <header>
    <h1><a href="/">☕ Питоновая кружка</a></h1>
  </header>
  <main>
    {% block content %}{% endblock %}
  </main>
  <footer><p>© 2026 Кафе «Питоновая кружка»</p></footer>
</body>
</html>
```

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

`cafe/urls.py` (создайте этот файл вручную):
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

Откройте `http://localhost:8000/menu/` — должен отобразиться список блюд из БД.

</details>

---

## Часть 5: Собираем всё вместе

> **Теория:** [README.md — Блок 5](../README.md#блок-5-собираем-всё-вместе-15-мин) | **Примеры:** [`examples/05_cafe_menu_complete/`](../examples/05_cafe_menu_complete/)

### Задание 5.1

Улучшите страницу меню: добавьте CSS и JavaScript-фильтрацию по категориям.

**CSS (статические файлы):**
1. Убедитесь, что `'django.contrib.staticfiles'` есть в `INSTALLED_APPS` (присутствует по умолчанию) и `DEBUG = True` в `settings.py` — иначе dev-сервер не будет отдавать статику
2. Создайте `cafe/static/cafe/css/style.css` с Flexbox-сеткой `.menu-grid` и карточками `.menu-card`
3. Подключите CSS в `base.html` через `{% load static %}` и тег `{% static 'cafe/css/style.css' %}`
4. Замените список `<ul>` в шаблоне на сетку карточек

**JavaScript (фильтрация):**  
5. В view добавьте в контекст `"categories": Category.objects.all()`  
6. В шаблоне добавьте кнопки-фильтры `<button data-category="{{ category.id }}">` и атрибут `data-category="{{ item.category.id }}"` на каждой карточке  
7. Создайте `cafe/static/cafe/js/menu.js` — по клику на кнопку скрывать/показывать карточки нужной категории  
8. Подключите JS через `{% static 'cafe/js/menu.js' %}` перед `</body>`

<details>
<summary>Подсказка</summary>

Структура статики: `<app>/static/<app>/css/style.css` — двойное имя приложения намеренно, чтобы избежать коллизий при `collectstatic`.

`{% load static %}` нужно добавить в начало каждого шаблона, где используется тег `{% static %}`. В `base.html` — один раз в самом начале файла, до `<!DOCTYPE html>`.

В JS: `document.querySelectorAll(".filter-btn")` — все кнопки. При клике: `btn.dataset.category` — значение `data-category`. Карточки скрывать через `card.style.display = "none"`, показывать через `card.style.display = ""`.

</details>

<details>
<summary>Решение</summary>

`cafe_project/settings.py` — проверьте, что есть (по умолчанию присутствует):
```python
DEBUG = True

INSTALLED_APPS = [
    "django.contrib.staticfiles",  # ← нужен для {% static %}
    # ...
    "cafe",
]

STATIC_URL = "static/"
```

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

.page-title { font-size: 1.8rem; margin-bottom: 20px; }

.category-filter {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.filter-btn {
  padding: 6px 16px;
  border: 2px solid #3498db;
  background: #fff;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 600;
}

.filter-btn--active {
  background: #3498db;
  color: #fff;
}

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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.09);
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

`cafe/static/cafe/js/menu.js`:
```javascript
// Скрипт подключён в конце <body>, поэтому DOM уже загружен —
// DOMContentLoaded не нужен, обращаемся к элементам напрямую.
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
  <script src="{% static 'cafe/js/menu.js' %}"></script>
</body>
</html>
```

`cafe/views.py` (обновлённый):
```python
from django.shortcuts import render
from cafe.models import Category, MenuItem


def menu_list(request):
    menu_items = MenuItem.objects.all().select_related("category")
    categories = Category.objects.all()
    return render(request, "cafe/menu_list.html", {
        "menu_items": menu_items,
        "categories": categories,
    })
```

`cafe/templates/cafe/menu_list.html` (обновлённый):
```html
{% extends "base.html" %}

{% block title %}Меню{% endblock %}

{% block content %}
  <h2 class="page-title">Меню кафе</h2>

  <div class="category-filter" id="category-filter">
    <button class="filter-btn filter-btn--active" data-category="all">Все</button>
    {% for category in categories %}
      <button class="filter-btn" data-category="{{ category.id }}">
        {{ category.name }}
      </button>
    {% endfor %}
  </div>

  {% if menu_items %}
    <div class="menu-grid">
      {% for item in menu_items %}
        <div class="menu-card {% if not item.is_available %}menu-card--unavailable{% endif %}"
             data-category="{{ item.category.id }}">
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

</details>

---

## Бонусное задание

### Задание Б.1: Поиск по названию блюда

Добавьте на страницу меню поле поиска, которое в реальном времени фильтрует карточки по названию. Требования:
- `<input type="text" id="menu-search" placeholder="Поиск...">` в шаблоне
- У каждой карточки атрибут `data-name="{{ item.name|lower }}"` (фильтр `lower` приводит к нижнему регистру)
- JavaScript: при событии `input` скрывать карточки, название которых не содержит введённую строку
- Поиск и фильтр по категории должны работать **вместе** (оба условия применяются одновременно)

<details>
<summary>Подсказка</summary>

Храните текущую категорию в переменной `activeCategory`, а текущий запрос в `searchQuery`. Реализуйте единую функцию `applyFilters()` и вызывайте её из обоих обработчиков событий.

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

У карточек добавьте атрибут:
```html
<div class="menu-card ..." data-category="{{ item.category.id }}" data-name="{{ item.name|lower }}">
```

`cafe/static/cafe/js/menu.js` (расширенная версия):
```javascript
// Скрипт подключён в конце <body> — DOM уже загружен.
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
```

</details>

---

## Полезные ресурсы

- [MDN Web Docs — HTML](https://developer.mozilla.org/ru/docs/Web/HTML) — справочник по HTML-тегам на русском
- [MDN Web Docs — CSS](https://developer.mozilla.org/ru/docs/Web/CSS) — справочник по CSS с примерами
- [Django Templates](https://docs.djangoproject.com/en/5.0/topics/templates/) — официальная документация по шаблонам
- [Django Static Files](https://docs.djangoproject.com/en/5.0/howto/static-files/) — работа со статическими файлами в Django
