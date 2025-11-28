"""
Add product_id column to todos table if missing.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check if column exists
cursor.execute("PRAGMA table_info(todos)")
cols = [r[1] for r in cursor.fetchall()]
if 'product_id' in cols:
    print('Column product_id already exists in todos')
else:
    try:
        cursor.execute('ALTER TABLE todos ADD COLUMN product_id INTEGER')
        conn.commit()
        print('Added product_id column to todos')
    except Exception as e:
        print('Error adding column:', e)

conn.close()
