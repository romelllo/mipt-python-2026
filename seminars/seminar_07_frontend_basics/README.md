# Семинар 7: Основы Frontend-разработки

**Модуль:** 3 — Создание Web-сервисов на Python  
**Дата:** 16.03.2026  
**Презентация:** [ссылка на презентацию]

---

## Цели семинара

После этого семинара вы сможете:

- **Называть** роли HTML, CSS и JavaScript в цепочке «контент → дизайн → взаимодействие»
- **Создавать** корректную HTML-структуру страницы и использовать ключевые теги (`div`, `h1`–`h6`, `p`, `a`, `img`, `ul`/`li`)
- **Применять** CSS-стили — встроенный `<style>` и внешний `.css`-файл — для оформления страниц
- **Добавлять** простую JavaScript-интерактивность: обработчики событий, изменение DOM
- **Подключать** HTML/CSS/JS к Django-приложению через шаблоны, `{% static %}` и `{% block %}`

> **Важно:** Вы — Python-разработчики. Глубоко знать frontend не обязательно. Цель семинара — понять, как браузер «видит» страницу, чтобы уметь создавать Django-шаблоны и не бояться подправить CSS или добавить одну JS-кнопку.

---

## Подготовка

```bash
# Убедитесь, что виртуальное окружение активировано
source .venv/bin/activate  # Linux/Mac

# Проверьте Django
python -c "import django; print(django.get_version())"

# Откройте примеры в браузере (просто двойной клик на файле):
#   seminars/seminar_07_frontend_basics/examples/01_html_basics.html
#   seminars/seminar_07_frontend_basics/examples/02_css_styling.html
#   seminars/seminar_07_frontend_basics/examples/03_javascript_basics.html

# Убедитесь, что у вас есть Django-проект кафе из семинара 6.
# Если нет — создайте быстро:
django-admin startproject cafe_project
cd cafe_project
python manage.py startapp cafe
# Добавьте модели Category и MenuItem в cafe/models.py (из семинара 6)
# python manage.py makemigrations && python manage.py migrate
# python manage.py createsuperuser
# python manage.py runserver
```

---

## План семинара

Семинар построен по принципу **«теория → практика»**: после каждого блока теории переходите к соответствующим упражнениям в файле [`exercises/frontend_practice.md`](exercises/frontend_practice.md).

| Время | Тема | Практика |
|-------|------|----------|
| 10 мин | Блок 1: HTML-структура и теги | → Упражнения: Часть 1 |
| 15 мин | Блок 2: CSS-стилизация | → Упражнения: Часть 2 |
| 10 мин | Блок 3: JavaScript — основы | → Упражнения: Часть 3 |
| 20 мин | Блок 4: Django Templates | → Упражнения: Часть 4 |
| 15 мин | Блок 5: Собираем всё вместе | → Упражнения: Часть 5 |
| 10 мин | Подведение итогов | — |

**Итого:** ~80 мин теории + практика + 10 мин итоги = ~90 минут

---

## Блок 1: HTML-структура и теги (10 мин)

HTML описывает **содержимое** страницы: что здесь есть — заголовок, список, картинка, ссылка. Браузер читает HTML и строит из него дерево объектов (DOM — Document Object Model), с которым потом работают CSS и JavaScript.

```
HTML (что есть)  →  CSS (как выглядит)  →  JavaScript (что делает)
```

### Структура HTML-документа

Каждый HTML-файл имеет одинаковый «скелет»:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <!-- Метаинформация: не отображается на странице -->
  <meta charset="UTF-8" />
  <title>Кафе «Питоновая кружка»</title>
</head>
<body>
  <!-- Всё видимое содержимое — здесь -->
  <h1>Привет!</h1>
</body>
</html>
```

### Ключевые теги

| Тег | Назначение | Пример |
|-----|-----------|--------|
| `<h1>`…`<h6>` | Заголовки (h1 — главный) | `<h1>Меню</h1>` |
| `<p>` | Параграф текста | `<p>Описание блюда</p>` |
| `<div>` | Блочный контейнер (группировка) | `<div class="card">...</div>` |
| `<a href="...">` | Ссылка | `<a href="/menu/">Меню</a>` |
| `<img src="..." alt="...">` | Картинка | `<img src="coffee.jpg" alt="Кофе" />` |
| `<ul>` / `<ol>` + `<li>` | Список (маркированный / нумерованный) | `<ul><li>Капучино</li></ul>` |

**Правило:** только один `<h1>` на странице. `<div>` не несёт смысла сам по себе — это просто обёртка для группировки и стилизации.

> **Подробнее:** см. файл [`examples/01_html_basics.html`](examples/01_html_basics.html) — полная разметка страницы кафе с комментариями на русском.

### Практика

Перейдите к файлу [`exercises/frontend_practice.md`](exercises/frontend_practice.md) и выполните **Часть 1: HTML-структура** (задание 1.1).

---

## Блок 2: CSS-стилизация (15 мин)

CSS описывает **внешний вид** элементов: цвет, шрифт, отступы, расположение. Браузер применяет CSS к DOM-дереву и рисует результат.

### Два способа подключить CSS

**Способ 1 — Встроенный блок `<style>`** (для небольших, страницеспецифичных стилей):

```html
<head>
  <style>
    body { font-family: Arial, sans-serif; background: #f5f5f5; }
    h1   { color: #2980b9; text-align: center; }
  </style>
</head>
```

**Способ 2 — Внешний файл `styles.css`** (для больших проектов, стили переиспользуются):

```html
<head>
  <link rel="stylesheet" href="styles.css" />
</head>
```

**Когда использовать:** внешний файл — всегда для реальных проектов. `<style>` — для быстрых экспериментов или правил конкретной страницы.

### Ключевые CSS-свойства

```css
/* Текст */
color: #333;                  /* Цвет текста */
font-size: 1.2rem;            /* Размер шрифта */
font-weight: bold;            /* Жирность */
text-align: center;           /* Выравнивание */

/* Блок */
background-color: #fff;       /* Фон */
width: 200px;                 /* Ширина */
padding: 16px;                /* Внутренний отступ */
margin: 8px;                  /* Внешний отступ */
border-radius: 10px;          /* Скруглённые углы */
box-shadow: 0 2px 8px rgba(0,0,0,0.1); /* Тень */

/* Flexbox — расположение дочерних элементов в строку/столбец */
display: flex;
gap: 16px;                    /* Расстояние между элементами */
flex-wrap: wrap;              /* Перенос на новую строку */
```

### Карточка меню на CSS

```html
<!-- HTML: карточка блюда -->
<div class="menu-card">
  <h2 class="menu-card__title">Капучино</h2>
  <p class="menu-card__price">250 ₽</p>
</div>
```

```css
/* CSS: стили карточки */
.menu-card {
  background: #fff;
  border-radius: 10px;
  padding: 18px;
  width: 200px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.09);
  transition: transform 0.2s;  /* Плавный эффект hover */
}

.menu-card:hover {
  transform: translateY(-4px);  /* Поднять при наведении */
}

.menu-card__price { color: #e74c3c; font-weight: bold; }
```

> **Подробнее:** см. файлы [`examples/02_css_styling.html`](examples/02_css_styling.html) и [`examples/02_styles.css`](examples/02_styles.css) — демонстрация классов, Flexbox и псевдоклассов с карточками меню.

### Практика

Перейдите к файлу [`exercises/frontend_practice.md`](exercises/frontend_practice.md) и выполните **Часть 2: CSS-стилизация** (задание 2.1).

---

## Блок 3: JavaScript — основы (10 мин)

JavaScript добавляет **поведение** к странице: реакцию на клики, изменение содержимого без перезагрузки, фильтрацию списков.

### Два способа подключить JS

**Способ 1 — Встроенный `<script>`** (в конце `<body>`, чтобы HTML уже загрузился):

```html
<body>
  <button id="btn">Нажми меня</button>

  <script>
    // document.getElementById — найти элемент по id
    const btn = document.getElementById("btn");

    // addEventListener — подписаться на событие "click"
    btn.addEventListener("click", function () {
      console.log("Кнопка нажата!");        // Вывод в консоль браузера (F12)
      btn.textContent = "Нажата! ✓";        // Изменить текст кнопки
    });
  </script>
</body>
```

**Способ 2 — Внешний файл `script.js`** (с атрибутом `defer`):

```html
<head>
  <!-- defer: файл загружается параллельно, выполняется после HTML -->
  <script src="script.js" defer></script>
</head>
```

### Три главных инструмента DOM

```javascript
// 1. Найти элемент
const el = document.getElementById("my-id");
const items = document.querySelectorAll(".menu-card");  // Все по классу

// 2. Изменить элемент
el.textContent = "Новый текст";           // Изменить текстовое содержимое
el.style.display = "none";               // Скрыть элемент
el.style.display = "";                   // Показать элемент (убрать скрытие)
el.classList.add("active");              // Добавить CSS-класс
el.classList.remove("active");           // Убрать CSS-класс

// 3. Подписаться на событие
el.addEventListener("click", function () { /* обработчик */ });
el.addEventListener("input", function () { /* при вводе текста */ });
```

**Когда использовать:** JS — только для интерактивности на стороне клиента (без обращения к серверу). Для работы с данными — Django views.

> **Подробнее:** см. файлы [`examples/03_javascript_basics.html`](examples/03_javascript_basics.html) и [`examples/03_script.js`](examples/03_script.js) — счётчик, показать/скрыть и фильтрация списка с подробными комментариями.

### Практика

Перейдите к файлу [`exercises/frontend_practice.md`](exercises/frontend_practice.md) и выполните **Часть 3: JavaScript — основы** (задание 3.1).

---

## Блок 4: Django Templates (20 мин)

Шаблоны в Django — это HTML-файлы с дополнительным синтаксисом для вставки данных из Python и управления структурой страницы.

### Переменные и теги шаблона

```
Синтаксис            | Назначение
---------------------|------------------------------
{{ переменная }}     | Вывести значение переменной
{{ item.price }}     | Вывести атрибут объекта
{{ items|length }}   | Применить фильтр к переменной
{% тег %}            | Управляющая конструкция
{% if %} / {% endif %}  | Условие
{% for %} / {% endfor %} | Цикл
{% url 'имя' %}      | Сгенерировать URL по имени маршрута
{% static 'путь' %}  | Ссылка на статический файл
{% load static %}    | Загрузить библиотеку тегов
{% block %} / {% endblock %} | Блок для наследования
{% extends "base.html" %}    | Наследоваться от базового шаблона
```

### Наследование шаблонов: `{% extends %}` и `{% block %}`

Главный инструмент для **DRY** в шаблонах — наследование. Базовый шаблон содержит общую структуру, дочерние заполняют блоки:

```html
<!-- templates/base.html — общий «скелет» -->
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
  <title>{% block title %}Кафе{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'cafe/css/style.css' %}" />
</head>
<body>
  <header>☕ Питоновая кружка</header>
  <main>
    {% block content %}{% endblock %}
  </main>
</body>
</html>
```

```html
<!-- cafe/templates/cafe/menu_list.html — дочерний шаблон -->
{% extends "base.html" %}

{% block title %}Меню — Кафе{% endblock %}

{% block content %}
  <h2>Наше меню</h2>
  {% for item in menu_items %}
    <p>{{ item.name }} — {{ item.price }} ₽</p>
  {% endfor %}
{% endblock %}
```

### Цикл и условие в шаблоне

```html
{% for item in menu_items %}
  <div class="menu-card">
    {{ item.name }}
    {% if item.is_available %}
      <button>В корзину</button>
    {% else %}
      <button disabled>Нет в наличии</button>
    {% endif %}
  </div>
{% empty %}
  <p>Меню пустое.</p>  <!-- Если menu_items пустой -->
{% endfor %}
```

### View: передача данных в шаблон

```python
# cafe/views.py
from django.shortcuts import render
from cafe.models import Category, MenuItem


def menu_list(request):
    """Передаём queryset-ы в шаблон через словарь контекста."""
    return render(
        request,
        "cafe/menu_list.html",
        {
            "menu_items": MenuItem.objects.all().select_related("category"),
            "categories": Category.objects.all(),
        },
    )
```

### Статические файлы в Django

Django управляет статикой (CSS, JS, картинки) через специальный механизм:

```
Структура в приложении:
  cafe/
  └── static/
      └── cafe/              ← двойное имя — избегаем коллизий при collectstatic
          ├── css/
          │   └── style.css
          └── js/
              └── menu.js

В шаблоне:
  {% load static %}
  <link rel="stylesheet" href="{% static 'cafe/css/style.css' %}" />
  <script src="{% static 'cafe/js/menu.js' %}" defer></script>
```

> **Подробнее:** см. файлы в [`examples/04_django_templates/`](examples/04_django_templates/) — `base.html`, `menu_list.html`, `views.py` и `urls.py` с подробными комментариями.

### Практика

Перейдите к файлу [`exercises/frontend_practice.md`](exercises/frontend_practice.md) и выполните **Часть 4: Django Templates** (задание 4.1).

---

## Блок 5: Собираем всё вместе (15 мин)

Итоговая задача — добавить к Django-проекту кафе полноценную страницу меню: HTML-структура из шаблона, стили из CSS, фильтрация из JavaScript.

### Архитектура итогового решения

```
Запрос браузера: GET /menu/
         │
         ▼
cafe/views.py — menu_list()
  ├── Достаёт из БД: MenuItem.objects.all(), Category.objects.all()
  └── render(request, "cafe/menu_list.html", context)
         │
         ▼
cafe/templates/cafe/menu_list.html
  ├── {% extends "base.html" %}          ← структура страницы
  ├── {% for item in menu_items %}       ← рендерит карточки
  └── data-category="{{ item.category.id }}"  ← данные для JS
         │
         ▼
cafe/static/cafe/css/style.css          ← оформление карточек, grid
cafe/static/cafe/js/menu.js             ← фильтрация по категориям
```

### Ключевой паттерн: data-атрибуты как мост между Django и JS

Данные из Python (ID категорий) попадают в HTML через шаблон, а JS их считывает:

```html
<!-- В шаблоне Django: item.category.id — это Python-объект -->
<div class="menu-card" data-category="{{ item.category.id }}">
  {{ item.name }}
</div>

<button class="filter-btn" data-category="{{ category.id }}">
  {{ category.name }}
</button>
```

```javascript
// В JavaScript: читаем то, что Django записал в шаблон
btn.addEventListener("click", function () {
  const selectedCategory = btn.dataset.category; // "3" (строка)

  cards.forEach(function (card) {
    const match = card.dataset.category === selectedCategory;
    card.style.display = match ? "" : "none";
  });
});
```

**Правило:** Django генерирует данные на сервере → записывает в `data-*` атрибуты → JavaScript читает их на клиенте. Это чистое разделение ответственности: сервер не знает про JS, JS не делает запросов к серверу.

> **Подробнее:** см. файлы в [`examples/05_cafe_menu_complete/`](examples/05_cafe_menu_complete/) — полный шаблон `menu_list.html`, файлы `style.css` и `menu.js` с подробными комментариями.

### Практика

Перейдите к файлу [`exercises/frontend_practice.md`](exercises/frontend_practice.md) и выполните **Часть 5: Собираем всё вместе** (задание 5.1).

---

## Подведение итогов

### Шпаргалка

| Концепция | Ключевое |
|-----------|----------|
| HTML | Описывает **структуру** (что есть на странице) |
| CSS | Описывает **внешний вид** (как выглядит) |
| JavaScript | Добавляет **поведение** (что делает при взаимодействии) |
| `<style>` | Встроенный CSS — удобно для экспериментов |
| `<link href="...">` | Внешний CSS-файл — для реальных проектов |
| `<script defer>` | Внешний JS-файл — выполняется после загрузки HTML |
| `{{ переменная }}` | Вывести Python-значение в Django-шаблоне |
| `{% for %}` / `{% if %}` | Управляющие теги Django-шаблона |
| `{% extends %}` | Наследование шаблонов — избегаем дублирования HTML |
| `{% block %}` | Именованные «дыры» в базовом шаблоне |
| `{% load static %}` | Загрузить поддержку `{% static %}` |
| `{% static 'путь' %}` | Ссылка на статический файл (CSS/JS/картинка) |
| `data-category="..."` | Передать данные из Django-шаблона в JavaScript |

### Ключевые выводы

1. **HTML → CSS → JS — это три отдельных языка с чёткими ролями.** HTML — контент, CSS — дизайн, JS — взаимодействие. Не смешивайте их без необходимости.

2. **Django-шаблоны генерируют HTML на сервере.** CSS и JS — это статические файлы, которые браузер загружает и выполняет сам. `data-*`-атрибуты — удобный «мост» между ними.

3. **Не нужно знать frontend глубоко — нужно понять принцип.** `{% for item in items %}` в шаблоне, один CSS-файл для стилей и один JS-файл для интерактивности — этого достаточно для большинства backend-задач.

> **Главное правило:** веб-разработка — это практика. Откройте браузерные DevTools, нажмите F12 и изучайте страницы, которыми пользуетесь каждый день. Реальный навык появляется только так.

---

## Файлы семинара

```
seminar_07_frontend_basics/
├── README.md                                     # Этот файл
├── examples/
│   ├── 01_html_basics.html                       # Структура HTML, ключевые теги
│   ├── 02_css_styling.html                       # CSS: встроенный и внешний
│   ├── 02_styles.css                             # Внешний CSS-файл к 02_css_styling.html
│   ├── 03_javascript_basics.html                 # JavaScript: DOM, события
│   ├── 03_script.js                              # Внешний JS-файл к 03_javascript_basics.html
│   ├── 04_django_templates/
│   │   ├── base.html                             # Базовый шаблон с блоками
│   │   ├── menu_list.html                        # Дочерний шаблон меню
│   │   ├── views.py                              # Пример Django-view
│   │   └── urls.py                              # URL-конфигурация
│   └── 05_cafe_menu_complete/
│       ├── menu_list.html                        # Полный шаблон меню с поиском
│       └── static/cafe/
│           ├── css/style.css                     # CSS страницы меню
│           └── js/menu.js                        # JS-фильтрация по категориям
└── exercises/
    └── frontend_practice.md                      # Практические задания
```

---

## Дополнительные материалы

- [MDN Web Docs — HTML](https://developer.mozilla.org/ru/docs/Web/HTML) — справочник по тегам и атрибутам на русском
- [MDN Flexbox Guide](https://developer.mozilla.org/ru/docs/Learn/CSS/CSS_layout/Flexbox) — пошаговое руководство по Flexbox с примерами
- [Django Templates](https://docs.djangoproject.com/en/5.0/topics/templates/) — официальная документация: теги, фильтры, наследование
- [Django Static Files](https://docs.djangoproject.com/en/5.0/howto/static-files/) — как настроить и использовать статику в Django
- [JavaScript.info](https://javascript.info/ru) — лучший учебник по JavaScript на русском (от основ до продвинутых тем)
