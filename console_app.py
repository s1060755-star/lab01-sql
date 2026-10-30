import psycopg2

DB_CONFIG = {
    "dbname": "bookstore",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_database():
    """Створює всі необхідні таблиці та початкові дані, якщо вони відсутні"""
    conn = get_connection()
    cur = conn.cursor()
    
    # 1. Створення таблиць
    cur.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            author_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            country VARCHAR(50) DEFAULT 'Україна'
        );

        CREATE TABLE IF NOT EXISTS genres (
            genre_id SERIAL PRIMARY KEY,
            genre_name VARCHAR(50) UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS books (
            book_id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            isbn VARCHAR(13) UNIQUE NOT NULL,
            publication_year INT,
            pages INT,
            price DECIMAL(10, 2) NOT NULL,
            stock_quantity INT NOT NULL DEFAULT 0,
            author_id INT NOT NULL REFERENCES authors(author_id) ON DELETE CASCADE,
            genre_id INT NOT NULL REFERENCES genres(genre_id) ON DELETE RESTRICT
        );

        CREATE OR REPLACE VIEW view_catalog AS
        SELECT 
            b.book_id,
            b.title,
            CONCAT(a.first_name, ' ', a.last_name) AS author,
            g.genre_name,
            b.price,
            b.stock_quantity
        FROM books b
        JOIN authors a ON b.author_id = a.author_id
        JOIN genres g ON b.genre_id = g.genre_id;
    """)
    
    # 2. Додавання тестових даних, якщо таблиця книг порожня
    cur.execute("SELECT COUNT(*) FROM books;")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO authors (first_name, last_name, country) VALUES 
            ('Тарас', 'Шевченко', 'Україна'),
            ('Ліна', 'Костенко', 'Україна');

            INSERT INTO genres (genre_name) VALUES 
            ('Поезія'),
            ('Роман');

            INSERT INTO books (title, isbn, publication_year, pages, price, stock_quantity, author_id, genre_id) VALUES 
            ('Кобзар', '9789660356719', 1840, 250, 250.00, 15, 1, 1),
            ('Маруся Чурай', '9789662232014', 1979, 448, 320.00, 10, 2, 1);
        """)
    
    conn.commit()
    cur.close()
    conn.close()

def show_catalog():
    init_database()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT book_id, title, author, genre_name, price, stock_quantity FROM view_catalog;")
    books = cur.fetchall()
    print("\n--- КАТАЛОГ КНИГ ---")
    for book in books:
        print(f"ID: {book[0]} | Назва: {book[1]} | Автор: {book[2]} | Жанр: {book[3]} | Ціна: {book[4]} грн | Кількість: {book[5]} шт.")
    cur.close()
    conn.close()

def add_author():
    print("\n--- ДОДАВАННЯ НОВОГО АВТОРА ---")
    first_name = input("Введіть ім'я автора: ")
    last_name = input("Введіть прізвище автора: ")
    country = input("Введіть країну: ")
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO authors (first_name, last_name, country) VALUES (%s, %s, %s);",
        (first_name, last_name, country)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Автора успішно додано!")

if __name__ == "__main__":
    while True:
        print("\nОберіть дію:")
        print("1. Переглянути каталог книг")
        print("2. Додати нового автора")
        print("3. Вихід")
        choice = input("Ваш вибір (1-3): ")
        
        if choice == "1":
            show_catalog()
        elif choice == "2":
            add_author()
        elif choice == "3":
            print("До побачення!")
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")