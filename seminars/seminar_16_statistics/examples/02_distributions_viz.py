"""Блок 2: Распределения и визуализация.

Гистограммы, box plot, асимметрия и эксцесс на примере датасета Iris.

Запуск:
    python seminars/seminar_16_statistics/examples/02_distributions_viz.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

DATA_PATH = Path(__file__).parent.parent / "data" / "iris.csv"
OUTPUT_DIR = Path(__file__).parent.parent / "data"


# ============================================================
# Раздел 1: Гистограмма и форма распределения
# ============================================================


def demo_histogram(df: pd.DataFrame) -> None:
    """Построить гистограммы для числовых признаков."""
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle("Гистограммы признаков Iris", fontsize=14)

    numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    for ax, col in zip(axes.flat, numeric_cols, strict=True):
        ax.hist(df[col], bins=20, edgecolor="black", color="steelblue", alpha=0.7)
        ax.axvline(df[col].mean(), color="red", linestyle="--", label="среднее")
        ax.axvline(df[col].median(), color="orange", linestyle="-.", label="медиана")
        ax.set_title(col)
        ax.set_xlabel("Значение (см)")
        ax.set_ylabel("Частота")
        ax.legend(fontsize=8)

    plt.tight_layout()
    out_path = OUTPUT_DIR / "histograms.png"
    plt.savefig(out_path, dpi=100)
    print(f"Гистограммы сохранены: {out_path}")
    plt.show()


# ============================================================
# Раздел 2: Box plot
# ============================================================


def demo_boxplot(df: pd.DataFrame) -> None:
    """Построить box plot — «ящик с усами»."""
    print("\n" + "=" * 50)
    print("BOX PLOT — интерпретация элементов")
    print("=" * 50)
    print("  Нижний ус  : Q1 - 1.5 * IQR  (минимум без выбросов)")
    print("  Нижняя грань: Q1 (25-й перцентиль)")
    print("  Линия внутри: медиана (50-й перцентиль)")
    print("  Верхняя грань: Q3 (75-й перцентиль)")
    print("  Верхний ус : Q3 + 1.5 * IQR  (максимум без выбросов)")
    print("  Точки       : выбросы")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Box Plot: сравнение признаков по видам Iris", fontsize=13)

    # Box plot длины лепестка по видам
    species_list = df["species"].unique()
    data_petal = [df[df["species"] == s]["petal_length"].values for s in species_list]
    axes[0].boxplot(data_petal, labels=species_list, patch_artist=True)
    axes[0].set_title("Длина лепестка (petal_length)")
    axes[0].set_ylabel("Длина (см)")

    # Box plot ширины чашелистика по видам
    data_sepal = [df[df["species"] == s]["sepal_width"].values for s in species_list]
    axes[1].boxplot(data_sepal, labels=species_list, patch_artist=True)
    axes[1].set_title("Ширина чашелистика (sepal_width)")
    axes[1].set_ylabel("Ширина (см)")

    plt.tight_layout()
    out_path = OUTPUT_DIR / "boxplot.png"
    plt.savefig(out_path, dpi=100)
    print(f"\nBox plot сохранён: {out_path}")
    plt.show()


# ============================================================
# Раздел 3: Асимметрия и эксцесс
# ============================================================


def demo_skewness_kurtosis(df: pd.DataFrame) -> None:
    """Вычислить и интерпретировать асимметрию и эксцесс."""
    print("\n" + "=" * 50)
    print("АСИММЕТРИЯ (skewness) и ЭКСЦЕСС (kurtosis)")
    print("=" * 50)

    print("\nОпределения:")
    print("  Асимметрия (skewness):")
    print("    > 0  — правый хвост длиннее (правосторонняя)")
    print("    < 0  — левый хвост длиннее (левосторонняя)")
    print("    ≈ 0  — симметричное распределение")
    print("  Эксцесс (kurtosis, excess kurtosis):")
    print("    > 0  — остроконечное (лептокуртическое), тяжёлые хвосты")
    print("    < 0  — плосковершинное (платикуртическое)")
    print("    ≈ 0  — нормальное (мезокуртическое)")

    numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    print(f"\n{'Признак':<20} {'Асимметрия':>12} {'Эксцесс':>10}")
    print("-" * 44)
    for col in numeric_cols:
        skew = stats.skew(df[col])
        kurt = stats.kurtosis(df[col])  # excess kurtosis (нормальное = 0)
        print(f"{col:<20} {skew:>12.3f} {kurt:>10.3f}")

    # Сравнение: pandas vs scipy
    print("\nПроверка: pandas .skew() и .kurt() дают те же значения:")
    col = "petal_length"
    print(f"  scipy skew:    {stats.skew(df[col]):.4f}")
    print(f"  pandas skew(): {df[col].skew():.4f}")
    print(f"  scipy kurt:    {stats.kurtosis(df[col]):.4f}")
    print(f"  pandas kurt(): {df[col].kurt():.4f}")


# ============================================================
# Точка входа
# ============================================================


def main() -> None:
    """Запустить все демонстрации блока 2."""
    df = pd.read_csv(DATA_PATH)
    print(f"Загружен датасет: {df.shape[0]} строк")

    demo_histogram(df)
    demo_boxplot(df)
    demo_skewness_kurtosis(df)


if __name__ == "__main__":
    main()
