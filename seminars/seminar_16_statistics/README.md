# Семинар 16: Описательная статистика и статистика вывода

**Модуль:** 4 — Анализ данных в Python  
**Дата:** 18.05.2026  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1D2YrYmXxFy8rbO0lOw--DRKXZ0cJ_60rh9TVQyRsq4Q/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:

- Вычислять меры центральной тенденции (среднее, медиана, мода, усечённое среднее) и разброса (std, IQR, MAD) с помощью pandas и scipy
- Визуализировать распределения через гистограммы и box plot, интерпретировать асимметрию и эксцесс
- Строить доверительные интервалы для среднего и доли с заданным уровнем доверия
- Корректно формулировать статистические гипотезы и выбирать подходящий тест
- Применять тест Шапиро-Уилка, t-тест (независимый и парный), критерий Манна-Уитни
- Вычислять и интерпретировать корреляцию Пирсона и Спирмена

---

## Подготовка

```bash
# Установить зависимости (scipy, statsmodels, matplotlib, seaborn)
uv sync

# Активировать окружение
source .venv/bin/activate

# Проверить датасет
python -c "
import pandas as pd
df = pd.read_csv('seminars/seminar_16_statistics/data/iris.csv')
print(df.shape, df['species'].value_counts().to_dict())
"
```

**Датасет:** [Iris](https://en.wikipedia.org/wiki/Iris_flower_data_set) — классический датасет из 150 наблюдений трёх видов ириса (setosa, versicolor, virginica), 4 числовых признака в сантиметрах.

---

## План семинара

| Время   | Тема                                   | Практика                        |
|---------|----------------------------------------|---------------------------------|
| 20 мин  | Блок 1: Описательные статистики        | → Упражнения: Часть 1           |
| 15 мин  | Блок 2: Распределения и визуализация   | → Упражнения: Часть 2           |
| 20 мин  | Блок 3: Доверительные интервалы        | → Упражнения: Часть 3           |
| 25 мин  | Блок 4: Проверка гипотез               | → Упражнения: Часть 4           |
| 10 мин  | Блок 5: Корреляция                     | → Упражнения: Часть 5           |
| 5 мин   | Подведение итогов                      | —                               |

---

## Блок 1: Описательные статистики (20 мин)

### Меры центральной тенденции

| Мера | Формула / метод | Когда использовать |
|------|----------------|--------------------|
| Среднее (mean) | `col.mean()` | Симметричное распределение, нет выбросов |
| Медиана (median) | `col.median()` | Есть выбросы или скошенное распределение |
| Мода (mode) | `col.mode()[0]` | Категориальные / дискретные данные |
| Усечённое среднее | `scipy.stats.trim_mean(col, 0.1)` | Компромисс: убираем 10% крайних значений |

### Меры разброса

| Мера | Формула / метод | Особенности |
|------|----------------|-------------|
| Стандартное отклонение | `col.std()` | Те же единицы, что и данные; чувствительно к выбросам |
| Дисперсия | `col.var()` | Квадрат std; используется в формулах |
| Размах (range) | `col.max() - col.min()` | Максимально чувствителен к выбросам |
| IQR | `Q3 - Q1` | Устойчив к выбросам; основа box plot |
| MAD | `scipy.stats.median_abs_deviation(col)` | Самая устойчивая мера разброса |

### Перцентили и квартили

```python
col.quantile(0.25)   # Q1 — нижний квартиль (25-й перцентиль)
col.quantile(0.50)   # медиана (50-й перцентиль)
col.quantile(0.75)   # Q3 — верхний квартиль (75-й перцентиль)
```

### Сводная статистика в pandas

```python
df.describe()                              # count, mean, std, min, Q1, median, Q3, max

df.groupby("species")["petal_length"].agg(
    среднее="mean",
    медиана="median",
    стд="std",
)
```

> **Подробнее:** см. файл [`examples/01_descriptive_stats.py`](examples/01_descriptive_stats.py) — меры центральной тенденции, разброса, квантили и `.agg()` по группам

### Практика
Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 1** (задания 1.1–1.3).

---

## Блок 2: Распределения и визуализация (15 мин)

### Гистограмма

```python
import matplotlib.pyplot as plt

plt.hist(df["petal_length"], bins=20, edgecolor="black")
plt.axvline(df["petal_length"].mean(),   color="red",    linestyle="--", label="среднее")
plt.axvline(df["petal_length"].median(), color="orange", linestyle="-.", label="медиана")
plt.legend()
plt.show()
```

### Box plot («ящик с усами»)

```
  ─── верхний ус: Q3 + 1.5·IQR  (или максимум, если нет выбросов)
  ┌─────────────┐  ← Q3 (75-й перцентиль)
  │             │
  ├─────────────┤  ← медиана
  │             │
  └─────────────┘  ← Q1 (25-й перцентиль)
  ─── нижний ус: Q1 - 1.5·IQR
  ●  — выбросы (точки за пределами усов)
```

```python
data_by_species = [df[df["species"] == s]["petal_length"].values for s in df["species"].unique()]
plt.boxplot(data_by_species, labels=df["species"].unique())
plt.show()
```

### Асимметрия (skewness) и эксцесс (kurtosis)

| Показатель | Значение | Интерпретация |
|------------|----------|---------------|
| Асимметрия | > 0 | Правый хвост длиннее (правосторонняя) |
| Асимметрия | < 0 | Левый хвост длиннее (левосторонняя) |
| Эксцесс    | > 0 | Остроконечное, тяжёлые хвосты |
| Эксцесс    | < 0 | Плосковершинное |

```python
df["petal_length"].skew()   # асимметрия
df["petal_length"].kurt()   # избыточный эксцесс (нормальное распределение = 0)
```

> **Подробнее:** см. файл [`examples/02_distributions_viz.py`](examples/02_distributions_viz.py) — гистограммы, box plot по группам, таблица асимметрии/эксцесса

### Практика
Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 2** (задания 2.1–2.2).

---

## Блок 3: Доверительные интервалы (20 мин)

### Ключевые понятия

- **Генеральная совокупность** — все возможные наблюдения
- **Выборка** — подмножество, которое мы наблюдаем
- **Точечная оценка** — одно число, например, выборочное среднее x̄
- **Доверительный интервал (ДИ)** — диапазон, который с вероятностью (1-α) накрывает истинный параметр

> ⚠️ 95% ДИ — не «истинное значение с 95% вероятностью находится в интервале», а «если повторить эксперимент 100 раз, 95 из построенных интервалов накроют истинное значение».

### ДИ для среднего — scipy

```python
from scipy import stats

col = df["sepal_length"]
n = len(col)
mean = col.mean()
se = stats.sem(col)   # стандартная ошибка = std / sqrt(n)

# t-распределение (для малых выборок или неизвестной σ)
ci = stats.t.interval(0.95, df=n - 1, loc=mean, scale=se)
print(f"95% ДИ: [{ci[0]:.4f}, {ci[1]:.4f}]")
```

### ДИ для среднего — statsmodels

```python
import statsmodels.stats.api as sms

ci = sms.DescrStatsW(col).tconfint_mean(alpha=0.05)
print(f"95% ДИ: [{ci[0]:.4f}, {ci[1]:.4f}]")
```

### ДИ для доли — statsmodels

```python
from statsmodels.stats.proportion import proportion_confint

successes = (df["petal_length"] > 4).sum()
n = len(df)

ci = proportion_confint(successes, n, alpha=0.05, method="wilson")
print(f"95% ДИ для доли: [{ci[0]:.4f}, {ci[1]:.4f}]")
```

**Методы:** `normal` (нормальное приближение), `wilson` (рекомендуется), `agresti_coull`.

> **Подробнее:** см. файл [`examples/03_confidence_intervals.py`](examples/03_confidence_intervals.py) — ДИ для среднего и доли, влияние размера выборки на ширину ДИ

### Практика
Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 3** (задания 3.1–3.2).

---

## Блок 4: Проверка гипотез (25 мин)

### Логика проверки гипотез

```
H₀ (нулевая)     : «разницы нет», «эффекта нет»
H₁ (альтернативная): «разница есть», «эффект есть»

p-значение < α  →  отвергаем H₀  (результат статистически значим)
p-значение ≥ α  →  нет оснований отвергнуть H₀

Типичные α: 0.05, 0.01, 0.001
```

> ⚠️ p-значение — **не** вероятность того, что H₀ верна. Это вероятность получить наблюдаемый результат (или более экстремальный), если H₀ верна.

### Тест нормальности Шапиро-Уилка

```python
from scipy import stats

stat, p = stats.shapiro(df["petal_length"])
# H₀: данные нормальные
# p < 0.05 → отвергаем нормальность
print(f"p = {p:.4f}  → {'нормальное' if p >= 0.05 else 'не нормальное'}")
```

**Рекомендация:** при n > 50 используйте совместно с визуальной проверкой (Q-Q plot или гистограмма).

### Выбор теста

```
Нормальность? ──── ДА ──── Независимые группы? ── ДА → t-тест независимый
                  │                              └── НЕТ → t-тест парный
                  └── НЕТ ─ Независимые группы? ── ДА → Манна-Уитни
                                                  └── НЕТ → Уилкоксон
```

### t-тест для независимых выборок

```python
from scipy import stats

group1 = df[df["species"] == "versicolor"]["petal_length"]
group2 = df[df["species"] == "virginica"]["petal_length"]

# equal_var=False — тест Уэлча (не требует равенства дисперсий, предпочтителен)
stat, p = stats.ttest_ind(group1, group2, equal_var=False)
print(f"t = {stat:.4f},  p = {p:.4f}")
```

### t-тест для парных выборок

```python
stat, p = stats.ttest_rel(before, after)
```

### Критерий Манна-Уитни (непараметрический)

```python
stat, p = stats.mannwhitneyu(group1, group2, alternative="two-sided")
# alternative: "two-sided", "less", "greater"
```

### Практическая значимость: Cohen's d

```python
import numpy as np

d = (group1.mean() - group2.mean()) / np.sqrt((group1.std()**2 + group2.std()**2) / 2)
# |d| < 0.2 — маленький, 0.2–0.5 — средний, > 0.8 — большой эффект
```

> **Подробнее:** см. файл [`examples/04_hypothesis_testing.py`](examples/04_hypothesis_testing.py) — логика гипотез, Шапиро-Уилк, t-тесты, Манна-Уитни, Cohen's d

### Практика
Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 4** (задания 4.1–4.3).

---

## Блок 5: Корреляция (10 мин)

### Ключевые понятия

- **Корреляция** — мера линейной (Пирсон) или монотонной (Спирмен) связи между двумя переменными
- Диапазон: от -1 до +1
- Интерпретация: |r| < 0.1 — незначимая, 0.1–0.3 — слабая, 0.3–0.5 — умеренная, > 0.5 — сильная

> ⚠️ **Корреляция ≠ причинно-следственная связь!**

### Пирсон vs Спирмен

| | Пирсон | Спирмен |
|---|---|---|
| Тип связи | Линейная | Монотонная |
| Предположения | Нормальность, нет выбросов | Отсутствуют |
| Данные | Числовые (интервальные) | Числовые или порядковые |

```python
from scipy import stats

# Пирсон
r, p = stats.pearsonr(df["petal_length"], df["petal_width"])

# Спирмен
r, p = stats.spearmanr(df["petal_length"], df["petal_width"])

# Корреляционная матрица (pandas)
df.corr(method="pearson")
df.corr(method="spearman")
```

> **Подробнее:** см. файл [`examples/05_correlation.py`](examples/05_correlation.py) — Пирсон, Спирмен, тепловая карта корреляций, scatter plot с линией регрессии

### Практика
Перейдите к файлу [`exercises/exercises.md`](exercises/exercises.md) и выполните **Часть 5** (задания 5.1–5.2).

---

## Подведение итогов

### Шпаргалка

| Задача | Инструмент | Пример |
|--------|-----------|--------|
| Меры центральной тенденции | `pandas` | `col.mean()`, `col.median()` |
| Меры разброса | `pandas`, `scipy` | `col.std()`, `stats.median_abs_deviation(col)` |
| Сводная статистика | `pandas` | `df.describe()`, `.groupby().agg()` |
| Гистограмма / Box plot | `matplotlib` | `plt.hist()`, `plt.boxplot()` |
| Асимметрия, эксцесс | `pandas` | `col.skew()`, `col.kurt()` |
| ДИ для среднего | `scipy`, `statsmodels` | `stats.t.interval(...)` |
| ДИ для доли | `statsmodels` | `proportion_confint(...)` |
| Нормальность | `scipy` | `stats.shapiro(col)` |
| t-тест независимый | `scipy` | `stats.ttest_ind(g1, g2)` |
| t-тест парный | `scipy` | `stats.ttest_rel(before, after)` |
| Манна-Уитни | `scipy` | `stats.mannwhitneyu(g1, g2)` |
| Корреляция Пирсона | `scipy` | `stats.pearsonr(x, y)` |
| Корреляция Спирмена | `scipy` | `stats.spearmanr(x, y)` |

### Ключевые выводы

1. Выбирайте меры статистики с учётом формы распределения: среднее и std — для нормальных данных, медиана и IQR — для данных с выбросами.
2. Перед t-тестом всегда проверяйте нормальность; при нарушении — переходите к критерию Манна-Уитни.
3. Статистическая значимость (p < 0.05) не равна практической значимости — всегда вычисляйте размер эффекта (Cohen's d).

---

## Файлы семинара

```
seminar_16_statistics/
├── README.md                        # этот файл
├── data/
│   └── iris.csv                     # датасет Iris (150 строк, 5 столбцов)
├── examples/
│   ├── 01_descriptive_stats.py      # меры центральной тенденции и разброса
│   ├── 02_distributions_viz.py      # гистограммы, box plot, асимметрия
│   ├── 03_confidence_intervals.py   # ДИ для среднего и доли
│   ├── 04_hypothesis_testing.py     # Шапиро-Уилк, t-тесты, Манна-Уитни
│   └── 05_correlation.py            # корреляция Пирсона и Спирмена
└── exercises/
    └── exercises.md                 # практические задания (Части 1–5 + бонус)
```

**Запуск примеров:**

```bash
python seminars/seminar_16_statistics/examples/01_descriptive_stats.py
python seminars/seminar_16_statistics/examples/02_distributions_viz.py
python seminars/seminar_16_statistics/examples/03_confidence_intervals.py
python seminars/seminar_16_statistics/examples/04_hypothesis_testing.py
python seminars/seminar_16_statistics/examples/05_correlation.py
```

---

## Дополнительные материалы

- [SciPy Stats — документация](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Statsmodels — документация](https://www.statsmodels.org/stable/index.html)
- [Pandas — описательная статистика](https://pandas.pydata.org/docs/user_guide/basics.html#descriptive-statistics)
- [StatQuest: Statistics Fundamentals (YouTube)](https://www.youtube.com/playlist?list=PLblh5JKOoLUK0FLuzwntyYI10UQFUhsY9)
- [Seeing Theory — визуальное введение в вероятность и статистику](https://seeing-theory.brown.edu/)
- [Think Stats (Allen Downey) — бесплатная книга](https://greenteapress.com/wp/think-stats-2e/)
