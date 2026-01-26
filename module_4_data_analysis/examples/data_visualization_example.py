"""
Пример: Работа с NumPy и визуализация данных

Демонстрация базовых операций с NumPy и создания визуализаций.
"""

import numpy as np
import matplotlib.pyplot as plt


def numpy_basics():
    """Основы работы с NumPy"""
    print("=" * 60)
    print("Основы NumPy")
    print("=" * 60)
    
    # Создание массивов
    arr1 = np.array([1, 2, 3, 4, 5])
    arr2 = np.arange(0, 10, 2)
    arr3 = np.linspace(0, 1, 5)
    
    print("\n1. Создание массивов:")
    print(f"arr1: {arr1}")
    print(f"arr2: {arr2}")
    print(f"arr3: {arr3}")
    
    # Многомерные массивы
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"\nМатрица:\n{matrix}")
    print(f"Размерность: {matrix.shape}")
    
    # Математические операции
    print("\n2. Математические операции:")
    print(f"arr1 * 2 = {arr1 * 2}")
    print(f"arr1 + 10 = {arr1 + 10}")
    print(f"Среднее: {np.mean(arr1)}")
    print(f"Сумма: {np.sum(arr1)}")
    print(f"Стандартное отклонение: {np.std(arr1):.2f}")


def create_visualizations():
    """Создание различных типов визуализаций"""
    print("\n" + "=" * 60)
    print("Создание визуализаций")
    print("=" * 60)
    
    # Данные для графиков
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # Создание фигуры с несколькими графиками
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Примеры визуализаций данных', fontsize=16)
    
    # График 1: Линейный график
    axes[0, 0].plot(x, y1, label='sin(x)', color='blue')
    axes[0, 0].plot(x, y2, label='cos(x)', color='red')
    axes[0, 0].set_title('Линейные графики')
    axes[0, 0].set_xlabel('x')
    axes[0, 0].set_ylabel('y')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # График 2: Scatter plot
    np.random.seed(42)
    x_scatter = np.random.randn(100)
    y_scatter = 2 * x_scatter + np.random.randn(100)
    axes[0, 1].scatter(x_scatter, y_scatter, alpha=0.5)
    axes[0, 1].set_title('Точечный график (Scatter)')
    axes[0, 1].set_xlabel('X')
    axes[0, 1].set_ylabel('Y')
    axes[0, 1].grid(True, alpha=0.3)
    
    # График 3: Гистограмма
    data = np.random.randn(1000)
    axes[1, 0].hist(data, bins=30, edgecolor='black', alpha=0.7)
    axes[1, 0].set_title('Гистограмма')
    axes[1, 0].set_xlabel('Значение')
    axes[1, 0].set_ylabel('Частота')
    axes[1, 0].grid(True, alpha=0.3)
    
    # График 4: Bar chart
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [23, 45, 56, 78, 32]
    axes[1, 1].bar(categories, values, color='skyblue', edgecolor='black')
    axes[1, 1].set_title('Столбчатая диаграмма')
    axes[1, 1].set_xlabel('Категория')
    axes[1, 1].set_ylabel('Значение')
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    # Сохранение графика
    output_file = 'data_visualization_example.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\nГрафики сохранены в файл: {output_file}")
    
    # Показать график (закомментируйте, если запускаете без GUI)
    # plt.show()
    
    plt.close()


def statistical_analysis():
    """Простой статистический анализ"""
    print("\n" + "=" * 60)
    print("Статистический анализ")
    print("=" * 60)
    
    # Генерация данных
    np.random.seed(42)
    data = np.random.randn(1000)
    
    print("\nОписательная статистика:")
    print(f"Среднее: {np.mean(data):.4f}")
    print(f"Медиана: {np.median(data):.4f}")
    print(f"Стандартное отклонение: {np.std(data):.4f}")
    print(f"Минимум: {np.min(data):.4f}")
    print(f"Максимум: {np.max(data):.4f}")
    print(f"25-й перцентиль: {np.percentile(data, 25):.4f}")
    print(f"75-й перцентиль: {np.percentile(data, 75):.4f}")


def main():
    """Главная функция"""
    numpy_basics()
    statistical_analysis()
    create_visualizations()
    
    print("\n" + "=" * 60)
    print("Анализ завершен!")
    print("=" * 60)


if __name__ == "__main__":
    main()
