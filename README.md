# Second-Hand Marketplace - Quick Start Guide

## System Requirements
- Windows 10+ with PowerShell
- Python 3.11+ (installed via winget or python.org)

---

## Quick Start (Copy & Paste)

### 1. Open PowerShell in the project folder
```powershell
cd C:\sample\inpu\second_hand_marketplace
```

### 2. Create and activate virtual environment (one-time setup)
```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Initialize database (one-time setup)
```powershell
.venv\Scripts\python.exe scripts\create_tables_if_missing.py
```

### 4. Generate product images (one-time setup)
```powershell
.venv\Scripts\python.exe scripts\generate_images.py
```

### 5. Add sample products (one-time setup)
```powershell
.venv\Scripts\python.exe scripts\seed_products.py
```

### 6. Add sample cars (one-time setup)
```powershell
.venv\Scripts\python.exe scripts\seed_cars.py
```

### 7. Start the Flask web server
```powershell
.venv\Scripts\python.exe app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

### 7. Open in Browser
Visit: **http://127.0.0.1:5000**

---

## Default Admin Login
- **Email:** admin@site.com
- **Password:** admin123

---

## What Each Script Does

| Script | Purpose | Run Once? |
|--------|---------|-----------|
| `scripts/create_tables_if_missing.py` | Creates database tables and default admin user | Yes |
| `scripts/generate_images.py` | Generates 45 sample product images | Yes |
| `scripts/seed_products.py` | Adds 45 sample products to database | Yes |
| `scripts/seed_cars.py` | Adds 30 sample cars to database | Yes |
| `app.py` | Starts the Flask web server | Every time you want to run |

---

## Features

### 🚗 Car Listings (New!)
- Dedicated OLX-style car marketplace at `/cars`
- Advanced filtering sidebar:
  - **Car Brand** - Search by Maruti, Hyundai, Tata, BMW, etc.
  - **Price Range** - Filter min/max price in rupees
  - **Fuel Type** - Petrol, Diesel, Electric, Hybrid, LPG
  - **Year of Manufacture** - Filter by year range (2000-2024)
- Individual car detail pages with:
  - Full car specifications (brand, year, fuel type, mileage, transmission, owner status)
  - Seller information and contact details
  - Customer reviews and ratings
  - Similar cars recommendations
  - Add to cart functionality
  - Save to favorites
- Responsive grid layout matching OLX Cars page design
- Sort by price (low→high, high→low) or latest listings
- Sample data: 30+ realistic second-hand cars

### Browse Products
- Homepage shows 8 recent products
- `/listings` page shows all products with filters:
  - Search by name/description
  - Filter by category
  - Filter by price range (min/max)
  - Sort by price (low→high, high→low) or newest

### User Accounts
- Register new account at `/register`
- Login at `/login`
- Dashboard shows your listings and favorites

### Sell Products
1. Login
2. Click "Add Product" in navbar
3. Fill title, category, price, description, upload image
4. Submit - product appears on marketplace

### Product Features
- View product details with images
- Leave reviews and ratings
- Add/remove favorites
- Contact seller

### Admin Panel
- Login as admin
- Go to `/admin` to see all users and products
- Manage marketplace

---

## Troubleshooting

### "Python was not found"
**Solution:** Install Python 3.11+ from https://www.python.org/downloads/
- During installation, check ✓ "Add Python to PATH"
- Open a new PowerShell window after install

### "Module not found" errors
**Solution:** Reinstall dependencies:
```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### "Port 5000 already in use"
**Solution:** Find and stop the process using port 5000:
```powershell
Get-Process -Name python | Stop-Process -Force
```

### Database errors
**Solution:** Recreate the database:
```powershell
# Delete old database
Remove-Item database.db -Force

# Recreate tables and seed data
.venv\Scripts\python.exe scripts\create_tables_if_missing.py
.venv\Scripts\python.exe scripts\seed_products.py
```

---

## File Structure

```
second_hand_marketplace/
├── app.py                           # Main Flask application
├── database.db                      # SQLite database (created automatically)
├── init_db.py                       # Initial DB setup
├── requirements.txt                 # Python dependencies
├── .venv/                          # Virtual environment (created by venv)
├── scripts/
│   ├── create_tables_if_missing.py # Create tables safely
│   ├── generate_images.py          # Generate placeholder images
│   ├── seed_products.py            # Add sample products
│   ├── seed_cars.py                # Add sample cars
│   └── list_tables.py              # View database tables
├── staticc/
│   ├── style.css                   # Styles
│   └── uploads/                    # Product images (generated)
└── templates/
    ├── base.html                   # Base template
    ├── home.html                   # Homepage
    ├── listings.html               # Browse products
    ├── product_detail.html         # Product details
    ├── add_product.html            # Add/edit product
    ├── cars_list.html              # Car listings (NEW)
    ├── car_detail.html             # Car detail page (NEW)
    ├── dashboard.html              # User dashboard
    ├── admin.html                  # Admin panel
    ├── login.html                  # Login
    ├── register.html               # Register
    └── messages.html               # Messages demo
```

---

## Stop the Server

Press **Ctrl+C** in the PowerShell where you ran `app.py`

---

## Keep Server Running in Background

If you want to keep the server running while using PowerShell:

```powershell
Start-Process -FilePath ".venv\Scripts\python.exe" -ArgumentList "app.py" -WindowStyle Hidden
```

Then visit http://127.0.0.1:5000 in your browser. To stop: use Task Manager to kill python.exe processes.

---

## Next Steps

- **Add more products:** Modify `scripts/seed_products.py` and run it again
- **Customize:** Edit templates in `templates/` folder
- **Change styles:** Edit `staticc/style.css`
- **Change admin password:** Login as admin and change in profile (if feature added)

---

## Support

If you see errors:
1. Check the error message in PowerShell
2. Run the troubleshooting steps above
3. Or recreate the database from scratch

Enjoy your marketplace! 🎉
