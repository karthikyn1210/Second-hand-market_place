"""
Update Furniture product images to use the newly copied furniture images from staticc/images/furniture.
Maps each furniture product to a unique furniture image.
"""
import sqlite3
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, '..', 'database.db')
UPLOADS = os.path.join(BASE, '..', 'staticc', 'uploads')

if not os.path.exists(DB):
    print('Database not found:', DB)
    raise SystemExit(1)

# gather furniture images from uploads (the ones we just copied)
all_uploads = [f for f in os.listdir(UPLOADS) if os.path.isfile(os.path.join(UPLOADS, f))]
# look for files that are furniture-related or match the furniture images we copied
furniture_images = [f for f in all_uploads if f.lower().endswith(('.webp', '.png', '.jpg', '.jpeg')) and any(k in f.lower() for k in ['360_f_','walnut','dining','615','814'])]
furniture_images = sorted(list(dict.fromkeys(furniture_images)))

print('Found furniture images from staticc/images/furniture:')
for img in furniture_images:
    print(f'  - {img}')

if not furniture_images:
    print('No furniture images found')
    raise SystemExit(1)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# fetch furniture products
products = cur.execute("SELECT id, title, category FROM products WHERE LOWER(category) LIKE '%furniture%'").fetchall()
print(f'\nFound {len(products)} Furniture products')

used = set()
idx = 0
assignments = {}

for p in products:
    pid = p['id']
    # pick next unused image
    chosen = None
    for i in range(len(furniture_images)):
        cand = furniture_images[(idx + i) % len(furniture_images)]
        if cand not in used:
            chosen = cand
            idx = (idx + i + 1) % len(furniture_images)
            break
    # if none unused, allow reuse by cycling
    if not chosen:
        chosen = furniture_images[idx % len(furniture_images)]
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

print(f'\nUpdated {len(assignments)} Furniture products')
print('Done.')
