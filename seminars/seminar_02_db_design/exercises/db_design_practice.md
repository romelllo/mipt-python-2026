# Практические задания: Продвинутый SQL

## Подготовка

1. Откройте DB Browser for SQLite или консоль sqlite3
2. Загрузите расширенную базу данных:
   ```bash
   sqlite3 university.db < data/university_extended.sql
   ```
   Или используйте базу из семинара 1:
   ```bash
   sqlite3 university.db < ../seminar_01_intro_to_sql/data/university.sql
   ```

> **Как работать с заданиями:** прочитайте условие, попробуйте написать запрос самостоятельно, и только после этого раскройте решение для проверки. Не копируйте — пишите сами!

---

## Часть 1: Логические операторы

> **Теория:** [README.md — Блок 1](../README.md#блок-1-логические-операторы) | **Примеры:** [`examples/01_operators_and_filters.sql`](../examples/01_operators_and_filters.sql), раздел 1

### Задание 1.1
Найдите всех активных студентов, поступивших после 2020 года.

<details>
<summary>Подсказка</summary>

Используйте `AND` для объединения двух условий: `is_active = 1` и `enrollment_year > 2020`.
</details>

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
<summary>Подсказка</summary>

Используйте `OR` для проверки двух возможных значений.
</details>

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
<summary>Подсказка</summary>

Используйте `NOT` или оператор `!=` / `<>`.
</details>

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

### Задание 1.4
Найдите активных студентов 2021 или 2022 года поступления с GPA выше 4.0.

<details>
<summary>Подсказка</summary>

Скобки важны! Сначала объедините условия по году в скобках через `OR`, затем добавьте `AND` для GPA и активности.
</details>

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name, enrollment_year, gpa
FROM students
WHERE (enrollment_year = 2021 OR enrollment_year = 2022)
  AND gpa > 4.0
  AND is_active = 1;
```
</details>

---

## Часть 2: LIKE, IN, BETWEEN

> **Теория:** [README.md — Блок 2](../README.md#блок-2-операторы-фильтрации) | **Примеры:** [`examples/01_operators_and_filters.sql`](../examples/01_operators_and_filters.sql), разделы 2-4

### Задание 2.1
Найдите всех студентов, чья фамилия заканчивается на "ова".

<details>
<summary>Подсказка</summary>

Используйте `LIKE` с шаблоном `'%ова'` — символ `%` означает «любое количество любых символов перед».
</details>

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
<summary>Подсказка</summary>

Используйте `LIKE '%university%'` — `%` с обеих сторон означает «в любом месте строки».
</details>

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
<summary>Подсказка</summary>

Оператор `IN` позволяет проверить значение по списку: `WHERE поле IN (значение1, значение2, ...)`.
</details>

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
<summary>Подсказка</summary>

Оператор `BETWEEN` включает обе границы: `WHERE поле BETWEEN нижняя AND верхняя`.
</details>

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name, gpa
FROM students
WHERE gpa BETWEEN 3.8 AND 4.3;
```
</details>

### Задание 2.5
Найдите студентов, чьё имя начинается на букву, вторая буква которого — 'а'.

<details>
<summary>Подсказка</summary>

Символ `_` в `LIKE` означает ровно один символ: `'_а%'`.
</details>

<details>
<summary>Решение</summary>

```sql
SELECT first_name, last_name
FROM students
WHERE first_name LIKE '_а%';
```
</details>

---

## Часть 3: ORDER BY, LIMIT, DISTINCT

> **Теория:** [README.md — Блок 3](../README.md#блок-3-сортировка-и-ограничение) | **Примеры:** [`examples/01_operators_and_filters.sql`](../examples/01_operators_and_filters.sql), разделы 5-7

### Задание 3.1
Выведите всех студентов, отсортированных по GPA от высшего к низшему.

<details>
<summary>Подсказка</summary>

Используйте `ORDER BY gpa DESC` для сортировки по убыванию.
</details>

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
<summary>Подсказка</summary>

Сначала отсортируйте по убыванию GPA, затем ограничьте результат с помощью `LIMIT 3`.
</details>

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
<summary>Подсказка</summary>

Используйте `SELECT DISTINCT` для получения уникальных значений.
</details>

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
<summary>Подсказка</summary>

Используйте `LIMIT` с `OFFSET`: нужно пропустить первые 3 записи (`OFFSET 3`) и взять следующие 3 (`LIMIT 3`).
</details>

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

> **Теория:** [README.md — Блок 4](../README.md#блок-4-join--объединение-таблиц) | **Примеры:** [`examples/02_joins_examples.sql`](../examples/02_joins_examples.sql)

### Задание 4.1
Выведите имена студентов и названия курсов, на которые они записаны (INNER JOIN).

<details>
<summary>Подсказка</summary>

Нужно объединить три таблицы: `students` → `enrollments` → `courses`. Используйте `INNER JOIN` дважды, связывая по `student_id` и `course_id`.
</details>

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
<summary>Подсказка</summary>

Используйте `LEFT JOIN`, чтобы включить курсы без студентов. Агрегируйте с помощью `COUNT()` и `GROUP BY`.
</details>

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
<summary>Подсказка</summary>

Используйте `INNER JOIN` для объединения таблиц и `WHERE e.grade IS NOT NULL` для фильтрации.
</details>

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

### Задание 4.4
Найдите студентов, которые НЕ записаны ни на один курс (используйте LEFT JOIN).

<details>
<summary>Подсказка</summary>

Используйте `LEFT JOIN` и проверьте `WHERE e.enrollment_id IS NULL` — это покажет строки, для которых не нашлось совпадений в enrollments.
</details>

<details>
<summary>Решение</summary>

```sql
SELECT s.first_name, s.last_name, s.email
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
WHERE e.enrollment_id IS NULL;
```
</details>

---

## Часть 5: Агрегатные функции

> **Теория:** [README.md — Блок 5](../README.md#блок-5-агрегатные-функции-и-group-by) | **Примеры:** [`examples/03_aggregation_grouping.sql`](../examples/03_aggregation_grouping.sql), раздел 1

### Задание 5.1
Посчитайте общее количество студентов.

<details>
<summary>Подсказка</summary>

Используйте `COUNT(*)`.
</details>

<details>
<summary>Решение</summary>

```sql
SELECT COUNT(*) AS total_students FROM students;
```
</details>

### Задание 5.2
Найдите средний GPA всех активных студентов (округлите до 2 знаков).

<details>
<summary>Подсказка</summary>

Используйте `ROUND(AVG(gpa), 2)` и `WHERE is_active = 1`.
</details>

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
<summary>Подсказка</summary>

Используйте `MIN()` и `MAX()` в одном запросе.
</details>

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
<summary>Подсказка</summary>

Используйте `SUM(credits)`.
</details>

<details>
<summary>Решение</summary>

```sql
SELECT SUM(credits) AS total_credits FROM courses;
```
</details>

---

## Часть 6: GROUP BY и HAVING

> **Теория:** [README.md — Блок 5](../README.md#блок-5-агрегатные-функции-и-group-by) (GROUP BY) | **Примеры:** [`examples/03_aggregation_grouping.sql`](../examples/03_aggregation_grouping.sql), разделы 2-3

### Задание 6.1
Посчитайте количество студентов по каждому году поступления.

<details>
<summary>Подсказка</summary>

Используйте `GROUP BY enrollment_year` и `COUNT(*)`.
</details>

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
<summary>Подсказка</summary>

Используйте `HAVING` для фильтрации групп (после `GROUP BY`). `WHERE` фильтрует строки до группировки, а `HAVING` — после.
</details>

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

> **Теория:** [README.md — Блок 6](../README.md#блок-6-вложенные-запросы-подзапросы) | **Примеры:** [`examples/03_aggregation_grouping.sql`](../examples/03_aggregation_grouping.sql), раздел 5

### Задание 7.1
Найдите студентов с GPA выше среднего.

<details>
<summary>Подсказка</summary>

Используйте подзапрос `(SELECT AVG(gpa) FROM students)` в условии `WHERE`.
</details>

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
<summary>Подсказка</summary>

Внутренний запрос находит `course_id` через `enrollments` и `students`, а внешний запрос выбирает курсы по этим `course_id`.
</details>

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
<summary>Подсказка</summary>

Используйте `NOT IN` с подзапросом, который возвращает все `student_id` из `enrollments`.
</details>

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

### Задание 7.4
Для каждого студента выведите его GPA и отклонение от среднего GPA.

<details>
<summary>Подсказка</summary>

Используйте скалярный подзапрос в `SELECT` для получения среднего GPA, затем вычислите разницу.
</details>

<details>
<summary>Решение</summary>

```sql
SELECT 
    first_name,
    last_name,
    gpa,
    (SELECT ROUND(AVG(gpa), 2) FROM students) AS avg_gpa,
    ROUND(gpa - (SELECT AVG(gpa) FROM students), 2) AS diff_from_avg
FROM students
ORDER BY gpa DESC;
```
</details>

---

## Бонусные задания

Эти задания объединяют несколько тем. Попробуйте решить их самостоятельно!

### Задание Б.1
Выведите рейтинг курсов по популярности (количеству записей), включая процент заполнения.

<details>
<summary>Подсказка</summary>

Используйте `LEFT JOIN` + `COUNT()` + `GROUP BY`. Для процента: `100.0 * COUNT(...) / max_students`.
</details>

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
<summary>Подсказка</summary>

Используйте `HAVING` с `COUNT(grade)` и `SUM(CASE WHEN grade = 'A' THEN 1 ELSE 0 END)` — если они равны, значит все оценки 'A'.
</details>

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

### Задание Б.4
Выведите статистику по факультетам: количество студентов, средний GPA, количество курсов.

<details>
<summary>Подсказка</summary>

Эта задача требует расширенной БД (`university_extended.sql`). Используйте `LEFT JOIN` с таблицей `departments`.
</details>

<details>
<summary>Решение</summary>

```sql
SELECT 
    d.dept_name AS "Факультет",
    COUNT(DISTINCT s.student_id) AS "Студентов",
    ROUND(AVG(s.gpa), 2) AS "Средний GPA",
    COUNT(DISTINCT c.course_id) AS "Курсов"
FROM departments d
LEFT JOIN students s ON d.dept_id = s.dept_id
LEFT JOIN courses c ON d.dept_id = c.dept_id
GROUP BY d.dept_id
ORDER BY COUNT(DISTINCT s.student_id) DESC;
```
</details>
