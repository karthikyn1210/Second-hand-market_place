"""
Replace product images for Electronics, Furniture, and Others categories 
using available images from staticc/images/{electronics,furniture,others}.
- Maps each product in these categories to unique images from the corresponding folders (uploaded versions).
"""
import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, '..', 'database.db')
UPLOADS = os.path.join(BASE, '..', 'staticc', 'uploads')

if not os.path.exists(DB):
    print('Database not found:', DB)
    raise SystemExit(1)

# gather available images by category
all_uploads = [f for f in os.listdir(UPLOADS) if os.path.isfile(os.path.join(UPLOADS, f))]

# Electronics images: start with 'electronics_' or contain names from electronics folder
electronics_images = [f for f in all_uploads if f.lower().startswith('electronics_') or any(k.lower() in f.lower() for k in ['lenovo','macbook','iphone','asus','sony','airpods','laptop','phone','headphones'])]
electronics_images = sorted(list(dict.fromkeys(electronics_images)))

# Furniture images: start with 'furniture_' or contain names from furniture folder
furniture_images = [f for f in all_uploads if f.lower().startswith('furniture_') or any(k.lower() in f.lower() for k in ['table','chair','sofa','bed','walnut','dining','cabinet'])]
furniture_images = sorted(list(dict.fromkeys(furniture_images)))

# Others images: start with 'others_' or contain names from others folder
others_images = [f for f in all_uploads if f.lower().startswith('others_') or any(k.lower() in f.lower() for k in ['purifier','telescope','coffee','maker','filter','dust'])]
others_images = sorted(list(dict.fromkeys(others_images)))

print('Found electronics images:', len(electronics_images), electronics_images[:3] if electronics_images else 'NONE')
print('Found furniture images:', len(furniture_images), furniture_images[:3] if furniture_images else 'NONE')
print('Found others images:', len(others_images), others_images[:3] if others_images else 'NONE')

if not electronics_images and not furniture_images and not others_images:
    print('No images found for these categories')
    raise SystemExit(1)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Mapping of category to image candidates
category_images = {
    'Electronics': electronics_images,
    'Furniture': furniture_images,
    'Other': others_images,
}

assignments = {}
total_products = 0
total_todos = 0

for category_name, image_list in category_images.items():
    if not image_list:
        print(f'Skipping {category_name} (no images)')
        continue

    # fetch products in this category
    products = cur.execute(f"SELECT id, title, category FROM products WHERE LOWER(category) LIKE ?", (f'%{category_name.lower()}%',)).fetchall()
    print(f'\nFound {len(products)} {category_name} products')

    used = set()
    idx = 0
    product_image_map = {}
    
    for p in products:
        pid = p['id']
        # pick next unused image
        chosen = None
        for i in range(len(image_list)):
            cand = image_list[(idx + i) % len(image_list)]
            if cand not in used:
                chosen = cand
                idx = (idx + i + 1) % len(image_list)
                break
        # if none unused, allow reuse by cycling
        if not chosen:
            chosen = image_list[idx % len(image_list)]
            idx += 1

        chosen_path = f"uploads/{chosen}"
        try:
            cur.execute("UPDATE products SET image_path = ? WHERE id = ?", (chosen_path, pid))
            used.add(chosen)
            product_image_map[pid] = chosen_path
            assignments[pid] = chosen_path
            total_products += 1
            print(f'  Product {pid} ({p["title"]}) -> {chosen_path}')
        except Exception as e:
            print(f'  Error updating product {pid}: {e}')

    # Update todos for this category
    todos = cur.execute(f"SELECT id, product_id FROM todos WHERE LOWER(item_type) = ?", (category_name.lower(),)).fetchall()
    print(f'Found {len(todos)} {category_name} todos')
    
    for t in todos:
        tid = t['id']
        pid = t['product_id']
        new_img = None
        
        # prefer product image if product_id exists and was mapped
        if pid and pid in product_image_map:
            new_img = product_image_map[pid]
        else:
            # pick any unused image
            chosen = None
            for cand in image_list:
                if cand not in used:
                    chosen = cand
                    break
            if not chosen:
                # if all used, just reuse round-robin
                chosen = image_list[idx % len(image_list)]
                idx += 1
            new_img = f"uploads/{chosen}"
            used.add(chosen)

        try:
            cur.execute("UPDATE todos SET image_path = ? WHERE id = ?", (new_img, tid))
            total_todos += 1
            print(f'  Todo {tid} -> {new_img}')
        except Exception as e:
            print(f'  Error updating todo {tid}: {e}')

conn.commit()
conn.close()

print('\n' + '='*60)
print('SUMMARY:')
print(f'Products updated: {total_products}')
print(f'Todos updated: {total_todos}')
print('Done.')
