import sqlite3
db = 'c:\\sample\\inpu\\second_hand_marketplace\\database.db'
conn = sqlite3.connect(db)
cur = conn.cursor()
rows = cur.execute("SELECT id, title, category FROM products WHERE LOWER(title) LIKE '%laptop%' OR LOWER(category) LIKE '%laptop%'").fetchall()
print(f'Found {len(rows)} laptop-related products:')
for r in rows:
    print(f'  id={r[0]} title={r[1]} category={r[2]}')
conn.close()
