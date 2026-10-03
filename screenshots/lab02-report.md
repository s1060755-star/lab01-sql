# Лабораторна робота №02: Створення складних SQL запитів

---

## Інформація про студентку
- **Студентка:** s1060755-star
- **Репозиторій:** [https://github.com/s1060755-star/lab01-sql](https://github.com/s1060755-star/lab01-sql)
- **База даних:** PostgreSQL (Supabase)

---

## Рівень 1

### Завдання 1.1: INNER JOIN — Список товарів з категоріями та постачальниками
```sql
SELECT 
    p.product_name, 
    c.category_name, 
    s.company_name, 
    p.unit_price
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
INNER JOIN suppliers s ON p.supplier_id = s.supplier_id
ORDER BY c.category_name, p.product_name;
Завдання 1.2: LEFT JOIN — Клієнти та кількість замовлень
SQL
SELECT 
    c.contact_name, 
    c.customer_type, 
    r.region_name,
    COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN regions r ON c.region_id = r.region_id
GROUP BY c.customer_id, c.contact_name, c.customer_type, r.region_name
ORDER BY order_count DESC;
Завдання 1.3: Множинне з'єднання (5 таблиць)
SQL
SELECT 
    o.order_id,
    o.order_date,
    c.contact_name AS customer_name,
    p.product_name,
    cat.category_name,
    e.first_name || ' ' || e.last_name AS employee_name,
    oi.quantity,
    oi.unit_price
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN categories cat ON p.category_id = cat.category_id
JOIN employees e ON o.employee_id = e.employee_id
ORDER BY o.order_date DESC
LIMIT 20;
Завдання 1.4: Агрегатні функції — Товари по категоріях
SQL
SELECT 
    c.category_name,
    COUNT(p.product_id) AS product_count,
    AVG(p.unit_price) AS avg_price,
    MIN(p.unit_price) AS min_price,
    MAX(p.unit_price) AS max_price
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name
ORDER BY product_count DESC;
Завдання 1.5: Продажі за регіонами (SUM, GROUP BY, HAVING)
SQL
SELECT 
    COALESCE(r.region_name, 'Без регіону') AS region_name,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) AS total_sales,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN regions r ON c.region_id = r.region_id
GROUP BY r.region_name
HAVING SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) > 1000
ORDER BY total_sales DESC;
Завдання 1.6: Постачальники з кількістю товарів більше 2
SQL
SELECT 
    s.supplier_id,
    s.company_name,
    COUNT(p.product_id) AS total_products
FROM suppliers s
JOIN products p ON s.supplier_id = p.supplier_id
GROUP BY s.supplier_id, s.company_name
HAVING COUNT(p.product_id) > 2
ORDER BY total_products DESC;
Завдання 1.7: Корельований підзапит — Ціна вище середньої в категорії
SQL
SELECT 
    p.product_name, 
    p.unit_price, 
    c.category_name
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id
WHERE p.unit_price > (
    SELECT AVG(p2.unit_price)
    FROM products p2
    WHERE p2.category_id = p.category_id
)
ORDER BY c.category_name, p.unit_price DESC;
Завдання 1.8: Підзапит з IN — Клієнти з замовленнями у 2024 році
SQL
SELECT 
    customer_id, 
    contact_name, 
    company_name
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id
    FROM orders
    WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01'
);
Завдання 1.9: Підзапит у SELECT — Кількість продажів товарів
SQL
SELECT 
    p.product_id,
    p.product_name,
    p.unit_price,
    COALESCE((
        SELECT SUM(oi.quantity)
        FROM order_items oi
        WHERE oi.product_id = p.product_id
    ), 0) AS total_units_sold
FROM products p
ORDER BY total_units_sold DESC;
Рівень 2
Завдання 2.1: RIGHT JOIN — Аналіз категорій
SQL
SELECT 
    c.category_name,
    COUNT(p.product_id) AS products_count,
    COALESCE(AVG(p.unit_price), 0) AS avg_price
FROM products p
RIGHT JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_id, c.category_name
ORDER BY products_count DESC;
Завдання 2.2: Self-Join — Співробітники та їх керівники
SQL
SELECT 
    e1.first_name || ' ' || e1.last_name AS employee,
    e1.title AS employee_title,
    COALESCE(e2.first_name || ' ' || e2.last_name, 'Немає (Топ-менеджер)') AS manager,
    COALESCE(e2.title, '-') AS manager_title
FROM employees e1
LEFT JOIN employees e2 ON e1.reports_to = e2.employee_id
ORDER BY e2.last_name, e1.last_name;
Завдання 2.3: Віконні функції — Ранжування товарів
SQL
SELECT 
    p.product_name,
    c.category_name,
    p.unit_price,
    RANK() OVER (PARTITION BY c.category_name ORDER BY p.unit_price DESC) AS price_rank,
    DENSE_RANK() OVER (PARTITION BY c.category_name ORDER BY p.unit_price DESC) AS price_dense_rank,
    ROW_NUMBER() OVER (PARTITION BY c.category_name ORDER BY p.unit_price DESC) AS row_num
FROM products p
JOIN categories c ON p.category_id = c.category_id
ORDER BY c.category_name, p.unit_price DESC;
Завдання 2.4: Віконні функції — LAG / LEAD
SQL
SELECT 
    customer_id,
    order_id,
    order_date,
    freight,
    LAG(freight, 1, 0.0) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_freight,
    LEAD(freight, 1, 0.0) OVER (PARTITION BY customer_id ORDER BY order_date) AS next_order_freight,
    freight - LAG(freight, 1, 0.0) OVER (PARTITION BY customer_id ORDER BY order_date) AS freight_diff
FROM orders
ORDER BY customer_id, order_date;
Рівень 3
Завдання 3.1: Materialized View
SQL
CREATE MATERIALIZED VIEW mv_monthly_sales AS
SELECT
    EXTRACT(YEAR FROM o.order_date) AS year,
    EXTRACT(MONTH FROM o.order_date) AS month,
    c.category_name,
    r.region_name,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS orders_count,
    AVG(oi.quantity * oi.unit_price * (1 - oi.discount)) AS avg_order_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
JOIN customers cu ON o.customer_id = cu.customer_id
LEFT JOIN regions r ON cu.region_id = r.region_id
WHERE o.order_status = 'delivered'
GROUP BY year, month, c.category_name, r.region_name;

CREATE INDEX idx_mv_monthly_sales_date ON mv_monthly_sales(year, month);
Завдання 3.2: Рекурсивний запит (Recursive CTE)
SQL
WITH RECURSIVE employee_hierarchy AS (
    SELECT 
        employee_id, 
        first_name, 
        last_name, 
        title, 
        reports_to,
        0 AS level,
        CAST(last_name || ' ' || first_name AS VARCHAR(1000)) AS hierarchy_path
    FROM employees
    WHERE reports_to IS NULL

    UNION ALL

    SELECT 
        e.employee_id, 
        e.first_name, 
        e.last_name, 
        e.title, 
        e.reports_to,
        eh.level + 1,
        CAST(eh.hierarchy_path || ' -> ' || e.last_name || ' ' || e.first_name AS VARCHAR(1000))
    FROM employees e
    JOIN employee_hierarchy eh ON e.reports_to = eh.employee_id
)
SELECT * FROM employee_hierarchy ORDER BY hierarchy_path;
Завдання 3.3: EXPLAIN ANALYZE та індекси
SQL
EXPLAIN ANALYZE
SELECT p.product_name, c.category_name, p.unit_price
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.unit_price > 50;

CREATE INDEX idx_products_unit_price ON products(unit_price);
Висновки
Під час виконання лабораторної роботи №2 я закріпила практичні навички роботи зі складними SQL-запитами в PostgreSQL (Supabase). У ході роботи я успішно реалізувала різні типи з'єднань таблиць (INNER, LEFT, RIGHT, SELF JOIN), виконала агрегацію та фільтрацію даних, застосувала підзапити й віконні функції, створила матеріалізоване подання, побудувала рекурсивний запит та проаналізувала час виконання запитів із використанням індексів.
