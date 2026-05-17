"""Блок 3: Доверительные интервалы.

Доверительные интервалы для среднего и доли с использованием
scipy и statsmodels на примере датасета Iris.

Запуск:
    python seminars/seminar_16_statistics/examples/03_confidence_intervals.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.stats.api as sms
from scipy import stats

DATA_PATH = Path(__file__).parent.parent / "data" / "iris.csv"


# ============================================================
# Раздел 1: Ключевые понятия
# ============================================================


def explain_concepts() -> None:
    """Объяснить ключевые понятия."""
    print("=" * 55)
    print("КЛЮЧЕВЫЕ ПОНЯТИЯ")
    print("=" * 55)
    print("""
Генеральная совокупность (population):
    все возможные наблюдения (все цветки ириса в мире).

Выборка (sample):
    подмножество, которое мы наблюдаем (наши 150 цветков).

Точечная оценка (point estimate):
    одно число, оценивающее параметр — например, среднее x̄.

Доверительный интервал (confidence interval, CI):
    диапазон значений, в котором с заданной вероятностью
    находится истинный параметр генеральной совокупности.

95% ДИ:  «Если повторить эксперимент 100 раз, примерно 95 из
          построенных интервалов накроют истинное значение».

Формула ДИ для среднего (при неизвестной σ, t-распределение):
    x̄ ± t(α/2, n-1) * s / √n
""")


# ============================================================
# Раздел 2: ДИ для среднего — scipy
# ============================================================


def demo_ci_mean_scipy(df: pd.DataFrame) -> None:
    """Вычислить ДИ для среднего через scipy.stats.t.interval."""
    col = df["sepal_length"]
    n = len(col)
    mean = col.mean()
    se = stats.sem(col)  # стандартная ошибка = std / sqrt(n)

    print("\n" + "=" * 55)
    print("ДИ ДЛЯ СРЕДНЕГО — scipy (sepal_length)")
    print("=" * 55)

    for confidence in [0.90, 0.95, 0.99]:
        ci = stats.t.interval(confidence, df=n - 1, loc=mean, scale=se)
        print(
            f"  {int(confidence*100)}% ДИ: [{ci[0]:.4f}, {ci[1]:.4f}]"
            f"  (ширина: {ci[1]-ci[0]:.4f})"
        )

    print(f"\n  Точечная оценка (среднее): {mean:.4f}")
    print(f"  Стандартная ошибка (SE):   {se:.4f}")
    print(f"  Размер выборки:            {n}")
    print("\n  Вывод: чем уже ДИ — тем точнее оценка.")
    print("  С ростом уверенности (90→99%) интервал расширяется.")


# ============================================================
# Раздел 3: ДИ для среднего — statsmodels
# ============================================================


def demo_ci_mean_statsmodels(df: pd.DataFrame) -> None:
    """Вычислить ДИ для среднего через statsmodels."""
    col = df["sepal_length"]

    print("\n" + "=" * 55)
    print("ДИ ДЛЯ СРЕДНЕГО — statsmodels (sepal_length)")
    print("=" * 55)

    ci = sms.DescrStatsW(col).tconfint_mean(alpha=0.05)
    print(f"  95% ДИ: [{ci[0]:.4f}, {ci[1]:.4f}]")
    print("  (результат совпадает с scipy)")


# ============================================================
# Раздел 4: ДИ для доли — statsmodels
# ============================================================


def demo_ci_proportion(df: pd.DataFrame) -> None:
    """Вычислить ДИ для доли класса через statsmodels."""
    print("\n" + "=" * 55)
    print("ДИ ДЛЯ ДОЛИ — statsmodels")
    print("=" * 55)

    # Вопрос: какова доля цветков с длиной лепестка > 4 см?
    threshold = 4.0
    successes = (df["petal_length"] > threshold).sum()
    n = len(df)
    proportion = successes / n

    print(f"  Порог: petal_length > {threshold} см")
    print(f"  Количество: {successes} из {n}")
    print(f"  Доля (точечная оценка): {proportion:.4f} ({proportion*100:.1f}%)")

    from statsmodels.stats.proportion import proportion_confint

    for method in ["normal", "wilson", "agresti_coull"]:
        ci = proportion_confint(successes, n, alpha=0.05, method=method)
        print(f"  95% ДИ ({method:15s}): [{ci[0]:.4f}, {ci[1]:.4f}]")

    print("\n  Рекомендация: метод Wilson предпочтителен при малых выборках")
    print("  или крайних значениях доли (близких к 0 или 1).")


# ============================================================
# Раздел 5: Влияние размера выборки на ДИ
# ============================================================


def demo_sample_size_effect(df: pd.DataFrame) -> None:
    """Показать, как размер выборки влияет на ширину ДИ."""
    print("\n" + "=" * 55)
    print("ВЛИЯНИЕ РАЗМЕРА ВЫБОРКИ НА ШИРИНУ ДИ")
    print("=" * 55)

    col = df["sepal_length"]
    rng = np.random.default_rng(42)

    print(f"  {'n':>5}  {'Среднее':>9}  {'ДИ нижний':>10}  {'ДИ верхний':>10}  {'Ширина':>8}")
    print("  " + "-" * 50)
    for n in [10, 30, 50, 100, 150]:
        sample = rng.choice(col.values, size=n, replace=False)
        mean = sample.mean()
        se = stats.sem(sample)
        ci = stats.t.interval(0.95, df=n - 1, loc=mean, scale=se)
        width = ci[1] - ci[0]
        print(f"  {n:>5}  {mean:>9.4f}  {ci[0]:>10.4f}  {ci[1]:>10.4f}  {width:>8.4f}")

    print("\n  Вывод: при увеличении n в 4 раза ширина ДИ уменьшается вдвое.")
    print("  Ширина ∝ 1/√n")


# ============================================================
# Точка входа
# ============================================================


def main() -> None:
    """Запустить все демонстрации блока 3."""
    df = pd.read_csv(DATA_PATH)
    explain_concepts()
    demo_ci_mean_scipy(df)
    demo_ci_mean_statsmodels(df)
    demo_ci_proportion(df)
    demo_sample_size_effect(df)


if __name__ == "__main__":
    main()
