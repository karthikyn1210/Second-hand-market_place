"""
Analyze uploads folder to identify:
1. Duplicate images (same content hash)
2. Unused images (not referenced in products or todos tables)
3. Provide report and cleanup recommendations
"""
import sqlite3
import os
import hashlib
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, '..', 'database.db')
UPLOADS = os.path.join(BASE, '..', 'staticc', 'uploads')

if not os.path.exists(DB):
    print('Database not found:', DB)
    raise SystemExit(1)

# Get all files in uploads
all_files = [f for f in os.listdir(UPLOADS) if os.path.isfile(os.path.join(UPLOADS, f))]
print(f'Total files in uploads: {len(all_files)}')

# Calculate hash for each file to find duplicates
file_hashes = {}
hash_to_files = defaultdict(list)
for fname in all_files:
    fpath = os.path.join(UPLOADS, fname)
    try:
        with open(fpath, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
            file_hashes[fname] = file_hash
            hash_to_files[file_hash].append(fname)
    except Exception as e:
        print(f'Error hashing {fname}: {e}')

# Find duplicates
duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
print(f'\nDuplicate file groups found: {len(duplicates)}')
for file_hash, files in duplicates.items():
    print(f'  Hash {file_hash[:8]}... has {len(files)} copies:')
    for f in files:
        print(f'    - {f}')

# Get all images referenced in database
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Get images from products
product_images = set()
try:
    cur.execute("SELECT image_path FROM products")
    for row in cur.fetchall():
        if row[0]:
            # extract filename from path like "uploads/filename.jpg"
            fname = row[0].split('/')[-1] if '/' in row[0] else row[0]
            product_images.add(fname)
except Exception as e:
    print(f'Error reading products: {e}')

# Get images from todos
todo_images = set()
try:
    cur.execute("SELECT image_path FROM todos")
    for row in cur.fetchall():
        if row[0]:
            fname = row[0].split('/')[-1] if '/' in row[0] else row[0]
            todo_images.add(fname)
except Exception as e:
    print(f'Error reading todos: {e}')

conn.close()

referenced_images = product_images | todo_images
print(f'\nImages referenced in database: {len(referenced_images)}')

# Find unused images
unused_images = []
for fname in all_files:
    if fname not in referenced_images:
        unused_images.append(fname)

print(f'Unused images (not referenced in DB): {len(unused_images)}')
for img in sorted(unused_images):
    print(f'  - {img}')

# Images that are duplicates AND unused
duplicate_unused = []
for file_hash, files in duplicates.items():
    # keep first one, mark rest as removable
    for f in files[1:]:
        if f in unused_images:
            duplicate_unused.append(f)

print(f'\nImages that are BOTH duplicate AND unused: {len(duplicate_unused)}')
for img in sorted(duplicate_unused):
    print(f'  - {img}')

print(f'\n{len(unused_images)} unused + {len(duplicates)} duplicate groups')
print(f'Safe to remove: {len(duplicate_unused)} duplicate unused + {len(unused_images)} fully unused = {len(duplicate_unused) + len(unused_images)} images')
