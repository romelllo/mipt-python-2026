-- ============================================
-- Семинар 1: Базовые запросы (SELECT, UPDATE, DELETE)
-- ============================================
-- Выполните этот файл ПОСЛЕ 01_create_tables.sql и 02_insert_data.sql
-- Запускайте запросы по одному для изучения результатов

-- ============================================
-- 1. SELECT — выборка данных
-- ============================================

-- Получить ВСЕ данные из таблицы (все столбцы, все строки)
SELECT * FROM students;

-- Получить только определённые столбцы
SELECT first_name, last_name, email FROM students;

-- Получить столбцы с псевдонимами (AS)
SELECT 
    first_name AS имя, 
    last_name AS фамилия, 
    gpa AS средний_балл 
FROM students;


-- ============================================
-- 2. WHERE — фильтрация по условию
-- ============================================

-- Студенты определённого года поступления
SELECT first_name, last_name, enrollment_year 
FROM students 
WHERE enrollment_year = 2021;

-- Студенты с GPA выше 4.0
SELECT first_name, last_name, gpa 
FROM students 
WHERE gpa > 4.0;

-- Только активные студенты
SELECT first_name, last_name, is_active 
FROM students 
WHERE is_active = 1;

-- Неактивные (отчисленные) студенты
SELECT first_name, last_name 
FROM students 
WHERE is_active = 0;


-- ============================================
-- 3. Операторы сравнения
-- ============================================
-- =   равно
-- <>  или !=  не равно
-- >   больше
-- <   меньше
-- >=  больше или равно
-- <=  меньше или равно

-- Студенты, поступившие НЕ в 2021 году
SELECT first_name, last_name, enrollment_year 
FROM students 
WHERE enrollment_year <> 2021;

-- Студенты с GPA от 4.0 и выше
SELECT first_name, last_name, gpa 
FROM students 
WHERE gpa >= 4.0;


-- ============================================
-- 4. UPDATE — обновление данных
-- ============================================

-- Обновить GPA для конкретного студента
UPDATE students 
SET gpa = 4.3 
WHERE student_id = 2;

-- Проверим изменение
SELECT first_name, last_name, gpa FROM students WHERE student_id = 2;

-- Обновить несколько полей одновременно
UPDATE students 
SET gpa = 3.9, is_active = 1 
WHERE student_id = 9;

-- Проверим
SELECT first_name, last_name, gpa, is_active FROM students WHERE student_id = 9;

-- ⚠️ ВАЖНО: Всегда используйте WHERE при UPDATE!
-- Без WHERE обновятся ВСЕ записи:
-- UPDATE students SET is_active = 0;  -- сделает ВСЕХ неактивными!


-- ============================================
-- 5. DELETE — удаление данных
-- ============================================

-- Сначала посмотрим, сколько записей будет затронуто
SELECT * FROM students WHERE student_id = 10;

-- Удалить конкретную запись
DELETE FROM students WHERE student_id = 10;

-- Проверим, что запись удалена
SELECT * FROM students WHERE student_id = 10;  -- пусто

-- Посмотрим оставшихся студентов
SELECT student_id, first_name, last_name FROM students;

-- ⚠️ ВАЖНО: Всегда используйте WHERE при DELETE!
-- Без WHERE удалятся ВСЕ записи:
-- DELETE FROM students;  -- удалит ВСЕХ студентов!


-- ============================================
-- 6. ALTER TABLE — изменение структуры таблицы
-- ============================================

-- Добавить новый столбец
ALTER TABLE students ADD COLUMN phone TEXT;

-- Проверим структуру таблицы
-- В консоли: .schema students

-- Посмотрим данные (phone будет NULL у существующих записей)
SELECT first_name, last_name, phone FROM students;

-- Заполним телефон для одного студента
UPDATE students SET phone = '+7-999-123-4567' WHERE student_id = 1;

-- Проверим
SELECT first_name, last_name, phone FROM students WHERE student_id = 1;


-- ============================================
-- 7. Полезные приёмы
-- ============================================

-- Подсчитать количество записей
SELECT COUNT(*) FROM students;

-- Подсчитать только активных
SELECT COUNT(*) FROM students WHERE is_active = 1;

-- Проверка на NULL (IS NULL, IS NOT NULL)
SELECT first_name, last_name, phone 
FROM students 
WHERE phone IS NULL;

SELECT first_name, last_name, phone 
FROM students 
WHERE phone IS NOT NULL;
