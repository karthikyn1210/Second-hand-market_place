import sqlite3
from datetime import datetime
import os

DB = "database.db"

if os.path.exists(DB):
    print("Database already exists (database.db). If you want a fresh DB, delete it and rerun.")
else:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # users table (is_admin: 0 normal user, 1 admin)
    cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    );
    """)

    # products table
    cur.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT,
        price REAL,
        description TEXT,
        image_path TEXT,
        user_id INTEGER,
        created_on TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)

    # favorites table
    cur.execute("""
    CREATE TABLE favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    );
    """)

    # reviews table
    cur.execute("""
    CREATE TABLE reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        rating INTEGER,
        comment TEXT,
        created_on TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    );
    """)

    # todos table (for managing bikes and cars inventory)
    cur.execute("""
    CREATE TABLE todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        item_type TEXT NOT NULL,
        price REAL,
        description TEXT,
        image_path TEXT,
        status TEXT DEFAULT 'pending',
        created_on TEXT,
        updated_on TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)

    # create a default admin user (email: admin@site.com, password: admin123)
    # Password will be plain here; instruct to change or we will set hashed in app on first run
    cur.execute("INSERT INTO users (name, email, password, is_admin) VALUES (?, ?, ?, ?)",
                ("Admin", "admin@site.com", "admin123", 1))

    conn.commit()
    conn.close()
    print("Database created: database.db")
    print("Admin created: email=admin@site.com password=admin123 (please change after first login)")
