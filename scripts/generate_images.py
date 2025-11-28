"""
Generate sample product images using PIL (Pillow).
Creates colorful placeholder images with product names.
"""
import os
from PIL import Image, ImageDraw, ImageFont
import random

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'staticc', 'uploads')

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define product images with colors and names
product_images = {
    'iphone12.jpg': ('iPhone 12 Pro', '#1f1f1f', '#00ff00'),
    'headphones.jpg': ('Sony Headphones', '#1a1a1a', '#ff6600'),
    'gopro.jpg': ('GoPro Camera', '#330000', '#ffff00'),
    'drone.jpg': ('DJI Drone', '#003300', '#00ff99'),
    'tv.jpg': ('Samsung TV', '#000033', '#00ccff'),
    'mtbike.jpg': ('Mountain Bike', '#330033', '#ff0066'),
    'roadbike.jpg': ('Road Bike', '#003333', '#ffcc00'),
    'bmx.jpg': ('BMX Bike', '#330000', '#ff9900'),
    'ebike.jpg': ('E-Bike', '#003300', '#66ff00'),
    'kidbike.jpg': ('Kids Bike', '#330033', '#ff00cc'),
    'macbook.jpg': ('MacBook Pro', '#1a1a1a', '#cccccc'),
    'xps.jpg': ('Dell XPS', '#000033', '#00ffff'),
    'gaming_laptop.jpg': ('Gaming Laptop', '#330000', '#ff0000'),
    'desktop.jpg': ('Desktop PC', '#1a1a1a', '#00ff00'),
    'ipad.jpg': ('iPad Pro', '#001a33', '#ffff99'),
    'civic.jpg': ('Honda Civic', '#1a0000', '#ff3333'),
    'corolla.jpg': ('Toyota Corolla', '#000033', '#3399ff'),
    'swift.jpg': ('Maruti Swift', '#330000', '#ff9900'),
    'xuv500.jpg': ('Mahindra XUV', '#003300', '#00ff99'),
    'pulsar.jpg': ('Bajaj Pulsar', '#1a0000', '#ff6666'),
    'dining_set.jpg': ('Dining Table', '#4d2600', '#ffcc99'),
    'sofa.jpg': ('L-Shaped Sofa', '#3d2817', '#cc9966'),
    'desk.jpg': ('Office Desk', '#2d1f0d', '#ffcc99'),
    'bed.jpg': ('King Bed', '#4d3d33', '#ff9999'),
    'bookshelf.jpg': ('Bookshelf', '#3d2817', '#cc9966'),
    'jacket.jpg': ('Winter Jacket', '#1a1a1a', '#ff6666'),
    'jeans.jpg': ('Denim Jeans', '#001f4d', '#6699ff'),
    'shoes.jpg': ('Nike Air Max', '#ffffff', '#ff0000'),
    'shirt.jpg': ('Formal Shirt', '#f2f2f2', '#3333ff'),
    'sweater.jpg': ('Woolen Sweater', '#660000', '#ff6666'),
    'gatsby.jpg': ('The Great Gatsby', '#1a0d00', '#ffcc99'),
    'python_book.jpg': ('Python Book', '#003300', '#ffff99'),
    'sapiens.jpg': ('Sapiens', '#330000', '#ffff00'),
    'habits.jpg': ('Atomic Habits', '#003366', '#00ffff'),
    'harrypotter.jpg': ('Harry Potter', '#330000', '#ffcc00'),
    'fitbit.jpg': ('Fitbit Watch', '#1a0d00', '#ff6666'),
    'charger.jpg': ('Wireless Charger', '#1a1a1a', '#00ff00'),
    'stand.jpg': ('Phone Stand', '#4d4d4d', '#cccccc'),
    'camera_bag.jpg': ('Camera Bag', '#3d2817', '#cc9966'),
    'powerbank.jpg': ('Power Bank', '#330000', '#ffff00'),
    'ps5.jpg': ('PlayStation 5', '#000033', '#00ffff'),
    'vintage_camera.jpg': ('Vintage Camera', '#1a0d00', '#ffcc99'),
    'espresso.jpg': ('Espresso Machine', '#3d2817', '#cc9966'),
    'purifier.jpg': ('Air Purifier', '#f2f2f2', '#3333ff'),
    'telescope.jpg': ('Telescope', '#000000', '#ffff00'),
}

def generate_product_image(filename, title, bg_color, text_color):
    """Generate a simple product image with title."""
    # Create image: 400x300 pixels
    img = Image.new('RGB', (400, 300), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default
    try:
        font = ImageFont.truetype('arial.ttf', 40)
        font_small = ImageFont.truetype('arial.ttf', 20)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw decorative elements
    draw.rectangle([50, 50, 350, 250], outline=text_color, width=3)
    draw.ellipse([120, 80, 280, 200], fill=text_color, outline=text_color)
    
    # Add text
    # Wrap text if too long
    words = title.split()
    if len(words) > 2:
        line1 = ' '.join(words[:len(words)//2])
        line2 = ' '.join(words[len(words)//2:])
        bbox1 = draw.textbbox((0, 0), line1, font=font)
        w1 = bbox1[2] - bbox1[0]
        bbox2 = draw.textbbox((0, 0), line2, font=font)
        w2 = bbox2[2] - bbox2[0]
        draw.text(((400 - w1) // 2, 110), line1, fill=text_color, font=font)
        draw.text(((400 - w2) // 2, 160), line2, fill=text_color, font=font)
    else:
        bbox = draw.textbbox((0, 0), title, font=font)
        w = bbox[2] - bbox[0]
        draw.text(((400 - w) // 2, 130), title, fill=text_color, font=font)
    
    draw.text((10, 270), "Second-Hand", fill=text_color, font=font_small)
    
    # Save image
    img.save(os.path.join(UPLOAD_FOLDER, filename))
    print(f"✓ Generated: {filename}")

def generate_all_images():
    """Generate all product images."""
    for filename, (title, bg_color, text_color) in product_images.items():
        try:
            generate_product_image(filename, title, bg_color, text_color)
        except Exception as e:
            print(f"✗ Failed to generate {filename}: {e}")

if __name__ == '__main__':
    print(f"Generating product images in: {UPLOAD_FOLDER}")
    generate_all_images()
    print(f"✓ All images generated successfully!")
