"""
Populate `todos` table with products in categories Cars and Bikes, assigning unique images.
This script will:
- Read products where category contains 'car' or 'bike' (case-insensitive)
- Build todos entries referencing those products
- Ensure no two todos use the same image (falls back to cycling through uploads)
- Skip products that already have a todo (avoid duplicates)
"""

import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'database.db')
UPLOADS_DIR = os.path.join(BASE_DIR, '..', 'staticc', 'uploads')

if not os.path.exists(DB_PATH):
    print("Database not found:", DB_PATH)
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Gather available upload image filenames
available_images = [f for f in os.listdir(UPLOADS_DIR) if os.path.isfile(os.path.join(UPLOADS_DIR, f))]
if not available_images:
    print("No images found in uploads folder", UPLOADS_DIR)
    conn.close()
    raise SystemExit(1)

# Normalize: store as 'uploads/<filename>' when saving to DB
available_paths = [f"uploads/{f}" for f in available_images]

# Build used_images from existing todos
used_rows = cursor.execute("SELECT image_path FROM todos WHERE image_path IS NOT NULL").fetchall()
used_images = set(r[0] for r in used_rows if r[0])

# Get products that are cars or bikes
products = cursor.execute("SELECT id, title, category, price, description, image_path FROM products WHERE LOWER(category) LIKE '%car%' OR LOWER(category) LIKE '%bike%'").fetchall()

print(f"Found {len(products)} candidate products (cars/bikes).")

inserted = 0
cycle_idx = 0
for p in products:
    pid = p['id']
    title = p['title']
    category = p['category'] or ''
    price = p['price']
    desc = p['description']
    prod_img = p['image_path']

    # Skip if a todo for this product already exists
    exists = cursor.execute("SELECT 1 FROM todos WHERE product_id = ?", (pid,)).fetchone()
    if exists:
        print(f"Skipping product {pid} (todo exists)")
        continue

    chosen = None
    # Try product image if present and not used
    if prod_img:
        norm = prod_img if prod_img.startswith('uploads/') else prod_img
        if norm not in used_images and os.path.exists(os.path.join(UPLOADS_DIR, os.path.basename(norm))):
            chosen = norm

    # Otherwise pick next available upload that isn't used
    if not chosen:
        for i in range(len(available_paths)):
            idx = (cycle_idx + i) % len(available_paths)
            candidate = available_paths[idx]
            if candidate not in used_images:
                chosen = candidate
                cycle_idx = idx + 1
                break

    if not chosen:
        print(f"No unused images available for product {pid} - {title}")
        continue

    # Determine item_type from category string
    cat_lower = (category or '').lower()
    if 'bike' in cat_lower:
        item_type = 'Bike'
    else:
        item_type = 'Car'

    now = datetime.utcnow().isoformat()
    try:
        cursor.execute(
            "INSERT INTO todos (user_id, title, category, item_type, price, description, image_path, status, created_on, updated_on, product_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (1, title, category, item_type, float(price) if price else 0.0, desc, chosen, 'pending', now, now, pid)
        )
        used_images.add(chosen)
        inserted += 1
        print(f"Inserted todo for product {pid}: {title} -> {chosen}")
    except Exception as e:
        print(f"Error inserting todo for product {pid}: {e}")

conn.commit()
conn.close()
print(f"\nDone. Inserted {inserted} todos.")
