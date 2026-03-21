# Покрытие тестами (Test Coverage)

## Что такое покрытие?

**Coverage (покрытие)** — метрика, показывающая, какой процент кода был выполнен во время тестов. Инструмент `pytest-cov` анализирует, какие строки и ветви кода покрыты тестами, а какие — нет.

```
Строка покрыта ✅  →  тест выполнил эту строку хотя бы раз
Строка не покрыта ❌ →  ни один тест не дошёл до этой строки
```

## Установка

```bash
# pytest-cov уже есть в dev-зависимостях проекта
uv sync

# Проверка
python -c "import pytest_cov; print('pytest-cov установлен')"
```

## Запуск с покрытием

```bash
# Базовый запуск — вывод в терминал (отчёт term-missing)
pytest --cov=seminars/seminar_08_testing_and_containerization/examples \
       --cov-report=term-missing \
       seminars/seminar_08_testing_and_containerization/examples/02_pytest_basics.py -v

# Покрытие с HTML-отчётом (открыть htmlcov/index.html)
pytest --cov=seminars/seminar_08_testing_and_containerization/examples \
       --cov-report=html \
       --cov-report=term-missing \
       seminars/seminar_08_testing_and_containerization/examples/ -v

# Минимальный процент покрытия (упасть, если меньше 80%)
pytest --cov=seminars/seminar_08_testing_and_containerization/examples \
       --cov-fail-under=80 \
       seminars/seminar_08_testing_and_containerization/examples/ -v
```

## Чтение отчёта в терминале

```
---------- coverage: platform darwin, python 3.11 ----------
Name                                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------------------
seminars/seminar_08_testing_and_containerization/examples/01_...py      87      4    95%   45, 102-104
seminars/seminar_08_testing_and_containerization/examples/02_...py      61      0   100%
---------------------------------------------------------------------------------------
TOTAL                                                     148      4    97%
```

| Колонка | Значение |
|---------|---------|
| `Stmts` | Всего исполняемых строк в файле |
| `Miss` | Строк, не выполненных ни одним тестом |
| `Cover` | Процент покрытых строк |
| `Missing` | Номера непокрытых строк |

## HTML-отчёт

После запуска с `--cov-report=html` откройте файл `htmlcov/index.html` в браузере:

- **Зелёные строки** — покрыты тестами ✅
- **Красные строки** — не покрыты ❌
- **Жёлтые строки** — частичное покрытие ветвей (branch coverage)

```bash
# Открыть HTML-отчёт (macOS)
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html
```

## Branch coverage (покрытие ветвей)

Обычный coverage считает строки. **Branch coverage** проверяет, были ли покрыты все ветви условий (`if`/`else`):

```bash
# Включить покрытие ветвей
pytest --cov=. --cov-branch --cov-report=term-missing .
```

Пример: если у вас есть `if x > 0: return "positive" else: return "negative"`,
branch coverage потребует тестов для обоих случаев.

## Конфигурация в pyproject.toml

Чтобы не писать флаги каждый раз, добавьте в `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--cov=seminars --cov-report=term-missing --cov-fail-under=70"

[tool.coverage.run]
branch = true           # включить branch coverage
omit = [
    "*/migrations/*",   # пропустить миграции Django
    "*/tests/*",        # не считать сами тесты
    "*/__init__.py",    # пропустить инит-файлы
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",     # строка с этим комментарием игнорируется
    "if __name__ == .__main__.:",  # блок main() не считаем
    "raise NotImplementedError",
]
```

## Сколько процентов покрытия достаточно?

| Уровень | Процент | Когда достаточно |
|---------|---------|-----------------|
| Минимум | 70–80%  | Небольшие учебные проекты |
| Хороший | 80–90%  | Продакшн-код без критичной безопасности |
| Высокий | 90–100% | Финансовые системы, медицина, безопасность |

> **Важно:** 100% покрытие ≠ отсутствие багов. Покрытие показывает,
> что код был *выполнен*, но не то, что он *правильно* работает.
> Важнее качество тестов, чем процент покрытия.

## Пример: интерпретация отчёта

```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
calculate.py            20      3    85%   34-36

# Строки 34-36:
# 34:    if quantity < 0:
# 35:        raise ValueError(...)   ← нет теста для отрицательного количества!
# 36:    if price > MAX_PRICE:
```

**Что делать:** добавить тест для отрицательного количества — `pytest.raises(ValueError)`.
