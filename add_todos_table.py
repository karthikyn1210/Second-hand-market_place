"""
Add todos table to existing database
"""

import sqlite3
import os

DB_PATH = "database.db"

if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if todos table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='todos'")
        if cursor.fetchone():
            print("Todos table already exists!")
        else:
            # Create todos table
            cursor.execute("""
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
            conn.commit()
            print("Todos table created successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
else:
    print("Database does not exist!")
