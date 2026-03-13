/**
 * Семинар 7: JavaScript для страницы меню кафе
 * Файл: static/cafe/js/menu.js
 *
 * В Django подключается через:
 *   {% load static %}
 *   <script src="{% static 'cafe/js/menu.js' %}"></script>
 *
 * Функциональность:
 *   1. Фильтрация карточек меню по категории (кнопки)
 *   2. Поиск по названию блюда (поле ввода)
 *   3. Обновление счётчика видимых карточек
 *
 * Примечание: скрипт работает с data-атрибутами карточек:
 *   data-category="{{ item.category.id }}"  — для фильтра по категории
 *   data-name="{{ item.name|lower }}"        — для поиска по названию
 */

// ============================================================
// Инициализация: ждём полной загрузки DOM
// ============================================================
document.addEventListener("DOMContentLoaded", function () {

  // Находим все нужные элементы
  const menuGrid = document.getElementById("menu-grid");
  const filterButtons = document.querySelectorAll(".filter-btn");
  const searchInput = document.getElementById("menu-search");
  const visibleCountEl = document.getElementById("visible-count");
  const noResultsEl = document.getElementById("no-results");

  // Если на странице нет меню — ничего не делаем
  if (!menuGrid) return;

  // Получаем все карточки меню
  const cards = menuGrid.querySelectorAll(".menu-card");

  // Текущее состояние фильтров
  let activeCategory = "all";  // "all" или id категории (строка)
  let searchQuery = "";         // Текст из поля поиска

  // ============================================================
  // Главная функция: применить оба фильтра и обновить счётчик
  // ============================================================
  function applyFilters() {
    let visibleCount = 0;

    cards.forEach(function (card) {
      const cardCategory = card.dataset.category;  // Из data-category="..."
      const cardName = card.dataset.name;           // Из data-name="..."

      // Проверяем фильтр по категории
      const categoryMatch =
        activeCategory === "all" || cardCategory === activeCategory;

      // Проверяем поиск по названию
      const searchMatch = cardName.includes(searchQuery);

      // Карточка видима только если оба условия выполнены
      if (categoryMatch && searchMatch) {
        card.style.display = "";   // Показать карточку
        visibleCount++;
      } else {
        card.style.display = "none";  // Скрыть карточку
      }
    });

    // Обновляем счётчик
    if (visibleCountEl) {
      visibleCountEl.textContent = visibleCount;
    }

    // Показываем «Ничего не найдено» если нет результатов
    if (noResultsEl) {
      noResultsEl.style.display = visibleCount === 0 ? "block" : "none";
    }
  }

  // ============================================================
  // Фильтрация по категории: обработчик кнопок
  // ============================================================
  filterButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      // Убираем класс "активна" у всех кнопок
      filterButtons.forEach(function (b) {
        b.classList.remove("filter-btn--active");
      });

      // Добавляем класс "активна" нажатой кнопке
      btn.classList.add("filter-btn--active");

      // Обновляем текущую категорию
      activeCategory = btn.dataset.category;

      // Применяем фильтры
      applyFilters();
    });
  });

  // ============================================================
  // Поиск по названию: обработчик поля ввода
  // ============================================================
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      // Приводим к нижнему регистру для поиска без учёта регистра
      searchQuery = searchInput.value.toLowerCase().trim();
      applyFilters();
    });
  }

  // Начальное применение фильтров (на случай если URL содержит ?category=)
  applyFilters();

  console.log("menu.js загружен. Карточек:", cards.length);
});
