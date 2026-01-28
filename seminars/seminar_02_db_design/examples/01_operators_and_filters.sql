-- ============================================
-- Семинар 2: Логические операторы и фильтрация
-- ============================================
-- Используйте БД university из семинара 1
-- или выполните data/university.sql

-- ============================================
-- 1. Логические операторы: AND, OR, NOT
-- ============================================

-- AND: все условия должны быть истинны
-- Активные студенты 2021 года
SELECT first_name, last_name, enrollment_year, is_active
FROM students
WHERE enrollment_year = 2021 AND is_active = 1;

-- OR: хотя бы одно условие истинно
-- Студенты 2020 или 2022 года
SELECT first_name, last_name, enrollment_year
FROM students
WHERE enrollment_year = 2020 OR enrollment_year = 2022;

-- NOT: отрицание
-- Неактивные студенты
SELECT first_name, last_name, is_active
FROM students
WHERE NOT is_active = 1;
-- Или эквивалентно:
SELECT first_name, last_name, is_active
FROM students
WHERE is_active != 1;

-- Комбинация операторов (скобки важны!)
-- Активные студенты 2021 или 2022 года с GPA > 4.0
SELECT first_name, last_name, enrollment_year, gpa
FROM students
WHERE (enrollment_year = 2021 OR enrollment_year = 2022) 
  AND gpa > 4.0 
  AND is_active = 1;


-- ============================================
-- 2. LIKE — поиск по шаблону
-- ============================================
-- % — любое количество любых символов (включая 0)
-- _ — ровно один любой символ

-- Фамилии, начинающиеся на 'К'
SELECT first_name, last_name
FROM students
WHERE last_name LIKE 'К%';

-- Фамилии, заканчивающиеся на 'ова'
SELECT first_name, last_name
FROM students
WHERE last_name LIKE '%ова';

-- Email, содержащий 'ov'
SELECT first_name, last_name, email
FROM students
WHERE email LIKE '%ov%';

-- Имена ровно из 5 символов
SELECT first_name, last_name
FROM students
WHERE first_name LIKE '_____';

-- Имена, где вторая буква 'а'
SELECT first_name, last_name
FROM students
WHERE first_name LIKE '_а%';


-- ============================================
-- 3. IN — проверка вхождения в список
-- ============================================

-- Студенты определённых годов
SELECT first_name, last_name, enrollment_year
FROM students
WHERE enrollment_year IN (2020, 2021, 2022);

-- Эквивалентно (но IN короче и читабельнее):
SELECT first_name, last_name, enrollment_year
FROM students
WHERE enrollment_year = 2020 
   OR enrollment_year = 2021 
   OR enrollment_year = 2022;

-- Курсы определённых преподавателей
SELECT course_name, instructor
FROM courses
WHERE instructor IN ('Проф. Смирнов', 'Доц. Орлов');

-- NOT IN — исключение из списка
SELECT first_name, last_name, enrollment_year
FROM students
WHERE enrollment_year NOT IN (2019, 2023);


-- ============================================
-- 4. BETWEEN — диапазон значений
-- ============================================

-- GPA от 3.5 до 4.5 (включительно!)
SELECT first_name, last_name, gpa
FROM students
WHERE gpa BETWEEN 3.5 AND 4.5;

-- Эквивалентно:
SELECT first_name, last_name, gpa
FROM students
WHERE gpa >= 3.5 AND gpa <= 4.5;

-- Студенты, поступившие с 2020 по 2022 год
SELECT first_name, last_name, enrollment_year
FROM students
WHERE enrollment_year BETWEEN 2020 AND 2022;

-- NOT BETWEEN — вне диапазона
SELECT first_name, last_name, gpa
FROM students
WHERE gpa NOT BETWEEN 3.0 AND 4.0;


-- ============================================
-- 5. ORDER BY — сортировка
-- ============================================

-- По возрастанию (ASC — по умолчанию)
SELECT first_name, last_name, gpa
FROM students
ORDER BY gpa ASC;

-- По убыванию
SELECT first_name, last_name, gpa
FROM students
ORDER BY gpa DESC;

-- По нескольким полям
-- Сначала по году (возр.), потом по GPA (убыв.)
SELECT first_name, last_name, enrollment_year, gpa
FROM students
ORDER BY enrollment_year ASC, gpa DESC;

-- Можно сортировать по номеру столбца
SELECT first_name, last_name, gpa
FROM students
ORDER BY 3 DESC;  -- 3-й столбец = gpa


-- ============================================
-- 6. LIMIT и OFFSET — ограничение результатов
-- ============================================

-- Топ-5 студентов по GPA
SELECT first_name, last_name, gpa
FROM students
ORDER BY gpa DESC
LIMIT 5;

-- Пагинация: страница 2 (записи 6-10)
SELECT first_name, last_name, gpa
FROM students
ORDER BY gpa DESC
LIMIT 5 OFFSET 5;

-- Или альтернативный синтаксис
SELECT first_name, last_name, gpa
FROM students
ORDER BY gpa DESC
LIMIT 5, 5;  -- LIMIT offset, count


-- ============================================
-- 7. DISTINCT — уникальные значения
-- ============================================

-- Уникальные годы поступления
SELECT DISTINCT enrollment_year
FROM students
ORDER BY enrollment_year;

-- Уникальные преподаватели
SELECT DISTINCT instructor
FROM courses;

-- Уникальные комбинации
SELECT DISTINCT enrollment_year, is_active
FROM students
ORDER BY enrollment_year;

-- Количество уникальных годов
SELECT COUNT(DISTINCT enrollment_year) AS unique_years
FROM students;


-- ============================================
-- 8. Комбинирование операторов
-- ============================================

-- Сложный запрос: активные студенты 2020-2022 годов
-- с GPA от 4.0 до 5.0, отсортированные по GPA
SELECT first_name, last_name, enrollment_year, gpa
FROM students
WHERE is_active = 1
  AND enrollment_year BETWEEN 2020 AND 2022
  AND gpa BETWEEN 4.0 AND 5.0
ORDER BY gpa DESC
LIMIT 10;
