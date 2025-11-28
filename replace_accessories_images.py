"""
Update Accessories product images to use the newly copied images from staticc/images/others.
Maps each accessories product to a unique image from the others folder.
"""
import sqlite3
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, '..', 'database.db')
UPLOADS = os.path.join(BASE, '..', 'staticc', 'uploads')

if not os.path.exists(DB):
    print('Database not found:', DB)
    raise SystemExit(1)

# gather images from others folder that were just copied
all_uploads = [f for f in os.listdir(UPLOADS) if os.path.isfile(os.path.join(UPLOADS, f))]
# look for files from others folder: air-purifier, coffee, telescope, photo-, dr-luttke
others_images = [f for f in all_uploads if f.lower().endswith(('.webp', '.png', '.jpg', '.jpeg')) and any(k in f.lower() for k in ['air-purifier','coffee','telescope','photo-','dr-luttke','skywatcher'])]
others_images = sorted(list(dict.fromkeys(others_images)))

print('Found images from staticc/images/others:')
for img in others_images:
    print(f'  - {img}')

if not others_images:
    print('No others images found')
    raise SystemExit(1)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# fetch accessories products
products = cur.execute("SELECT id, title, category FROM products WHERE LOWER(category) LIKE '%accessori%'").fetchall()
print(f'\nFound {len(products)} Accessories products')

used = set()
idx = 0
assignments = {}

for p in products:
    pid = p['id']
    # pick next unused image
    chosen = None
    for i in range(len(others_images)):
        cand = others_images[(idx + i) % len(others_images)]
        if cand not in used:
            chosen = cand
            idx = (idx + i + 1) % len(others_images)
            break
    # if none unused, allow reuse by cycling
    if not chosen:
        chosen = others_images[idx % len(others_images)]
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

print(f'\nUpdated {len(assignments)} Accessories products')
print('Done.')
