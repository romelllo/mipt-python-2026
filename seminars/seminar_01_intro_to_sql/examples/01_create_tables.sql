-- ============================================
-- Семинар 1: Создание таблиц (CREATE TABLE)
-- ============================================
-- Этот файл демонстрирует создание таблиц с разными
-- типами данных и ограничениями

-- ============================================
-- Удаляем таблицы, если они существуют
-- (для возможности повторного запуска скрипта)
-- ============================================
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;

-- ============================================
-- Таблица студентов
-- ============================================
-- Демонстрирует: PRIMARY KEY, NOT NULL, UNIQUE, DEFAULT, CHECK
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Автоинкремент ID
    first_name TEXT NOT NULL,                      -- Обязательное поле
    last_name TEXT NOT NULL,                       -- Обязательное поле
    email TEXT UNIQUE,                             -- Уникальный email
    birth_date TEXT,                               -- Дата в формате 'YYYY-MM-DD'
    enrollment_year INTEGER NOT NULL,              -- Год поступления
    gpa REAL DEFAULT 0.0,                          -- Средний балл (по умолчанию 0)
    is_active INTEGER DEFAULT 1                    -- 1 = активен, 0 = отчислен
);

-- ============================================
-- Таблица курсов
-- ============================================
-- Демонстрирует: CHECK constraint
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT UNIQUE NOT NULL,              -- Код курса, например 'CS101'
    course_name TEXT NOT NULL,                     -- Название курса
    credits INTEGER NOT NULL CHECK(credits > 0),   -- Кредиты (должно быть > 0)
    instructor TEXT NOT NULL,                      -- Преподаватель
    max_students INTEGER DEFAULT 30                -- Макс. количество студентов
);

-- ============================================
-- Связующая таблица (многие-ко-многим)
-- ============================================
-- Демонстрирует: внешние ключи (изучим подробнее на семинаре 2)
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    grade TEXT,                                    -- Оценка: 'A', 'B', 'C', 'D', 'F'
    enrollment_date TEXT DEFAULT (date('now')),    -- Дата записи
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- ============================================
-- Проверка созданных таблиц
-- ============================================
-- В консоли sqlite3 используйте:
--   .tables          -- список всех таблиц
--   .schema students -- структура таблицы students

-- В DB Browser: вкладка "Database Structure"
