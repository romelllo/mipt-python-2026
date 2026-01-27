-- ============================================
-- Семинар 2: Примеры всех типов JOIN
-- ============================================
-- Используйте БД university из семинара 1
-- или выполните: sqlite3 university.db < ../seminar_01_intro_to_sql/data/university.sql

-- ============================================
-- Схема базы данных university:
-- ============================================
-- students:     student_id, first_name, last_name, email, birth_date, enrollment_year, gpa, is_active
-- courses:      course_id, course_code, course_name, credits, instructor, max_students
-- enrollments:  enrollment_id, student_id, course_id, grade, enrollment_date
--
-- Связи:
-- students (1) ←── (N) enrollments (N) ──→ (1) courses

-- ============================================
-- 1. INNER JOIN — только совпадающие записи
-- ============================================
-- Возвращает строки, где есть совпадение в обеих таблицах
-- Студенты без записей на курсы НЕ попадут в результат

-- Студенты и их курсы (только те, кто записан)
SELECT 
    s.first_name || ' ' || s.last_name AS "Студент",
    c.course_name AS "Курс",
    e.grade AS "Оценка"
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_id = c.course_id
ORDER BY s.last_name, c.course_name;

-- Результат (пример):
-- +------------------+---------------------------+--------+
-- | Студент          | Курс                      | Оценка |
-- +------------------+---------------------------+--------+
-- | Ольга Васильева  | Введение в программирование| A     |
-- | Ольга Васильева  | Линейная алгебра          | A      |
-- | Дмитрий Волков   | Введение в программирование| B     |
-- | ...              | ...                       | ...    |
-- +------------------+---------------------------+--------+


-- ============================================
-- 2. LEFT JOIN — все из левой + совпадения из правой
-- ============================================
-- Все студенты, даже те, кто не записан ни на один курс

SELECT 
    s.first_name || ' ' || s.last_name AS "Студент",
    s.enrollment_year AS "Год поступления",
    COALESCE(c.course_name, 'Не записан на курсы') AS "Курс"
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
LEFT JOIN courses c ON e.course_id = c.course_id
ORDER BY s.last_name;

-- Результат: все студенты (включая Николая Зайцева, который не записан ни на один курс)


-- ============================================
-- 3. LEFT JOIN — найти записи БЕЗ совпадений
-- ============================================
-- Студенты, которые НЕ записаны ни на один курс

SELECT 
    s.first_name || ' ' || s.last_name AS "Студент без курсов",
    s.email
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
WHERE e.enrollment_id IS NULL;

-- Результат:
-- +-------------------+------------------------+
-- | Студент без курсов| email                  |
-- +-------------------+------------------------+
-- | Николай Зайцев    | zaytsev@university.ru  |
-- | Татьяна Лебедева  | lebedeva@university.ru |
-- +-------------------+------------------------+


-- ============================================
-- 4. LEFT JOIN — все курсы с количеством студентов
-- ============================================
-- Все курсы, включая те, на которые никто не записан

SELECT 
    c.course_code AS "Код",
    c.course_name AS "Курс",
    c.instructor AS "Преподаватель",
    COUNT(e.student_id) AS "Записано",
    c.max_students AS "Макс.",
    ROUND(100.0 * COUNT(e.student_id) / c.max_students, 1) || '%' AS "Заполнение"
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id
ORDER BY COUNT(e.student_id) DESC;

-- Результат:
-- +--------+-----------------------------+---------------+---------+------+------------+
-- | Код    | Курс                        | Преподаватель | Записано| Макс.| Заполнение |
-- +--------+-----------------------------+---------------+---------+------+------------+
-- | CS101  | Введение в программирование | Проф. Смирнов | 6       | 50   | 12.0%      |
-- | MATH101| Линейная алгебра            | Доц. Орлов    | 3       | 60   | 5.0%       |
-- | ...    | ...                         | ...           | ...     | ...  | ...        |
-- +--------+-----------------------------+---------------+---------+------+------------+


-- ============================================
-- 5. RIGHT JOIN (эмуляция в SQLite)
-- ============================================
-- SQLite не поддерживает RIGHT JOIN напрямую
-- Решение: переставить таблицы местами и использовать LEFT JOIN
--
-- Вместо:  A RIGHT JOIN B ON ...
-- Пишем:   B LEFT JOIN A ON ...

-- Все курсы с информацией о студентах (эквивалент RIGHT JOIN)
SELECT 
    c.course_name AS "Курс",
    COALESCE(s.first_name || ' ' || s.last_name, 'Нет записей') AS "Студент"
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
LEFT JOIN students s ON e.student_id = s.student_id
ORDER BY c.course_name;


-- ============================================
-- 6. FULL OUTER JOIN (эмуляция в SQLite)
-- ============================================
-- SQLite не поддерживает FULL OUTER JOIN напрямую
-- Эмулируем через UNION двух LEFT JOIN

-- Все студенты и все курсы (включая несвязанные)
SELECT 
    s.first_name || ' ' || s.last_name AS student,
    c.course_name
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
LEFT JOIN courses c ON e.course_id = c.course_id

UNION

SELECT 
    s.first_name || ' ' || s.last_name,
    c.course_name
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
LEFT JOIN students s ON e.student_id = s.student_id;


-- ============================================
-- 7. CROSS JOIN — декартово произведение
-- ============================================
-- Все возможные комбинации (используйте осторожно!)
-- Если в students 10 записей и в courses 6 записей,
-- CROSS JOIN вернёт 10 × 6 = 60 строк

-- Пример: все возможные комбинации студент-курс
SELECT 
    s.first_name || ' ' || s.last_name AS student,
    c.course_name
FROM students s
CROSS JOIN courses c
WHERE s.is_active = 1
LIMIT 10;  -- Ограничиваем для примера

-- Практическое применение: генерация расписания, тестовых данных


-- ============================================
-- 8. SELF JOIN — соединение таблицы с самой собой
-- ============================================
-- Пример: найти студентов из одного года поступления

SELECT 
    s1.first_name || ' ' || s1.last_name AS "Студент 1",
    s2.first_name || ' ' || s2.last_name AS "Студент 2",
    s1.enrollment_year AS "Год поступления"
FROM students s1
INNER JOIN students s2 ON s1.enrollment_year = s2.enrollment_year 
    AND s1.student_id < s2.student_id  -- Избегаем дубликатов и пар с самим собой
ORDER BY s1.enrollment_year, s1.last_name;

-- Результат: пары студентов, поступивших в один год
-- +------------------+------------------+-----------------+
-- | Студент 1        | Студент 2        | Год поступления |
-- +------------------+------------------+-----------------+
-- | Алексей Козлов   | Анна Кузнецова   | 2020            |
-- | Иван Петров      | Дмитрий Волков   | 2021            |
-- | Иван Петров      | Ольга Васильева  | 2021            |
-- | Дмитрий Волков   | Ольга Васильева  | 2021            |
-- | Мария Сидорова   | Елена Новикова   | 2022            |
-- | Сергей Морозов   | Татьяна Лебедева | 2023            |
-- +------------------+------------------+-----------------+


-- ============================================
-- 9. Множественные JOIN — сложные запросы
-- ============================================

-- Полный отчёт: студенты, их курсы, оценки и преподаватели
SELECT 
    s.first_name || ' ' || s.last_name AS "Студент",
    s.gpa AS "GPA",
    c.course_code AS "Код курса",
    c.course_name AS "Курс",
    c.instructor AS "Преподаватель",
    COALESCE(e.grade, 'Нет оценки') AS "Оценка"
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_id = c.course_id
WHERE s.is_active = 1
ORDER BY s.last_name, c.course_code;


-- ============================================
-- 10. JOIN с агрегацией
-- ============================================

-- Количество курсов у каждого студента
SELECT 
    s.first_name || ' ' || s.last_name AS "Студент",
    s.gpa AS "GPA",
    COUNT(e.course_id) AS "Кол-во курсов",
    COALESCE(GROUP_CONCAT(c.course_code, ', '), 'Нет курсов') AS "Курсы"
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
LEFT JOIN courses c ON e.course_id = c.course_id
GROUP BY s.student_id
ORDER BY COUNT(e.course_id) DESC;

-- Результат:
-- +------------------+-----+---------------+----------------------+
-- | Студент          | GPA | Кол-во курсов | Курсы                |
-- +------------------+-----+---------------+----------------------+
-- | Иван Петров      | 4.2 | 3             | CS101, MATH101, PHYS101|
-- | Дмитрий Волков   | 4.0 | 3             | CS101, MATH101, PHYS101|
-- | Ольга Васильева  | 4.1 | 2             | CS101, MATH101       |
-- | ...              | ... | ...           | ...                  |
-- | Николай Зайцев   | 3.2 | 0             | Нет курсов           |
-- +------------------+-----+---------------+----------------------+


-- ============================================
-- 11. JOIN с подзапросом
-- ============================================

-- Студенты, записанные на курсы профессора Смирнова
SELECT DISTINCT
    s.first_name || ' ' || s.last_name AS "Студент",
    s.email
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_id = c.course_id
WHERE c.instructor = 'Проф. Смирнов'
ORDER BY s.last_name;


-- Студенты с количеством курсов выше среднего
SELECT 
    s.first_name || ' ' || s.last_name AS "Студент",
    COUNT(e.course_id) AS "Курсов"
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id
HAVING COUNT(e.course_id) > (
    SELECT AVG(course_count) FROM (
        SELECT COUNT(*) AS course_count 
        FROM enrollments 
        GROUP BY student_id
    )
)
ORDER BY COUNT(e.course_id) DESC;


-- ============================================
-- 12. Практические задачи с JOIN
-- ============================================

-- Задача 1: Отличники — студенты, у которых все оценки 'A'
SELECT 
    s.first_name || ' ' || s.last_name AS "Отличник",
    s.gpa AS "GPA",
    COUNT(e.grade) AS "Курсов с оценкой"
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
WHERE e.grade IS NOT NULL
GROUP BY s.student_id
HAVING COUNT(e.grade) = SUM(CASE WHEN e.grade = 'A' THEN 1 ELSE 0 END)
   AND COUNT(e.grade) > 0
ORDER BY s.gpa DESC;


-- Задача 2: Курсы с указанием среднего GPA записавшихся студентов
SELECT 
    c.course_name AS "Курс",
    c.instructor AS "Преподаватель",
    COUNT(e.student_id) AS "Студентов",
    ROUND(AVG(s.gpa), 2) AS "Средний GPA студентов"
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
LEFT JOIN students s ON e.student_id = s.student_id
GROUP BY c.course_id
ORDER BY AVG(s.gpa) DESC NULLS LAST;


-- Задача 3: Преподаватели и статистика по их курсам
SELECT 
    c.instructor AS "Преподаватель",
    COUNT(DISTINCT c.course_id) AS "Курсов",
    SUM(c.credits) AS "Всего кредитов",
    COUNT(DISTINCT e.student_id) AS "Уникальных студентов"
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.instructor
ORDER BY COUNT(DISTINCT e.student_id) DESC;
