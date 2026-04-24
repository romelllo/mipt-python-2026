"""Блок 3: Быстрый осмотр данных — head, tail, info, describe."""

from pathlib import Path

import pandas as pd


def load_df() -> pd.DataFrame:
    """Загружает датасет студентов."""
    data_path = Path(__file__).parent.parent / "data" / "students.csv"
    return pd.read_csv(data_path)


# ============================================================
# Первый взгляд на данные
# ============================================================


def demo_head_tail(df: pd.DataFrame) -> None:
    """head() и tail() — первые и последние строки."""
    print("=" * 50)
    print("head() и tail()")
    print("=" * 50)

    # По умолчанию — 5 строк
    print("Первые 5 строк (head):")
    print(df.head())

    print("\nПоследние 3 строки (tail(3)):")
    print(df.tail(3))


def demo_info(df: pd.DataFrame) -> None:
    """info() — сводка о структуре и пропусках."""
    print("\n" + "=" * 50)
    print("info() — структура таблицы")
    print("=" * 50)

    # info() печатает:
    # - количество строк и столбцов
    # - имя, количество non-null значений и тип каждого столбца
    # - использование памяти
    df.info()

    # Обратите внимание: scholarship имеет меньше non-null значений
    # — это сигнал о пропущенных данных!


def demo_describe(df: pd.DataFrame) -> None:
    """describe() — статистическая сводка."""
    print("\n" + "=" * 50)
    print("describe() — статистика числовых столбцов")
    print("=" * 50)

    # По умолчанию — только числовые столбцы
    print(df.describe())

    print("\ndescribe() для текстовых столбцов:")
    # include='str' — статистика для строковых столбцов
    print(df.describe(include="str"))

    print("\ndescribe() для ВСЕХ столбцов:")
    print(df.describe(include="all"))


def demo_value_counts(df: pd.DataFrame) -> None:
    """value_counts() — частота значений в столбце."""
    print("\n" + "=" * 50)
    print("value_counts() — распределение по городам")
    print("=" * 50)

    print(df["city"].value_counts())

    # Нормированные частоты (доли)
    print("\nДоли (normalize=True):")
    print(df["city"].value_counts(normalize=True).round(2))


def main() -> None:
    """Точка входа."""
    df = load_df()
    demo_head_tail(df)
    demo_info(df)
    demo_describe(df)
    demo_value_counts(df)


if __name__ == "__main__":
    main()
