"""
Семинар 6: ForeignKey и связи между моделями.

Этот модуль демонстрирует:
- ForeignKey — связь «многие к одному»
- Параметр on_delete и все его варианты
- Прямой и обратный доступ к связанным объектам
- Примеры моделей с различными типами связей

Примечание: этот файл содержит примеры кода Django для изучения.
Он выводит примеры на экран.
"""

# ============================================================
# 1. ForeignKey — определение связи
# ============================================================

FOREIGNKEY_BASICS = """
=== ForeignKey — связь «многие к одному» ===

# Один заказ принадлежит одному клиенту,
# но у клиента может быть много заказов.

from django.db import models


class Category(models.Model):
    \"\"\"Категория блюд.\"\"\"
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    \"\"\"Позиция в меню — принадлежит одной категории.\"\"\"
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,                  # Связь с моделью Category
        on_delete=models.CASCADE,  # Что делать при удалении категории
        related_name="items",      # Имя для обратного доступа
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Order(models.Model):
    \"\"\"Заказ клиента.\"\"\"
    customer_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.pk} — {self.customer_name}"


class OrderItem(models.Model):
    \"\"\"Позиция в заказе — связывает заказ с пунктом меню.\"\"\"
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT,  # Нельзя удалить блюдо, если оно в заказе
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"
"""

# ============================================================
# 2. on_delete — стратегии удаления
# ============================================================

ON_DELETE_OPTIONS = """
=== on_delete — что происходит при удалении родительского объекта ===

1. CASCADE — каскадное удаление
   Удаляется родитель → удаляются все дочерние объекты.

   category = models.ForeignKey(Category, on_delete=models.CASCADE)
   # Удалили категорию "Напитки" → удалились Капучино, Латте, Эспрессо

   Когда использовать:
   - Комментарии к посту (удалён пост → удалены комментарии)
   - Позиции заказа (удалён заказ → удалены позиции)


2. PROTECT — запрет удаления
   Если есть дочерние объекты, удаление запрещено (ProtectedError).

   category = models.ForeignKey(Category, on_delete=models.PROTECT)
   # Нельзя удалить категорию "Напитки", пока в ней есть блюда

   Когда использовать:
   - Категории товаров (нельзя случайно удалить с товарами)
   - Авторы книг (нельзя удалить автора, пока есть его книги)


3. SET_NULL — установка NULL
   При удалении родителя у дочерних объектов поле = NULL.
   ВАЖНО: нужно null=True в определении поля!

   category = models.ForeignKey(
       Category, on_delete=models.SET_NULL, null=True
   )
   # Удалили категорию → у блюд category = None

   Когда использовать:
   - Отдел сотрудника (отдел расформирован → сотрудник без отдела)
   - Назначенный исполнитель задачи


4. SET_DEFAULT — установка значения по умолчанию
   При удалении родителя — ставится значение по умолчанию.
   ВАЖНО: нужно указать default!

   category = models.ForeignKey(
       Category, on_delete=models.SET_DEFAULT, default=1
   )
   # Удалили категорию → блюда переносятся в категорию с id=1

   Когда использовать:
   - Перенос в категорию "Разное" при удалении основной


5. DO_NOTHING — ничего не делать
   Django не предпринимает действий. Ответственность на программисте.
   Может привести к ошибкам целостности БД!

   category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

   Когда использовать:
   - Почти никогда. Только если БД сама обрабатывает каскады.
"""

# ============================================================
# 3. Работа со связанными объектами
# ============================================================

RELATED_OBJECTS = """
=== Работа со связанными объектами ===

# --- Прямой доступ (от дочернего к родительскому) ---

item = MenuItem.objects.get(name="Капучино")
print(item.category)           # <Category: Напитки>
print(item.category.name)      # "Напитки"
print(item.category.id)        # 1


# --- Обратный доступ (от родительского к дочерним) ---
# Используется related_name (или по умолчанию: модель_set)

drinks = Category.objects.get(name="Напитки")

# Все пункты меню в категории
drinks.items.all()
# <QuerySet [<MenuItem: Капучино>, <MenuItem: Латте>, ...]>

# Количество
drinks.items.count()  # 7

# Фильтрация связанных объектов
drinks.items.filter(price__lt=200)
# <QuerySet [<MenuItem: Эспрессо>]>

# Проверка наличия
drinks.items.exists()  # True


# --- Фильтрация через связи (двойное подчёркивание) ---

# Все пункты меню из категории "Напитки"
MenuItem.objects.filter(category__name="Напитки")

# Все категории, в которых есть недорогие пункты
Category.objects.filter(items__price__lt=200)

# Все заказы, содержащие Капучино
Order.objects.filter(items__menu_item__name="Капучино")


# --- Создание связанных объектов ---

# Через ForeignKey
order = Order.objects.create(customer_name="Алиса")
cappuccino = MenuItem.objects.get(name="Капучино")
OrderItem.objects.create(
    order=order,
    menu_item=cappuccino,
    quantity=2,
)

# Через обратную связь
order.items.create(
    menu_item=MenuItem.objects.get(name="Круассан"),
    quantity=1,
)
"""

# ============================================================
# 4. select_related и prefetch_related
# ============================================================

OPTIMIZATION = """
=== Оптимизация запросов ===

# Проблема N+1 запросов:
items = MenuItem.objects.all()
for item in items:
    print(item.category.name)  # Каждый раз — отдельный SQL-запрос!

# Решение 1: select_related (для ForeignKey, OneToOne)
# Делает JOIN — один запрос вместо N+1
items = MenuItem.objects.select_related("category").all()
for item in items:
    print(item.category.name)  # Данные уже загружены!

# Решение 2: prefetch_related (для обратных связей, ManyToMany)
# Делает 2 запроса вместо N+1
categories = Category.objects.prefetch_related("items").all()
for cat in categories:
    print(cat.items.count())  # Данные уже загружены!
"""


# ============================================================
# Функции демонстрации
# ============================================================


def demonstrate_foreignkey() -> None:
    """Демонстрация ForeignKey."""
    print("=" * 60)
    print("1. ForeignKey — определение связи")
    print("=" * 60)
    print(FOREIGNKEY_BASICS)


def demonstrate_on_delete() -> None:
    """Демонстрация on_delete."""
    print("\n" + "=" * 60)
    print("2. on_delete — стратегии удаления")
    print("=" * 60)
    print(ON_DELETE_OPTIONS)


def demonstrate_related() -> None:
    """Демонстрация работы со связанными объектами."""
    print("\n" + "=" * 60)
    print("3. Работа со связанными объектами")
    print("=" * 60)
    print(RELATED_OBJECTS)


def demonstrate_optimization() -> None:
    """Демонстрация оптимизации запросов."""
    print("\n" + "=" * 60)
    print("4. Оптимизация: select_related / prefetch_related")
    print("=" * 60)
    print(OPTIMIZATION)


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 6: FOREIGNKEY И СВЯЗИ МЕЖДУ МОДЕЛЯМИ")
    print("=" * 60)

    demonstrate_foreignkey()
    demonstrate_on_delete()
    demonstrate_related()
    demonstrate_optimization()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
