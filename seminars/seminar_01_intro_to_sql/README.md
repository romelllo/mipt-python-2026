# Семинар 1: Введение в базы данных. Знакомство с SQL

**Модуль:** 2 — Объектно-ориентированное программирование и основы работы с базами данных в Python
**Дата:** 02.02.2026
**Презентация:** [ссылка на презентацию]

---

## Цели семинара

После этого семинара вы сможете:
- Понимать что такое реляционные базы данных и SQL
- Создавать и удалять таблицы (CREATE TABLE, DROP TABLE)
- Изменять структуру таблиц (ALTER TABLE)
- Вставлять, обновлять и удалять данные (INSERT, UPDATE, DELETE)
- Писать простые запросы выборки (SELECT с WHERE)
- Работать с SQLite через консоль и DB Browser

---

## План семинара

| Время | Тема |
|-------|------|
| 10-15 мин | Обзор темы: что такое БД, SQL, SQLite |
| 15 мин | CREATE TABLE, типы данных, ограничения |
| 15 мин | INSERT INTO, UPDATE, DELETE |
| 10 мин | ALTER TABLE, DROP TABLE |
| 25 мин | SELECT с простым WHERE |
| 10 мин | Практика: самостоятельные задания |

---

## Содержание

### 1. Что такое база данных?

**База данных** — организованная коллекция структурированных данных.

**Реляционная модель:**
- Данные хранятся в **таблицах** (отношениях)
- Таблицы состоят из **строк** (записей) и **столбцов** (полей)
- Таблицы связаны через **ключи**
- **SQL** (Structured Query Language) — язык для работы с данными

**SQLite — наша учебная СУБД:**
- Не требует установки сервера
- База данных — один файл `.db`
- Встроен в Python (модуль `sqlite3`)
- Идеален для обучения и прототипирования

### 2. Инструменты для работы

#### DB Browser for SQLite (рекомендуется)
- Скачать: https://sqlitebrowser.org/
- Графический интерфейс для работы с SQLite
- Удобно для начинающих

#### Консоль sqlite3
```bash
# Создать/открыть базу данных
sqlite3 university.db

# Полезные команды в консоли
.help           -- справка по командам
.tables         -- список таблиц
.schema         -- структура всех таблиц
.schema students -- структура конкретной таблицы
.mode column    -- табличный вывод
.headers on     -- показывать заголовки
.quit           -- выход
```

### 3. Типы данных в SQLite

| Тип | Описание | Пример |
|-----|----------|--------|
| INTEGER | Целое число | 1, 42, -100 |
| REAL | Число с плавающей точкой | 3.14, -0.5 |
| TEXT | Строка | 'Hello', 'Иванов' |
| BLOB | Бинарные данные | Изображения, файлы |
| NULL | Отсутствие значения | NULL |

### 4. CREATE TABLE — создание таблиц

```sql
CREATE TABLE имя_таблицы (
    столбец1 тип_данных ограничения,
    столбец2 тип_данных ограничения,
    ...
);
```

**Ограничения (constraints):**
- `PRIMARY KEY` — первичный ключ (уникальный идентификатор)
- `NOT NULL` — значение обязательно
- `UNIQUE` — значение должно быть уникальным
- `DEFAULT значение` — значение по умолчанию
- `CHECK(условие)` — проверка условия

**Пример:**
```sql
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    age INTEGER CHECK(age >= 16),
    is_active INTEGER DEFAULT 1
);
```

### 5. INSERT INTO — вставка данных

```sql
-- Вставка одной записи (все столбцы)
INSERT INTO students (first_name, last_name, email, age)
VALUES ('Иван', 'Петров', 'petrov@mail.ru', 20);

-- Вставка нескольких записей
INSERT INTO students (first_name, last_name, email, age)
VALUES
    ('Мария', 'Сидорова', 'sidorova@mail.ru', 19),
    ('Алексей', 'Козлов', 'kozlov@mail.ru', 21);
```

### 6. SELECT — выборка данных

```sql
-- Все столбцы и все строки
SELECT * FROM students;

-- Определённые столбцы
SELECT first_name, last_name FROM students;

-- С условием WHERE
SELECT * FROM students WHERE age > 20;

-- Несколько условий
SELECT * FROM students WHERE age >= 18 AND is_active = 1;
```

### 7. UPDATE — обновление данных

```sql
-- Обновить одно поле по условию
UPDATE students
SET email = 'new_email@mail.ru'
WHERE student_id = 1;

-- Обновить несколько полей
UPDATE students
SET age = 21, is_active = 0
WHERE last_name = 'Петров';

-- ⚠️ ВНИМАНИЕ: без WHERE обновятся ВСЕ записи!
UPDATE students SET is_active = 1;  -- обновит всех!
```

### 8. DELETE — удаление данных

```sql
-- Удалить записи по условию
DELETE FROM students WHERE student_id = 5;

-- Удалить по нескольким условиям
DELETE FROM students WHERE is_active = 0 AND age < 18;

-- ⚠️ ВНИМАНИЕ: без WHERE удалятся ВСЕ записи!
DELETE FROM students;  -- удалит всех!
```

### 9. ALTER TABLE — изменение структуры

```sql
-- Добавить столбец
ALTER TABLE students ADD COLUMN phone TEXT;

-- Переименовать таблицу
ALTER TABLE students RENAME TO university_students;

-- Переименовать столбец (SQLite 3.25+)
ALTER TABLE students RENAME COLUMN phone TO phone_number;

-- ⚠️ SQLite не поддерживает удаление столбцов напрямую
-- Нужно пересоздать таблицу
```

### 10. DROP TABLE — удаление таблицы

```sql
-- Удалить таблицу (безвозвратно!)
DROP TABLE students;

-- Удалить, если существует (без ошибки)
DROP TABLE IF EXISTS students;
```

---

## Файлы примеров

В папке `examples/`:
- `01_create_tables.sql` — создание таблиц с разными типами данных
- `02_insert_data.sql` — примеры вставки данных
- `03_basic_queries.sql` — SELECT, UPDATE, DELETE

В папке `data/`:
- `university.sql` — полный скрипт для создания учебной БД

---

## Практические задания

### Задание 1: Создание таблицы
Создайте таблицу `books` со следующими полями:
- `book_id` — первичный ключ
- `title` — название (обязательное)
- `author` — автор (обязательное)
- `year` — год издания
- `pages` — количество страниц (больше 0)
- `is_available` — доступна ли (по умолчанию 1)

### Задание 2: Вставка данных
Добавьте 5 книг в таблицу `books`.

### Задание 3: Запросы
1. Выведите все книги
2. Выведите только названия и авторов
3. Выведите книги, изданные после 2000 года
4. Выведите книги автора "Пушкин"

### Задание 4: Обновление
1. Измените год издания у книги с `book_id = 1`
2. Сделайте все книги до 1950 года недоступными

### Задание 5: Удаление
1. Удалите книгу с `book_id = 3`

См. также файл `exercises/basic_sql_practice.md` для дополнительных заданий.

---

## Дополнительные материалы

- [SQLite Tutorial](https://www.sqlitetutorial.net/) — подробный туториал по SQLite
- [SQL Tutorial (W3Schools)](https://www.w3schools.com/sql/) — интерактивные примеры SQL
- [DB Browser for SQLite](https://sqlitebrowser.org/) — графический инструмент
- [SQLBolt](https://sqlbolt.com/) — интерактивные уроки SQL (уроки 1-4)
