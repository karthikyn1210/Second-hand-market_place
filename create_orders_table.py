"""
Create orders and order_items tables for payment and tracking system
"""
import sqlite3
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, '..', 'database.db')

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Create orders table
cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        order_number TEXT UNIQUE,
        total_price REAL,
        payment_status TEXT DEFAULT 'Pending',
        tracking_status TEXT DEFAULT 'Order Confirmed',
        tracking_id TEXT UNIQUE,
        estimated_delivery TEXT,
        shipping_address TEXT,
        phone_number TEXT,
        created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
""")

# Create order_items table
cur.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        product_title TEXT,
        quantity INTEGER DEFAULT 1,
        price REAL,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
""")

# Create tracking_history table for detailed tracking
cur.execute("""
    CREATE TABLE IF NOT EXISTS tracking_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        status TEXT,
        location TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        details TEXT,
        FOREIGN KEY(order_id) REFERENCES orders(id)
    )
""")

conn.commit()
conn.close()

print('Orders and tracking tables created successfully!')
