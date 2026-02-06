# Семинар 2: Проектирование базы данных

**Модуль:** 2 — Объектно-ориентированное программирование и основы работы с базами данных в Python  
**Дата:** 09.02.2026  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1OAlcbabylfiYCLEjZvn-f_VpJAkVWH2LyauaY4LTH5I/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:
- Использовать логические операторы (AND, OR, NOT)
- Применять операторы LIKE, IN, BETWEEN для фильтрации
- Сортировать и ограничивать результаты (ORDER BY, LIMIT)
- Использовать DISTINCT для уникальных значений
- Объединять таблицы с помощью JOIN
- Применять агрегатные функции (COUNT, SUM, AVG, MIN, MAX, ROUND)
- Группировать данные с помощью GROUP BY
- Писать вложенные запросы (подзапросы)
- Понимать принципы нормализации баз данных

---

## Подготовка

Перед началом работы загрузите расширенную базу данных:

```bash
sqlite3 university.db < data/university_extended.sql
```

Или, если вы используете базу из семинара 1:

```bash
sqlite3 university.db < ../seminar_01_intro_to_sql/data/university.sql
```

---

## План семинара

Семинар построен по принципу **«теория → практика»**: после каждого тематического блока вы переходите к упражнениям по этой теме в файле [`exercises/db_design_practice.md`](exercises/db_design_practice.md).

| Время | Тема | Практика |
|-------|------|----------|
| 5 мин | Повторение SELECT, знакомство с темами семинара | — |
| 10 мин | Блок 1: Логические операторы (AND, OR, NOT) | → Упражнения: Часть 1 |
| 10 мин | Блок 2: Операторы фильтрации (LIKE, IN, BETWEEN) | → Упражнения: Часть 2 |
| 10 мин | Блок 3: Сортировка и ограничение (ORDER BY, LIMIT, DISTINCT) | → Упражнения: Часть 3 |
| 20 мин | Блок 4: JOIN — объединение таблиц | → Упражнения: Часть 4 |
| 15 мин | Блок 5: Агрегатные функции и GROUP BY | → Упражнения: Часть 5-6 |
| 10 мин | Блок 6: Вложенные запросы (подзапросы) | → Упражнения: Часть 7 |
| 10 мин | Блок 7: Нормализация (1NF, 2NF, 3NF) | — |

---

## Блок 1: Логические операторы

Логические операторы позволяют комбинировать несколько условий в WHERE.

```sql
-- AND: все условия должны быть истинны
SELECT * FROM students
WHERE enrollment_year = 2021 AND gpa >= 4.0;

-- OR: хотя бы одно условие истинно
SELECT * FROM students
WHERE enrollment_year = 2020 OR enrollment_year = 2022;

-- NOT: отрицание условия
SELECT * FROM students
WHERE NOT is_active = 1;

-- Комбинация (скобки важны для приоритета!)
SELECT * FROM students
WHERE (enrollment_year = 2021 OR enrollment_year = 2022) AND gpa > 4.0;
```

> **Подробнее:** см. файл [`examples/01_operators_and_filters.sql`](examples/01_operators_and_filters.sql), раздел 1.

### Практика

Перейдите к файлу [`exercises/db_design_practice.md`](exercises/db_design_practice.md) и выполните **Часть 1: Логические операторы** (задания 1.1–1.4).

Попробуйте решить каждое задание самостоятельно, прежде чем раскрывать решение!

---

## Блок 2: Операторы фильтрации

### LIKE — поиск по шаблону
```sql
-- % — любое количество символов
-- _ — ровно один символ

-- Фамилии, начинающиеся на 'К'
SELECT * FROM students WHERE last_name LIKE 'К%';

-- Email, содержащий 'ov'
SELECT * FROM students WHERE email LIKE '%ov%';

-- Имена из 5 букв
SELECT * FROM students WHERE first_name LIKE '_____';
```

### IN — проверка вхождения в список
```sql
-- Студенты 2020, 2021 или 2022 года
SELECT * FROM students
WHERE enrollment_year IN (2020, 2021, 2022);

-- Эквивалентно:
SELECT * FROM students
WHERE enrollment_year = 2020
   OR enrollment_year = 2021
   OR enrollment_year = 2022;
```

### BETWEEN — диапазон значений
```sql
-- GPA от 3.5 до 4.5 включительно
SELECT * FROM students
WHERE gpa BETWEEN 3.5 AND 4.5;

-- Эквивалентно:
SELECT * FROM students
WHERE gpa >= 3.5 AND gpa <= 4.5;
```

> **Подробнее:** см. файл [`examples/01_operators_and_filters.sql`](examples/01_operators_and_filters.sql), разделы 2-4.

### Практика

Перейдите к файлу [`exercises/db_design_practice.md`](exercises/db_design_practice.md) и выполните **Часть 2: LIKE, IN, BETWEEN** (задания 2.1–2.5).

---

## Блок 3: Сортировка и ограничение

### ORDER BY — сортировка
```sql
-- По возрастанию (ASC — по умолчанию)
SELECT * FROM students ORDER BY gpa;

-- По убыванию
SELECT * FROM students ORDER BY gpa DESC;

-- По нескольким полям
SELECT * FROM students
ORDER BY enrollment_year ASC, gpa DESC;
```

### LIMIT — ограничение количества строк
```sql
-- Топ-5 студентов по GPA
SELECT first_name, last_name, gpa
FROM students
ORDER BY gpa DESC
LIMIT 5;

-- Пагинация: пропустить 5, взять следующие 5
SELECT * FROM students
ORDER BY student_id
LIMIT 5 OFFSET 5;
```

### DISTINCT — уникальные значения
```sql
-- Уникальные годы поступления
SELECT DISTINCT enrollment_year FROM students;

-- Уникальные комбинации год + активность
SELECT DISTINCT enrollment_year, is_active FROM students;
```

> **Подробнее:** см. файл [`examples/01_operators_and_filters.sql`](examples/01_operators_and_filters.sql), разделы 5-7.

### Практика

Перейдите к файлу [`exercises/db_design_practice.md`](exercises/db_design_practice.md) и выполните **Часть 3: ORDER BY, LIMIT, DISTINCT** (задания 3.1–3.4).

---

## Блок 4: JOIN — объединение таблиц

JOIN позволяет объединять данные из нескольких таблиц по связующим ключам.

```
Таблица A          Таблица B
┌────────┐        ┌────────┐
│   1    │───────▶│   1    │
│   2    │        │   2    │
│   3    │        │   4    │
└────────┘        └────────┘
```

### INNER JOIN — только совпадающие записи
```sql
SELECT s.first_name, s.last_name, c.course_name, e.grade
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_id = c.course_id;
```

### LEFT JOIN — все из левой + совпадения из правой
```sql
-- Все курсы, даже без студентов
SELECT c.course_name, COUNT(e.student_id) AS enrolled
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id;
```

### RIGHT JOIN — все из правой + совпадения из левой
```sql
-- SQLite не поддерживает RIGHT JOIN напрямую
-- Можно переставить таблицы и использовать LEFT JOIN
```

> **Подробнее:** см. файл [`examples/02_joins_examples.sql`](examples/02_joins_examples.sql) — все типы JOIN с примерами и визуализацией результатов.

### Практика

Перейдите к файлу [`exercises/db_design_practice.md`](exercises/db_design_practice.md) и выполните **Часть 4: JOIN** (задания 4.1–4.4).

---

## Блок 5: Агрегатные функции и GROUP BY

### Агрегатные функции

| Функция | Описание |
|---------|----------|
| COUNT() | Количество записей |
| SUM() | Сумма значений |
| AVG() | Среднее значение |
| MIN() | Минимальное значение |
| MAX() | Максимальное значение |
| ROUND(x, n) | Округление до n знаков |

```sql
-- Количество студентов
SELECT COUNT(*) AS total FROM students;

-- Средний GPA (округлённый)
SELECT ROUND(AVG(gpa), 2) AS avg_gpa FROM students;

-- Статистика по GPA
SELECT
    COUNT(*) AS total,
    ROUND(AVG(gpa), 2) AS avg_gpa,
    MIN(gpa) AS min_gpa,
    MAX(gpa) AS max_gpa
FROM students
WHERE is_active = 1;
```

### GROUP BY — группировка

```sql
-- Количество студентов по годам
SELECT enrollment_year, COUNT(*) AS count
FROM students
GROUP BY enrollment_year;

-- Средний GPA по годам
SELECT enrollment_year, ROUND(AVG(gpa), 2) AS avg_gpa
FROM students
GROUP BY enrollment_year
ORDER BY enrollment_year;

-- HAVING — фильтрация групп (после GROUP BY)
SELECT enrollment_year, COUNT(*) AS count
FROM students
GROUP BY enrollment_year
HAVING COUNT(*) >= 2;
```

> **Подробнее:** см. файл [`examples/03_aggregation_grouping.sql`](examples/03_aggregation_grouping.sql).

### Практика

Перейдите к файлу [`exercises/db_design_practice.md`](exercises/db_design_practice.md) и выполните:
- **Часть 5: Агрегатные функции** (задания 5.1–5.4)
- **Часть 6: GROUP BY и HAVING** (задания 6.1–6.4)

---

## Блок 6: Вложенные запросы (подзапросы)

Подзапрос — это SELECT внутри другого запроса.

```sql
-- Студенты с GPA выше среднего
SELECT first_name, last_name, gpa
FROM students
WHERE gpa > (SELECT AVG(gpa) FROM students);

-- Курсы, на которые записан студент с ID = 1
SELECT course_name FROM courses
WHERE course_id IN (
    SELECT course_id FROM enrollments WHERE student_id = 1
);

-- Студенты, которые НЕ записаны ни на один курс
SELECT first_name, last_name FROM students
WHERE student_id NOT IN (
    SELECT DISTINCT student_id FROM enrollments
);
```

> **Подробнее:** см. файл [`examples/03_aggregation_grouping.sql`](examples/03_aggregation_grouping.sql), раздел 5.

### Практика

Перейдите к файлу [`exercises/db_design_practice.md`](exercises/db_design_practice.md) и выполните **Часть 7: Вложенные запросы** (задания 7.1–7.4).

---

## Блок 7: Нормализация баз данных

**Зачем нужна нормализация?**
- Устранение избыточности данных
- Предотвращение аномалий при вставке/обновлении/удалении
- Обеспечение целостности данных

### Первая нормальная форма (1NF)
- Все значения атомарны (неделимы)
- Нет повторяющихся групп

**Плохо:**
| id | name | phones |
|----|------|--------|
| 1 | Иванов | +7-999-111, +7-999-222 |

**Хорошо:**
| id | name | phone |
|----|------|-------|
| 1 | Иванов | +7-999-111 |
| 1 | Иванов | +7-999-222 |

### Вторая нормальная форма (2NF)
- Находится в 1NF
- Все неключевые атрибуты зависят от всего первичного ключа

### Третья нормальная форма (3NF)
- Находится в 2NF
- Нет транзитивных зависимостей (неключевые атрибуты не зависят друг от друга)

---

## Файлы семинара

В папке `examples/`:
- [`01_operators_and_filters.sql`](examples/01_operators_and_filters.sql) — логические операторы, LIKE, IN, BETWEEN, ORDER BY, LIMIT, DISTINCT
- [`02_joins_examples.sql`](examples/02_joins_examples.sql) — все типы JOIN с примерами
- [`03_aggregation_grouping.sql`](examples/03_aggregation_grouping.sql) — агрегатные функции, GROUP BY, подзапросы

В папке `data/`:
- [`university_extended.sql`](data/university_extended.sql) — расширенная БД университета (20 студентов, 10 курсов, факультеты)

В папке `exercises/`:
- [`db_design_practice.md`](exercises/db_design_practice.md) — упражнения по каждому блоку (с решениями)

---

## Дополнительные материалы

- [SQLBolt](https://sqlbolt.com/) — интерактивные уроки (уроки 5-12)
- [Visual JOIN](https://joins.spathon.com/) — визуализация JOIN
- [SQL Tutorial (W3Schools)](https://www.w3schools.com/sql/) — GROUP BY, JOIN
- [Database Normalization](https://www.guru99.com/database-normalization.html) — нормализация
