"""Блок 8: Векторизованные операции и линейная алгебра."""

import numpy as np

# ============================================================
# Векторизованные операции
# ============================================================


def demo_vectorized_ops() -> None:
    """Арифметика над массивами без циклов."""
    print("=" * 50)
    print("Векторизованные операции")
    print("=" * 50)

    grades = np.array([85.0, 91.0, 60.0, 77.0, 95.0, 72.0])
    print(f"Оценки: {grades}")

    # Операции применяются поэлементно
    print(f"\n+10 баллов: {grades + 10}")
    print(f"×1.1 (бонус 10%): {grades * 1.1}")
    print(f"Квадрат: {grades**2}")

    # Сравнение — возвращает булев массив
    mask = grades >= 85
    print(f"\nОценки >= 85: {mask}")
    print(f"Отличники: {grades[mask]}")

    # Универсальные функции (ufunc)
    print(f"\nnp.sqrt(grades): {np.sqrt(grades).round(2)}")
    print(f"np.log(grades):  {np.log(grades).round(2)}")

    # Агрегаты
    print(f"\nМинимум: {grades.min()}")
    print(f"Максимум: {grades.max()}")
    print(f"Среднее: {grades.mean():.2f}")
    print(f"Стд. отклонение: {grades.std():.2f}")


# ============================================================
# Нормализация
# ============================================================


def demo_normalization() -> None:
    """Min-max нормализация и стандартизация (z-score)."""
    print("\n" + "=" * 50)
    print("Нормализация данных")
    print("=" * 50)

    scores = np.array([60.0, 70.0, 80.0, 90.0, 100.0])
    print(f"Исходные оценки: {scores}")

    # Min-max нормализация → диапазон [0, 1]
    min_val, max_val = scores.min(), scores.max()
    normalized = (scores - min_val) / (max_val - min_val)
    print(f"\nMin-max нормализация: {normalized}")

    # Z-score стандартизация → среднее=0, std=1
    mean, std = scores.mean(), scores.std()
    standardized = (scores - mean) / std
    print(f"Z-score стандартизация: {standardized.round(3)}")
    print(f"  среднее после: {standardized.mean():.10f} (≈ 0)")
    print(f"  std после:     {standardized.std():.10f} (≈ 1)")


# ============================================================
# Нормы векторов
# ============================================================


def demo_norms() -> None:
    """np.linalg.norm — длина вектора и расстояние."""
    print("\n" + "=" * 50)
    print("Нормы векторов (np.linalg.norm)")
    print("=" * 50)

    # Профиль студента: [оценка_матем, оценка_физика, оценка_CS]
    student_a = np.array([85.0, 78.0, 92.0])
    student_b = np.array([60.0, 55.0, 70.0])

    # L2-норма (евклидова длина вектора)
    norm_a = np.linalg.norm(student_a)
    norm_b = np.linalg.norm(student_b)
    print(f"Профиль A: {student_a}, ||A|| = {norm_a:.2f}")
    print(f"Профиль B: {student_b}, ||B|| = {norm_b:.2f}")

    # Евклидово расстояние между студентами
    distance = np.linalg.norm(student_a - student_b)
    print(f"\nРасстояние между A и B: {distance:.2f}")

    # L1-норма (сумма абсолютных значений)
    norm_l1 = np.linalg.norm(student_a, ord=1)
    print(f"L1-норма профиля A: {norm_l1:.2f}")


# ============================================================
# Скалярное произведение
# ============================================================


def demo_dot_product() -> None:
    """np.dot — скалярное произведение и матричное умножение."""
    print("\n" + "=" * 50)
    print("Скалярное произведение (np.dot)")
    print("=" * 50)

    # Взвешенная оценка: веса предметов
    weights = np.array([0.4, 0.3, 0.3])  # матем, физика, CS
    grades = np.array([85.0, 78.0, 92.0])

    # Взвешенная сумма = скалярное произведение
    weighted_score = np.dot(weights, grades)
    print(f"Оценки: {grades}")
    print(f"Веса:   {weights}")
    print(f"Взвешенная оценка: {weighted_score:.2f}")

    # Матричное умножение
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    print(f"\nA:\n{A}")
    print(f"B:\n{B}")
    print(f"A @ B (матричное умножение):\n{A @ B}")
    # A @ B эквивалентно np.dot(A, B) для 2D массивов


# ============================================================
# Решение системы линейных уравнений
# ============================================================


def demo_linalg_solve() -> None:
    """np.linalg.solve — решение системы Ax = b."""
    print("\n" + "=" * 50)
    print("Решение системы уравнений (np.linalg.solve)")
    print("=" * 50)

    # Задача: найти коэффициенты a, b, c для квадратичной модели
    # оценки = a * часы_занятий^2 + b * часы_занятий + c
    # Три точки: (1ч → 60), (3ч → 75), (5ч → 95)
    #
    # Система:
    #  a*1 + b*1 + c = 60
    #  a*9 + b*3 + c = 75
    #  a*25 + b*5 + c = 95

    A = np.array([[1, 1, 1], [9, 3, 1], [25, 5, 1]], dtype=float)
    b = np.array([60.0, 75.0, 95.0])

    print("Матрица коэффициентов A:")
    print(A)
    print(f"\nВектор правых частей b: {b}")

    x = np.linalg.solve(A, b)
    print(f"\nРешение x = [a, b, c]: {x.round(4)}")

    # Проверка: A @ x должно быть равно b
    residual = np.linalg.norm(A @ x - b)
    print(f"Невязка ||Ax - b|| = {residual:.2e}  (≈ 0 — решение верное)")

    # Предсказание для 4 часов занятий
    hours = 4.0
    predicted = x[0] * hours**2 + x[1] * hours + x[2]
    print(f"\nПредсказанная оценка при {hours} часах: {predicted:.1f}")


def main() -> None:
    """Точка входа."""
    demo_vectorized_ops()
    demo_normalization()
    demo_norms()
    demo_dot_product()
    demo_linalg_solve()


if __name__ == "__main__":
    main()
