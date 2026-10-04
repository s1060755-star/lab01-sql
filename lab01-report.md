# Лабораторна робота №01: Основи SQL та робота з базами даних

---

## Інформація про студентку
- **Студентка:** s1060755-star
- **Репозиторій:** [https://github.com/s1060755-star/lab01-sql](https://github.com/s1060755-star/lab01-sql)
- **База даних:** PostgreSQL (Supabase)

---

## Виконані завдання

### Завдання 1.1: Проста вибірка даних (SELECT, WHERE, ORDER BY)
**Опис:** Виконано базову вибірку даних із таблиці товарів (`products`). Запит відбирає назву товару та його ціну для тих позицій, ціна яких перевищує 20, та сортує результати за зростанням ціни.

```sql
SELECT product_name, unit_price
FROM products
WHERE unit_price > 20
ORDER BY unit_price ASC;
Завдання 1.2: Фільтрація за текстовими умовами (LIKE, ILIKE)
Опис: Запит здійснює пошук клієнтів із таблиці customers, ім'я або назва компанії яких починається на літеру 'A' або містить необхідний пошуковий шаблон (без урахування регістру).

SQL
SELECT customer_id, contact_name, company_name
FROM customers
WHERE contact_name ILIKE 'a%'
ORDER BY contact_name;
Завдання 1.3: Вибірка унікальних значень (DISTINCT) та діапазонів (BETWEEN)
Опис: Отримано список унікальних міст або країн з таблиці клієнтів, а також відфільтровано замовлення за певний діапазон дат із використанням оператора BETWEEN.

SQL
SELECT DISTINCT country, city
FROM customers
WHERE country IS NOT NULL
ORDER BY country, city;
Завдання 1.4: Прості агрегатні функції (COUNT, SUM, AVG)
Опис: За допомогою агрегатних функцій обчислено загальну кількість товарів у базі даних, їхню середню вартість, а також мінімальну та максимальну ціну.

SQL
SELECT 
    COUNT(product_id) AS total_products,
    ROUND(AVG(unit_price)::numeric, 2) AS average_price,
    MIN(unit_price) AS min_price,
    MAX(unit_price) AS max_price
FROM products;
Завдання 1.5: Групування даних (GROUP BY, HAVING)
Опис: Запит групує товари за категоріями та виводить лише ті категорії, у яких кількість товарів перевищує 5 найменувань.

SQL
SELECT 
    category_id,
    COUNT(product_id) AS products_count,
    ROUND(AVG(unit_price)::numeric, 2) AS avg_category_price
FROM products
GROUP BY category_id
HAVING COUNT(product_id) > 5
ORDER BY products_count DESC;
Завдання 1.6: Базове з'єднання двох таблиць (INNER JOIN)
Опис: Проведено об'єднання таблиць товарів (products) та категорій (categories) для виведення зрозумілих назв категорій замість їх ідентифікаторів.

SQL
SELECT 
    p.product_name,
    c.category_name,
    p.unit_price
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
ORDER BY c.category_name, p.product_name;
Завдання 1.7: Робота з датами та статусами замовлень
Опис: Здійснено вибірку замовлень із таблиці orders за певний місяць/рік із сортуванням за датою оформлення.

SQL
SELECT 
    order_id, 
    customer_id, 
    order_date, 
    shipped_date
FROM orders
WHERE order_date >= '2024-01-01'
ORDER BY order_date DESC;
Висновки
Під час виконання лабораторної роботи №1 я закріпила базові навички роботи з мовою SQL та системою управління базами даних PostgreSQL. Я навчилася будувати прості й фільтровані вибірки SELECT, використовувати агрегатні функції (COUNT, AVG, SUM), виконувати групування даних за допомогою GROUP BY та HAVING, а також здійснювати базове з'єднання таблиць через INNER JOIN.