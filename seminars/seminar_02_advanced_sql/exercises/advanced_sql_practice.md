# Практические задания: Сложные SQL-запросы

## Подготовка

1. Откройте DB Browser for SQLite или консоль sqlite3
2. Загрузите базу данных `university.db` из семинара 1:
   ```bash
   sqlite3 university.db < ../seminar_01_intro_to_sql/data/university.sql
   ```

---

## Часть 1: Логические операторы

### Задание 1.1
Найдите всех активных студентов, поступивших после 2020 года.

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name, enrollment_year
FROM students
WHERE is_active = 1 AND enrollment_year > 2020;
```
</details>

### Задание 1.2
Найдите студентов 2020 или 2023 года поступления.

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name, enrollment_year
FROM students
WHERE enrollment_year = 2020 OR enrollment_year = 2023;
```
</details>

### Задание 1.3
Найдите студентов, которые НЕ поступили в 2021 году.

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name, enrollment_year
FROM students
WHERE NOT enrollment_year = 2021;
-- или
SELECT first_name, last_name, enrollment_year
FROM students
WHERE enrollment_year != 2021;
```
</details>

---

## Часть 2: LIKE, IN, BETWEEN

### Задание 2.1
Найдите всех студентов, чья фамилия заканчивается на "ова".

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name
FROM students
WHERE last_name LIKE '%ова';
```
</details>

### Задание 2.2
Найдите студентов, чей email содержит "university".

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name, email
FROM students
WHERE email LIKE '%university%';
```
</details>

### Задание 2.3
Найдите студентов, поступивших в 2020, 2021 или 2022 году (используйте IN).

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name, enrollment_year
FROM students
WHERE enrollment_year IN (2020, 2021, 2022);
```
</details>

### Задание 2.4
Найдите студентов с GPA от 3.8 до 4.3 включительно.

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name, gpa
FROM students
WHERE gpa BETWEEN 3.8 AND 4.3;
```
</details>

---

## Часть 3: ORDER BY, LIMIT, DISTINCT

### Задание 3.1
Выведите всех студентов, отсортированных по GPA от высшего к низшему.

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name, gpa
FROM students
ORDER BY gpa DESC;
```
</details>

### Задание 3.2
Выведите топ-3 студентов с самым высоким GPA.

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name, gpa
FROM students
ORDER BY gpa DESC
LIMIT 3;
```
</details>

### Задание 3.3
Выведите уникальные годы поступления студентов.

<details>
<summary>Решение</summary>

```sql
SELECT DISTINCT enrollment_year
FROM students
ORDER BY enrollment_year;
```
</details>

### Задание 3.4
Выведите студентов с 4-го по 6-го в рейтинге по GPA.

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name, gpa
FROM students
ORDER BY gpa DESC
LIMIT 3 OFFSET 3;
```
</details>

---

## Часть 4: JOIN

### Задание 4.1
Выведите имена студентов и названия курсов, на которые они записаны (INNER JOIN).

<details>
<summary>Решение</summary>

```sql
SELECT s.first_name, s.last_name, c.course_name
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_id = c.course_id
ORDER BY s.last_name, c.course_name;
```
</details>

### Задание 4.2
Выведите все курсы и количество записавшихся студентов (включая курсы без студентов).

<details>
<summary>Решение</summary>

```sql
SELECT c.course_name, COUNT(e.student_id) AS enrolled
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id
ORDER BY enrolled DESC;
```
</details>

### Задание 4.3
Найдите студентов с их оценками по курсам (только записи с выставленными оценками).

<details>
<summary>Решение</summary>

```sql
SELECT s.first_name, s.last_name, c.course_name, e.grade
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_id = c.course_id
WHERE e.grade IS NOT NULL
ORDER BY s.last_name;
```
</details>

---

## Часть 5: Агрегатные функции

### Задание 5.1
Посчитайте общее количество студентов.

<details>
<summary>Решение</summary>

```sql
SELECT COUNT(*) AS total_students FROM students;
```
</details>

### Задание 5.2
Найдите средний GPA всех активных студентов (округлите до 2 знаков).

<details>
<summary>Решение</summary>

```sql
SELECT ROUND(AVG(gpa), 2) AS avg_gpa
FROM students
WHERE is_active = 1;
```
</details>

### Задание 5.3
Найдите минимальный и максимальный GPA.

<details>
<summary>Решение</summary>

```sql
SELECT MIN(gpa) AS min_gpa, MAX(gpa) AS max_gpa
FROM students;
```
</details>

### Задание 5.4
Посчитайте общее количество кредитов всех курсов.

<details>
<summary>Решение</summary>

```sql
SELECT SUM(credits) AS total_credits FROM courses;
```
</details>

---

## Часть 6: GROUP BY и HAVING

### Задание 6.1
Посчитайте количество студентов по каждому году поступления.

<details>
<summary>Решение</summary>

```sql
SELECT enrollment_year, COUNT(*) AS student_count
FROM students
GROUP BY enrollment_year
ORDER BY enrollment_year;
```
</details>

### Задание 6.2
Найдите средний GPA по каждому году поступления.

<details>
<summary>Решение</summary>

```sql
SELECT enrollment_year, ROUND(AVG(gpa), 2) AS avg_gpa
FROM students
GROUP BY enrollment_year
ORDER BY enrollment_year;
```
</details>

### Задание 6.3
Найдите года, в которые поступило более 2 студентов.

<details>
<summary>Решение</summary>

```sql
SELECT enrollment_year, COUNT(*) AS student_count
FROM students
GROUP BY enrollment_year
HAVING COUNT(*) > 2;
```
</details>

### Задание 6.4
Посчитайте количество курсов у каждого преподавателя.

<details>
<summary>Решение</summary>

```sql
SELECT instructor, COUNT(*) AS course_count
FROM courses
GROUP BY instructor
ORDER BY course_count DESC;
```
</details>

---

## Часть 7: Вложенные запросы

### Задание 7.1
Найдите студентов с GPA выше среднего.

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name, gpa
FROM students
WHERE gpa > (SELECT AVG(gpa) FROM students)
ORDER BY gpa DESC;
```
</details>

### Задание 7.2
Найдите курсы, на которые записан студент "Петров" (используйте подзапрос).

<details>
<summary>Решение</summary>

```sql
SELECT course_name FROM courses
WHERE course_id IN (
    SELECT e.course_id FROM enrollments e
    JOIN students s ON e.student_id = s.student_id
    WHERE s.last_name = 'Петров'
);
```
</details>

### Задание 7.3
Найдите студентов, которые не записаны ни на один курс.

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name
FROM students
WHERE student_id NOT IN (
    SELECT DISTINCT student_id FROM enrollments
);
```
</details>

---

## Бонусные задания

### Задание Б.1
Выведите рейтинг курсов по популярности (количеству записей).

<details>
<summary>Решение</summary>

```sql
SELECT 
    c.course_name,
    c.instructor,
    COUNT(e.student_id) AS enrolled,
    c.max_students,
    ROUND(100.0 * COUNT(e.student_id) / c.max_students, 1) AS fill_percent
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id
ORDER BY enrolled DESC;
```
</details>

### Задание Б.2
Для каждого студента выведите количество курсов и его отклонение от среднего GPA.

<details>
<summary>Решение</summary>

```sql
SELECT 
    s.first_name,
    s.last_name,
    s.gpa,
    (SELECT ROUND(AVG(gpa), 2) FROM students) AS avg_gpa,
    ROUND(s.gpa - (SELECT AVG(gpa) FROM students), 2) AS diff,
    COUNT(e.course_id) AS courses
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id
ORDER BY s.gpa DESC;
```
</details>

### Задание Б.3
Найдите "отличников" — студентов, у которых все оценки 'A'.

<details>
<summary>Решение</summary>

```sql
SELECT s.first_name, s.last_name, COUNT(e.grade) AS courses
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
WHERE e.grade IS NOT NULL
GROUP BY s.student_id
HAVING COUNT(e.grade) = SUM(CASE WHEN e.grade = 'A' THEN 1 ELSE 0 END)
   AND COUNT(e.grade) > 0;
```
</details>
