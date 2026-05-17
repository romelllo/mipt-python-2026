"""Блок 4: Проверка гипотез.

Тест Шапиро-Уилка, t-тест Стьюдента (независимые и парные выборки),
критерий Манна-Уитни на примере датасета Iris.

Запуск:
    python seminars/seminar_16_statistics/examples/04_hypothesis_testing.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

DATA_PATH = Path(__file__).parent.parent / "data" / "iris.csv"

# Уровень значимости — стандартное значение в науке
ALPHA = 0.05


# ============================================================
# Вспомогательная функция
# ============================================================


def print_result(test_name: str, statistic: float, p_value: float, alpha: float = ALPHA) -> None:
    """Вывести результат статистического теста."""
    decision = "H₀ ОТВЕРГАЕТСЯ" if p_value < alpha else "H₀ НЕ ОТВЕРГАЕТСЯ"
    print(f"  {test_name}")
    print(f"    Статистика: {statistic:.4f}")
    print(f"    p-значение: {p_value:.4f}")
    print(f"    α = {alpha}  →  {decision}")


# ============================================================
# Раздел 1: Логика проверки гипотез
# ============================================================


def explain_hypothesis_testing() -> None:
    """Объяснить логику проверки гипотез."""
    print("=" * 55)
    print("ЛОГИКА ПРОВЕРКИ ГИПОТЕЗ")
    print("=" * 55)
    print("""
H₀ (нулевая гипотеза)  : «эффекта нет», «разницы нет»
H₁ (альтернативная)    : «эффект есть», «разница есть»

p-значение: вероятность получить наблюдаемый результат
            (или более экстремальный), если H₀ верна.

Правило принятия решения:
    p < α  →  отвергаем H₀ (результат статистически значим)
    p ≥ α  →  нет оснований отвергнуть H₀

Типичные значения α: 0.05, 0.01, 0.001

⚠️  p-значение НЕ равно вероятности того, что H₀ верна!
""")


# ============================================================
# Раздел 2: Тест нормальности Шапиро-Уилка
# ============================================================


def demo_shapiro(df: pd.DataFrame) -> None:
    """Проверить нормальность распределений тестом Шапиро-Уилка."""
    print("\n" + "=" * 55)
    print("ТЕСТ НОРМАЛЬНОСТИ ШАПИРО-УИЛКА")
    print("=" * 55)
    print("  H₀: данные распределены нормально")
    print("  H₁: данные не распределены нормально\n")

    numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    for col in numeric_cols:
        stat, p = stats.shapiro(df[col])
        decision = "нормальное" if p >= ALPHA else "НЕ нормальное"
        print(f"  {col:<20}  stat={stat:.4f}  p={p:.4f}  → {decision}")

    print("\n  Вывод: petal_length и petal_width — не нормальные")
    print("  (биквмодальное распределение из-за 3 видов).")
    print("  Для них лучше использовать непараметрические тесты.")

    # Для одного вида нормальность лучше
    print("\n  Тест Шапиро для setosa (petal_length):")
    setosa = df[df["species"] == "setosa"]["petal_length"]
    stat, p = stats.shapiro(setosa)
    decision = "нормальное" if p >= ALPHA else "НЕ нормальное"
    print(f"  stat={stat:.4f}  p={p:.4f}  → {decision}")


# ============================================================
# Раздел 3: t-тест для независимых выборок
# ============================================================


def demo_ttest_independent(df: pd.DataFrame) -> None:
    """Сравнить длину лепестка у двух видов с помощью t-теста."""
    print("\n" + "=" * 55)
    print("T-ТЕСТ ДЛЯ НЕЗАВИСИМЫХ ВЫБОРОК")
    print("=" * 55)
    print("  Вопрос: Отличается ли средняя длина лепестка")
    print("  у versicolor и virginica?\n")

    group1 = df[df["species"] == "versicolor"]["petal_length"]
    group2 = df[df["species"] == "virginica"]["petal_length"]

    print(f"  versicolor: n={len(group1)}, среднее={group1.mean():.3f}, std={group1.std():.3f}")
    print(f"  virginica:  n={len(group2)}, среднее={group2.mean():.3f}, std={group2.std():.3f}")
    print()

    print("  H₀: μ_versicolor = μ_virginica")
    print("  H₁: μ_versicolor ≠ μ_virginica\n")

    # equal_var=False — тест Уэлча (не требует равенства дисперсий)
    stat, p = stats.ttest_ind(group1, group2, equal_var=False)
    print_result("t-тест Уэлча (двусторонний)", stat, p)

    print("\n  Практическая значимость (effect size — Cohen's d):")
    pooled_std = np.sqrt((group1.std() ** 2 + group2.std() ** 2) / 2)
    d = (group1.mean() - group2.mean()) / pooled_std
    print(f"  Cohen's d = {d:.3f}  (|d|>0.8 — большой эффект)")


# ============================================================
# Раздел 4: t-тест для парных выборок
# ============================================================


def demo_ttest_paired(df: pd.DataFrame) -> None:
    """Сравнить два парных измерения t-тестом для зависимых выборок."""
    print("\n" + "=" * 55)
    print("T-ТЕСТ ДЛЯ ПАРНЫХ ВЫБОРОК")
    print("=" * 55)
    print("  Вопрос: Отличается ли длина лепестка от его ширины")
    print("  (для тех же цветков, вид setosa)?\n")

    setosa = df[df["species"] == "setosa"]
    petal_len = setosa["petal_length"]
    petal_wid = setosa["petal_width"]

    print(f"  petal_length: среднее={petal_len.mean():.3f}")
    print(f"  petal_width:  среднее={petal_wid.mean():.3f}")
    print()

    print("  H₀: среднее различие = 0")
    print("  H₁: среднее различие ≠ 0\n")

    stat, p = stats.ttest_rel(petal_len, petal_wid)
    print_result("Парный t-тест", stat, p)


# ============================================================
# Раздел 5: Критерий Манна-Уитни (непараметрический)
# ============================================================


def demo_mann_whitney(df: pd.DataFrame) -> None:
    """Сравнить группы непараметрическим критерием Манна-Уитни."""
    print("\n" + "=" * 55)
    print("КРИТЕРИЙ МАННА-УИТНИ (непараметрический)")
    print("=" * 55)
    print("  Когда использовать: данные не нормальные, порядковые")
    print("  или есть выбросы. Сравнивает медианы (ранги).\n")

    group1 = df[df["species"] == "setosa"]["petal_length"]
    group2 = df[df["species"] == "versicolor"]["petal_length"]

    print(f"  setosa:     n={len(group1)}, медиана={group1.median():.3f}")
    print(f"  versicolor: n={len(group2)}, медиана={group2.median():.3f}")
    print()

    print("  H₀: распределения в двух группах одинаковы")
    print("  H₁: одно распределение сдвинуто относительно другого\n")

    stat, p = stats.mannwhitneyu(group1, group2, alternative="two-sided")
    print_result("Критерий Манна-Уитни", stat, p)

    print("\n  Сравнение подходов:")
    print("  Параметрический (t-тест):    требует нормальности")
    print("  Непараметрический (MW-тест): более устойчив, но менее мощный")


# ============================================================
# Точка входа
# ============================================================


def main() -> None:
    """Запустить все демонстрации блока 4."""
    df = pd.read_csv(DATA_PATH)
    explain_hypothesis_testing()
    demo_shapiro(df)
    demo_ttest_independent(df)
    demo_ttest_paired(df)
    demo_mann_whitney(df)


if __name__ == "__main__":
    main()
