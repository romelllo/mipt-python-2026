"""Блок 1: Введение в Pandas и NumPy — загрузка данных."""

from pathlib import Path

import numpy as np
import pandas as pd

# ============================================================
# Роли библиотек
# ============================================================
# NumPy — быстрые многомерные массивы и математика
# Pandas — таблицы (DataFrame/Series) поверх NumPy


def demo_numpy_basics() -> None:
    """Демонстрация базовых возможностей NumPy."""
    print("=" * 50)
    print("NumPy — быстрые числовые массивы")
    print("=" * 50)

    # Создание массива из списка
    arr = np.array([1, 2, 3, 4, 5])
    print(f"Массив: {arr}")
    print(f"Тип элементов: {arr.dtype}")

    # Математика над всем массивом сразу (векторизация)
    print(f"Умножить на 2: {arr * 2}")
    print(f"Среднее: {arr.mean():.2f}")


def demo_pandas_basics() -> None:
    """Демонстрация базовых возможностей Pandas."""
    print("\n" + "=" * 50)
    print("Pandas — таблицы данных (DataFrame)")
    print("=" * 50)

    # Series — одномерный ряд с метками
    grades = pd.Series([85, 91, 60, 77], name="grade_math")
    print("Series (оценки по математике):")
    print(grades)

    # DataFrame — двумерная таблица
    data = {
        "name": ["Алексей", "Мария", "Дмитрий"],
        "grade_math": [85, 91, 60],
        "city": ["Москва", "СПб", "Москва"],
    }
    df = pd.DataFrame(data)
    print("\nDataFrame (мини-таблица):")
    print(df)


def load_dataset() -> pd.DataFrame:
    """Загружает датасет студентов из CSV-файла.

    Returns:
        DataFrame с данными студентов.
    """
    # Путь относительно директории семинара
    data_path = Path(__file__).parent.parent / "data" / "students.csv"
    df = pd.read_csv(data_path)
    return df


def demo_load() -> None:
    """Демонстрация загрузки CSV-файла."""
    print("\n" + "=" * 50)
    print("Загрузка данных из CSV")
    print("=" * 50)

    df = load_dataset()

    print(f"Тип объекта: {type(df)}")
    print(f"Загружено строк: {len(df)}")
    print("\nПервые 3 строки:")
    print(df.head(3))

    # Другие форматы загрузки (для справки):
    # pd.read_excel("file.xlsx")
    # pd.read_json("file.json")
    # pd.read_sql("SELECT * FROM table", connection)


def main() -> None:
    """Точка входа."""
    demo_numpy_basics()
    demo_pandas_basics()
    demo_load()


if __name__ == "__main__":
    main()
