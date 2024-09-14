import sqlite3

# Database connection details
database = "mydb.sqlite3"

def create_tables(cur):
    # Create 'sales' table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            quantity INTEGER,
            sale_date TEXT,
            total_amount REAL
        );
    """)

    # Create 'products' table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price REAL
        );
    """)

    # Create 'customers' table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            join_date TEXT
        );
    """)

    # Create 'orders' table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id INTEGER,
            order_date TEXT,
            order_amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        );
    """)

def insert_data(cur):
    # Insert data into 'sales' table
    cur.executemany("""
        INSERT INTO sales (product_name, quantity, sale_date, total_amount) VALUES (?, ?, ?, ?)
    """, [
        ('Laptop', 5, '2024-09-01', 5000.00),
        ('Smartphone', 10, '2024-09-02', 3000.00),
        ('Headphones', 20, '2024-09-03', 1000.00),
        ('Monitor', 8, '2024-09-04', 1600.00),
        ('Keyboard', 15, '2024-09-05', 450.00)
    ])

    # Insert data into 'products' table
    cur.executemany("""
        INSERT INTO products (name, category, price) VALUES (?, ?, ?)
    """, [
        ('Laptop', 'Electronics', 1000.00),
        ('Smartphone', 'Electronics', 300.00),
        ('Headphones', 'Accessories', 50.00),
        ('Monitor', 'Electronics', 200.00),
        ('Keyboard', 'Accessories', 30.00)
    ])

    # Insert data into 'customers' table
    cur.executemany("""
        INSERT INTO customers (name, email, join_date) VALUES (?, ?, ?)
    """, [
        ('Alice Johnson', 'alice.johnson@example.com', '2024-01-15'),
        ('Bob Smith', 'bob.smith@example.com', '2024-03-22'),
        ('Carol Davis', 'carol.davis@example.com', '2024-05-10'),
        ('David Brown', 'david.brown@example.com', '2024-07-01'),
        ('Emily White', 'emily.white@example.com', '2024-08-20')
    ])

    # Insert data into 'orders' table
    cur.executemany("""
        INSERT INTO orders (customer_id, product_id, order_date, order_amount) VALUES (?, ?, ?, ?)
    """, [
        (1, 1, '2024-09-01', 1000.00),
        (2, 2, '2024-09-02', 300.00),
        (3, 3, '2024-09-03', 50.00),
        (4, 4, '2024-09-04', 200.00),
        (5, 5, '2024-09-05', 30.00)
    ])

def main():
    # Establishing the connection
    conn = sqlite3.connect(database)
    
    # Creating a cursor object to execute SQL queries
    cur = conn.cursor()

    try:
        # Create tables
        create_tables(cur)

        # Insert data into tables
        insert_data(cur)

        # Commit the transaction
        conn.commit()

        print("Tables created and data inserted successfully!")
    
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback if there is any error
    
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
