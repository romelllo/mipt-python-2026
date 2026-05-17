"""Блок 1: Описательные статистики.

Меры центральной тенденции, меры разброса, квантили и сводная статистика
на примере датасета Iris.

Запуск:
    python seminars/seminar_16_statistics/examples/01_descriptive_stats.py
"""

from pathlib import Path

import pandas as pd
from scipy import stats

DATA_PATH = Path(__file__).parent.parent / "data" / "iris.csv"


# ============================================================
# Раздел 1: Загрузка данных
# ============================================================


def load_data() -> pd.DataFrame:
    """Загрузить датасет Iris."""
    df = pd.read_csv(DATA_PATH)
    print("=== Датасет Iris ===")
    print(df.head())
    print(f"\nРазмер: {df.shape[0]} строк, {df.shape[1]} столбцов")
    print(f"Виды: {df['species'].unique()}")
    return df


# ============================================================
# Раздел 2: Меры центральной тенденции
# ============================================================


def demo_centrality(df: pd.DataFrame) -> None:
    """Показать меры центральной тенденции для длины лепестка."""
    col = df["petal_length"]

    print("\n" + "=" * 50)
    print("МЕРЫ ЦЕНТРАЛЬНОЙ ТЕНДЕНЦИИ (petal_length)")
    print("=" * 50)

    mean = col.mean()
    median = col.median()
    mode = col.mode()[0]
    # Усечённое среднее — среднее без 10% крайних значений
    trimmed_mean = stats.trim_mean(col, proportiontocut=0.1)

    print(f"Среднее (mean):              {mean:.3f}")
    print(f"Медиана (median):            {median:.3f}")
    print(f"Мода (mode):                 {mode:.3f}")
    print(f"Усечённое среднее (10%):     {trimmed_mean:.3f}")

    print("\nКогда использовать:")
    print("  среднее   — симметричное распределение без выбросов")
    print("  медиана   — есть выбросы или скошенное распределение")
    print("  мода      — категориальные данные или дискретные значения")


# ============================================================
# Раздел 3: Меры разброса
# ============================================================


def demo_variation(df: pd.DataFrame) -> None:
    """Показать меры разброса для длины лепестка."""
    col = df["petal_length"]

    print("\n" + "=" * 50)
    print("МЕРЫ РАЗБРОСА (petal_length)")
    print("=" * 50)

    data_range = col.max() - col.min()
    q1 = col.quantile(0.25)
    q3 = col.quantile(0.75)
    iqr = q3 - q1
    variance = col.var()          # выборочная дисперсия (ddof=1)
    std = col.std()               # стандартное отклонение
    mad = stats.median_abs_deviation(col)  # медианное абсолютное отклонение

    print(f"Размах (range):              {data_range:.3f}")
    print(f"Q1 (25-й перцентиль):        {q1:.3f}")
    print(f"Q3 (75-й перцентиль):        {q3:.3f}")
    print(f"IQR (межквартильный размах): {iqr:.3f}")
    print(f"Дисперсия (variance):        {variance:.3f}")
    print(f"Стд. отклонение (std):       {std:.3f}")
    print(f"MAD:                         {mad:.3f}")

    print("\nКогда использовать:")
    print("  std  — стандартная мера при нормальном распределении")
    print("  IQR  — устойчива к выбросам, используется в box plot")
    print("  MAD  — самая устойчивая к выбросам мера разброса")


# ============================================================
# Раздел 4: Перцентили и квартили
# ============================================================


def demo_percentiles(df: pd.DataFrame) -> None:
    """Показать перцентили и квантили."""
    col = df["petal_length"]

    print("\n" + "=" * 50)
    print("ПЕРЦЕНТИЛИ И КВАНТИЛИ (petal_length)")
    print("=" * 50)

    percentiles = [0, 10, 25, 50, 75, 90, 100]
    for p in percentiles:
        value = col.quantile(p / 100)
        print(f"  {p:3d}-й перцентиль: {value:.2f}")

    print("\nИнтерпретация:")
    print("  50-й перцентиль = медиана")
    print("  25-й и 75-й = нижний и верхний квартили (Q1, Q3)")
    print("  90-й: 90% наблюдений ниже этого значения")


# ============================================================
# Раздел 5: Сводная статистика через pandas
# ============================================================


def demo_describe(df: pd.DataFrame) -> None:
    """Показать возможности pandas describe()."""
    print("\n" + "=" * 50)
    print("СВОДНАЯ СТАТИСТИКА: df.describe()")
    print("=" * 50)

    # Числовые переменные
    print("\nЧисловые столбцы:")
    print(df.describe().round(3))

    # Статистика по группам (по виду)
    print("\nСреднее по видам:")
    print(df.groupby("species")[["petal_length", "petal_width"]].mean().round(3))

    # agg — несколько статистик сразу
    print("\nНесколько статистик через .agg():")
    result = df.groupby("species")["sepal_length"].agg(
        среднее="mean",
        медиана="median",
        стд="std",
        мин="min",
        макс="max",
    )
    print(result.round(3))


# ============================================================
# Точка входа
# ============================================================


def main() -> None:
    """Запустить все демонстрации блока 1."""
    df = load_data()
    demo_centrality(df)
    demo_variation(df)
    demo_percentiles(df)
    demo_describe(df)


if __name__ == "__main__":
    main()
