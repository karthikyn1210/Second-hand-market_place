"""
Update Electronics product images to use the newly copied electronics images from staticc/images/electronics.
Maps each electronics product to a unique electronics image.
"""
import sqlite3
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, '..', 'database.db')
UPLOADS = os.path.join(BASE, '..', 'staticc', 'uploads')

if not os.path.exists(DB):
    print('Database not found:', DB)
    raise SystemExit(1)

# gather electronics images from uploads (the ones we just copied)
all_uploads = [f for f in os.listdir(UPLOADS) if os.path.isfile(os.path.join(UPLOADS, f))]
electronics_images = [f for f in all_uploads if f.lower().endswith(('.webp', '.png', '.jpg', '.jpeg')) and any(k in f.lower() for k in ['lenovo','macbook','iphone','asus','sony','yoga','proart','wh-1000'])]
electronics_images = sorted(list(dict.fromkeys(electronics_images)))

print('Found electronics images from staticc/images/electronics:')
for img in electronics_images:
    print(f'  - {img}')

if not electronics_images:
    print('No electronics images found')
    raise SystemExit(1)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# fetch electronics products
products = cur.execute("SELECT id, title, category FROM products WHERE LOWER(category) LIKE '%electronic%'").fetchall()
print(f'\nFound {len(products)} Electronics products')

used = set()
idx = 0
assignments = {}

for p in products:
    pid = p['id']
    # pick next unused image
    chosen = None
    for i in range(len(electronics_images)):
        cand = electronics_images[(idx + i) % len(electronics_images)]
        if cand not in used:
            chosen = cand
            idx = (idx + i + 1) % len(electronics_images)
            break
    # if none unused, allow reuse by cycling
    if not chosen:
        chosen = electronics_images[idx % len(electronics_images)]
        idx += 1

    chosen_path = f"uploads/{chosen}"
    try:
        cur.execute("UPDATE products SET image_path = ? WHERE id = ?", (chosen_path, pid))
        used.add(chosen)
        assignments[pid] = chosen_path
        print(f'Product {pid} ({p["title"]}) -> {chosen_path}')
    except Exception as e:
        print(f'Error updating product {pid}: {e}')

conn.commit()
conn.close()

print(f'\nUpdated {len(assignments)} Electronics products')
print('Done.')
