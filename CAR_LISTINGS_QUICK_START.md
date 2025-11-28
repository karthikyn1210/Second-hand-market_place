# 🚗 Car Listings - Quick Start Guide

## Getting Started

### 1. If app is already running
Skip to step 3 - just open your browser!

### 2. Start the app (first time or after reboot)
```powershell
cd c:\sample\inpu\second_hand_marketplace
.venv\Scripts\python.exe app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### 3. View Car Listings
Visit: **http://127.0.0.1:5000/cars**

---

## 🎯 Quick Features

### Filter by Brand
- Type "Maruti", "Hyundai", "BMW", etc.
- Click "Apply Filters"

### Filter by Price
- Set Min: ₹400,000
- Set Max: ₹800,000
- Click "Apply Filters"

### Filter by Fuel Type
- Select from dropdown: Petrol, Diesel, Electric, Hybrid, LPG
- Click "Apply Filters"

### Filter by Year
- Set From: 2020
- Set To: 2024
- Click "Apply Filters"

### Sort Results
- Click dropdown: "Latest Listings", "Price: Low to High", "Price: High to Low"

### View Car Details
- Click "👁️ View Details" on any car card
- See full specs, seller info, reviews
- Check similar cars below

### Add Car to Cart
- Click "🛒 Add to Cart"
- Go to 🛒 Cart in navbar
- Proceed to checkout

### Save to Favorites
- Click "❤️ Save Fav" on detail page
- View later from your profile

---

## 🔗 Direct URLs

**View all cars**: http://127.0.0.1:5000/cars

**View specific car**: http://127.0.0.1:5000/car/77

**Filter by brand**: http://127.0.0.1:5000/cars?brand=Maruti

**Filter by price range**: http://127.0.0.1:5000/cars?price_min=400000&price_max=600000

**Filter by fuel type**: http://127.0.0.1:5000/cars?fuel_type=Diesel

**Filter by year**: http://127.0.0.1:5000/cars?year_min=2020&year_max=2023

**Combined filters**: 
```
http://127.0.0.1:5000/cars?brand=Hyundai&price_min=700000&price_max=1000000&fuel_type=Petrol
```

---

## 📊 What's Available

| Feature | Details |
|---------|---------|
| **Total Cars** | 30+ |
| **Brands** | Maruti, Hyundai, Tata, BMW, Audi, VW, Kia, etc. |
| **Price Range** | ₹350,000 - ₹1,400,000 |
| **Years** | 2014 - 2022 |
| **Fuel Types** | Petrol, Diesel, Electric, Hybrid, LPG |

---

## 🎨 Design Highlights

✨ **Modern OLX-style layout**
- Clean card-based grid
- Professional gradient backgrounds
- Smooth hover animations

📱 **Fully responsive**
- Works on desktop, tablet, mobile
- Auto-adjusting layout

🔍 **Advanced filtering**
- 4 filter types (brand, price, fuel, year)
- Instant JavaScript sorting
- Active filter display

🛒 **Shopping integration**
- Add cars to cart
- Save to favorites
- Leave reviews & ratings

---

## ❓ Common Questions

### Q: How do I add more cars?
A: Edit `scripts/seed_cars.py` and add new car entries, then run:
```powershell
.venv\Scripts\python.exe scripts\seed_cars.py
```

### Q: How do I change car images?
A: Replace images in `staticc/uploads/` folder with same filenames

### Q: Can I sell cars?
A: Yes! Login → Click "➕ Add Product" → Select category "Cars"

### Q: Where are car reviews?
A: Scroll down on car detail page to see reviews and add your own (login required)

### Q: How do I contact the seller?
A: Click "💬 Contact Seller" button on car detail page

---

## 📋 Navigation

**From Navbar**:
- 🏠 Home → Back to homepage
- 🛍️ Browse → All products (including cars)
- **🚗 Cars** ← Car listings (NEW!)
- 🎉 Offers → Special deals
- 🛒 Cart → Shopping cart
- 📊 Dashboard → Your listings (if logged in)

---

## 🔐 Login Credentials

**Default Admin Account**:
- Email: `admin@site.com`
- Password: `admin123`

**Or Register** a new account at `/register`

---

## 🆘 Troubleshooting

**Cars not showing?**
```powershell
.venv\Scripts\python.exe scripts\seed_cars.py
```

**Filter not working?**
- Refresh page (F5 or Cmd+R)
- Check browser console (F12)

**Images not loading?**
- Check `staticc/uploads/` folder has images
- Refresh page

**App crashed?**
- Press Ctrl+C to stop
- Run again: `.venv\Scripts\python.exe app.py`

---

## 📞 Support

All features documented in:
- `README.md` - Setup & general features
- `CAR_LISTINGS_DOCUMENTATION.md` - Detailed car module docs
- `CAR_LISTINGS_IMPLEMENTATION_SUMMARY.md` - What's new

---

## 🚀 Next Steps

1. **Explore**: Browse all cars at `/cars`
2. **Filter**: Try different filter combinations
3. **Details**: Click on a car to see full details
4. **Cart**: Add cars to cart and checkout
5. **Favorites**: Save cars you like
6. **Review**: Leave reviews for cars you're interested in
7. **Sell**: Add your own cars for sale!

---

**Enjoy browsing! 🎉**
