import sqlite3
from datetime import datetime


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("pharmacy.db")
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                quantity INTEGER,
                price REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                contact TEXT,
                address TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                customer_id INTEGER,
                quantity INTEGER,
                date TEXT,
                total_price REAL,
                FOREIGN KEY (product_id) REFERENCES products(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
        self.conn.commit()

    def add_product(self, name, quantity, price):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
                       (name, quantity, price))
        self.conn.commit()

    def get_all_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()

    def get_product(self, product_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        return cursor.fetchone()

    def update_product(self, product_id, name, quantity, price):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE products SET name = ?, quantity = ?, price = ? WHERE id = ?",
                       (name, quantity, price, product_id))
        self.conn.commit()

    def delete_product(self, product_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.conn.commit()

    def add_customer(self, name, contact, address):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO customers (name, contact, address) VALUES (?, ?, ?)",
                       (name, contact, address))
        self.conn.commit()

    def get_all_customers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers")
        return cursor.fetchall()

    def get_customer(self, customer_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        return cursor.fetchone()

    def update_customer(self, customer_id, name, contact, address):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE customers SET name = ?, contact = ?, address = ? WHERE id = ?",
                       (name, contact, address, customer_id))
        self.conn.commit()

    def delete_customer(self, customer_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        self.conn.commit()

    def add_sale(self, product_id, customer_id, quantity, total_price):
        cursor = self.conn.cursor()
        # Проверка существования товара
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        if not cursor.fetchone():
            raise ValueError(f"Товар с ID {product_id} не найден.")

        # Проверка существования клиента
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        if not cursor.fetchone():
            raise ValueError(f"Клиент с ID {customer_id} не найден.")

        # Добавление продажи
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO sales (product_id, customer_id, quantity, date, total_price) VALUES (?, ?, ?, ?, ?)",
            (product_id, customer_id, quantity, date, total_price))
        # Уменьшение количества товара
        cursor.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (quantity, product_id))
        self.conn.commit()

    def get_all_sales(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sales")
        return cursor.fetchall()