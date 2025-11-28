"""
Remove products whose category indicates Clothing or Book, and cascade-delete related rows in todos, favorites, reviews.
This script expects the database at ../database.db and will print counts of affected rows.
"""
import sqlite3
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, '..', 'database.db')

if not os.path.exists(DB):
    print('Database not found:', DB)
    raise SystemExit(1)

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Find product ids to remove
rows = cur.execute("SELECT id, title, category FROM products WHERE LOWER(category) LIKE '%cloth%' OR LOWER(category) LIKE '%book%'").fetchall()
if not rows:
    print('No Clothing or Book products found.')
    conn.close()
    raise SystemExit(0)

ids = [r[0] for r in rows]
print('Will remove', len(ids), 'products:')
for r in rows:
    print(f"- id={r[0]} title={r[1]} category={r[2]}")

placeholders = ','.join('?' for _ in ids)

# Delete related todos
try:
    cur.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='todos'")
    if cur.fetchone()[0]:
        deleted_todos = cur.execute(f"SELECT COUNT(*) FROM todos WHERE product_id IN ({placeholders})", ids).fetchone()[0]
        cur.execute(f"DELETE FROM todos WHERE product_id IN ({placeholders})", ids)
    else:
        deleted_todos = 0
except Exception:
    deleted_todos = 0

# Delete related favorites (if table exists and column product_id present)
try:
    cur.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='favorites'")
    if cur.fetchone()[0]:
        deleted_favs = cur.execute(f"SELECT COUNT(*) FROM favorites WHERE product_id IN ({placeholders})", ids).fetchone()[0]
        cur.execute(f"DELETE FROM favorites WHERE product_id IN ({placeholders})", ids)
    else:
        deleted_favs = 0
except Exception:
    deleted_favs = 0

# Delete related reviews
try:
    cur.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='reviews'")
    if cur.fetchone()[0]:
        deleted_reviews = cur.execute(f"SELECT COUNT(*) FROM reviews WHERE product_id IN ({placeholders})", ids).fetchone()[0]
        cur.execute(f"DELETE FROM reviews WHERE product_id IN ({placeholders})", ids)
    else:
        deleted_reviews = 0
except Exception:
    deleted_reviews = 0

# Finally delete products
deleted_products = cur.execute(f"SELECT COUNT(*) FROM products WHERE id IN ({placeholders})", ids).fetchone()[0]
cur.execute(f"DELETE FROM products WHERE id IN ({placeholders})", ids)

conn.commit()
conn.close()

print('\nDeletion summary:')
print('Products removed:', deleted_products)
print('Todos removed:', deleted_todos)
print('Favorites removed:', deleted_favs)
print('Reviews removed:', deleted_reviews)
print('Done.')
