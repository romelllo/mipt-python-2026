# Семинар 13: Введение в анализ данных (Pandas & NumPy)

**Модуль:** 4 — Анализ данных в Python  
**Дата:** 27.04.2026  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1gEpRjo0QKrWedUcA3dfMm9VLagOiAR4KCUx4lxPBz2I/edit?usp=sharing)

---

## Цели семинара

- **Называть** роли библиотек Pandas и NumPy и загружать данные из CSV в DataFrame.
- **Находить** структурные проблемы данных: пропуски, дубликаты, неверные типы.
- **Реализовывать** фильтрацию, группировку и агрегацию с помощью Pandas.
- **Применять** операции NumPy: индексация, reshape, transpose, нормализация.
- **Выбирать** подходящий инструмент (loc/iloc, groupby/transform, dot/solve) для конкретной задачи.

---

## Подготовка

```bash
# Из корня репозитория
uv sync

# Перейдите в директорию семинара
cd seminars/seminar_13_data_analysis_basics

# Проверьте, что всё работает
python examples/01_intro_load.py
```

---

## План семинара

Каждый теоретический блок сразу сопровождается практикой — не ждите конца семинара.

| Время  | Тема                                                        | Практика                              |
|--------|-------------------------------------------------------------|---------------------------------------|
| 15 мин | Блоки 1–2: Введение + структура DataFrame                   | → Упражнения: Часть 1                 |
| 30 мин | Блоки 3–4: Осмотр данных + предобработка                    | → Упражнения: Часть 2                 |
| 20 мин | Блоки 5–6: Индексация, фильтрация + GroupBy                 | → Упражнения: Часть 3                 |
| 10 мин | Блок 7: NumPy массивы                                       | → Упражнения: Часть 4                 |
| 10 мин | Блок 8: Векторизованные операции и линейная алгебра         | → Упражнения: Часть 5                 |
| 5 мин  | Подведение итогов                        |      —            |

---

## Блок 1: Введение в Pandas и NumPy (5 мин)

**NumPy** — фундамент числовых вычислений в Python. Предоставляет быстрый многомерный массив `ndarray` и математические операции над ним без Python-циклов.

**Pandas** — библиотека для работы с табличными данными. Строится поверх NumPy и добавляет именованные строки/столбцы, удобную работу с пропусками и мощные инструменты агрегации.

```python
import numpy as np
import pandas as pd

# NumPy: быстрая математика над массивами
arr = np.array([85, 91, 60, 77, 95])
print(arr.mean())   # 81.6 — без единого цикла

# Pandas: загрузка CSV в таблицу
df = pd.read_csv("data/students.csv")
print(type(df))     # <class 'pandas.core.frame.DataFrame'>
print(len(df))      # 30
```

**Когда использовать:** Pandas — для табличных данных с именованными столбцами. NumPy — для числовых матриц и линейной алгебры.

> **Подробнее:** см. файл [`examples/01_intro_load.py`](examples/01_intro_load.py) — загрузка CSV, создание Series и DataFrame вручную, обзор форматов (Excel, JSON, SQL).

### Практика

После Блока 2 перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 1** (задания 1.1–1.2).

---

## Блок 2: Структура и атрибуты DataFrame (10 мин)

Прежде чем анализировать данные, нужно понять их структуру. Pandas предоставляет набор атрибутов для этого.

| Атрибут   | Что возвращает                          | Пример                  |
|-----------|-----------------------------------------|-------------------------|
| `ndim`    | Количество измерений (всегда 2)         | `2`                     |
| `shape`   | Кортеж (строки, столбцы)               | `(30, 7)`               |
| `size`    | Общее число ячеек                       | `210`                   |
| `columns` | Index с именами столбцов               | `Index(['name', ...])`  |
| `dtypes`  | Тип данных каждого столбца             | `name: object, age: int64` |
| `axes`    | Список [индекс строк, индекс столбцов] | `[RangeIndex(30), Index(...)]` |

```python
df = pd.read_csv("data/students.csv")

print(df.shape)    # (30, 7)
print(df.columns.tolist())
# ['name', 'age', 'city', 'grade_math', 'grade_physics', 'grade_cs', 'scholarship']

# Только числовые столбцы
numeric = df.select_dtypes(include="number")
print(numeric.columns.tolist())
# ['age', 'grade_math', 'grade_physics', 'grade_cs', 'scholarship']
```

> **Подробнее:** см. файл [`examples/02_dataframe_structure.py`](examples/02_dataframe_structure.py) — все атрибуты с примерами, `set_index` и `reset_index`.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 1** (задание 1.2 — работа с именным индексом).

---

## Блок 3: Быстрый осмотр данных (10 мин)

Четыре метода, которые нужно вызывать **на любом новом датасете**:

```python
df.head()      # первые 5 строк — посмотреть на данные
df.tail(3)     # последние 3 строки
df.info()      # структура: типы, non-null counts, память
df.describe()  # статистика: mean, std, min, max, квартили
```

**Проблема:** `info()` показывает `Non-Null Count` — если он меньше общего числа строк, в столбце есть пропуски.

```python
df.info()
# scholarship    21 non-null    float64
# ↑ 30 строк, но только 21 non-null → 9 пропусков!
```

**Дополнительно:** `value_counts()` — частота значений в категориальном столбце:

```python
df["city"].value_counts()
# Москва              8
# Санкт-Петербург     7
# Казань              7
# Новосибирск         7
```

> **Подробнее:** см. файл [`examples/03_inspection.py`](examples/03_inspection.py) — `head/tail`, `info`, `describe` с `include="all"`, `value_counts` с нормировкой.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 2** (задание 2.1).

---

## Блок 4: Предобработка данных (20 мин)

Реальные данные всегда «грязные». Предобработка — обязательный шаг перед анализом.

### Пропущенные значения

**Проблема:** NaN в числовых столбцах ломает агрегаты и модели.
**Решение:** обнаружить → выбрать стратегию → применить.

```python
# Обнаружение
df.isnull().sum()          # количество NaN в каждом столбце

# Стратегия 1: удалить строки с пропусками
df_clean = df.dropna(subset=["scholarship"])

# Стратегия 2: заполнить медианой (устойчива к выбросам)
median_val = df["scholarship"].median()
df["scholarship"] = df["scholarship"].fillna(median_val)
```

**Когда использовать:** `dropna` — если пропусков мало (<5%). `fillna(median)` — если пропусков много или нельзя терять строки.

### Дубликаты

```python
df.duplicated().sum()      # количество дублей
df[df.duplicated(keep=False)]  # показать все дублирующиеся строки
df = df.drop_duplicates()  # оставить только уникальные
```

### Операции со столбцами

```python
# Переименование
df = df.rename(columns={"grade_cs": "grade_computer_science"})

# Добавление вычисляемого столбца
df["grade_avg"] = (df["grade_math"] + df["grade_physics"] + df["grade_cs"]) / 3

# Удаление
df = df.drop(columns=["grade_avg"])
```

> **Подробнее:** см. файл [`examples/04_preprocessing.py`](examples/04_preprocessing.py) — полный пайплайн: пропуски, дубликаты, rename, add/drop columns, astype.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 2** (задание 2.2).

---

## Блок 5: Индексация и фильтрация (10 мин)

### loc и iloc

| Метод  | Принцип         | Пример                              |
|--------|-----------------|-------------------------------------|
| `loc`  | По **меткам**   | `df.loc[0:4, ["name", "city"]]`     |
| `iloc` | По **позиции**  | `df.iloc[0:5, 0:2]`                 |

> ⚠️ `loc` включает правую границу среза, `iloc` — нет (как обычные срезы Python).

```python
# loc — по меткам строк и именам столбцов
df.loc[0:2, ["name", "grade_math"]]

# iloc — по числовым позициям
df.iloc[0:3, 0:3]   # строки 0,1,2 и столбцы 0,1,2
df.iloc[-3:]        # последние 3 строки
```

### Булева индексация

```python
# Одно условие
df[df["city"] == "Москва"]

# Несколько условий: & (и), | (или), ~ (не)
df[(df["grade_math"] >= 90) & (df["city"] == "Санкт-Петербург")]

# query() — читаемый строковый синтаксис
df.query("grade_cs >= 90 and age <= 20")
```

> **Подробнее:** см. файл [`examples/05_indexing_filtering.py`](examples/05_indexing_filtering.py) — `loc`, `iloc`, булева индексация, `isin()`, `query()`.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 3** (задание 3.1).

---

## Блок 6: GroupBy и агрегация (10 мин)

`groupby()` реализует паттерн **Split → Apply → Combine**: разбить данные на группы, применить функцию к каждой группе, объединить результаты.

```python
# Среднее по одному столбцу
df.groupby("city")["grade_math"].mean()

# Несколько агрегатных функций через agg()
df.groupby("city").agg(
    avg_math=("grade_math", "mean"),
    total_scholarship=("scholarship", "sum"),
    count=("name", "count"),
)
```

**transform()** — агрегат той же длины, что исходный DataFrame (для добавления нового столбца):

```python
# Средний балл по городу для каждой строки
df["city_avg"] = df.groupby("city")["grade_math"].transform("mean")

# Отклонение от среднего по городу
df["vs_city_avg"] = df["grade_math"] - df["city_avg"]
```

**Когда использовать:** `agg()` — для сводных таблиц. `transform()` — для добавления группового агрегата как нового столбца.

> **Подробнее:** см. файл [`examples/06_groupby.py`](examples/06_groupby.py) — `groupby`, `agg`, `transform`, сортировка результатов.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 3** (задание 3.2).

---

## Блок 7: NumPy массивы (10 мин)

`ndarray` — основной объект NumPy. Все элементы одного типа, хранятся в непрерывной памяти → операции в 10–100 раз быстрее Python-списков.

### Атрибуты ndarray

```python
arr = np.array([[1.0, 2.5, 3.7], [4.1, 5.9, 6.3]])

arr.ndim   # 2 — количество измерений
arr.shape  # (2, 3) — строки × столбцы
arr.size   # 6 — всего элементов
arr.dtype  # float64 — тип элементов
```

### Индексация

```python
mat = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

mat[0, 1]    # 2 — строка 0, столбец 1
mat[1, :]    # [4, 5, 6] — вся строка 1
mat[:, 2]    # [3, 6, 9] — весь столбец 2
mat[0:2, 0:2]  # подматрица 2×2
```

### reshape и transpose

```python
arr = np.arange(12)          # [0, 1, ..., 11]
mat = arr.reshape(3, 4)      # матрица 3×4
mat_T = mat.T                # транспонирование → (4, 3)
flat = mat.flatten()         # обратно в 1D
```

> **Подробнее:** см. файл [`examples/07_numpy_arrays.py`](examples/07_numpy_arrays.py) — создание массивов, атрибуты, индексация 1D/2D, reshape, flatten, transpose.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 4** (задания 4.1–4.2).

---

## Блок 8: Векторизованные операции и линейная алгебра (10 мин)

### Векторизация

**Проблема:** Python-цикл по 1 000 000 элементов — медленно.
**Решение:** NumPy применяет операцию ко всему массиву сразу (C-код под капотом).

```python
grades = np.array([85.0, 91.0, 60.0, 77.0, 95.0])

grades + 10          # [95, 101, 70, 87, 105]
grades >= 85         # [True, True, False, False, True]
grades[grades >= 85] # [85, 91, 95]
```

### Нормализация

```python
# Min-max → [0, 1]
normalized = (grades - grades.min()) / (grades.max() - grades.min())

# Z-score → среднее=0, std=1
standardized = (grades - grades.mean()) / grades.std()
```

### Линейная алгебра

```python
# Норма вектора (евклидово расстояние от нуля)
np.linalg.norm(np.array([85, 78, 92]))   # ≈ 147.6

# Расстояние между двумя профилями
np.linalg.norm(student_a - student_b)

# Взвешенная сумма = скалярное произведение
weights = np.array([0.4, 0.3, 0.3])
np.dot(grades_vector, weights)           # взвешенный балл

# Решение системы Ax = b
x = np.linalg.solve(A, b)
```

> **Подробнее:** см. файл [`examples/08_vectorized_linalg.py`](examples/08_vectorized_linalg.py) — векторизация, нормализация, `linalg.norm`, `dot`, матричное умножение, `linalg.solve`.

### Практика

Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 5** (задания 5.1–5.2).

---

## Подведение итогов

### Шпаргалка

| Задача                          | Инструмент                                      |
|---------------------------------|-------------------------------------------------|
| Загрузить CSV                   | `pd.read_csv("file.csv")`                       |
| Структура таблицы               | `df.info()`, `df.shape`, `df.dtypes`            |
| Статистика                      | `df.describe()`                                 |
| Пропуски                        | `df.isnull().sum()`, `fillna()`, `dropna()`     |
| Дубликаты                       | `df.duplicated().sum()`, `drop_duplicates()`    |
| Фильтрация по условию           | `df[df["col"] > value]`, `df.query(...)`        |
| Выбор по позиции                | `df.iloc[rows, cols]`                           |
| Выбор по метке                  | `df.loc[rows, cols]`                            |
| Группировка + агрегация         | `df.groupby("col").agg(...)`                    |
| Групповой агрегат как столбец   | `df.groupby("col")["val"].transform("mean")`    |
| Быстрая математика              | NumPy: `arr * 2`, `arr.mean()`, `np.sqrt(arr)`  |
| Нормализация                    | `(x - x.min()) / (x.max() - x.min())`          |
| Расстояние между векторами      | `np.linalg.norm(a - b)`                         |
| Взвешенная сумма                | `np.dot(values, weights)`                       |
| Решение системы уравнений       | `np.linalg.solve(A, b)`                         |

### Ключевые выводы

1. **Сначала осмотр, потом анализ.** Всегда начинайте с `info()` и `describe()` — это экономит часы отладки.
2. **Предобработка — не опциональна.** Пропуски и дубликаты искажают любой анализ. Обрабатывайте их явно.
3. **Векторизация вместо циклов.** Если вы пишете `for` над DataFrame или ndarray — скорее всего, есть более быстрый способ.

---

## Файлы семинара

```
seminar_13_data_analysis_basics/
├── README.md                          # Этот файл
├── data/
│   └── students.csv                   # Датасет студентов (30 строк, 7 столбцов)
├── examples/
│   ├── 01_intro_load.py               # Введение: NumPy, Pandas, загрузка CSV
│   ├── 02_dataframe_structure.py      # Атрибуты DataFrame: shape, dtypes, axes
│   ├── 03_inspection.py               # head, tail, info, describe, value_counts
│   ├── 04_preprocessing.py            # Пропуски, дубликаты, операции со столбцами
│   ├── 05_indexing_filtering.py       # loc, iloc, булева индексация, query
│   ├── 06_groupby.py                  # groupby, agg, transform
│   ├── 07_numpy_arrays.py             # ndarray, атрибуты, индексация, reshape, .T
│   └── 08_vectorized_linalg.py        # Векторизация, нормализация, norm, dot, solve
└── exercises/
    └── exercises.md                   # Практические задания (Части 1–5 + Бонус)
```

**Запуск примеров** (из директории семинара):

```bash
python examples/01_intro_load.py
python examples/04_preprocessing.py
python examples/08_vectorized_linalg.py
```

---

## Дополнительные материалы

- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html) — официальный быстрый старт, охватывает 80% повседневных задач
- [NumPy Quickstart Tutorial](https://numpy.org/doc/stable/user/quickstart.html) — официальный туториал по ndarray
- [Real Python: Pandas DataFrames 101](https://realpython.com/pandas-dataframe/) — подробный разбор с примерами
- [Real Python: NumPy Tutorial](https://realpython.com/numpy-tutorial/) — NumPy с нуля до линейной алгебры
- [Pandas Cheat Sheet (PDF)](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf) — шпаргалка для распечатки
