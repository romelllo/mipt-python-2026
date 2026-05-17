"""Блок 5: Корреляционный анализ.

Коэффициенты корреляции Пирсона и Спирмена,
визуализация корреляционной матрицы на примере датасета Iris.

Запуск:
    python seminars/seminar_16_statistics/examples/05_correlation.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

DATA_PATH = Path(__file__).parent.parent / "data" / "iris.csv"
OUTPUT_DIR = Path(__file__).parent.parent / "data"

ALPHA = 0.05


# ============================================================
# Раздел 1: Понятие корреляции
# ============================================================


def explain_correlation() -> None:
    """Объяснить понятие корреляции."""
    print("=" * 55)
    print("КОРРЕЛЯЦИЯ — ключевые понятия")
    print("=" * 55)
    print("""
Корреляция измеряет силу и направление линейной связи
между двумя переменными.

Диапазон: от -1 до +1
    +1  — идеальная положительная линейная связь
     0  — нет линейной связи
    -1  — идеальная отрицательная линейная связь

Интерпретация силы (по Коэну):
    |r| < 0.1   — незначимая
    |r| 0.1–0.3 — слабая
    |r| 0.3–0.5 — умеренная
    |r| > 0.5   — сильная

⚠️  Корреляция ≠ причинно-следственная связь!
⚠️  Пирсон чувствителен к выбросам и нелинейным связям.
""")


# ============================================================
# Раздел 2: Корреляция Пирсона
# ============================================================


def demo_pearson(df: pd.DataFrame) -> None:
    """Вычислить и интерпретировать корреляцию Пирсона."""
    print("\n" + "=" * 55)
    print("КОРРЕЛЯЦИЯ ПИРСОНА (линейная)")
    print("=" * 55)
    print("  Предположения: нормальное распределение, линейная связь\n")

    pairs = [
        ("petal_length", "petal_width"),
        ("sepal_length", "petal_length"),
        ("sepal_width", "petal_length"),
    ]

    for col1, col2 in pairs:
        r, p = stats.pearsonr(df[col1], df[col2])
        significance = "значимо" if p < ALPHA else "не значимо"
        print(f"  {col1} × {col2}")
        print(f"    r = {r:.4f},  p = {p:.4f}  ({significance})")

    print("\n  Корреляционная матрица (pandas):")
    numeric_df = df.select_dtypes(include="number")
    print(numeric_df.corr(method="pearson").round(3))


# ============================================================
# Раздел 3: Корреляция Спирмена
# ============================================================


def demo_spearman(df: pd.DataFrame) -> None:
    """Вычислить и сравнить корреляцию Спирмена с Пирсоном."""
    print("\n" + "=" * 55)
    print("КОРРЕЛЯЦИЯ СПИРМЕНА (ранговая)")
    print("=" * 55)
    print("  Предположения: монотонная связь (не обязательно линейная)")
    print("  Используется: данные порядковые, есть выбросы,")
    print("  распределение не нормальное.\n")

    col1, col2 = "petal_length", "petal_width"

    r_p, p_p = stats.pearsonr(df[col1], df[col2])
    r_s, p_s = stats.spearmanr(df[col1], df[col2])

    print(f"  {col1} × {col2}:")
    print(f"    Пирсон:  r = {r_p:.4f},  p = {p_p:.4e}")
    print(f"    Спирмен: r = {r_s:.4f},  p = {p_s:.4e}")
    print()

    print("  Когда результаты расходятся — вероятно, нелинейная связь.")
    print("  Корреляционная матрица (Спирмен):")
    numeric_df = df.select_dtypes(include="number")
    print(numeric_df.corr(method="spearman").round(3))


# ============================================================
# Раздел 4: Визуализация
# ============================================================


def demo_correlation_plot(df: pd.DataFrame) -> None:
    """Построить scatter plot и тепловую карту корреляций."""
    numeric_df = df.select_dtypes(include="number")
    corr_matrix = numeric_df.corr(method="pearson")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Корреляционный анализ Iris", fontsize=13)

    # Scatter plot: длина лепестка vs ширина лепестка
    colors = {"setosa": "blue", "versicolor": "orange", "virginica": "green"}
    for species, group in df.groupby("species"):
        axes[0].scatter(
            group["petal_length"],
            group["petal_width"],
            label=species,
            color=colors[species],
            alpha=0.7,
        )
    # Линия регрессии
    x = df["petal_length"].values
    y = df["petal_width"].values
    slope, intercept, *_ = stats.linregress(x, y)
    x_line = np.linspace(x.min(), x.max(), 100)
    axes[0].plot(x_line, slope * x_line + intercept, "r--", label=f"r={stats.pearsonr(x,y)[0]:.2f}")
    axes[0].set_xlabel("petal_length (см)")
    axes[0].set_ylabel("petal_width (см)")
    axes[0].set_title("Scatter plot: petal_length vs petal_width")
    axes[0].legend()

    # Тепловая карта корреляций
    im = axes[1].imshow(corr_matrix.values, vmin=-1, vmax=1, cmap="RdBu_r")
    axes[1].set_xticks(range(len(corr_matrix.columns)))
    axes[1].set_yticks(range(len(corr_matrix.columns)))
    axes[1].set_xticklabels(corr_matrix.columns, rotation=45, ha="right")
    axes[1].set_yticklabels(corr_matrix.columns)
    axes[1].set_title("Тепловая карта корреляций (Пирсон)")
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix.columns)):
            axes[1].text(j, i, f"{corr_matrix.values[i, j]:.2f}", ha="center", va="center", fontsize=9)
    plt.colorbar(im, ax=axes[1])

    plt.tight_layout()
    out_path = OUTPUT_DIR / "correlation.png"
    plt.savefig(out_path, dpi=100)
    print(f"\nГрафики корреляции сохранены: {out_path}")
    plt.show()


# ============================================================
# Точка входа
# ============================================================


def main() -> None:
    """Запустить все демонстрации блока 5."""
    df = pd.read_csv(DATA_PATH)
    explain_correlation()
    demo_pearson(df)
    demo_spearman(df)
    demo_correlation_plot(df)


if __name__ == "__main__":
    main()
