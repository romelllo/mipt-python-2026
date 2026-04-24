"""Блок 4: Предобработка данных — пропуски, дубликаты, операции со столбцами."""

from pathlib import Path

import pandas as pd


def load_df() -> pd.DataFrame:
    """Загружает датасет студентов."""
    data_path = Path(__file__).parent.parent / "data" / "students.csv"
    return pd.read_csv(data_path)


# ============================================================
# Пропущенные значения (Missing Values)
# ============================================================


def demo_missing_values(df: pd.DataFrame) -> None:
    """Обнаружение и обработка пропущенных значений."""
    print("=" * 50)
    print("Пропущенные значения")
    print("=" * 50)

    # isnull() возвращает булеву маску True там, где NaN
    print("Маска пропусков (первые 5 строк):")
    print(df.isnull().head())

    # isnull().sum() — количество пропусков в каждом столбце
    print("\nКоличество пропусков по столбцам:")
    print(df.isnull().sum())

    # Процент пропусков
    print("\nПроцент пропусков:")
    missing_pct = (df.isnull().sum() / len(df) * 100).round(1)
    print(missing_pct[missing_pct > 0])


def demo_handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Стратегии обработки пропусков."""
    print("\n" + "=" * 50)
    print("Обработка пропусков")
    print("=" * 50)

    print(f"Строк до обработки: {len(df)}")

    # --- Стратегия 1: dropna() — удалить строки с пропусками ---
    df_dropped = df.dropna()
    print(f"После dropna(): {len(df_dropped)} строк")

    # dropna(subset=[...]) — удалять только если пропуск в конкретных столбцах
    df_dropped_subset = df.dropna(subset=["scholarship"])
    print(f"После dropna(subset=['scholarship']): {len(df_dropped_subset)} строк")

    # --- Стратегия 2: fillna() — заполнить пропуски ---
    # Заполнить медианой (устойчиво к выбросам)
    median_scholarship = df["scholarship"].median()
    df_filled = df.copy()
    df_filled["scholarship"] = df_filled["scholarship"].fillna(median_scholarship)
    print(f"\nМедиана стипендии: {median_scholarship}")
    print(f"Пропусков после fillna: {df_filled['scholarship'].isnull().sum()}")

    # Заполнить нулём
    df_zero = df.copy()
    df_zero["scholarship"] = df_zero["scholarship"].fillna(0)
    print(f"Пропусков после fillna(0): {df_zero['scholarship'].isnull().sum()}")

    return df_filled


# ============================================================
# Дубликаты
# ============================================================


def demo_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Обнаружение и удаление дубликатов."""
    print("\n" + "=" * 50)
    print("Дубликаты")
    print("=" * 50)

    # duplicated() — булева маска: True для повторяющихся строк
    print(f"Количество дубликатов: {df.duplicated().sum()}")

    # Показать сами дубликаты
    dupes = df[df.duplicated(keep=False)]
    print("\nДублирующиеся строки:")
    print(dupes)

    # drop_duplicates() — оставить только уникальные строки
    df_clean = df.drop_duplicates()
    print(f"\nСтрок после drop_duplicates(): {len(df_clean)}")

    return df_clean


# ============================================================
# Операции со столбцами
# ============================================================


def demo_column_operations(df: pd.DataFrame) -> None:
    """Переименование, добавление и удаление столбцов."""
    print("\n" + "=" * 50)
    print("Операции со столбцами")
    print("=" * 50)

    df = df.copy()

    # --- Переименование ---
    df = df.rename(columns={"grade_cs": "grade_computer_science"})
    print("После rename:")
    print(df.columns.tolist())

    # --- Добавление нового столбца ---
    # Средний балл по трём предметам
    df["grade_avg"] = (
        df["grade_math"] + df["grade_physics"] + df["grade_computer_science"]
    ) / 3
    df["grade_avg"] = df["grade_avg"].round(1)
    print("\nНовый столбец grade_avg (первые 3 строки):")
    print(
        df[
            [
                "name",
                "grade_math",
                "grade_physics",
                "grade_computer_science",
                "grade_avg",
            ]
        ].head(3)
    )

    # --- Удаление столбца ---
    df = df.drop(columns=["grade_avg"])
    print(f"\nПосле drop(columns=['grade_avg']): {df.columns.tolist()}")

    # --- Изменение типа столбца ---
    df["age"] = df["age"].astype(float)
    print(f"\nТип столбца age после astype(float): {df['age'].dtype}")


def main() -> None:
    """Точка входа."""
    df = load_df()
    demo_missing_values(df)
    df_filled = demo_handle_missing(df)
    df_clean = demo_duplicates(df_filled)
    demo_column_operations(df_clean)


if __name__ == "__main__":
    main()
