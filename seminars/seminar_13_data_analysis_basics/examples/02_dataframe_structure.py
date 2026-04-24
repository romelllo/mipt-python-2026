"""Блок 2: Структура и атрибуты DataFrame."""

from pathlib import Path

import pandas as pd


def load_df() -> pd.DataFrame:
    """Загружает датасет студентов."""
    data_path = Path(__file__).parent.parent / "data" / "students.csv"
    return pd.read_csv(data_path)


# ============================================================
# Атрибуты DataFrame
# ============================================================


def demo_shape_and_size(df: pd.DataFrame) -> None:
    """Размерность и количество элементов."""
    print("=" * 50)
    print("Размерность DataFrame")
    print("=" * 50)

    # ndim — количество измерений (для DataFrame всегда 2)
    print(f"ndim  : {df.ndim}  (строки и столбцы)")

    # shape — кортеж (строки, столбцы)
    print(f"shape : {df.shape}  → {df.shape[0]} строк, {df.shape[1]} столбцов")

    # size — общее число ячеек (строки × столбцы)
    print(f"size  : {df.size}  (всего ячеек)")


def demo_columns_and_axes(df: pd.DataFrame) -> None:
    """Имена столбцов и оси."""
    print("\n" + "=" * 50)
    print("Столбцы и оси")
    print("=" * 50)

    # columns — Index с именами столбцов
    print("columns:")
    print(df.columns.tolist())

    # axes[0] — индекс строк, axes[1] — индекс столбцов
    print(f"\naxes[0] (индекс строк): {df.axes[0][:5].tolist()} ...")
    print(f"axes[1] (индекс столбцов): {df.axes[1].tolist()}")


def demo_dtypes(df: pd.DataFrame) -> None:
    """Типы данных каждого столбца."""
    print("\n" + "=" * 50)
    print("Типы данных (dtypes)")
    print("=" * 50)

    # dtypes — Series с типом каждого столбца
    print(df.dtypes)

    print("\nПодсчёт типов:")
    print(df.dtypes.value_counts())

    # Выбрать только числовые столбцы
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    print(f"\nЧисловые столбцы: {numeric_cols}")

    # Выбрать только текстовые столбцы
    str_cols = df.select_dtypes(include="str").columns.tolist()
    print(f"Текстовые столбцы: {str_cols}")


def demo_index(df: pd.DataFrame) -> None:
    """Индекс строк."""
    print("\n" + "=" * 50)
    print("Индекс строк")
    print("=" * 50)

    print(f"Тип индекса: {type(df.index)}")
    print(f"Первые 5 значений: {df.index[:5].tolist()}")

    # Установить столбец 'name' как индекс
    df_indexed = df.set_index("name")
    print("\nПосле set_index('name'):")
    print(df_indexed.head(3))


def main() -> None:
    """Точка входа."""
    df = load_df()
    demo_shape_and_size(df)
    demo_columns_and_axes(df)
    demo_dtypes(df)
    demo_index(df)


if __name__ == "__main__":
    main()
