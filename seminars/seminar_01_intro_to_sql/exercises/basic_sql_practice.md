# Практические задания: Основы SQL

## Подготовка

1. Откройте консоль sqlite3
2. Создайте новую базу данных `practice.db`
3. Выполните скрипты из папки `examples/` для создания учебных данных

---

## Часть 1: CREATE TABLE

### Задание 1.1
Создайте таблицу `books` со следующими полями:
- `book_id` — целое число, первичный ключ, автоинкремент
- `title` — текст, обязательное поле
- `author` — текст, обязательное поле
- `year_published` — целое число
- `pages` — целое число, больше 0
- `is_available` — целое число, по умолчанию 1

<details>
<summary>Решение</summary>

```sql
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year_published INTEGER,
    pages INTEGER CHECK(pages > 0),
    is_available INTEGER DEFAULT 1
);
```
</details>

### Задание 1.2
Создайте таблицу `employees` со следующими полями:
- `employee_id` — первичный ключ
- `name` — обязательное поле
- `position` — обязательное поле
- `salary` — число с плавающей точкой, не меньше 0
- `hire_date` — текст (дата)
- `email` — уникальное значение

<details>
<summary>Решение</summary>

```sql
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    salary REAL CHECK(salary >= 0),
    hire_date TEXT,
    email TEXT UNIQUE
);
```
</details>

---

## Часть 2: INSERT INTO

### Задание 2.1
Добавьте 5 книг в таблицу `books`:
1. "Война и мир", Толстой, 1869, 1225 страниц
2. "Преступление и наказание", Достоевский, 1866, 672 страницы
3. "Мастер и Маргарита", Булгаков, 1967, 480 страниц
4. "1984", Оруэлл, 1949, 328 страниц
5. "Гарри Поттер", Роулинг, 1997, 309 страниц

<details>
<summary>Решение</summary>

```sql
INSERT INTO books (title, author, year_published, pages)
VALUES
    ('Война и мир', 'Толстой', 1869, 1225),
    ('Преступление и наказание', 'Достоевский', 1866, 672),
    ('Мастер и Маргарита', 'Булгаков', 1967, 480),
    ('1984', 'Оруэлл', 1949, 328),
    ('Гарри Поттер', 'Роулинг', 1997, 309);
```
</details>

### Задание 2.2
Добавьте 3 сотрудников в таблицу `employees`.

<details>
<summary>Решение</summary>

```sql
INSERT INTO employees (name, position, salary, hire_date, email)
VALUES
    ('Иванов Иван', 'Менеджер', 80000, '2020-03-15', 'ivanov@company.ru'),
    ('Петрова Мария', 'Разработчик', 120000, '2021-07-01', 'petrova@company.ru'),
    ('Сидоров Алексей', 'Аналитик', 95000, '2022-01-10', 'sidorov@company.ru');
```
</details>

---

## Часть 3: SELECT

### Задание 3.1
Напишите запрос для вывода всех книг.

<details>
<summary>Решение</summary>

```sql
SELECT * FROM books;
```
</details>

### Задание 3.2
Выведите только названия и авторов книг.

<details>
<summary>Решение</summary>

```sql
SELECT title, author FROM books;
```
</details>

### Задание 3.3
Найдите все книги, изданные после 1900 года.

<details>
<summary>Решение</summary>

```sql
SELECT * FROM books WHERE year_published > 1900;
```
</details>

### Задание 3.4
Найдите книги с количеством страниц больше 500.

<details>
<summary>Решение</summary>

```sql
SELECT title, author, pages FROM books WHERE pages > 500;
```
</details>

### Задание 3.5
Найдите книги автора "Толстой".

<details>
<summary>Решение</summary>

```sql
SELECT * FROM books WHERE author = 'Толстой';
```
</details>

---

## Часть 4: UPDATE

### Задание 4.1
Измените год издания книги "1984" на 1948.

<details>
<summary>Решение</summary>

```sql
UPDATE books SET year_published = 1948 WHERE title = '1984';
```
</details>

### Задание 4.2
Сделайте все книги до 1900 года недоступными (is_available = 0).

<details>
<summary>Решение</summary>

```sql
UPDATE books SET is_available = 0 WHERE year_published < 1900;
```
</details>

### Задание 4.3
Увеличьте зарплату всем сотрудникам на должности "Разработчик" на 10000.

<details>
<summary>Решение</summary>

```sql
UPDATE employees SET salary = salary + 10000 WHERE position = 'Разработчик';
```
</details>

---

## Часть 5: DELETE

### Задание 5.1
Удалите книгу "Гарри Поттер".

<details>
<summary>Решение</summary>

```sql
DELETE FROM books WHERE title = 'Гарри Поттер';
```
</details>

### Задание 5.2
Удалите все недоступные книги.

<details>
<summary>Решение</summary>

```sql
DELETE FROM books WHERE is_available = 0;
```
</details>

---

## Часть 6: ALTER TABLE

### Задание 6.1
Добавьте в таблицу `books` столбец `genre` (жанр).

<details>
<summary>Решение</summary>

```sql
ALTER TABLE books ADD COLUMN genre TEXT;
```
</details>

### Задание 6.2
Заполните жанр для оставшихся книг.

<details>
<summary>Решение</summary>

```sql
UPDATE books SET genre = 'Роман' WHERE title = 'Война и мир';
UPDATE books SET genre = 'Роман' WHERE title = 'Преступление и наказание';
UPDATE books SET genre = 'Фантастика' WHERE title = 'Мастер и Маргарита';
UPDATE books SET genre = 'Антиутопия' WHERE title = '1984';
```
</details>

---

## Часть 7: DROP TABLE

### Задание 7.1
Удалите таблицу `employees`.

<details>
<summary>Решение</summary>

```sql
DROP TABLE employees;
-- или безопасный вариант:
DROP TABLE IF EXISTS employees;
```
</details>

---

## Бонусные задания

### Задание Б.1
Создайте таблицу `orders` для интернет-магазина:
- ID заказа
- ID клиента
- Дата заказа (по умолчанию — сегодня)
- Сумма заказа (не меньше 0)
- Статус ('new', 'processing', 'shipped', 'delivered')

### Задание Б.2
Используя таблицу `students` из примеров, найдите:
1. Всех студентов 2022 года поступления
2. Студентов с GPA выше 4.0
3. Активных студентов с GPA от 3.5 до 4.5
