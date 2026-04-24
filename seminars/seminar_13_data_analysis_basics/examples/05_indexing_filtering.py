"""Блок 5: Индексация и фильтрация — loc, iloc, булева индексация."""

from pathlib import Path

import pandas as pd


def load_df() -> pd.DataFrame:
    """Загружает датасет студентов."""
    data_path = Path(__file__).parent.parent / "data" / "students.csv"
    return pd.read_csv(data_path)


# ============================================================
# loc — доступ по меткам (label-based)
# ============================================================


def demo_loc(df: pd.DataFrame) -> None:
    """Индексация по меткам строк и именам столбцов."""
    print("=" * 50)
    print("loc — доступ по меткам")
    print("=" * 50)

    # df.loc[строки, столбцы]
    # Одна строка по индексу
    print("Строка с индексом 0:")
    print(df.loc[0])

    # Диапазон строк + конкретные столбцы
    print("\nСтроки 0–2, столбцы name и grade_math:")
    print(df.loc[0:2, ["name", "grade_math"]])

    # Установим name как индекс для наглядности
    df_named = df.set_index("name")
    print("\nПосле set_index('name') — строка 'Мария Петрова':")
    print(df_named.loc["Мария Петрова", ["grade_math", "grade_physics"]])


# ============================================================
# iloc — доступ по позиции (position-based)
# ============================================================


def demo_iloc(df: pd.DataFrame) -> None:
    """Индексация по целочисленным позициям."""
    print("\n" + "=" * 50)
    print("iloc — доступ по позиции")
    print("=" * 50)

    # df.iloc[строки, столбцы] — только целые числа или срезы
    print("Первая строка (iloc[0]):")
    print(df.iloc[0])

    print("\nСтроки 0–2, столбцы 0–2 (iloc[0:3, 0:3]):")
    print(df.iloc[0:3, 0:3])

    # Последние 3 строки
    print("\nПоследние 3 строки (iloc[-3:]):")
    print(df.iloc[-3:])

    # Каждая вторая строка
    print("\nКаждая вторая строка (iloc[::2]) — первые 4:")
    print(df.iloc[::2].head(4))


# ============================================================
# Булева индексация (условная фильтрация)
# ============================================================


def demo_boolean_indexing(df: pd.DataFrame) -> None:
    """Фильтрация строк по условию."""
    print("\n" + "=" * 50)
    print("Булева индексация")
    print("=" * 50)

    # Одно условие: студенты из Москвы
    moscow_students = df[df["city"] == "Москва"]
    print(f"Студентов из Москвы: {len(moscow_students)}")
    print(moscow_students[["name", "city", "grade_math"]].head(4))

    # Несколько условий: & (и), | (или), ~ (не)
    # Отличники по математике (>= 90) из Санкт-Петербурга
    top_spb = df[(df["grade_math"] >= 90) & (df["city"] == "Санкт-Петербург")]
    print(f"\nОтличники по математике из СПб: {len(top_spb)}")
    print(top_spb[["name", "city", "grade_math"]])

    # Студенты без стипендии (NaN)
    no_scholarship = df[df["scholarship"].isnull()]
    print(f"\nСтудентов без стипендии: {len(no_scholarship)}")

    # isin() — фильтр по списку значений
    big_cities = df[df["city"].isin(["Москва", "Санкт-Петербург"])]
    print(f"\nСтудентов из Москвы или СПб: {len(big_cities)}")

    # query() — удобный строковый синтаксис
    high_cs = df.query("grade_cs >= 90 and age <= 20")
    print(f"\nМолодые отличники по CS (query): {len(high_cs)}")
    print(high_cs[["name", "age", "grade_cs"]])


def main() -> None:
    """Точка входа."""
    df = load_df()
    demo_loc(df)
    demo_iloc(df)
    demo_boolean_indexing(df)


if __name__ == "__main__":
    main()
