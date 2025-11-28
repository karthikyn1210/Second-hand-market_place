"""
Remove unused images from uploads folder.
These images are not referenced in products or todos tables.
"""
import sqlite3
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, '..', 'database.db')
UPLOADS = os.path.join(BASE, '..', 'staticc', 'uploads')

if not os.path.exists(DB):
    print('Database not found:', DB)
    raise SystemExit(1)

# Get all files in uploads
all_files = [f for f in os.listdir(UPLOADS) if os.path.isfile(os.path.join(UPLOADS, f))]

# Get all images referenced in database
conn = sqlite3.connect(DB)
cur = conn.cursor()

referenced_images = set()
try:
    cur.execute("SELECT image_path FROM products")
    for row in cur.fetchall():
        if row[0]:
            fname = row[0].split('/')[-1] if '/' in row[0] else row[0]
            referenced_images.add(fname)
    
    cur.execute("SELECT image_path FROM todos")
    for row in cur.fetchall():
        if row[0]:
            fname = row[0].split('/')[-1] if '/' in row[0] else row[0]
            referenced_images.add(fname)
except Exception as e:
    print(f'Error reading database: {e}')
    conn.close()
    raise SystemExit(1)

conn.close()

# Find unused images
unused_images = [f for f in all_files if f not in referenced_images]

print(f'Found {len(unused_images)} unused images to remove:')
for img in sorted(unused_images):
    print(f'  - {img}')

# Remove them
removed_count = 0
for img in unused_images:
    fpath = os.path.join(UPLOADS, img)
    try:
        os.remove(fpath)
        removed_count += 1
        print(f'Removed: {img}')
    except Exception as e:
        print(f'Error removing {img}: {e}')

print(f'\nRemoved {removed_count} unused images')
print(f'Remaining: {len(all_files) - removed_count} images in uploads')
print('Done.')
