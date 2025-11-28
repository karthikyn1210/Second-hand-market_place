"""
Replace bike product and todo images with images from staticc/images/bike (already copied to staticc/uploads as bike_...)
- Assign each bike product a unique bike image when possible
- Update todos (item_type='Bike') to reference the product image (if product_id present), otherwise assign a remaining unique bike image
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

# gather bike images available in uploads
all_uploads = [f for f in os.listdir(UPLOADS) if os.path.isfile(os.path.join(UPLOADS, f))]
# consider images that look like bike images: start with 'bike_' or contain 'bike' or named ebike/mtbike/roadbike/bmx/pulsar
bike_candidates = [f for f in all_uploads if f.lower().startswith('bike_') or 'bike' in f.lower() or any(k in f.lower() for k in ['ebike','mtbike','roadbike','bmx','pulsar','yamaha','kidbike'])]
# dedupe and keep stable order
bike_candidates = sorted(list(dict.fromkeys(bike_candidates)))

if not bike_candidates:
    print('No bike candidate images found in uploads folder')
    raise SystemExit(1)

print('Found bike images:', bike_candidates)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# fetch bike products
products = cur.execute("SELECT id, title, category, image_path FROM products WHERE LOWER(category) LIKE '%bike%' OR LOWER(category) LIKE '%bikes%'").fetchall()
print('Found', len(products), 'bike products')

used = set()
assignments = {}
idx = 0
for p in products:
    pid = p['id']
    # pick next unused bike image
    chosen = None
    for i in range(len(bike_candidates)):
        cand = bike_candidates[(idx + i) % len(bike_candidates)]
        if cand not in used:
            chosen = cand
            idx = (idx + i + 1) % len(bike_candidates)
            break
    # if none unused (more products than images), allow reuse by cycling
    if not chosen:
        chosen = bike_candidates[idx % len(bike_candidates)]
        idx += 1

    chosen_path = f"uploads/{chosen}"
    try:
        cur.execute("UPDATE products SET image_path = ? WHERE id = ?", (chosen_path, pid))
        used.add(chosen)
        assignments[pid] = chosen_path
        print(f'Product {pid} -> {chosen_path}')
    except Exception as e:
        print('Error updating product', pid, e)

conn.commit()

# Update todos where item_type = 'Bike'
bike_todos = cur.execute("SELECT id, product_id FROM todos WHERE LOWER(item_type) = 'bike'").fetchall()
print('Found', len(bike_todos), 'bike todos')

todo_assignments = {}
for t in bike_todos:
    tid = t['id']
    pid = t['product_id']
    new_img = None
    # prefer product image if product_id exists and was updated
    if pid and pid in assignments:
        new_img = assignments[pid]
    else:
        # pick any unused bike image
        chosen = None
        for cand in bike_candidates:
            if cand not in used:
                chosen = cand
                break
        if not chosen:
            # if all used, just reuse round-robin
            chosen = bike_candidates[idx % len(bike_candidates)]
            idx += 1
        new_img = f"uploads/{chosen}"
        used.add(chosen)

    try:
        cur.execute("UPDATE todos SET image_path = ? WHERE id = ?", (new_img, tid))
        todo_assignments[tid] = new_img
        print(f'Todo {tid} -> {new_img}')
    except Exception as e:
        print('Error updating todo', tid, e)

conn.commit()
conn.close()

print('\nSummary:')
print('Products updated:', len(assignments))
print('Todos updated:', len(todo_assignments))
print('Done.')
