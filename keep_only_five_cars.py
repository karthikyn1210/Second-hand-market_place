"""
Keep only the first 5 car products and delete the rest.
Also delete any todos associated with removed cars.
"""
import sqlite3
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, '..', 'database.db')

if not os.path.exists(DB):
    print('Database not found:', DB)
    raise SystemExit(1)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Get all cars ordered by ID
all_cars = cur.execute("SELECT id FROM products WHERE LOWER(category) = 'cars' ORDER BY id").fetchall()
print(f'Total cars in database: {len(all_cars)}')

if len(all_cars) <= 5:
    print('Already 5 or fewer cars. No deletion needed.')
    conn.close()
    raise SystemExit(0)

# Keep first 5, delete the rest
keep_ids = [car['id'] for car in all_cars[:5]]
delete_ids = [car['id'] for car in all_cars[5:]]

print(f'\nKeeping cars with IDs: {keep_ids}')
print(f'Deleting cars with IDs: {delete_ids}')

# Delete todos associated with deleted cars
placeholders = ','.join('?' for _ in delete_ids)
try:
    cur.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='todos'")
    if cur.fetchone()[0]:
        deleted_todos = cur.execute(f"DELETE FROM todos WHERE product_id IN ({placeholders})", delete_ids).rowcount
        print(f'Deleted {deleted_todos} todos associated with removed cars')
except Exception as e:
    print(f'Error deleting todos: {e}')

# Delete the car products
deleted_products = cur.execute(f"DELETE FROM products WHERE id IN ({placeholders})", delete_ids).rowcount
print(f'Deleted {deleted_products} car products')

conn.commit()
conn.close()

print(f'\nFinal result: {len(keep_ids)} cars remaining in database')
print('Done.')
