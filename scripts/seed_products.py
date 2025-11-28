"""
Seed script: Add diverse second-hand products to the database.
Categories: Electronics, Bikes, PCs, Cars, Furniture, Clothing, Books, Accessories, Other
"""
import sqlite3
from datetime import datetime, timedelta
import os

DB = 'database.db'

products = [
    # Electronics
    ("iPhone 12 Pro - Excellent Condition", "Electronics", 450.00, "Mint condition iPhone 12 Pro 128GB Space Gray. All original box and accessories included. No scratches.", "uploads/iphone12.jpg", 1),
    ("Sony WH-1000XM4 Headphones", "Electronics", 180.00, "Premium noise-cancelling wireless headphones. Barely used. Great sound quality.", "uploads/headphones.jpg", 1),
    ("GoPro Hero 11 Action Camera", "Electronics", 250.00, "Waterproof 4K action camera with mounts. Original packaging and 2 batteries included.", "uploads/gopro.jpg", 1),
    ("DJI Mini 3 Drone", "Electronics", 320.00, "Compact 4K drone, excellent for travel. Comes with controller and 2 batteries.", "uploads/drone.jpg", 1),
    ("Samsung 65\" 4K TV", "Electronics", 380.00, "65-inch QLED Smart TV, 2022 model. Excellent picture quality. Remote included.", "uploads/tv.jpg", 1),
    
    # Bikes
    ("Trek Mountain Bike - 21 Speed", "Bikes", 220.00, "21-speed mountain bike, perfect for trails. Recently serviced, all gears work smoothly.", "uploads/mtbike.jpg", 1),
    ("Giant Road Bike - Carbon Frame", "Bikes", 450.00, "Premium carbon frame road bike, 16-speed Shimano gears. Almost like new.", "uploads/roadbike.jpg", 1),
    ("BMX Stunt Bike - Professional", "Bikes", 150.00, "High-quality BMX bike for tricks. Great for beginners and experienced riders.", "uploads/bmx.jpg", 1),
    ("Electric Bike - 40km Range", "Bikes", 680.00, "E-bike with 40km electric range on single charge. Lightweight and easy to fold.", "uploads/ebike.jpg", 1),
    ("Children's Bicycle - 20 Inch", "Bikes", 75.00, "Kids' bike with training wheels. Bright blue color, safe and sturdy.", "uploads/kidbike.jpg", 1),
    
    # PCs & Laptops
    ("MacBook Pro 14\" M2 - 2023", "Laptops", 1200.00, "MacBook Pro 14-inch M2 Pro, 16GB RAM, 512GB SSD. Pristine condition, AppleCare+ included.", "uploads/macbook.jpg", 1),
    ("Dell XPS 13 Laptop", "Laptops", 650.00, "Intel i7, 16GB RAM, 512GB SSD. Great for work and gaming. Includes original charger.", "uploads/xps.jpg", 1),
    ("Gaming Laptop - ASUS ROG", "Laptops", 900.00, "ASUS ROG with RTX 3060, i7-11th Gen, 16GB RAM. Perfect for gaming and content creation.", "uploads/gaming_laptop.jpg", 1),
    ("Desktop PC - High Performance", "Laptops", 750.00, "Custom built PC: i9-12900K, RTX 3080Ti, 32GB RAM, 1TB SSD. Gaming & streaming ready.", "uploads/desktop.jpg", 1),
    ("iPad Pro 12.9 - 256GB", "Laptops", 480.00, "iPad Pro 12.9-inch M1 chip, 256GB storage. Perfect for design and productivity.", "uploads/ipad.jpg", 1),
    
    # Cars & Vehicles
    ("Honda Civic 2015 - Automatic", "Cars", 8500.00, "Well-maintained Honda Civic, 85,000 km. Clean interior, no major issues. Service records available.", "uploads/civic.jpg", 1),
    ("Toyota Corolla 2018 - Sedan", "Cars", 10200.00, "Toyota Corolla automatic, 72,000 km. Single owner, excellent fuel efficiency.", "uploads/corolla.jpg", 1),
    ("Maruti Swift 2016 - Family Car", "Cars", 6800.00, "Affordable family car, 95,000 km. Well-maintained, good mileage, no accidents.", "uploads/swift.jpg", 1),
    ("Mahindra XUV500 SUV 2017", "Cars", 11500.00, "Spacious SUV, 78,000 km, auto transmission. Great for family trips and city driving.", "uploads/xuv500.jpg", 1),
    ("Bajaj Pulsar Bike 2019", "Cars", 4200.00, "Sporty bike, 35,000 km, well-maintained engine. Good mileage, perfect condition.", "uploads/pulsar.jpg", 1),
    
    # Furniture
    ("Wooden Dining Table Set - 6 Seater", "Furniture", 320.00, "Solid wood dining table with 6 chairs. Modern design, great condition.", "uploads/dining_set.jpg", 1),
    ("L-Shaped Sofa - Grey Fabric", "Furniture", 450.00, "Comfortable 5-seater L-shaped sofa, grey fabric. Perfect for living room.", "uploads/sofa.jpg", 1),
    ("Office Desk - Computer Desk", "Furniture", 150.00, "Modern computer desk with shelf, suitable for home office. Sturdy and spacious.", "uploads/desk.jpg", 1),
    ("King Size Bed Frame with Mattress", "Furniture", 380.00, "Wooden bed frame with premium memory foam mattress. Excellent comfort and support.", "uploads/bed.jpg", 1),
    ("Bookshelf - 5 Tier Storage", "Furniture", 95.00, "5-tier bookshelf, wooden construction. Perfect for organizing books and décor.", "uploads/bookshelf.jpg", 1),
    
    # Clothing
    ("Winter Jacket - Men's XL", "Clothing", 65.00, "Warm winter jacket, barely worn. Waterproof, windproof, perfect for cold seasons.", "uploads/jacket.jpg", 1),
    ("Designer Jeans - Branded", "Clothing", 45.00, "Premium denim jeans, original brand, perfect fit. Hardly used.", "uploads/jeans.jpg", 1),
    ("Sports Shoes - Nike Air Max", "Clothing", 75.00, "Nike Air Max running shoes, size 10. Comfortable and stylish.", "uploads/shoes.jpg", 1),
    ("Formal Shirt - Cotton", "Clothing", 25.00, "Quality cotton formal shirt, white color. Perfect for office wear.", "uploads/shirt.jpg", 1),
    ("Woolen Sweater - Burgundy", "Clothing", 35.00, "Cozy woolen sweater, perfect for winter. Excellent condition.", "uploads/sweater.jpg", 1),
    
    # Books
    ("The Great Gatsby - Classic Fiction", "Books", 12.00, "Original hardcover edition, great condition. A timeless classic.", "uploads/gatsby.jpg", 1),
    ("Python Programming - Technical", "Books", 28.00, "Learn Python guide, comprehensive book for beginners and intermediates.", "uploads/python_book.jpg", 1),
    ("Sapiens by Yuval Noah Harari", "Books", 18.00, "Fascinating history of humankind. Lightly used, hardcover.", "uploads/sapiens.jpg", 1),
    ("Atomic Habits - Self Improvement", "Books", 20.00, "Popular self-help book on building good habits. Excellent condition.", "uploads/habits.jpg", 1),
    ("Harry Potter Collection - 7 Books", "Books", 55.00, "Complete Harry Potter series, hardcover collection. Perfect for fans.", "uploads/harrypotter.jpg", 1),
    
    # Accessories
    ("Smart Watch - Fitbit", "Accessories", 120.00, "Fitbit smartwatch with heart rate monitor. Tracks fitness and sleep. Like new.", "uploads/fitbit.jpg", 1),
    ("Wireless Charger - Fast Charging", "Accessories", 28.00, "15W fast wireless charger for phones. Works with all Qi-enabled devices.", "uploads/charger.jpg", 1),
    ("Phone Stand - Desktop", "Accessories", 15.00, "Adjustable phone stand for desk. Aluminum construction, stable and sleek.", "uploads/stand.jpg", 1),
    ("Camera Bag - Professional", "Accessories", 65.00, "Spacious camera bag with protective padding. Organizer for lenses and accessories.", "uploads/camera_bag.jpg", 1),
    ("Portable Power Bank - 30000mAh", "Accessories", 45.00, "High-capacity power bank, fast charging support. Charges phone 5+ times.", "uploads/powerbank.jpg", 1),
    
    # Other
    ("Gaming Console - PlayStation 5", "Other", 450.00, "PS5 with 2 controllers and 3 games. Excellent condition, all accessories included.", "uploads/ps5.jpg", 1),
    ("Vintage Camera - Canon AE-1", "Other", 180.00, "Classic film camera, fully functional. Great for photography enthusiasts.", "uploads/vintage_camera.jpg", 1),
    ("Coffee Maker - Espresso Machine", "Other", 140.00, "Semi-automatic espresso machine. Makes great coffee, easy to clean.", "uploads/espresso.jpg", 1),
    ("Air Purifier - HEPA Filter", "Other", 95.00, "HEPA air purifier for rooms up to 500 sq ft. Removes 99% allergens.", "uploads/purifier.jpg", 1),
    ("Telescope - Beginner Friendly", "Other", 85.00, "Entry-level telescope for stargazing. Good optical quality, easy to set up.", "uploads/telescope.jpg", 1),
]

def seed_products():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    
    # Get current time and create staggered timestamps
    base_time = datetime.utcnow()
    
    inserted = 0
    for i, (title, category, price, description, image_path, user_id) in enumerate(products):
        # Stagger creation times (each product 1 day earlier)
        created_on = (base_time - timedelta(days=i)).isoformat()
        try:
            cur.execute("""
                INSERT INTO products (title, category, price, description, image_path, user_id, created_on)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (title, category, price, description, image_path, user_id, created_on))
            inserted += 1
        except sqlite3.IntegrityError as e:
            print(f"Skipped: {title} (likely duplicate)")
    
    conn.commit()
    conn.close()
    print(f"✓ Inserted {inserted}/{len(products)} products into database")

if __name__ == '__main__':
    seed_products()
