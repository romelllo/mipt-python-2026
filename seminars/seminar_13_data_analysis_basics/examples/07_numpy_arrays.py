"""Блок 7: NumPy массивы — ndarray, атрибуты, индексация, reshape, transpose."""

import numpy as np

# ============================================================
# Создание массивов
# ============================================================


def demo_array_creation() -> None:
    """Способы создания ndarray."""
    print("=" * 50)
    print("Создание массивов NumPy")
    print("=" * 50)

    # Из списка Python
    arr1d = np.array([10, 20, 30, 40, 50])
    print(f"1D из списка: {arr1d}")

    # Двумерный массив (матрица)
    arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"\n2D матрица:\n{arr2d}")

    # Специальные массивы
    print(f"\nnp.zeros((2, 3)):\n{np.zeros((2, 3))}")
    print(f"\nnp.ones((2, 4)):\n{np.ones((2, 4))}")
    print(f"\nnp.arange(0, 10, 2): {np.arange(0, 10, 2)}")
    print(f"\nnp.linspace(0, 1, 5): {np.linspace(0, 1, 5)}")

    # Случайные числа (фиксируем seed для воспроизводимости)
    rng = np.random.default_rng(seed=42)
    rand_arr = rng.integers(50, 100, size=(3, 4))
    print(f"\nСлучайные целые (3×4):\n{rand_arr}")


# ============================================================
# Атрибуты ndarray
# ============================================================


def demo_array_attributes() -> None:
    """ndim, shape, size, dtype."""
    print("\n" + "=" * 50)
    print("Атрибуты ndarray")
    print("=" * 50)

    arr = np.array([[1.0, 2.5, 3.7], [4.1, 5.9, 6.3]])

    print(f"Массив:\n{arr}")
    print(f"\nndim  : {arr.ndim}   (количество измерений)")
    print(f"shape : {arr.shape}  (строки × столбцы)")
    print(f"size  : {arr.size}   (всего элементов)")
    print(f"dtype : {arr.dtype}  (тип элементов)")

    # Изменение типа
    arr_int = arr.astype(int)
    print(f"\nПосле astype(int):\n{arr_int}")
    print(f"dtype : {arr_int.dtype}")


# ============================================================
# Индексация и срезы
# ============================================================


def demo_indexing() -> None:
    """Индексация одномерных и двумерных массивов."""
    print("\n" + "=" * 50)
    print("Индексация массивов")
    print("=" * 50)

    arr = np.array([10, 20, 30, 40, 50, 60])

    print(f"Массив: {arr}")
    print(f"arr[0]   = {arr[0]}   (первый элемент)")
    print(f"arr[-1]  = {arr[-1]}  (последний элемент)")
    print(f"arr[1:4] = {arr[1:4]} (срез)")
    print(f"arr[::2] = {arr[::2]} (каждый второй)")

    # Двумерный массив
    mat = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"\nМатрица:\n{mat}")
    print(f"mat[0, 1]  = {mat[0, 1]}  (строка 0, столбец 1)")
    print(f"mat[1, :]  = {mat[1, :]}  (вся строка 1)")
    print(f"mat[:, 2]  = {mat[:, 2]}  (весь столбец 2)")
    print(f"mat[0:2, 0:2]:\n{mat[0:2, 0:2]}")

    # Булева индексация
    print(f"\nЭлементы > 5: {arr[arr > 30]}")


# ============================================================
# reshape и transpose
# ============================================================


def demo_reshape_transpose() -> None:
    """Изменение формы и транспонирование."""
    print("\n" + "=" * 50)
    print("reshape и transpose")
    print("=" * 50)

    arr = np.arange(12)
    print(f"Исходный массив: {arr}")

    # reshape — изменить форму без копирования данных
    mat_3x4 = arr.reshape(3, 4)
    print(f"\nreshape(3, 4):\n{mat_3x4}")

    mat_2x6 = arr.reshape(2, 6)
    print(f"\nreshape(2, 6):\n{mat_2x6}")

    # -1 означает «вычислить автоматически»
    mat_4x3 = arr.reshape(4, -1)
    print(f"\nreshape(4, -1) → shape={mat_4x3.shape}:\n{mat_4x3}")

    # flatten() — всегда возвращает копию в виде 1D
    flat = mat_3x4.flatten()
    print(f"\nflatten(): {flat}")

    # transpose() — поменять строки и столбцы
    print(f"\nМатрица 3×4:\n{mat_3x4}")
    print(f"\nТранспонированная (4×3):\n{mat_3x4.T}")
    print(f"shape до: {mat_3x4.shape}, после .T: {mat_3x4.T.shape}")


def main() -> None:
    """Точка входа."""
    demo_array_creation()
    demo_array_attributes()
    demo_indexing()
    demo_reshape_transpose()


if __name__ == "__main__":
    main()
