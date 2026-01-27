-- ============================================
-- Семинар 2: Агрегатные функции и GROUP BY
-- ============================================
-- Используйте БД university из семинара 1

-- ============================================
-- 1. Агрегатные функции
-- ============================================

-- COUNT — количество записей
SELECT COUNT(*) AS total_students FROM students;

-- COUNT с условием
SELECT COUNT(*) AS active_students 
FROM students 
WHERE is_active = 1;

-- COUNT(column) — не считает NULL
SELECT COUNT(grade) AS graded_enrollments FROM enrollments;
SELECT COUNT(*) AS total_enrollments FROM enrollments;

-- SUM — сумма
SELECT SUM(credits) AS total_credits FROM courses;

-- AVG — среднее
SELECT AVG(gpa) AS average_gpa FROM students;

-- MIN и MAX
SELECT MIN(gpa) AS min_gpa, MAX(gpa) AS max_gpa FROM students;

-- ROUND — округление
SELECT ROUND(AVG(gpa), 2) AS avg_gpa_rounded FROM students;

-- Комбинация функций в одном запросе
SELECT 
    COUNT(*) AS total,
    ROUND(AVG(gpa), 2) AS avg_gpa,
    ROUND(MIN(gpa), 2) AS min_gpa,
    ROUND(MAX(gpa), 2) AS max_gpa,
    ROUND(MAX(gpa) - MIN(gpa), 2) AS gpa_range
FROM students
WHERE is_active = 1;


-- ============================================
-- 2. GROUP BY — группировка
-- ============================================

-- Количество студентов по годам поступления
SELECT enrollment_year, COUNT(*) AS student_count
FROM students
GROUP BY enrollment_year
ORDER BY enrollment_year;

-- Средний GPA по годам
SELECT enrollment_year, ROUND(AVG(gpa), 2) AS avg_gpa
FROM students
GROUP BY enrollment_year
ORDER BY enrollment_year;

-- Количество курсов по преподавателям
SELECT instructor, COUNT(*) AS course_count
FROM courses
GROUP BY instructor
ORDER BY course_count DESC;

-- Сумма кредитов по преподавателям
SELECT instructor, SUM(credits) AS total_credits
FROM courses
GROUP BY instructor;

-- Группировка по нескольким полям
SELECT enrollment_year, is_active, COUNT(*) AS count
FROM students
GROUP BY enrollment_year, is_active
ORDER BY enrollment_year, is_active;


-- ============================================
-- 3. HAVING — фильтрация групп
-- ============================================
-- WHERE фильтрует ДО группировки
-- HAVING фильтрует ПОСЛЕ группировки

-- Годы с более чем 2 студентами
SELECT enrollment_year, COUNT(*) AS student_count
FROM students
GROUP BY enrollment_year
HAVING COUNT(*) > 2
ORDER BY enrollment_year;

-- Преподаватели с суммой кредитов > 5
SELECT instructor, SUM(credits) AS total_credits
FROM courses
GROUP BY instructor
HAVING SUM(credits) > 5;

-- Комбинация WHERE и HAVING
-- Активные студенты, группированные по годам,
-- только годы со средним GPA > 4.0
SELECT enrollment_year, ROUND(AVG(gpa), 2) AS avg_gpa
FROM students
WHERE is_active = 1
GROUP BY enrollment_year
HAVING AVG(gpa) > 4.0
ORDER BY avg_gpa DESC;


-- ============================================
-- 4. Агрегация с JOIN
-- ============================================

-- Количество записей на каждый курс
SELECT c.course_name, COUNT(e.student_id) AS enrolled
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id
ORDER BY enrolled DESC;

-- Количество курсов у каждого студента
SELECT s.first_name, s.last_name, COUNT(e.course_id) AS courses
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id
ORDER BY courses DESC;

-- Средняя оценка по курсам (числовой эквивалент)
SELECT 
    c.course_name,
    COUNT(e.grade) AS graded,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 5
            WHEN 'B' THEN 4
            WHEN 'C' THEN 3
            WHEN 'D' THEN 2
            WHEN 'F' THEN 1
        END
    ), 2) AS avg_grade
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
WHERE e.grade IS NOT NULL
GROUP BY c.course_id
ORDER BY avg_grade DESC;


-- ============================================
-- 5. Вложенные запросы (подзапросы)
-- ============================================

-- Студенты с GPA выше среднего
SELECT first_name, last_name, gpa
FROM students
WHERE gpa > (SELECT AVG(gpa) FROM students)
ORDER BY gpa DESC;

-- Курсы, на которые записан конкретный студент
SELECT course_name FROM courses
WHERE course_id IN (
    SELECT course_id FROM enrollments WHERE student_id = 1
);

-- Студенты, НЕ записанные ни на один курс
SELECT first_name, last_name FROM students
WHERE student_id NOT IN (
    SELECT DISTINCT student_id FROM enrollments
);

-- Подзапрос в SELECT (скалярный подзапрос)
SELECT 
    first_name,
    last_name,
    gpa,
    (SELECT ROUND(AVG(gpa), 2) FROM students) AS avg_gpa,
    ROUND(gpa - (SELECT AVG(gpa) FROM students), 2) AS diff_from_avg
FROM students
ORDER BY gpa DESC;

-- Подзапрос в FROM (производная таблица)
SELECT enrollment_year, avg_gpa
FROM (
    SELECT enrollment_year, ROUND(AVG(gpa), 2) AS avg_gpa
    FROM students
    GROUP BY enrollment_year
) AS year_stats
WHERE avg_gpa > 4.0;


-- ============================================
-- 6. Практические примеры
-- ============================================

-- Топ-3 курса по популярности
SELECT c.course_name, COUNT(e.student_id) AS students
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id
ORDER BY students DESC
LIMIT 3;

-- Статистика по каждому году поступления
SELECT 
    enrollment_year,
    COUNT(*) AS total,
    SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) AS active,
    SUM(CASE WHEN is_active = 0 THEN 1 ELSE 0 END) AS inactive,
    ROUND(AVG(gpa), 2) AS avg_gpa
FROM students
GROUP BY enrollment_year
ORDER BY enrollment_year;

-- Отличники (все оценки 'A')
SELECT s.first_name, s.last_name, COUNT(e.grade) AS courses_completed
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
WHERE e.grade IS NOT NULL
GROUP BY s.student_id
HAVING COUNT(e.grade) = SUM(CASE WHEN e.grade = 'A' THEN 1 ELSE 0 END)
   AND COUNT(e.grade) > 0;
