/**
 * Семинар 7: Внешний JavaScript-файл для 03_javascript_basics.html
 *
 * Этот файл подключается через <script src="03_script.js" defer>
 * и обрабатывает:
 *   - Счётчик (блок 2)
 *   - Показать/скрыть сообщение (блок 3)
 *   - Фильтрацию списка по вводу (блок 4)
 *
 * defer гарантирует, что скрипт выполнится после загрузки всего HTML,
 * поэтому все document.getElementById(...) найдут свои элементы.
 */

// ============================================================
// Блок 2: Счётчик — изменение textContent элемента
// ============================================================

// Находим элемент с id="counter-value"
const counterDisplay = document.getElementById("counter-value");

// Счётчик хранится в переменной JavaScript
let count = 0;

// Функция обновления отображения счётчика
function updateCounter() {
  // .textContent — текстовое содержимое элемента (безопаснее, чем .innerHTML)
  counterDisplay.textContent = count;
}

// Кнопка "+1": при клике увеличить счётчик
document.getElementById("btn-increment").addEventListener("click", function () {
  count += 1;
  updateCounter();
  console.log("Счётчик увеличен до:", count);
});

// Кнопка "−1": при клике уменьшить счётчик
document.getElementById("btn-decrement").addEventListener("click", function () {
  count -= 1;
  updateCounter();
  console.log("Счётчик уменьшен до:", count);
});

// Кнопка "Сбросить": вернуть к нулю
document.getElementById("btn-reset").addEventListener("click", function () {
  count = 0;
  updateCounter();
  console.log("Счётчик сброшен.");
});

// ============================================================
// Блок 3: Показать / скрыть элемент
// ============================================================

const btnToggle = document.getElementById("btn-toggle");
const statusMessage = document.getElementById("status-message");

// Флаг: сейчас видимо или скрыто?
let isVisible = false;

btnToggle.addEventListener("click", function () {
  if (isVisible) {
    // Скрыть: устанавливаем display: none через style
    statusMessage.style.display = "none";
    btnToggle.textContent = "Показать сообщение";
    isVisible = false;
  } else {
    // Показать: убираем скрытие
    statusMessage.style.display = "block";
    btnToggle.textContent = "Скрыть сообщение";
    isVisible = true;
  }
});

// ============================================================
// Блок 4: Фильтрация списка при вводе текста
// ============================================================

const filterInput = document.getElementById("filter-input");
// querySelectorAll — найти ВСЕ <li> внутри #menu-list
const menuItems = document.querySelectorAll("#menu-list li");

// Событие "input" — срабатывает при каждом изменении текста в поле
filterInput.addEventListener("input", function () {
  // .value — текущее значение поля ввода
  // .toLowerCase() — привести к нижнему регистру для сравнения без учёта регистра
  const query = filterInput.value.toLowerCase();

  // Перебираем все элементы списка
  menuItems.forEach(function (item) {
    // data-name — пользовательский атрибут, заданный в HTML
    const name = item.dataset.name.toLowerCase();

    if (name.includes(query)) {
      // Показать элемент
      item.style.display = "";
    } else {
      // Скрыть элемент
      item.style.display = "none";
    }
  });
});

// Сообщение в консоли при загрузке скрипта
console.log("03_script.js загружен! Блоки 2, 3, 4 активны.");
