# Лабораторна робота №02: Створення складних SQL запитів

---

## Інформація про студента
- **Студент:** s1060755-star
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