Звіт з лабораторної роботи №3.
 Модифікація даних та транзакції
 Виконала: Скоп'юк Олександра Іванівна 
Група: ІПЗ-31
 Рівень складності : Середній 
Мета роботи:   Здобути практичні навички безпечної модифікації даних у реляційних базах даних, опанувати механізми транзакцій для забезпечення цілісності даних, навчитися працювати з обмеженнями цілісності та каскадними операціями при зміні взаємопов'язаних записів. 
 Виконання роботи   
 Рівень 1. Базові операції модифікації   
 Крок 1. Створення структури бази даних   Я створила базу даних для системи управління бібліотекою та реалізувала чотири основні таблиці з необхідними обмеженнями цілісності:SQLCREATE DATABASE library_lab3;
(Створено таблиці authors, books, readers, lendings із первинними, зовнішніми ключами та перевірками CHECK)
```sql
евірте структуру в дереві DBeaver (розгорніть схему та таблиці):
library_lab3 -> Tables -> authors, books, lendings, readers
```
![Результат виконання завдання 1.1](screenshots1.png)
Крок 2. Додавання тестових данихЯ виконала вставку початкових даних у всі створені таблиці.Додавання авторів, книг та читачів:  
```sql
SERT INTO authors (first_name, last_name, birth_year, country)
VALUES
    ('Тарас', 'Шевченко', 1814, 'Україна'),
    ('Іван', 'Франко', 1856, 'Україна'),
    ('Леся', 'Українка', 1871, 'Україна'),
    ('Михайло', 'Коцюбинський', 1864, 'Україна'),
    ('Панас', 'Мирний', 1849, 'Україна');
Перевірка доданих авторів:SQLSELECT * FROM authors ORDER BY birth_year;
```
![Результат виконання завдання 1.2](screenshots2.png)
Фрагмент результату у вкладці Data внизу DBeaver:
Plaintext author_id | first_name |   last_name    | birth_year | country |         created_at |
-----------+------------+----------------+------------+---------+----------------------------+
         1 | Тарас      | Шевченко       |       1814 | Україна | 2025-10-15 10:23:45.000000 |
         5 | Панас      | Мирний         |       1849 | Україна | 2025-10-15 10:23:45.000000 |
         2 | Іван       | Франко         |       1856 | Україна | 2025-10-15 10:23:45.000000 |
         4 | Михайло    | Коцюбинський   |       1864 | Україна | 2025-10-15 10:23:45.000000 |
         3 | Леся       | Українка       |       1871 | Україна | 2025-10-15 10:23:45.000000 |
        
         
Крок 3. Безпечне оновлення записівЯ продемонструвала важливість перевірки даних перед їх оновленням.Перевірка поточного стану та оновлення:
![Результат виконання завдання 1.3](screenshots3.png)
```sql
еревірка до оновлення
SELECT book_id, title, total_copies, available_copies FROM books WHERE book_id = 1;
```
2. Безпечне оновлення
```sql
UPDATE books 
SET available_copies = available_copies - 1 
WHERE book_id = 1 AND available_copies > 0;
```
3. Перевірка після оновлення
```sql
SELECT book_id, title, total_copies, available_copies FROM books WHERE book_id = 1;
```
Plaintext book_id | title  | total_copies | available_copies |
---------+--------+--------------+------------------+
       1 | Кобзар |           10 |                7 |
Крок 4. Операції з транзакціямиЯ реалізувала процес видачі книги як атомарну операцію за допомогою транзакції.SQLBEGIN;
```sql
-- Видача книги
INSERT INTO lendings (book_id, reader_id, due_date)
VALUES (1, 1, CURRENT_DATE + INTERVAL '14 days');
```
![Результат виконання завдання 1.4](screenshots4.png)
Зменшення кількості доступних примірників
```sql
UPDATE books
SET available_copies = available_copies - 1
WHERE book_id = 1 AND available_copies > 0;
```

 Перевірка результатів перед підтвердженням
 ```sql
SELECT * FROM lendings WHERE lending_id = LASTVAL();
SELECT available_copies FROM books WHERE book_id = 1;
COMMIT;
```
Paintext lending_id | book_id | reader_id | lending_date |  due_date  | return_date |
------------+---------+-----------+--------------+------------+-------------+
          1 |       1 |         1 | 2025-10-15   | 2025-10-29 | NULL        |

  комірка available_copies: 6
 статус виконання нижче: COMMIT (успішно)
Крок 5. Демонстрація ROLLBACKЯ показала відкат транзакції при виникненні помилки порушення цілісності.SQLBEGIN;
![Результат виконання завдання 1.5](screenshots5.png)
Спроба видалити автора, у якого є книги
```sql
DELETE FROM authors WHERE author_id = 1;
```
Відкат при помилці
```sql
ROLLBACK;
```
Перевірка
```sql
SELECT * FROM authors WHERE author_id = 1;
```
PintextERROR: update or delete on table "authors" violates foreign key constraint "books_author_id_fkey" on table "books"
DETAIL: Key (author_id)=(1) is still referenced from table "books".

А нижче рядок: ROLLBACK та повернений рядок з Тарасом Шевченком за запитом SELECT.
Крок 6. Безпечне видаленняЯ виконала видалення записів з обов'язковою попередньою перевіркою.SQL-- Перевірка перед видаленням
```sql
SELECT * FROM readers 
WHERE status = 'Inactive' 
  AND reader_id NOT IN (
      SELECT DISTINCT reader_id FROM lendings WHERE return_date IS NULL
  );
```
Видалення неактивних читачів без боргів
```sql
DELETE FROM readers
WHERE status = 'Inactive' 
  AND reader_id NOT IN (
      SELECT DISTINCT reader_id FROM lendings WHERE return_date IS NULL
  );
  ```
![Результат виконання завдання 1.6](screenshots6.png)