# Практические задания: Введение в анализ данных (Pandas & NumPy)

## Подготовка

```bash
# Из директории семинара
cd seminars/seminar_13_data_analysis_basics

# Убедитесь, что зависимости установлены
uv sync

# Запустите любой пример для проверки окружения
python examples/01_intro_load.py
```

> **Как работать с заданиями:** прочитайте условие, попробуйте ответить самостоятельно, и только после этого раскройте решение для проверки.

---

## Часть 1: Введение и структура DataFrame

> **Теория:** [README.md — Блок 1](../README.md#блок-1-введение-в-pandas-и-numpy-5-мин) и [Блок 2](../README.md#блок-2-структура-и-атрибуты-dataframe-10-мин) | **Примеры:** [`examples/01_intro_load.py`](../examples/01_intro_load.py), [`examples/02_dataframe_structure.py`](../examples/02_dataframe_structure.py)

### Задание 1.1

Загрузите `data/students.csv` в DataFrame. Выведите `shape` и список столбцов. Затем выведите только числовые столбцы, используя `select_dtypes`.

<details>
<summary>Подсказка</summary>

`pd.read_csv()` — загрузка. `df.shape` — кортеж (строки, столбцы). `df.columns.tolist()` — список имён. `df.select_dtypes(include="number")` — только числовые столбцы.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd

df = pd.read_csv("data/students.csv")
print(f"shape: {df.shape}")           # (30, 7)
print(f"столбцы: {df.columns.tolist()}")

numeric_cols = df.select_dtypes(include="number").columns.tolist()
print(f"числовые: {numeric_cols}")
# ['age', 'grade_math', 'grade_physics', 'grade_cs', 'scholarship']
```

</details>

---

### Задание 1.2

Загрузите датасет и установите столбец `name` как индекс. Убедитесь, что `df.index` теперь содержит имена. Затем обратитесь к строке `"Наталья Попова"` через `loc` и выведите её оценки по трём предметам.

<details>
<summary>Подсказка</summary>

`df.set_index("name")` — установить индекс. После этого `df.loc["Наталья Попова", ["grade_math", "grade_physics", "grade_cs"]]` вернёт нужные значения.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd

df = pd.read_csv("data/students.csv").set_index("name")
print(f"Тип индекса: {type(df.index)}")
print(f"Первые 3 значения индекса: {df.index[:3].tolist()}")

grades = df.loc["Наталья Попова", ["grade_math", "grade_physics", "grade_cs"]]
print("\nОценки Натальи Поповой:")
print(grades)
```

</details>

---

## Часть 2: Осмотр и предобработка данных

> **Теория:** [README.md — Блок 3](../README.md#блок-3-быстрый-осмотр-данных-10-мин) и [Блок 4](../README.md#блок-4-предобработка-данных-20-мин) | **Примеры:** [`examples/03_inspection.py`](../examples/03_inspection.py), [`examples/04_preprocessing.py`](../examples/04_preprocessing.py)

### Задание 2.1

Вызовите `df.info()` и `df.describe()`. Ответьте: в каком столбце есть пропуски и сколько их? Какой предмет имеет наибольшее стандартное отклонение оценок?

<details>
<summary>Подсказка</summary>

`info()` показывает `Non-Null Count` — если он меньше числа строк, есть пропуски. В `describe()` строка `std` содержит стандартные отклонения; `.idxmax()` найдёт столбец с максимумом.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd

df = pd.read_csv("data/students.csv")
df.info()
# scholarship имеет меньше non-null значений → в нём пропуски

stats = df.describe()
grade_cols = ["grade_math", "grade_physics", "grade_cs"]
most_spread = stats.loc["std", grade_cols].idxmax()
missing_count = df["scholarship"].isnull().sum()

print(f"\nПропусков в scholarship: {missing_count}")
print(f"Наибольший разброс оценок: {most_spread}")
```

</details>

---

### Задание 2.2

Напишите функцию `clean(df)`, которая:
1. Удаляет дубликаты.
2. Заполняет пропуски в `scholarship` медианой.
3. Добавляет столбец `grade_avg` — среднее трёх оценок (округлить до 1 знака).

Примените её к датасету и проверьте результат.

<details>
<summary>Подсказка</summary>

Работайте с копией: `df = df.copy()`. Медиана: `df["scholarship"].median()`. Новый столбец: сумма трёх столбцов, делённая на 3.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Удаляет дубликаты, заполняет пропуски, добавляет средний балл."""
    df = df.copy()
    df = df.drop_duplicates()
    df["scholarship"] = df["scholarship"].fillna(df["scholarship"].median())
    df["grade_avg"] = (
        (df["grade_math"] + df["grade_physics"] + df["grade_cs"]) / 3
    ).round(1)
    return df


df_raw = pd.read_csv("data/students.csv")
df_clean = clean(df_raw)

print(f"Строк: {len(df_clean)}  (было {len(df_raw)})")
print(f"Пропусков в scholarship: {df_clean['scholarship'].isnull().sum()}")
print(df_clean[["name", "grade_avg", "scholarship"]].head(5))
```

</details>

---

## Часть 3: Индексация и группировка

> **Теория:** [README.md — Блок 5](../README.md#блок-5-индексация-и-фильтрация-10-мин) и [Блок 6](../README.md#блок-6-groupby-и-агрегация-10-мин) | **Примеры:** [`examples/05_indexing_filtering.py`](../examples/05_indexing_filtering.py), [`examples/06_groupby.py`](../examples/06_groupby.py)

### Задание 3.1

Найдите студентов, у которых оценка по математике **выше среднего по их городу**. Выведите их имена, город и оценку. Используйте `groupby` + `transform`.

<details>
<summary>Подсказка</summary>

`df.groupby("city")["grade_math"].transform("mean")` возвращает Series той же длины, что DataFrame, — среднее по городу для каждой строки. Затем отфильтруйте булевой маской.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd

df = pd.read_csv("data/students.csv")
df["city_avg_math"] = df.groupby("city")["grade_math"].transform("mean")
above_avg = df[df["grade_math"] > df["city_avg_math"]]
print(above_avg[["name", "city", "grade_math", "city_avg_math"]].to_string(index=False))
```

</details>

---

### Задание 3.2

Постройте сводную таблицу по городам: среднее по каждому из трёх предметов и количество студентов. Отсортируйте по среднему баллу CS по убыванию.

<details>
<summary>Подсказка</summary>

`df.groupby("city").agg(...)` с именованными агрегатами: `avg_math=("grade_math", "mean")` и т.д. Сортировка: `.sort_values("avg_cs", ascending=False)`.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd

df = pd.read_csv("data/students.csv")
summary = df.groupby("city").agg(
    avg_math=("grade_math", "mean"),
    avg_physics=("grade_physics", "mean"),
    avg_cs=("grade_cs", "mean"),
    students=("name", "count"),
).round(1)
print(summary.sort_values("avg_cs", ascending=False))
```

</details>

---

## Часть 4: NumPy массивы

> **Теория:** [README.md — Блок 7](../README.md#блок-7-numpy-массивы-10-мин) | **Примеры:** [`examples/07_numpy_arrays.py`](../examples/07_numpy_arrays.py)

### Задание 4.1

Создайте массив из 12 чисел (1–12), измените форму на матрицу 3×4. Выведите атрибуты `ndim`, `shape`, `size`. Затем транспонируйте матрицу и убедитесь, что `shape` изменился на (4, 3).

<details>
<summary>Подсказка</summary>

`np.arange(1, 13).reshape(3, 4)` — создание и reshape. `.T` — транспонирование. Проверьте `shape` до и после.

</details>

<details>
<summary>Решение</summary>

```python
import numpy as np

mat = np.arange(1, 13).reshape(3, 4)
print(f"ndim={mat.ndim}, shape={mat.shape}, size={mat.size}")
print(mat)

mat_T = mat.T
print(f"\nПосле .T: shape={mat_T.shape}")
print(mat_T)
```

</details>

---

### Задание 4.2

Из матрицы 4×4 (числа 1–16) извлеките: вторую строку, третий столбец и подматрицу 2×2 из правого нижнего угла. Затем с помощью булевой индексации выберите все элементы матрицы, которые делятся на 3.

<details>
<summary>Подсказка</summary>

`mat[1, :]` — строка, `mat[:, 2]` — столбец, `mat[2:, 2:]` — правый нижний угол. Булева маска: `mat[mat % 3 == 0]`.

</details>

<details>
<summary>Решение</summary>

```python
import numpy as np

mat = np.arange(1, 17).reshape(4, 4)
print("Матрица:\n", mat)
print("Вторая строка:", mat[1, :])
print("Третий столбец:", mat[:, 2])
print("Правый нижний угол 2×2:\n", mat[2:, 2:])
print("Делятся на 3:", mat[mat % 3 == 0])
```

</details>

---

## Часть 5: Векторизованные операции и линейная алгебра

> **Теория:** [README.md — Блок 8](../README.md#блок-8-векторизованные-операции-и-линейная-алгебра-10-мин) | **Примеры:** [`examples/08_vectorized_linalg.py`](../examples/08_vectorized_linalg.py)

### Задание 5.1

Загрузите оценки по математике из CSV в массив NumPy. Примените min-max нормализацию. Проверьте, что минимум результата равен 0, максимум — 1.

<details>
<summary>Подсказка</summary>

`df["grade_math"].to_numpy(dtype=float)` — конвертация. Формула: `(x - x.min()) / (x.max() - x.min())`.

</details>

<details>
<summary>Решение</summary>

```python
import numpy as np
import pandas as pd

df = pd.read_csv("data/students.csv")
grades = df["grade_math"].to_numpy(dtype=float)

normalized = (grades - grades.min()) / (grades.max() - grades.min())
print(f"Минимум: {normalized.min():.4f}")   # 0.0
print(f"Максимум: {normalized.max():.4f}")  # 1.0
```

</details>

---

### Задание 5.2

Вычислите взвешенный итоговый балл для каждого студента: математика — 40%, физика — 30%, CS — 30%. Используйте `np.dot`. Добавьте результат как столбец `weighted_score` в DataFrame и выведите топ-3 студентов.

<details>
<summary>Подсказка</summary>

Матрица оценок: `df[cols].to_numpy(dtype=float)` — форма (N, 3). Вектор весов: `np.array([0.4, 0.3, 0.3])`. `np.dot(matrix, weights)` даёт вектор длины N. Топ-3: `.nlargest(3, "weighted_score")`.

</details>

<details>
<summary>Решение</summary>

```python
import numpy as np
import pandas as pd

df = pd.read_csv("data/students.csv").drop_duplicates()
cols = ["grade_math", "grade_physics", "grade_cs"]

grades_matrix = df[cols].to_numpy(dtype=float)
weights = np.array([0.4, 0.3, 0.3])

df = df.copy()
df["weighted_score"] = np.dot(grades_matrix, weights).round(1)
top3 = df.nlargest(3, "weighted_score")[["name", "city", "weighted_score"]]
print(top3.to_string(index=False))
```

</details>

---

## Бонусное задание

### Бонус: Полный пайплайн — от сырых данных до рейтинга

Объедините всё изученное: загрузите датасет, очистите его, вычислите взвешенный балл через NumPy и постройте итоговую таблицу городов с колонками `students`, `avg_weighted_score` и `top_student` (имя лучшего студента города). Отсортируйте по `avg_weighted_score` по убыванию.

<details>
<summary>Подсказка</summary>

1. Используйте функцию `clean()` из Части 2 (или напишите аналог).
2. Вычислите `weighted_score` через `np.dot`, как в Части 5.
3. Для `top_student` используйте `groupby("city")["weighted_score"].idxmax()`, затем возьмите имена через `df.loc[...]`.

</details>

<details>
<summary>Решение</summary>

```python
import numpy as np
import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Удаляет дубликаты и заполняет пропуски медианой."""
    df = df.copy()
    df = df.drop_duplicates()
    df["scholarship"] = df["scholarship"].fillna(df["scholarship"].median())
    return df


df = clean(pd.read_csv("data/students.csv")).reset_index(drop=True)

# Взвешенный балл через NumPy
cols = ["grade_math", "grade_physics", "grade_cs"]
weights = np.array([0.4, 0.3, 0.3])
df["weighted_score"] = np.dot(df[cols].to_numpy(dtype=float), weights).round(1)

# Сводная таблица городов
summary = df.groupby("city").agg(
    students=("name", "count"),
    avg_weighted_score=("weighted_score", "mean"),
)

# Лучший студент в каждом городе
top_idx = df.groupby("city")["weighted_score"].idxmax()
summary["top_student"] = df.loc[top_idx, ["city", "name"]].set_index("city")["name"]

summary["avg_weighted_score"] = summary["avg_weighted_score"].round(1)
print(summary.sort_values("avg_weighted_score", ascending=False))
```

</details>

---

## Полезные ресурсы

- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html) — официальный быстрый старт
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html) — официальный туториал
- [Real Python: Pandas DataFrames](https://realpython.com/pandas-dataframe/) — подробный разбор
- [Real Python: NumPy Tutorial](https://realpython.com/numpy-tutorial/) — NumPy с нуля
- [Pandas Cheat Sheet (PDF)](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf) — шпаргалка
