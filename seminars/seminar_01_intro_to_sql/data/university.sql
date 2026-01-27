-- ============================================
-- Семинар 1: Полный скрипт создания учебной БД
-- ============================================
-- Этот файл содержит все команды для создания 
-- и заполнения базы данных "Университет"
--
-- Использование:
--   sqlite3 university.db < university.sql
-- или в DB Browser: Execute SQL

-- ============================================
-- Удаление существующих таблиц
-- ============================================
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;

-- ============================================
-- Создание таблиц
-- ============================================

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    birth_date TEXT,
    enrollment_year INTEGER NOT NULL,
    gpa REAL DEFAULT 0.0,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT UNIQUE NOT NULL,
    course_name TEXT NOT NULL,
    credits INTEGER NOT NULL CHECK(credits > 0),
    instructor TEXT NOT NULL,
    max_students INTEGER DEFAULT 30
);

CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    grade TEXT,
    enrollment_date TEXT DEFAULT (date('now')),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- ============================================
-- Заполнение данными
-- ============================================

INSERT INTO students (first_name, last_name, email, birth_date, enrollment_year, gpa, is_active)
VALUES 
    ('Иван', 'Петров', 'petrov@university.ru', '2003-05-15', 2021, 4.2, 1),
    ('Мария', 'Сидорова', 'sidorova@university.ru', '2004-02-20', 2022, 3.9, 1),
    ('Алексей', 'Козлов', 'kozlov@university.ru', '2002-11-20', 2020, 4.5, 1),
    ('Елена', 'Новикова', 'novikova@university.ru', '2004-03-08', 2022, 3.8, 1),
    ('Дмитрий', 'Волков', 'volkov@university.ru', '2003-07-25', 2021, 4.0, 1),
    ('Анна', 'Кузнецова', 'kuznetsova@university.ru', '2002-09-12', 2020, 4.7, 1),
    ('Сергей', 'Морозов', 'morozov@university.ru', '2004-01-30', 2023, 3.5, 1),
    ('Ольга', 'Васильева', 'vasilieva@university.ru', '2003-12-05', 2021, 4.1, 1),
    ('Николай', 'Зайцев', 'zaytsev@university.ru', '2001-06-18', 2019, 3.2, 0),
    ('Татьяна', 'Лебедева', 'lebedeva@university.ru', '2004-08-22', 2023, 4.3, 1);

INSERT INTO courses (course_code, course_name, credits, instructor, max_students)
VALUES 
    ('CS101', 'Введение в программирование', 4, 'Проф. Смирнов', 50),
    ('CS201', 'Структуры данных', 4, 'Проф. Смирнов', 40),
    ('MATH101', 'Линейная алгебра', 3, 'Доц. Орлов', 60),
    ('MATH201', 'Математический анализ', 4, 'Проф. Иванова', 50),
    ('PHYS101', 'Общая физика', 4, 'Доц. Петрова', 45),
    ('ENG101', 'Английский язык', 2, 'Ст.преп. Сорокина', 25);

INSERT INTO enrollments (student_id, course_id, grade)
VALUES 
    (1, 1, 'A'), (1, 3, 'B'), (1, 5, 'A'),
    (2, 1, 'B'), (2, 4, NULL),
    (3, 2, 'A'), (3, 4, 'A'),
    (4, 1, 'C'), (4, 6, 'A'),
    (5, 1, 'B'), (5, 3, 'B'), (5, 5, 'C'),
    (6, 2, 'A'), (6, 4, 'B'),
    (7, 1, NULL), (7, 6, 'B'),
    (8, 1, 'A'), (8, 3, 'A');

-- ============================================
-- Проверка данных
-- ============================================

SELECT 'Студенты:' AS '';
SELECT * FROM students;

SELECT 'Курсы:' AS '';
SELECT * FROM courses;

SELECT 'Записи на курсы:' AS '';
SELECT * FROM enrollments;
