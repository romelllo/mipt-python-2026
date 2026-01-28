-- ============================================
-- Семинар 2: Расширенная база данных университета
-- ============================================
-- Этот файл расширяет базовую БД university дополнительными
-- данными для практики сложных SQL-запросов.
--
-- Использование:
--   sqlite3 university.db < university_extended.sql
-- или запустите сначала university.sql из семинара 1

-- ============================================
-- Удаление существующих таблиц
-- ============================================
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS departments;

-- ============================================
-- Создание таблиц
-- ============================================

-- Факультеты (новая таблица для JOIN-ов)
CREATE TABLE departments (
    dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_name TEXT NOT NULL UNIQUE,
    building TEXT,
    head_name TEXT
);

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    birth_date TEXT,
    enrollment_year INTEGER NOT NULL,
    gpa REAL DEFAULT 0.0,
    is_active INTEGER DEFAULT 1,
    dept_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT UNIQUE NOT NULL,
    course_name TEXT NOT NULL,
    credits INTEGER NOT NULL CHECK(credits > 0),
    instructor TEXT NOT NULL,
    max_students INTEGER DEFAULT 30,
    dept_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    grade TEXT CHECK(grade IN ('A', 'B', 'C', 'D', 'F') OR grade IS NULL),
    enrollment_date TEXT DEFAULT (date('now')),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- ============================================
-- Индексы для оптимизации
-- ============================================
CREATE INDEX idx_students_year ON students(enrollment_year);
CREATE INDEX idx_students_gpa ON students(gpa);
CREATE INDEX idx_students_dept ON students(dept_id);
CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);
CREATE INDEX idx_courses_dept ON courses(dept_id);

-- ============================================
-- Заполнение данными
-- ============================================

-- Факультеты
INSERT INTO departments (dept_name, building, head_name) VALUES
    ('Информатика', 'Главный корпус', 'Проф. Смирнов А.В.'),
    ('Математика', 'Корпус М', 'Проф. Иванова Е.П.'),
    ('Физика', 'Корпус Ф', 'Проф. Петров С.И.'),
    ('Иностранные языки', 'Корпус Л', 'Доц. Сорокина Н.К.');

-- Студенты (20 человек)
INSERT INTO students (first_name, last_name, email, birth_date, enrollment_year, gpa, is_active, dept_id)
VALUES 
    ('Иван', 'Петров', 'petrov@university.ru', '2003-05-15', 2021, 4.2, 1, 1),
    ('Мария', 'Сидорова', 'sidorova@university.ru', '2004-02-20', 2022, 3.9, 1, 2),
    ('Алексей', 'Козлов', 'kozlov@university.ru', '2002-11-20', 2020, 4.5, 1, 1),
    ('Елена', 'Новикова', 'novikova@university.ru', '2004-03-08', 2022, 3.8, 1, 2),
    ('Дмитрий', 'Волков', 'volkov@university.ru', '2003-07-25', 2021, 4.0, 1, 3),
    ('Анна', 'Кузнецова', 'kuznetsova@university.ru', '2002-09-12', 2020, 4.7, 1, 1),
    ('Сергей', 'Морозов', 'morozov@university.ru', '2004-01-30', 2023, 3.5, 1, 4),
    ('Ольга', 'Васильева', 'vasilieva@university.ru', '2003-12-05', 2021, 4.1, 1, 2),
    ('Николай', 'Зайцев', 'zaytsev@university.ru', '2001-06-18', 2019, 3.2, 0, 3),
    ('Татьяна', 'Лебедева', 'lebedeva@university.ru', '2004-08-22', 2023, 4.3, 1, 1),
    ('Андрей', 'Соколов', 'sokolov@university.ru', '2003-04-11', 2021, 3.7, 1, 3),
    ('Екатерина', 'Попова', 'popova@university.ru', '2002-10-03', 2020, 4.4, 1, 2),
    ('Михаил', 'Федоров', 'fedorov@university.ru', '2004-07-19', 2023, 3.6, 1, 1),
    ('Виктория', 'Орлова', 'orlova@university.ru', '2003-01-25', 2021, 4.8, 1, 2),
    ('Павел', 'Николаев', 'nikolaev@university.ru', '2002-12-08', 2020, 3.9, 1, 3),
    ('Юлия', 'Ковалева', 'kovaleva@university.ru', '2004-05-30', 2022, 4.1, 1, 4),
    ('Артём', 'Егоров', 'egorov@university.ru', '2003-09-14', 2021, 3.4, 0, 1),
    ('Светлана', 'Белова', 'belova@university.ru', '2004-02-28', 2023, 4.6, 1, 2),
    ('Денис', 'Черных', 'chernykh@university.ru', '2002-08-07', 2020, 4.0, 1, 3),
    ('Наталья', 'Громова', 'gromova@university.ru', '2003-11-22', 2022, 3.8, 1, 4);

-- Курсы (10 курсов)
INSERT INTO courses (course_code, course_name, credits, instructor, max_students, dept_id)
VALUES 
    ('CS101', 'Введение в программирование', 4, 'Проф. Смирнов', 50, 1),
    ('CS201', 'Структуры данных', 4, 'Проф. Смирнов', 40, 1),
    ('CS301', 'Базы данных', 3, 'Доц. Кириллов', 35, 1),
    ('MATH101', 'Линейная алгебра', 3, 'Доц. Орлов', 60, 2),
    ('MATH201', 'Математический анализ', 4, 'Проф. Иванова', 50, 2),
    ('MATH301', 'Теория вероятностей', 3, 'Проф. Иванова', 45, 2),
    ('PHYS101', 'Общая физика', 4, 'Доц. Петрова', 45, 3),
    ('PHYS201', 'Квантовая механика', 4, 'Проф. Сидоров', 30, 3),
    ('ENG101', 'Английский язык', 2, 'Ст.преп. Сорокина', 25, 4),
    ('ENG201', 'Технический английский', 2, 'Доц. Козлова', 25, 4);

-- Записи на курсы (расширенный набор)
INSERT INTO enrollments (student_id, course_id, grade, enrollment_date) VALUES
    -- Иван Петров (student_id=1)
    (1, 1, 'A', '2021-09-01'), (1, 4, 'B', '2021-09-01'), (1, 7, 'A', '2022-02-01'),
    -- Мария Сидорова (student_id=2)
    (2, 1, 'B', '2022-09-01'), (2, 5, NULL, '2022-09-01'), (2, 9, 'A', '2022-09-01'),
    -- Алексей Козлов (student_id=3)
    (3, 2, 'A', '2021-02-01'), (3, 5, 'A', '2020-09-01'), (3, 3, 'A', '2022-02-01'),
    -- Елена Новикова (student_id=4)
    (4, 1, 'C', '2022-09-01'), (4, 9, 'A', '2022-09-01'), (4, 4, 'B', '2023-02-01'),
    -- Дмитрий Волков (student_id=5)
    (5, 1, 'B', '2021-09-01'), (5, 4, 'B', '2021-09-01'), (5, 7, 'C', '2022-02-01'),
    -- Анна Кузнецова (student_id=6)
    (6, 2, 'A', '2021-02-01'), (6, 5, 'B', '2020-09-01'), (6, 3, 'A', '2021-09-01'),
    -- Сергей Морозов (student_id=7)
    (7, 1, NULL, '2023-09-01'), (7, 9, 'B', '2023-09-01'),
    -- Ольга Васильева (student_id=8)
    (8, 1, 'A', '2021-09-01'), (8, 4, 'A', '2021-09-01'), (8, 6, 'B', '2022-09-01'),
    -- Николай Зайцев (student_id=9) — неактивный, нет записей
    -- Татьяна Лебедева (student_id=10) — новый студент, ещё нет оценок
    (10, 1, NULL, '2023-09-01'), (10, 4, NULL, '2023-09-01'),
    -- Андрей Соколов (student_id=11)
    (11, 7, 'B', '2021-09-01'), (11, 8, 'C', '2022-09-01'),
    -- Екатерина Попова (student_id=12)
    (12, 5, 'A', '2020-09-01'), (12, 6, 'A', '2021-09-01'), (12, 4, 'A', '2020-09-01'),
    -- Михаил Федоров (student_id=13)
    (13, 1, NULL, '2023-09-01'), (13, 3, NULL, '2023-09-01'),
    -- Виктория Орлова (student_id=14)
    (14, 5, 'A', '2021-09-01'), (14, 6, 'A', '2022-02-01'), (14, 4, 'A', '2021-09-01'),
    -- Павел Николаев (student_id=15)
    (15, 7, 'B', '2020-09-01'), (15, 8, 'B', '2021-09-01'),
    -- Юлия Ковалева (student_id=16)
    (16, 9, 'A', '2022-09-01'), (16, 10, 'A', '2023-02-01'),
    -- Артём Егоров (student_id=17) — неактивный
    (17, 1, 'D', '2021-09-01'), (17, 2, 'F', '2022-02-01'),
    -- Светлана Белова (student_id=18)
    (18, 5, NULL, '2023-09-01'), (18, 4, NULL, '2023-09-01'),
    -- Денис Черных (student_id=19)
    (19, 7, 'A', '2020-09-01'), (19, 8, 'A', '2021-09-01'), (19, 1, 'B', '2020-09-01'),
    -- Наталья Громова (student_id=20)
    (20, 9, 'B', '2022-09-01'), (20, 10, NULL, '2023-02-01');

-- ============================================
-- Проверка данных
-- ============================================
SELECT '=== Статистика базы данных ===' AS info;
SELECT 'Факультетов: ' || COUNT(*) FROM departments;
SELECT 'Студентов: ' || COUNT(*) || ' (активных: ' || SUM(is_active) || ')' FROM students;
SELECT 'Курсов: ' || COUNT(*) FROM courses;
SELECT 'Записей на курсы: ' || COUNT(*) FROM enrollments;
SELECT 'Оценок выставлено: ' || COUNT(grade) FROM enrollments;

-- ============================================
-- Примеры запросов для проверки
-- ============================================

-- Распределение студентов по факультетам
SELECT '=== Студенты по факультетам ===' AS info;
SELECT d.dept_name AS "Факультет", COUNT(s.student_id) AS "Студентов"
FROM departments d
LEFT JOIN students s ON d.dept_id = s.dept_id
GROUP BY d.dept_id
ORDER BY COUNT(s.student_id) DESC;

-- Популярность курсов
SELECT '=== Популярность курсов ===' AS info;
SELECT c.course_code, c.course_name, COUNT(e.student_id) AS enrolled
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id
ORDER BY enrolled DESC;
