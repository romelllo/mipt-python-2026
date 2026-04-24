"""Блок 6: GroupBy и агрегация."""

from pathlib import Path

import pandas as pd


def load_df() -> pd.DataFrame:
    """Загружает датасет студентов."""
    data_path = Path(__file__).parent.parent / "data" / "students.csv"
    return pd.read_csv(data_path)


# ============================================================
# groupby() — разбить-применить-объединить
# ============================================================


def demo_simple_groupby(df: pd.DataFrame) -> None:
    """Базовая группировка по одному столбцу."""
    print("=" * 50)
    print("Группировка по городу")
    print("=" * 50)

    # Средний балл по математике в каждом городе
    avg_math = df.groupby("city")["grade_math"].mean().round(1)
    print("Средний балл по математике:")
    print(avg_math)

    # Количество студентов в каждом городе
    count_by_city = df.groupby("city")["name"].count()
    print("\nКоличество студентов:")
    print(count_by_city)

    # Сумма стипендий по городам (NaN игнорируются автоматически)
    total_scholarship = df.groupby("city")["scholarship"].sum()
    print("\nСумма стипендий:")
    print(total_scholarship)


def demo_agg(df: pd.DataFrame) -> None:
    """agg() — несколько агрегатных функций сразу."""
    print("\n" + "=" * 50)
    print("agg() — несколько функций")
    print("=" * 50)

    # Несколько функций для одного столбца
    stats = df.groupby("city")["grade_math"].agg(["mean", "min", "max", "count"])
    stats.columns = ["среднее", "минимум", "максимум", "количество"]
    print("Статистика по математике по городам:")
    print(stats.round(1))

    # Разные функции для разных столбцов
    multi_agg = df.groupby("city").agg(
        avg_math=("grade_math", "mean"),
        avg_physics=("grade_physics", "mean"),
        total_scholarship=("scholarship", "sum"),
        student_count=("name", "count"),
    )
    print("\nМультиагрегация:")
    print(multi_agg.round(1))


def demo_groupby_filter(df: pd.DataFrame) -> None:
    """Группировка с последующей фильтрацией."""
    print("\n" + "=" * 50)
    print("Группировка + фильтрация")
    print("=" * 50)

    # Города, где средний балл по CS выше 85
    city_avg_cs = df.groupby("city")["grade_cs"].mean()
    top_cities = city_avg_cs[city_avg_cs > 85].index.tolist()
    print(f"Города со средним CS > 85: {top_cities}")

    # Студенты из этих городов
    top_students = df[df["city"].isin(top_cities)]
    print(f"Студентов из этих городов: {len(top_students)}")

    # sort_values — отсортировать результат
    print("\nГорода по убыванию среднего балла по математике:")
    print(df.groupby("city")["grade_math"].mean().round(1).sort_values(ascending=False))


def demo_transform(df: pd.DataFrame) -> None:
    """transform() — добавить агрегат как новый столбец."""
    print("\n" + "=" * 50)
    print("transform() — агрегат как новый столбец")
    print("=" * 50)

    df = df.copy()

    # Добавить столбец со средним баллом по городу для каждой строки
    df["city_avg_math"] = df.groupby("city")["grade_math"].transform("mean").round(1)

    # Отклонение студента от среднего по городу
    df["math_vs_city_avg"] = (df["grade_math"] - df["city_avg_math"]).round(1)

    print(
        df[["name", "city", "grade_math", "city_avg_math", "math_vs_city_avg"]].head(8)
    )


def main() -> None:
    """Точка входа."""
    df = load_df()
    demo_simple_groupby(df)
    demo_agg(df)
    demo_groupby_filter(df)
    demo_transform(df)


if __name__ == "__main__":
    main()
