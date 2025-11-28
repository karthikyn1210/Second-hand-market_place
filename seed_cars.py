"""
Seed script to add sample car data to the database
Run this script to populate the cars listing with sample data
"""

import sqlite3
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database.db")

def seed_cars():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Sample car data with realistic details
    cars = [
        ("Maruti Swift VXI 2022", "Cars", 450000, "🚗 Maruti Swift VXI | Year: 2022 | Petrol | Manual | 45,000 km | 1st Owner | Insurance Valid | Well Maintained", "swift.jpg", 1),
        ("Hyundai Creta 1.6 Diesel 2020", "Cars", 850000, "⚙️ Hyundai Creta | Year: 2020 | Diesel | Automatic | 62,000 km | 1st Owner | Excellent Condition", "creta.jpg", 1),
        ("Tata Nexon EV 2021", "Cars", 750000, "⚡ Tata Nexon EV | Year: 2021 | Electric | Automatic | 28,000 km | 1st Owner | Low Running Cost", "nexon_ev.jpg", 1),
        ("Honda City SV 2019", "Cars", 650000, "🔧 Honda City SV | Year: 2019 | Petrol | Manual | 78,000 km | 2nd Owner | Reliable & Fuel Efficient", "city.jpg", 1),
        ("Mahindra XUV500 W10 2018", "Cars", 750000, "🏎️ Mahindra XUV500 W10 | Year: 2018 | Diesel | Automatic | 95,000 km | 1st Owner | Premium Features", "xuv500.jpg", 1),
        ("Kia Seltos HTX Plus 2021", "Cars", 950000, "✨ Kia Seltos HTX Plus | Year: 2021 | Petrol | Manual | 35,000 km | 1st Owner | New Gen Technology", "seltos.jpg", 1),
        ("Skoda Superb Elegance 2017", "Cars", 1100000, "💎 Skoda Superb Elegance | Year: 2017 | Diesel | Automatic | 88,000 km | 1st Owner | Luxury Sedan", "superb.jpg", 1),
        ("Volkswagen Polo Highline 2020", "Cars", 550000, "🔷 Volkswagen Polo Highline | Year: 2020 | Petrol | Manual | 52,000 km | 1st Owner | German Engineering", "polo.jpg", 1),
        ("Toyota Fortuner 4x4 2016", "Cars", 1250000, "🛞 Toyota Fortuner 4x4 | Year: 2016 | Diesel | Manual | 125,000 km | 1st Owner | Off-Road Capable", "fortuner.jpg", 1),
        ("Renault Duster RxS 2019", "Cars", 580000, "🌟 Renault Duster RxS | Year: 2019 | Diesel | Manual | 68,000 km | 1st Owner | SUV Beast", "duster.jpg", 1),
        ("BMW 3 Series 2015", "Cars", 1400000, "🏁 BMW 3 Series | Year: 2015 | Petrol | Automatic | 110,000 km | 1st Owner | Sports Sedan", "bmw_3.jpg", 1),
        ("Audi A4 2.0 2014", "Cars", 950000, "⚡ Audi A4 2.0 | Year: 2014 | Petrol | Automatic | 135,000 km | 2nd Owner | Premium Build Quality", "audi_a4.jpg", 1),
        ("MG Hector Plus 2021", "Cars", 1050000, "🎯 MG Hector Plus | Year: 2021 | Petrol | Manual | 41,000 km | 1st Owner | AI Features", "hector.jpg", 1),
        ("Jeep Compass Limited Plus 2020", "Cars", 1200000, "🚙 Jeep Compass Limited Plus | Year: 2020 | Diesel | Manual | 55,000 km | 1st Owner | Adventure Ready", "compass.jpg", 1),
        ("Nissan Datsun GO 2018", "Cars", 350000, "🔔 Nissan Datsun GO | Year: 2018 | Petrol | Manual | 92,000 km | 2nd Owner | Budget Friendly", "datsun_go.jpg", 1),
        ("Maruti Baleno 2022", "Cars", 480000, "✔️ Maruti Baleno | Year: 2022 | Petrol | Automatic | 18,000 km | 1st Owner | Premium Hatchback", "baleno.jpg", 1),
        ("Hyundai i20 N Line 2021", "Cars", 620000, "🚀 Hyundai i20 N Line | Year: 2021 | Petrol | Manual | 33,000 km | 1st Owner | Sporty Hatchback", "i20.jpg", 1),
        ("Chevrolet Beat 2017", "Cars", 380000, "⭐ Chevrolet Beat | Year: 2017 | Petrol | Manual | 85,000 km | 1st Owner | Reliable Budget Car", "beat.jpg", 1),
        ("Force Motors Gurkha 2019", "Cars", 680000, "🦾 Force Motors Gurkha | Year: 2019 | Diesel | Manual | 62,000 km | 1st Owner | Heavy Duty SUV", "gurkha.jpg", 1),
        ("Mahindra Bolero 2020", "Cars", 520000, "🛡️ Mahindra Bolero | Year: 2020 | Diesel | Manual | 48,000 km | 1st Owner | Strong & Sturdy", "bolero.jpg", 1),
        ("Tata Harrier XT 2021", "Cars", 1150000, "🎪 Tata Harrier XT | Year: 2021 | Diesel | Automatic | 44,000 km | 1st Owner | Connected SUV", "harrier.jpg", 1),
        ("Citroen C5 Aircross 2021", "Cars", 1300000, "🌈 Citroen C5 Aircross | Year: 2021 | Petrol | Automatic | 32,000 km | 1st Owner | Comfortable SUV", "c5.jpg", 1),
        ("Mitsubishi Outlander 2015", "Cars", 850000, "🎨 Mitsubishi Outlander | Year: 2015 | Petrol | Automatic | 118,000 km | 1st Owner | Spacious SUV", "outlander.jpg", 1),
        ("Maruti Vitara Brezza 2020", "Cars", 720000, "🔥 Maruti Vitara Brezza | Year: 2020 | Diesel | Manual | 56,000 km | 1st Owner | Compact SUV", "brezza.jpg", 1),
        ("Honda BR-V 2019", "Cars", 820000, "🏠 Honda BR-V | Year: 2019 | Petrol | Manual | 74,000 km | 1st Owner | 7-Seater MPV", "br_v.jpg", 1),
        ("Mahindra TUV 300 2018", "Cars", 580000, "🚵 Mahindra TUV 300 | Year: 2018 | Diesel | Manual | 88,000 km | 1st Owner | Rugged Build", "tuv_300.jpg", 1),
        ("Hyundai Venue 2022", "Cars", 620000, "🎯 Hyundai Venue | Year: 2022 | Petrol | Manual | 22,000 km | 1st Owner | Connected Subcompact SUV", "venue.jpg", 1),
        ("Kia Sonet HTE 2021", "Cars", 780000, "💫 Kia Sonet HTE | Year: 2021 | Diesel | Manual | 41,000 km | 1st Owner | Feature-Rich Compact SUV", "sonet.jpg", 1),
        ("Renault Kwid RXT 2020", "Cars", 420000, "🎪 Renault Kwid RXT | Year: 2020 | Petrol | Manual | 65,000 km | 1st Owner | Spacious Budget Car", "kwid.jpg", 1),
        ("Volkswagen Vento Highline 2019", "Cars", 680000, "🌐 Volkswagen Vento Highline | Year: 2019 | Petrol | Manual | 71,000 km | 1st Owner | Sleek Sedan", "vento.jpg", 1),
    ]
    
    try:
        # Insert cars with staggered dates (most recent first)
        for i, car in enumerate(cars):
            title, category, price, description, image_path, user_id = car
            # Stagger the creation dates (most recent first)
            created_on = datetime.now() - timedelta(days=i)
            created_on_str = created_on.strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                "INSERT INTO products (title, category, price, description, image_path, user_id, created_on) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (title, category, price, description, image_path, user_id, created_on_str)
            )
        
        conn.commit()
        print(f"✅ Successfully added {len(cars)} sample cars to the database!")
        car_count = cursor.execute('SELECT COUNT(*) FROM products WHERE category = ?', ('Cars',)).fetchone()[0]
        print(f"   Total cars in database: {car_count}")
        
    except sqlite3.IntegrityError as e:
        print(f"⚠️  Some cars might already exist in database: {e}")
    except Exception as e:
        print(f"❌ Error seeding cars: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_cars()
