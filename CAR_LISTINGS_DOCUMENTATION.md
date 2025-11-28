# Car Listings Module - Documentation

## Overview

The Car Listings module is a specialized product vertical built into the Flask marketplace. It provides an OLX Cars-style experience with advanced filtering, detailed car specifications, and a professional user interface.

## Features

### 1. Car Listings Page (`/cars`)
- **OLX-Style Layout**: Professional classified ads marketplace design
- **Advanced Filter Sidebar** with:
  - 🔍 Car Brand - Search by manufacturer (Maruti, Hyundai, Tata, BMW, Audi, etc.)
  - 💰 Price Range - Min/Max price filtering in rupees
  - ⛽ Fuel Type - Petrol, Diesel, Electric, Hybrid, LPG
  - 📅 Year of Manufacture - Filter by year range (2000-2024)
- **Responsive Grid Layout** - Auto-fills columns based on screen size
- **Car Cards** with:
  - Product image with hover zoom effect
  - "NEW" badge indicator
  - Car title (brand + model)
  - Price in green with rupee symbol and comma formatting
  - Location and posted date metadata
  - Seller information
  - "View Details" and "Add to Cart" action buttons
- **Sorting Options**:
  - Latest Listings (newest first)
  - Price: Low to High
  - Price: High to Low
- **Filter Summary** - Shows active filters with option to clear
- **No Results State** - Friendly message when filters return 0 cars

### 2. Car Detail Page (`/car/<id>`)
- **Left Column** - Image showcase
  - Large product image (up to 500px height)
  - "VERIFIED SELLER" badge
  - Image gallery placeholder (extensible for multiple images)
  - Car specifications grid with icons:
    - 🚗 Brand
    - 📅 Year
    - ⛽ Fuel Type
    - 🛣️ Mileage
    - ⚙️ Transmission
    - 🏎️ Owner Status
  - Detailed description
  - Reviews & ratings section with ability to add reviews
  
- **Right Column** - Purchase & Info sidebar (sticky on desktop)
  - Prominent pricing display ("ASKING PRICE")
  - "Add to Cart" button (primary gradient)
  - "Save to Favorites" toggle
  - Seller Information Card with:
    - Seller avatar (first letter badge)
    - Name and verification status
    - Email contact
    - Contact button for messaging
  - Location Map placeholder
  - Safety Tips alert box
  
- **Similar Cars** - Recommendations section at bottom
  - Shows up to 4 similar cars by brand and price range
  - Quick view cards with images and pricing

### 3. Filter Functionality

#### Backend Filtering (app.py)
```python
@app.route("/cars")
def cars():
    brand = request.args.get('brand', '')              # Car brand search
    model = request.args.get('model', '')              # Model filter
    price_min = request.args.get('price_min', '0')    # Minimum price
    price_max = request.args.get('price_max', '999999')  # Maximum price
    fuel_type = request.args.get('fuel_type', '')      # Fuel type (Petrol/Diesel/etc)
    year_min = request.args.get('year_min', '2000')    # Year range start
    year_max = request.args.get('year_max', '2024')    # Year range end
```

**Query Building**:
- Dynamically constructs WHERE clauses based on provided filters
- Uses parameterized queries to prevent SQL injection
- Filters Category = 'Cars' only
- Returns up to 50 results sorted by creation date (newest first)

#### Frontend Sorting (JavaScript)
- Client-side sorting by price (ascending/descending)
- Dynamically reorders cards without page reload
- Parses price from card content

### 4. Sample Data

The `scripts/seed_cars.py` script includes 30 realistic second-hand cars:

**Brands Represented**:
- Indian: Maruti, Hyundai, Tata, Mahindra, Kia, Renault, Force Motors, Citroen, Nissan Datsun, MG, Jeep
- International: BMW, Audi, Volkswagen, Toyota, Mitsubishi

**Price Range**: ₹350,000 - ₹1,400,000
**Years**: 2014 - 2022
**Fuel Types**: Petrol, Diesel, Electric, Hybrid
**Features**: Mileage, transmission, owner status, conditions

**Example Car**:
```python
("Maruti Swift VXI 2022", "Cars", 450000, 
 "🚗 Maruti Swift VXI | Year: 2022 | Petrol | Manual | 45,000 km | 1st Owner | Insurance Valid | Well Maintained", 
 "swift.jpg", 1)
```

## Database Schema

All cars are stored in the `products` table with `category = 'Cars'`:

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,           -- "Maruti Swift VXI 2022"
    category TEXT NOT NULL,        -- "Cars" for all car entries
    price INTEGER NOT NULL,        -- ₹450000
    description TEXT,              -- Full car details with specs
    image_path TEXT,              -- Path to product image
    user_id INTEGER,              -- Seller ID
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```

## Routes & Endpoints

### Public Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/cars` | GET | Display car listings with filters |
| `/car/<id>` | GET | Show individual car details |
| `/car/<id>` | POST | Submit car review (requires login) |

### Query Parameters (for `/cars`)
```
/cars?brand=Maruti&price_min=400000&price_max=600000&fuel_type=Petrol&year_min=2020&year_max=2023
```

## UI Components

### Filter Card
- Sticky positioning on desktop (follows scroll)
- Responsive grid layout on mobile (stacks at top)
- Color-coded inputs with focus states (blue highlight)
- Active filter badges with icon indicators
- Apply & Reset buttons

### Car Card
- Hover animation: `translateY(-5px)` with shadow enhancement
- Image zoom effect on hover
- Badge system (NEW, FEATURED, OFFER)
- Quick action buttons (2-column layout)
- 4-column grid on desktop, 1-column on mobile

### Price Display
- Large bold green text (₹ symbol)
- Comma-formatted for readability
- E.g., "₹1,250,000"

### Seller Card
- Gradient background (light grey)
- Avatar circle with first letter of name
- Verification badge (✓ Verified Seller)
- Email display
- Contact button

## Integration with Existing Features

### Shopping Cart
- Cars can be added to cart like regular products
- `POST /add_to_cart/<id>` works with car product IDs
- Cart summary shows cars mixed with other products

### Favorites System
- Cars can be favorited like other products
- `POST /favorite/<id>` endpoint handles cars
- Favorites tracked in `favorites` table

### Reviews System
- Cars inherit review functionality from products
- `POST /product/<id>` endpoint handles car reviews
- Reviews stored with car product ID

### User Dashboard
- Cars appear in user's listings
- Seller stats include cars sold
- Favorites include saved cars

## Styling & CSS

### Color Scheme
- **Primary Gradient**: `#667eea` to `#764ba2` (purple/blue)
- **Secondary Gradient**: `#f5f7fa` to `#c3cfe2` (light blue)
- **Success Color**: `#28a745` (green for prices)
- **Warning Color**: `#ffc107` (yellow for alerts)

### Responsive Breakpoints
```css
@media (max-width: 768px) {
    /* Hide filter sidebar on mobile */
    .col-lg-3 { display: none; }
    
    /* Full width listings */
    .col-lg-9 { max-width: 100%; }
    
    /* Single column grid */
    .cars-grid { grid-template-columns: 1fr; }
}
```

### Animations
- **Fade In Up**: Cars grid enters with smooth animation
- **Hover Lift**: Car cards lift on hover with shadow
- **Image Zoom**: Images zoom 1.05x on hover
- **Button Transitions**: Color transitions on button hover

## Performance Considerations

### Database Optimization
- Queries limited to 50 results max
- Category filter prevents scanning all products
- Parameterized queries prevent SQL injection
- Index recommendation: `CREATE INDEX idx_cars ON products(category, created_on DESC)`

### Frontend Optimization
- Client-side sorting for immediate feedback
- Lazy load images if needed (future enhancement)
- CSS variables for reusable color values
- Minimal JavaScript for sorting only

## Future Enhancements

1. **Advanced Features**
   - Multiple image uploads per car
   - Embedded Google Maps for location
   - Mileage history/service records
   - Price negotiation/offers feature
   - Car inspection checklist

2. **Search Improvements**
   - Full-text search across title and description
   - Auto-complete for brand/model fields
   - Search history and saved searches
   - Email alerts for new listings matching criteria

3. **Social Features**
   - Test drive booking
   - Pre-owned certification badges
   - Seller ratings/reputation
   - Insurance verification
   - Financing calculator

4. **Admin Features**
   - Car verification workflow
   - Fraud detection for listings
   - Featured car promotion
   - Commission tracking for sales

5. **Mobile App**
   - Native iOS/Android app
   - Push notifications for saved searches
   - Image comparison tool
   - Augmented reality car visualization

## Testing Checklist

- [ ] Car listings page loads with all 30+ cars
- [ ] Filter by brand shows only matching cars
- [ ] Price range filter works correctly
- [ ] Fuel type filter displays correct results
- [ ] Year range filter functions properly
- [ ] Reset button clears all filters
- [ ] Sort by price (low→high) works
- [ ] Sort by price (high→low) works
- [ ] Sort by latest listings works
- [ ] Car detail page loads correctly
- [ ] Car images display properly
- [ ] Add to cart button works for cars
- [ ] Favorites toggle works
- [ ] Review submission works (when logged in)
- [ ] Similar cars section shows relevant recommendations
- [ ] Contact seller button displays correctly
- [ ] Responsive design works on mobile
- [ ] No console errors in browser
- [ ] All external links work
- [ ] Page load time is acceptable

## Troubleshooting

### Cars Not Showing
**Issue**: `/cars` returns 0 results
**Solution**:
```powershell
.venv\Scripts\python.exe scripts\seed_cars.py
```

### Images Not Loading
**Issue**: Car images show as broken
**Solution**: Ensure `staticc/uploads/` contains image files and check `app.py` has correct `UPLOAD_FOLDER` path

### Filters Not Working
**Issue**: Filter inputs don't change results
**Solution**: Check browser console for JavaScript errors and verify database has cars with matching criteria

### Mobile Layout Issues
**Issue**: Layout breaks on small screens
**Solution**: Test in Chrome DevTools mobile view (F12 → Toggle Device Toolbar)

## Code Examples

### Adding a New Car via Python
```python
import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute(
    "INSERT INTO products (title, category, price, description, image_path, user_id) VALUES (?, ?, ?, ?, ?, ?)",
    ("Honda City SV 2021", "Cars", 850000, "🚗 Honda City | Year: 2021 | Petrol | Manual | 35,000 km", "city.jpg", 1)
)
conn.commit()
conn.close()
```

### Filtering Cars via URL
```
http://127.0.0.1:5000/cars?brand=Maruti&price_min=400000&price_max=600000&fuel_type=Petrol
```

### Getting Car Details in JavaScript
```javascript
const price = document.querySelector('h2').textContent;  // Gets "₹450,000"
const specs = document.querySelectorAll('.specs-section p');  // Gets all specs
```

## Deployment Notes

For production deployment:

1. **Database**: Migrate to PostgreSQL or MySQL
2. **Images**: Use cloud storage (S3, Azure Blob, etc.)
3. **Search**: Implement Elasticsearch for advanced search
4. **Caching**: Add Redis for filter cache
5. **Security**: Use HTTPS and secure payment gateway
6. **Analytics**: Track user behavior on car listings
7. **Performance**: Use CDN for static assets and images

---

**Version**: 1.0  
**Last Updated**: 2024  
**Maintainer**: Development Team
