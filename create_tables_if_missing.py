import sqlite3
from datetime import datetime

DB = 'database.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0
);
''')

cur.execute('''CREATE TABLE IF NOT EXISTS products (
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
''')

cur.execute('''CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);
''')

cur.execute('''CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    rating INTEGER,
    comment TEXT,
    created_on TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);
''')

# ensure at least one admin exists; insert default admin if users table empty
cur.execute('SELECT COUNT(*) FROM users')
count = cur.fetchone()[0]
if count == 0:
    cur.execute("INSERT INTO users (name, email, password, is_admin) VALUES (?, ?, ?, ?)",
                ("Admin", "admin@site.com", "admin123", 1))
    print('Inserted default admin user: admin@site.com / admin123')

conn.commit()
conn.close()
print('Tables ensured in', DB)
