"""
Пример: Основы синтаксиса Python

Этот файл демонстрирует базовые концепции Python:
- Переменные и типы данных
- Операторы
- Условные конструкции
- Циклы
"""

def main():
    print("=" * 50)
    print("Основы синтаксиса Python")
    print("=" * 50)
    
    # Переменные и типы данных
    print("\n1. Переменные и типы данных:")
    name = "Python"  # str
    version = 3.12  # float
    year = 2024  # int
    is_popular = True  # bool
    
    print(f"Язык: {name}")
    print(f"Версия: {version}")
    print(f"Год: {year}")
    print(f"Популярен: {is_popular}")
    
    # Операторы
    print("\n2. Арифметические операторы:")
    a, b = 10, 3
    print(f"{a} + {b} = {a + b}")
    print(f"{a} - {b} = {a - b}")
    print(f"{a} * {b} = {a * b}")
    print(f"{a} / {b} = {a / b}")
    print(f"{a} // {b} = {a // b}")  # Целочисленное деление
    print(f"{a} % {b} = {a % b}")  # Остаток от деления
    print(f"{a} ** {b} = {a ** b}")  # Возведение в степень
    
    # Условные конструкции
    print("\n3. Условные конструкции:")
    score = 85
    
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "F"
    
    print(f"Оценка {score} соответствует уровню {grade}")
    
    # Циклы
    print("\n4. Циклы:")
    print("For цикл:")
    for i in range(5):
        print(f"  Итерация {i}")
    
    print("\nWhile цикл:")
    count = 0
    while count < 3:
        print(f"  Счетчик: {count}")
        count += 1
    
    # List comprehension
    print("\n5. List Comprehension:")
    squares = [x**2 for x in range(10)]
    print(f"Квадраты чисел от 0 до 9: {squares}")
    
    # Фильтрация с comprehension
    even_squares = [x**2 for x in range(10) if x % 2 == 0]
    print(f"Квадраты четных чисел: {even_squares}")


if __name__ == "__main__":
    main()
