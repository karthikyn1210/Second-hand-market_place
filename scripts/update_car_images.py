"""
Update car images in database to use actual image files from staticc/images folder
"""

import sqlite3
import os
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database.db")
UPLOADS_DIR = os.path.join(BASE_DIR, "..", "staticc", "uploads")

# Map car keywords to available image files
image_mapping = {
    "Swift": "swift.jpg",
    "Creta": "corolla.jpg",  # Using corolla as substitute
    "Nexon EV": "ebike.jpg",  # Using ebike as substitute (electric theme)
    "City": "civic.jpg",
    "XUV500": "xuv500.jpg",
    "Seltos": "corolla.jpg",
    "Superb": "desktop.jpg",  # Premium sedan
    "Polo": "jeans.jpg",  # Compact car
    "Fortuner": "gaming_laptop.jpg",  # Large/premium
    "Duster": "mtbike.jpg",  # Rugged/outdoor
    "BMW": "laptop.jpg",  # Premium
    "Audi": "macbook.jpg",  # Premium
    "Hector": "ipad.jpg",
    "Compass": "drone.jpg",  # Adventure theme
    "Datsun GO": "phone.jpg",  # Budget
    "Baleno": "jeans.jpg",  # Compact
    "i20": "headphones.jpg",
    "Beat": "powerbank.jpg",
    "Gurkha": "mtbike.jpg",  # Rugged
    "Bolero": "sofa.jpg",  # Strong
    "Harrier": "drone.jpg",
    "C5": "gaming_laptop.jpg",
    "Outlander": "desktop.jpg",
    "Brezza": "tablet.jpg",
    "BR-V": "ipad.jpg",
    "TUV 300": "charger.jpg",
    "Venue": "fitbit.jpg",
    "Sonet": "powerbank.jpg",
    "Kwid": "shirt.jpg",
    "Vento": "jeans.jpg",
}

# Real available images
available_images = [
    "bed.jpg", "bmx.jpg", "bookshelf.jpg", "camera_bag.jpg", "charger.jpg",
    "civic.jpg", "corolla.jpg", "desk.jpg", "desktop.jpg", "dining_set.jpg",
    "drone.jpg", "ebike.jpg", "espresso.jpg", "fitbit.jpg", "gaming_laptop.jpg",
    "gatsby.jpg", "gopro.jpg", "habits.jpg", "harrypotter.jpg", "headphones.jpg",
    "ipad.jpg", "iphone12.jpg", "jacket.jpg", "jeans.jpg", "kidbike.jpg",
    "macbook.jpg", "mtbike.jpg", "powerbank.jpg", "ps5.jpg", "pulsar.jpg",
    "purifier.jpg", "python_book.jpg", "roadbike.jpg", "sapiens.jpg", "shirt.jpg",
    "shoes.jpg", "sofa.jpg", "stand.jpg", "sweater.jpg", "swift.jpg",
    "telescope.jpg", "tv.jpg", "vintage_camera.jpg", "xps.jpg", "xuv500.jpg"
]

# Cycle through available images
image_list = available_images.copy()
image_idx = 0

def get_next_image():
    global image_idx
    img = image_list[image_idx % len(image_list)]
    image_idx += 1
    return img

def update_car_images():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get all cars
        cars = cursor.execute("SELECT id, title FROM products WHERE category = 'Cars'").fetchall()
        
        print(f"📸 Updating {len(cars)} car images...")
        
        updated_count = 0
        for car_id, title in cars:
            # Find a matching image
            image_file = None
            for keyword, img in image_mapping.items():
                if keyword.lower() in title.lower():
                    image_file = img
                    break
            
            # If no match found, use next available image
            if not image_file:
                image_file = get_next_image()
            
            # Verify image exists
            image_path = os.path.join(UPLOADS_DIR, image_file)
            if os.path.exists(image_path):
                # Update database
                cursor.execute(
                    "UPDATE products SET image_path = ? WHERE id = ?",
                    (f"uploads/{image_file}", car_id)
                )
                updated_count += 1
                print(f"  ✅ Car {car_id} ({title}) → {image_file}")
            else:
                print(f"  ⚠️  Image not found: {image_file}")
        
        conn.commit()
        print(f"\n✨ Successfully updated {updated_count} car images!")
        
    except Exception as e:
        print(f"❌ Error updating images: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_car_images()
