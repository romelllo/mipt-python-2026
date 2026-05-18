# Практические задания: Статистика в Python

## Подготовка

```bash
# Установить зависимости
uv sync

# Активировать окружение
source .venv/bin/activate

# Проверить наличие датасета
python -c "import pandas as pd; df = pd.read_csv('seminars/seminar_16_statistics/data/iris.csv'); print(df.shape)"
```

> **Как работать с заданиями:** попробуйте решить задание самостоятельно, прежде чем открывать подсказку или решение.

---

## Часть 1: Описательные статистики

> **Теория:** [README.md — Блок 1](../README.md#блок-1-описательные-статистики-20-мин) |
> **Примеры:** [`examples/01_descriptive_stats.py`](../examples/01_descriptive_stats.py)
>
> Меры центральной тенденции (среднее, медиана, мода, усечённое среднее),
> меры разброса (std, IQR, MAD), квантили, сводная статистика через pandas.

### Задание 1.1 — Сравнение среднего и медианы

Загрузите датасет `iris.csv`. Для столбца `sepal_length`:
1. Вычислите среднее, медиану и моду.
2. Объясните, почему среднее и медиана близки для этого признака.
3. Искусственно добавьте выброс (например, `1000`) и пересчитайте — что изменилось?

```python
import pandas as pd

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
# ваш код здесь
```

<details>
<summary>Подсказка</summary>

Используйте `.mean()`, `.median()`, `.mode()[0]`. Для добавления выброса создайте копию столбца: `col_with_outlier = pd.concat([df['sepal_length'], pd.Series([1000])])`.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
col = df["sepal_length"]

print("=== Исходные данные ===")
print(f"Среднее:  {col.mean():.3f}")
print(f"Медиана:  {col.median():.3f}")
print(f"Мода:     {col.mode()[0]:.3f}")
print("Среднее ≈ медиана → распределение близко к симметричному")

# Добавляем выброс
col_with_outlier = pd.concat([col, pd.Series([1000])], ignore_index=True)
print("\n=== С выбросом (1000) ===")
print(f"Среднее:  {col_with_outlier.mean():.3f}  ← сильно изменилось")
print(f"Медиана:  {col_with_outlier.median():.3f}  ← почти не изменилась")
print("Вывод: медиана устойчива к выбросам, среднее — нет.")
```

</details>

---

### Задание 1.2 — Меры разброса

Для каждого числового столбца датасета вычислите:
- стандартное отклонение (`std`)
- межквартильный размах (`IQR = Q3 - Q1`)
- коэффициент вариации (`CV = std / mean * 100%`)

Выведите результаты в виде таблицы. Какой признак относительно наиболее изменчив?

<details>
<summary>Подсказка</summary>

Используйте `.std()`, `.quantile(0.25)`, `.quantile(0.75)`. Коэффициент вариации вычислите вручную. Для красивого вывода можно создать `pd.DataFrame` из словаря.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

results = {}
for col in numeric_cols:
    s = df[col]
    std = s.std()
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    cv = std / s.mean() * 100
    results[col] = {"std": std, "IQR": iqr, "CV (%)": cv}

result_df = pd.DataFrame(results).T.round(3)
print(result_df)
print(f"\nНаиболее изменчивый признак: {result_df['CV (%)'].idxmax()}")
```

</details>

---

### Задание 1.3 — Сводная статистика по группам

С помощью `.groupby()` и `.agg()` выведите для каждого вида (species):
- среднее и медиану `petal_length`
- стандартное отклонение `petal_length`
- минимум и максимум `petal_length`

<details>
<summary>Подсказка</summary>

Используйте `df.groupby("species")["petal_length"].agg(...)`, передав словарь или список функций.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")

result = df.groupby("species")["petal_length"].agg(
    mean="mean",
    median="median",
    std="std",
    min="min",
    max="max",
)
print(result.round(3))
```

</details>

---

## Часть 2: Распределения и визуализация

> **Теория:** [README.md — Блок 2](../README.md#блок-2-распределения-и-визуализация-15-мин) |
> **Примеры:** [`examples/02_distributions_viz.py`](../examples/02_distributions_viz.py)
>
> Гистограммы, box plot, асимметрия и эксцесс.

### Задание 2.1 — Box plot и выбросы

Постройте box plot для `sepal_width` по каждому виду. Определите:
1. Есть ли выбросы у какого-либо вида?
2. У какого вида наибольший разброс (IQR)?

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
# ваш код здесь
```

<details>
<summary>Подсказка</summary>

Сгруппируйте данные по `species` и передайте списки в `plt.boxplot()`. Выбросы — точки за пределами усов. IQR = Q3 - Q1.

</details>

<details>
<summary>Решение</summary>

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")

species_list = df["species"].unique()
data = [df[df["species"] == s]["sepal_width"].values for s in species_list]

plt.figure(figsize=(8, 5))
plt.boxplot(data, labels=species_list, patch_artist=True)
plt.title("sepal_width по видам")
plt.ylabel("Ширина чашелистика (см)")
plt.show()

# IQR по видам
for s in species_list:
    col = df[df["species"] == s]["sepal_width"]
    iqr = col.quantile(0.75) - col.quantile(0.25)
    print(f"{s}: IQR = {iqr:.3f}")
```

</details>

---

### Задание 2.2 — Асимметрия и эксцесс

Вычислите асимметрию (skewness) и эксцесс (kurtosis) для всех числовых столбцов.
Для каких признаков распределение:
- правостороннее?
- левостороннее?
- остроконечное (лептокуртическое)?

<details>
<summary>Подсказка</summary>

Используйте `df[col].skew()` и `df[col].kurt()`. Правостороннее: skew > 0. Лептокуртическое: kurt > 0.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

print(f"{'Признак':<20} {'Асимметрия':>12} {'Эксцесс':>10}")
print("-" * 44)
for col in numeric_cols:
    skew = df[col].skew()
    kurt = df[col].kurt()
    skew_type = "правосторонняя" if skew > 0.5 else ("левосторонняя" if skew < -0.5 else "симметричная")
    print(f"{col:<20} {skew:>12.3f} {kurt:>10.3f}  ({skew_type})")
```

</details>

---

## Часть 3: Доверительные интервалы

> **Теория:** [README.md — Блок 3](../README.md#блок-3-доверительные-интервалы-20-мин) |
> **Примеры:** [`examples/03_confidence_intervals.py`](../examples/03_confidence_intervals.py)
>
> ДИ для среднего (scipy, statsmodels) и для доли.

### Задание 3.1 — ДИ для среднего при разных уровнях доверия

Вычислите 90%, 95% и 99% доверительные интервалы для среднего `petal_length`
у вида `virginica`. Сравните ширину интервалов.

<details>
<summary>Подсказка</summary>

Используйте `scipy.stats.t.interval(confidence, df=n-1, loc=mean, scale=sem)`,
где `sem = scipy.stats.sem(col)`.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd
from scipy import stats

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
col = df[df["species"] == "virginica"]["petal_length"]

n = len(col)
mean = col.mean()
se = stats.sem(col)

print(f"virginica petal_length: n={n}, среднее={mean:.4f}, SE={se:.4f}\n")

for confidence in [0.90, 0.95, 0.99]:
    ci = stats.t.interval(confidence, df=n - 1, loc=mean, scale=se)
    width = ci[1] - ci[0]
    print(f"  {int(confidence*100)}% ДИ: [{ci[0]:.4f}, {ci[1]:.4f}]  ширина={width:.4f}")
```

</details>

---

### Задание 3.2 — ДИ для доли

Какая доля цветков в датасете имеет `sepal_length > 6`?
Вычислите 95% доверительный интервал для этой доли тремя методами:
`normal`, `wilson`, `agresti_coull`.

<details>
<summary>Подсказка</summary>

Используйте `statsmodels.stats.proportion.proportion_confint(count, nobs, alpha=0.05, method=...)`.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd
from statsmodels.stats.proportion import proportion_confint

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
threshold = 6.0
successes = (df["sepal_length"] > threshold).sum()
n = len(df)
proportion = successes / n

print(f"sepal_length > {threshold}: {successes} из {n} ({proportion*100:.1f}%)\n")

for method in ["normal", "wilson", "agresti_coull"]:
    ci = proportion_confint(successes, n, alpha=0.05, method=method)
    print(f"  95% ДИ ({method:15s}): [{ci[0]:.4f}, {ci[1]:.4f}]")
```

</details>

---

## Часть 4: Проверка гипотез

> **Теория:** [README.md — Блок 4](../README.md#блок-4-проверка-гипотез-25-мин) |
> **Примеры:** [`examples/04_hypothesis_testing.py`](../examples/04_hypothesis_testing.py)
>
> Тест Шапиро-Уилка, t-тесты (независимые и парные), критерий Манна-Уитни.

### Задание 4.1 — Проверка нормальности

Проверьте нормальность распределения `petal_width` отдельно для каждого вида
с помощью теста Шапиро-Уилка (α = 0.05). Сделайте вывод.

<details>
<summary>Подсказка</summary>

`scipy.stats.shapiro(data)` возвращает `(statistic, p_value)`. Если p < 0.05 — отвергаем нормальность.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd
from scipy import stats

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
alpha = 0.05

print("Тест Шапиро-Уилка для petal_width по видам:\n")
for species in df["species"].unique():
    col = df[df["species"] == species]["petal_width"]
    stat, p = stats.shapiro(col)
    decision = "нормальное" if p >= alpha else "НЕ нормальное"
    print(f"  {species:<12}: stat={stat:.4f}, p={p:.4f}  → {decision}")
```

</details>

---

### Задание 4.2 — Независимый t-тест

Проверьте гипотезу: **средняя длина чашелистика (`sepal_length`) одинакова
у `setosa` и `versicolor`** (α = 0.05).

1. Сформулируйте H₀ и H₁.
2. Проведите t-тест (используйте `equal_var=False`).
3. Сделайте вывод и вычислите Cohen's d.

<details>
<summary>Подсказка</summary>

`scipy.stats.ttest_ind(group1, group2, equal_var=False)`.  
Cohen's d = (mean1 - mean2) / sqrt((std1² + std2²) / 2).

</details>

<details>
<summary>Решение</summary>

```python
import numpy as np
import pandas as pd
from scipy import stats

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
alpha = 0.05

g1 = df[df["species"] == "setosa"]["sepal_length"]
g2 = df[df["species"] == "versicolor"]["sepal_length"]

print("H₀: μ_setosa = μ_versicolor")
print("H₁: μ_setosa ≠ μ_versicolor\n")
print(f"setosa:     n={len(g1)}, среднее={g1.mean():.3f}, std={g1.std():.3f}")
print(f"versicolor: n={len(g2)}, среднее={g2.mean():.3f}, std={g2.std():.3f}\n")

stat, p = stats.ttest_ind(g1, g2, equal_var=False)
decision = "Отвергаем H₀" if p < alpha else "Не отвергаем H₀"
print(f"t = {stat:.4f},  p = {p:.4e}  → {decision}")

d = (g1.mean() - g2.mean()) / np.sqrt((g1.std() ** 2 + g2.std() ** 2) / 2)
print(f"Cohen's d = {d:.3f}")
```

</details>

---

### Задание 4.3 — Критерий Манна-Уитни

Сравните `petal_width` у `setosa` и `virginica` с помощью критерия Манна-Уитни.
Почему здесь предпочтителен непараметрический тест?

<details>
<summary>Подсказка</summary>

`scipy.stats.mannwhitneyu(x, y, alternative="two-sided")`. Сначала проверьте нормальность тестом Шапиро.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd
from scipy import stats

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
alpha = 0.05

g1 = df[df["species"] == "setosa"]["petal_width"]
g2 = df[df["species"] == "virginica"]["petal_width"]

# Проверка нормальности
for name, g in [("setosa", g1), ("virginica", g2)]:
    _, p = stats.shapiro(g)
    print(f"Шапиро {name}: p={p:.4f}  → {'нормальное' if p >= alpha else 'НЕ нормальное'}")

print("\nH₀: распределения petal_width одинаковы")
print("H₁: одно сдвинуто относительно другого\n")

stat, p = stats.mannwhitneyu(g1, g2, alternative="two-sided")
decision = "Отвергаем H₀" if p < alpha else "Не отвергаем H₀"
print(f"U = {stat:.1f},  p = {p:.4e}  → {decision}")
print(f"\nМедианы: setosa={g1.median():.3f}, virginica={g2.median():.3f}")
```

</details>

---

## Часть 5: Корреляционный анализ

> **Теория:** [README.md — Блок 5](../README.md#блок-5-корреляция-10-мин) |
> **Примеры:** [`examples/05_correlation.py`](../examples/05_correlation.py)
>
> Корреляция Пирсона и Спирмена, визуализация.

### Задание 5.1 — Корреляционная матрица

Вычислите корреляционные матрицы (Пирсон и Спирмен) для числовых признаков датасета.
Найдите пару признаков с наибольшей положительной корреляцией по Пирсону.

<details>
<summary>Подсказка</summary>

`df.corr(method="pearson")` и `df.corr(method="spearman")`. Чтобы найти максимум без диагонали, используйте `.where(lambda x: x < 1).stack().idxmax()`.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
numeric_df = df.select_dtypes(include="number")

pearson = numeric_df.corr(method="pearson")
spearman = numeric_df.corr(method="spearman")

print("Пирсон:\n", pearson.round(3))
print("\nСпирмен:\n", spearman.round(3))

# Максимальная корреляция (без диагонали)
max_pair = pearson.where(pearson < 1).stack().idxmax()
max_val = pearson.loc[max_pair]
print(f"\nМаксимальная корреляция Пирсона: {max_pair[0]} × {max_pair[1]} = {max_val:.3f}")
```

</details>

---

### Задание 5.2 — Значимость корреляции

Проверьте статистическую значимость корреляции между `sepal_length` и `sepal_width`.
Вычислите r Пирсона и r Спирмена, p-значения и сделайте вывод.

<details>
<summary>Подсказка</summary>

`scipy.stats.pearsonr(x, y)` и `scipy.stats.spearmanr(x, y)` возвращают `(correlation, p_value)`.

</details>

<details>
<summary>Решение</summary>

```python
import pandas as pd
from scipy import stats

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
x = df["sepal_length"]
y = df["sepal_width"]
alpha = 0.05

r_p, p_p = stats.pearsonr(x, y)
r_s, p_s = stats.spearmanr(x, y)

print(f"Пирсон:  r={r_p:.4f}, p={p_p:.4f}  → {'значимо' if p_p < alpha else 'не значимо'}")
print(f"Спирмен: r={r_s:.4f}, p={p_s:.4f}  → {'значимо' if p_s < alpha else 'не значимо'}")
print("\nВывод: слабая отрицательная корреляция (по всему датасету)")
print("внутри каждого вида корреляция может быть положительной — парадокс Симпсона!")
```

</details>

---

## Бонусные задания

### Бонус 1 — Параметрические vs непараметрические: когда выбор имеет значение

Сгенерируйте две выборки с сильно скошенным распределением (например, из log-нормального):
```python
import numpy as np
rng = np.random.default_rng(42)
a = rng.lognormal(mean=0, sigma=1, size=30)
b = rng.lognormal(mean=0.5, sigma=1, size=30)
```
Примените t-тест и критерий Манна-Уитни. Сравните p-значения. В каком случае тест
«видит» разницу более уверенно? Почему?

<details>
<summary>Подсказка</summary>

При скошенных данных t-тест может быть менее мощным, чем критерий Манна-Уитни.
Сначала проверьте нормальность тестом Шапиро.

</details>

<details>
<summary>Решение</summary>

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)
a = rng.lognormal(mean=0, sigma=1, size=30)
b = rng.lognormal(mean=0.5, sigma=1, size=30)

# Нормальность
_, p_a = stats.shapiro(a)
_, p_b = stats.shapiro(b)
print(f"Шапиро a: p={p_a:.4f}  → {'нормальное' if p_a >= 0.05 else 'НЕ нормальное'}")
print(f"Шапиро b: p={p_b:.4f}  → {'нормальное' if p_b >= 0.05 else 'НЕ нормальное'}\n")

# t-тест
t_stat, t_p = stats.ttest_ind(a, b, equal_var=False)
print(f"t-тест:        p = {t_p:.4f}")

# Манна-Уитни
u_stat, mw_p = stats.mannwhitneyu(a, b, alternative="two-sided")
print(f"Манна-Уитни:   p = {mw_p:.4f}")

print("\nПри ненормальных данных Манна-Уитни часто имеет большую мощность.")
```

</details>

---

### Бонус 2 — Полный анализ: от описательной статистики до вывода

Проведите полный статистический анализ: сравните `sepal_length` у всех трёх видов.
1. Описательная статистика (mean, std, median) для каждого вида.
2. Проверьте нормальность каждой группы.
3. Проведите попарные сравнения подходящим тестом (t-тест или Манна-Уитни).
4. Скорректируйте уровень значимости с учётом множественных сравнений
   (поправка Бонферрони: α_corrected = α / количество тестов).

<details>
<summary>Подсказка</summary>

3 пары (setosa-versicolor, setosa-virginica, versicolor-virginica) → поправка Бонферрони: α = 0.05 / 3 ≈ 0.0167. Используйте `itertools.combinations` для перебора пар.

</details>

<details>
<summary>Решение</summary>

```python
from itertools import combinations

import pandas as pd
from scipy import stats

df = pd.read_csv("seminars/seminar_16_statistics/data/iris.csv")
col = "sepal_length"
alpha = 0.05

species_list = df["species"].unique()

# 1. Описательная статистика
print("=== Описательная статистика ===")
print(df.groupby("species")[col].agg(["mean", "std", "median"]).round(3))

# 2. Нормальность
print("\n=== Нормальность (Шапиро-Уилка) ===")
normal_groups = {}
for s in species_list:
    data = df[df["species"] == s][col]
    _, p = stats.shapiro(data)
    normal_groups[s] = p >= alpha
    print(f"  {s}: p={p:.4f}  → {'нормальное' if normal_groups[s] else 'НЕ нормальное'}")

# 3. Попарные сравнения с поправкой Бонферрони
pairs = list(combinations(species_list, 2))
alpha_corrected = alpha / len(pairs)
print(f"\n=== Попарные сравнения (α Бонферрони = {alpha_corrected:.4f}) ===")
for s1, s2 in pairs:
    g1 = df[df["species"] == s1][col]
    g2 = df[df["species"] == s2][col]
    if normal_groups[s1] and normal_groups[s2]:
        stat, p = stats.ttest_ind(g1, g2, equal_var=False)
        test_name = "t-тест"
    else:
        stat, p = stats.mannwhitneyu(g1, g2, alternative="two-sided")
        test_name = "Манна-Уитни"
    decision = "значимо" if p < alpha_corrected else "не значимо"
    print(f"  {s1} vs {s2}: {test_name}, p={p:.4e}  → {decision}")
```

</details>

---

## Полезные ресурсы

- [SciPy Stats — документация](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Statsmodels — документация](https://www.statsmodels.org/stable/index.html)
- [Pandas — описательная статистика](https://pandas.pydata.org/docs/user_guide/basics.html#descriptive-statistics)
- [StatQuest: Statistics Fundamentals (YouTube)](https://www.youtube.com/playlist?list=PLblh5JKOoLUK0FLuzwntyYI10UQFUhsY9)
- [Видео: Что такое p-value? (StatQuest)](https://www.youtube.com/watch?v=vemZtEM63GY)
