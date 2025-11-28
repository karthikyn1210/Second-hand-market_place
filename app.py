import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime
import ast
if not hasattr(ast, "Str"):
    def _Str(s):
        return ast.Constant(value=s)
    ast.Str = _Str

# Module: app.py (top-level initialization)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "staticc", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__, 
    static_folder=os.path.join(BASE_DIR, "staticc"),
    static_url_path="/staticc",
    instance_path=BASE_DIR)
app.secret_key = "replace_this_with_a_strong_secret_key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- DB helper ---
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- auth helpers ---
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in.", "warning")
            return redirect(url_for("login"))
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        conn.close()
        if not user or user["is_admin"] != 1:
            flash("Admin access required.", "danger")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# --- routes ---
@app.route("/")
def home():
    # show recent products (limit 5)
    conn = get_db_connection()
    products = conn.execute("SELECT p.*, u.name as seller FROM products p LEFT JOIN users u ON p.user_id = u.id ORDER BY created_on DESC LIMIT 5").fetchall()
    conn.close()
    return render_template("home.html", products=products)

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if not name or not email or not password:
            flash("All fields are required.", "warning")
            return redirect(url_for("register"))

        hashed = generate_password_hash(password)
        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed))
            conn.commit()
            conn.close()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))

    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        if user:
            stored = user["password"]
            # stored may be unhashed if created by init_db; try check then fallback to raw compare
            if (stored and (check_password_hash(stored, password) or stored == password)):
                # if stored was plain text, re-hash it
                if not stored.startswith("pbkdf2:"):
                    conn = get_db_connection()
                    conn.execute("UPDATE users SET password = ? WHERE id = ?", (generate_password_hash(password), user["id"]))
                    conn.commit()
                    conn.close()
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["is_admin"] = user["is_admin"]
                flash(f"Welcome, {user['name']}!", "success")
                return redirect(url_for("home"))
        flash("Invalid credentials.", "danger")
        return redirect(url_for("login"))
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("home"))

# Add product
@app.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    if request.method == "POST":
        title = request.form["title"].strip()
        category = request.form["category"].strip()
        price = request.form["price"].strip()
        description = request.form["description"].strip()
        file = request.files.get("image")

        image_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{int(datetime.utcnow().timestamp())}_{file.filename}")
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image_path = f"uploads/{filename}"

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO products (title, category, price, description, image_path, user_id, created_on)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, category, float(price) if price else 0.0, description, image_path, session["user_id"], datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
        flash("Product added.", "success")
        return redirect(url_for("dashboard"))

    categories = ["Mobiles", "Laptops", "Books", "Furniture", "Clothing", "Accessories", "Other"]
    return render_template("add_product.html", categories=categories)

# Edit product
@app.route("/edit_product/<int:pid>", methods=["GET", "POST"])
@login_required
def edit_product(pid):
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (pid,)).fetchone()
    conn.close()
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for("dashboard"))
    if product["user_id"] != session["user_id"] and not session.get("is_admin"):
        flash("You cannot edit this product.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        title = request.form["title"].strip()
        category = request.form["category"].strip()
        price = request.form["price"].strip()
        description = request.form["description"].strip()
        file = request.files.get("image")

        image_path = product["image_path"]
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{int(datetime.utcnow().timestamp())}_{file.filename}")
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image_path = f"uploads/{filename}"

        conn = get_db_connection()
        conn.execute("""
            UPDATE products SET title=?, category=?, price=?, description=?, image_path=?, created_on=?
            WHERE id=?
        """, (title, category, float(price) if price else 0.0, description, image_path, datetime.utcnow().isoformat(), pid))
        conn.commit()
        conn.close()
        flash("Product updated.", "success")
        return redirect(url_for("dashboard"))

    categories = ["Mobiles", "Laptops", "Books", "Furniture", "Clothing", "Accessories", "Other"]
    return render_template("edit_product.html", product=product, categories=categories)

# Delete product
@app.route("/delete_product/<int:pid>", methods=["POST"])
@login_required
def delete_product(pid):
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (pid,)).fetchone()
    if not product:
        conn.close()
        flash("Product not found.", "warning")
        return redirect(url_for("dashboard"))

    if product["user_id"] != session["user_id"] and not session.get("is_admin"):
        conn.close()
        flash("You cannot delete this product.", "danger")
        return redirect(url_for("dashboard"))

    # optionally delete image file
    if product["image_path"]:
        path = os.path.join(app.config["UPLOAD_FOLDER"], os.path.basename(product["image_path"]))
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

    conn.execute("DELETE FROM products WHERE id = ?", (pid,))
    conn.execute("DELETE FROM favorites WHERE product_id = ?", (pid,))
    conn.execute("DELETE FROM reviews WHERE product_id = ?", (pid,))
    conn.commit()
    conn.close()
    flash("Product deleted.", "info")
    return redirect(url_for("dashboard"))

# Listings / browse / search
@app.route("/listings")
def listings():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "")
    sort = request.args.get("sort", "")  # price_asc, price_desc, newest
    min_price = request.args.get("min_price", "")
    max_price = request.args.get("max_price", "")

    sql = "SELECT p.*, u.name as seller FROM products p LEFT JOIN users u ON p.user_id = u.id WHERE 1=1"
    params = []

    if q:
        sql += " AND (p.title LIKE ? OR p.description LIKE ?)"
        qparam = f"%{q}%"
        params.extend([qparam, qparam])

    if category:
        sql += " AND p.category = ?"
        params.append(category)

    if min_price:
        sql += " AND p.price >= ?"
        params.append(float(min_price))
    if max_price:
        sql += " AND p.price <= ?"
        params.append(float(max_price))

    if sort == "price_asc":
        sql += " ORDER BY p.price ASC"
    elif sort == "price_desc":
        sql += " ORDER BY p.price DESC"
    else:
        sql += " ORDER BY p.created_on DESC"

    conn = get_db_connection()
    # Fetch all products (no limit - show all available listings)
    products = conn.execute(sql, tuple(params)).fetchall()
    
    # Get all unique categories from database
    all_categories = conn.execute("SELECT DISTINCT category FROM products ORDER BY category").fetchall()
    categories = [cat['category'] for cat in all_categories if cat['category']]
    conn.close()

    return render_template("listings.html", products=products, categories=categories, q=q, category=category, sort=sort, min_price=min_price, max_price=max_price)

# Product detail + reviews + add review
@app.route("/product/<int:pid>", methods=["GET", "POST"])
def product_detail(pid):
    conn = get_db_connection()
    product = conn.execute("SELECT p.*, u.name as seller, u.email as seller_email FROM products p LEFT JOIN users u ON p.user_id = u.id WHERE p.id = ?", (pid,)).fetchone()
    if not product:
        conn.close()
        flash("Product not found.", "warning")
        return redirect(url_for("listings"))

    if request.method == "POST":
        if "user_id" not in session:
            flash("Please login to leave a review.", "warning")
            return redirect(url_for("login"))
        rating = int(request.form.get("rating", 5))
        comment = request.form.get("comment", "").strip()
        conn.execute("INSERT INTO reviews (user_id, product_id, rating, comment, created_on) VALUES (?, ?, ?, ?, ?)",
                     (session["user_id"], pid, rating, comment, datetime.utcnow().isoformat()))
        conn.commit()

    reviews = conn.execute("SELECT r.*, u.name as reviewer FROM reviews r LEFT JOIN users u ON r.user_id = u.id WHERE r.product_id = ? ORDER BY r.created_on DESC", (pid,)).fetchall()
    # check favorite
    is_fav = False
    if "user_id" in session:
        fav = conn.execute("SELECT * FROM favorites WHERE user_id = ? AND product_id = ?", (session["user_id"], pid)).fetchone()
        is_fav = True if fav else False

    conn.close()
    return render_template("product_detail.html", product=product, reviews=reviews, is_fav=is_fav)

# Add/remove favorite
@app.route("/favorite/<int:pid>", methods=["POST"])
@login_required
def favorite(pid):
    action = request.form.get("action", "add")
    conn = get_db_connection()
    exists = conn.execute("SELECT * FROM favorites WHERE user_id = ? AND product_id = ?", (session["user_id"], pid)).fetchone()
    if action == "add" and not exists:
        conn.execute("INSERT INTO favorites (user_id, product_id) VALUES (?, ?)", (session["user_id"], pid))
        conn.commit()
        conn.close()
        flash("Added to favorites.", "success")
        return redirect(request.referrer or url_for("dashboard"))
    if action == "remove" and exists:
        conn.execute("DELETE FROM favorites WHERE id = ?", (exists["id"],))
        conn.commit()
        conn.close()
        flash("Removed from favorites.", "info")
        return redirect(request.referrer or url_for("dashboard"))
    conn.close()
    return redirect(request.referrer or url_for("dashboard"))

# Dashboard - user listings and favorites
@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db_connection()
    my_products = conn.execute("SELECT * FROM products WHERE user_id = ? ORDER BY created_on DESC", (session["user_id"],)).fetchall()
    favorites = conn.execute("""
        SELECT p.* FROM products p JOIN favorites f ON p.id = f.product_id WHERE f.user_id = ? ORDER BY p.created_on DESC
    """, (session["user_id"],)).fetchall()
    conn.close()
    return render_template("dashboard.html", my_products=my_products, favorites=favorites)

# Admin panel
@app.route("/admin")
@admin_required
def admin_panel():
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email, is_admin FROM users ORDER BY id DESC").fetchall()
    products = conn.execute("SELECT p.*, u.name as seller FROM products p LEFT JOIN users u ON p.user_id = u.id ORDER BY p.created_on DESC").fetchall()
    conn.close()
    return render_template("admin.html", users=users, products=products)

# Serve uploaded images (Flask static handles this, but route included for clarity)
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# Messages template demo (flash)
@app.route("/messages")
def messages_demo():
    return render_template("messages.html")

# --- Shopping Cart Routes ---
@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    products_in_cart = []
    total_price = 0
    
    if cart_items:
        conn = get_db_connection()
        placeholders = ",".join("?" * len(cart_items))
        products = conn.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", tuple(cart_items)).fetchall()
        conn.close()
        products_in_cart = [dict(p) for p in products]
        total_price = sum(p["price"] for p in products_in_cart)
    
    return render_template("cart.html", cart_items=products_in_cart, total=total_price)

@app.route("/add_to_cart/<int:pid>", methods=["POST"])
def add_to_cart(pid):
    if "cart" not in session:
        session["cart"] = []
    if pid not in session["cart"]:
        session["cart"].append(pid)
        session.modified = True
        flash("Product added to cart!", "success")
    else:
        flash("Already in cart!", "info")
    return redirect(request.referrer or url_for("cart"))

@app.route("/remove_from_cart/<int:pid>", methods=["POST"])
def remove_from_cart(pid):
    if "cart" in session and pid in session["cart"]:
        session["cart"].remove(pid)
        session.modified = True
        flash("Product removed from cart!", "info")
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart_items = session.get("cart", [])
    if not cart_items:
        flash("Your cart is empty!", "warning")
        return redirect(url_for("cart"))
    
    # Redirect to payment page
    return redirect(url_for("payment"))

# --- Payment Routes ---
@app.route("/payment", methods=["GET"])
@login_required
def payment():
    cart_items = session.get("cart", [])
    if not cart_items:
        flash("Your cart is empty!", "warning")
        return redirect(url_for("cart"))
    
    conn = get_db_connection()
    placeholders = ",".join("?" * len(cart_items))
    products = conn.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", tuple(cart_items)).fetchall()
    conn.close()
    
    products_list = [dict(p) for p in products]
    total_price = sum(p["price"] for p in products_list)
    
    return render_template("payment.html", cart_items=products_list, total=total_price)

@app.route("/process_payment", methods=["POST"])
@login_required
def process_payment():
    import random
    import string
    from datetime import timedelta
    
    cart_items = session.get("cart", [])
    if not cart_items:
        flash("Your cart is empty!", "warning")
        return redirect(url_for("cart"))
    
    # Get form data
    full_name = request.form.get("full_name", "").strip()
    phone = request.form.get("phone", "").strip()
    address_line1 = request.form.get("address_line1", "").strip()
    address_line2 = request.form.get("address_line2", "").strip()
    city = request.form.get("city", "").strip()
    state = request.form.get("state", "").strip()
    pincode = request.form.get("pincode", "").strip()
    payment_method = request.form.get("payment_method", "").strip()
    
    # Validate required fields
    if not all([full_name, phone, address_line1, city, state, pincode, payment_method]):
        flash("Please fill all required fields.", "danger")
        return redirect(url_for("payment"))
    
    # Validate phone
    if not phone.isdigit() or len(phone) != 10:
        flash("Phone number must be 10 digits.", "danger")
        return redirect(url_for("payment"))
    
    # Validate pincode
    if not pincode.isdigit() or len(pincode) != 6:
        flash("Pincode must be 6 digits.", "danger")
        return redirect(url_for("payment"))
    
    # Build full address
    full_address = f"{full_name}\n{address_line1}"
    if address_line2:
        full_address += f"\n{address_line2}"
    full_address += f"\n{city}, {state} - {pincode}"
    
    conn = get_db_connection()
    
    try:
        # Get products in cart
        placeholders = ",".join("?" * len(cart_items))
        products = conn.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", tuple(cart_items)).fetchall()
        products_list = [dict(p) for p in products]
        total_price = sum(p["price"] for p in products_list)
        
        # Generate unique order number and tracking ID
        now = datetime.utcnow()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        order_number = f"ORD-{timestamp}-{random_suffix}"
        
        random_tracking = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        tracking_id = f"TRK-{timestamp}-{random_tracking}"
        
        # Calculate estimated delivery (5-7 days from now)
        estimated_delivery = (now + timedelta(days=6)).strftime("%Y-%m-%d")
        
        # Create order record
        conn.execute(
            "INSERT INTO orders (user_id, order_number, total_price, payment_status, tracking_status, tracking_id, estimated_delivery, shipping_address, phone_number, created_on, updated_on) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                session["user_id"],
                order_number,
                total_price,
                "Completed" if payment_method != "COD" else "Pending",
                "Order Confirmed",
                tracking_id,
                estimated_delivery,
                full_address,
                phone,
                now.isoformat(),
                now.isoformat()
            )
        )
        conn.commit()
        
        # Get the order ID
        order = conn.execute("SELECT id FROM orders WHERE order_number = ?", (order_number,)).fetchone()
        order_id = order["id"]
        
        # Add items to order_items
        for product in products_list:
            conn.execute(
                "INSERT INTO order_items (order_id, product_id, product_title, quantity, price) VALUES (?, ?, ?, ?, ?)",
                (order_id, product["id"], product["title"], 1, product["price"])
            )
        
        # Add initial tracking history
        conn.execute(
            "INSERT INTO tracking_history (order_id, status, location, timestamp, details) VALUES (?, ?, ?, ?, ?)",
            (order_id, "Order Confirmed", "Order Processing Center", now.isoformat(), "Your order has been confirmed and is being prepared for shipment.")
        )
        
        conn.commit()
        conn.close()
        
        # Clear cart and redirect to tracking page
        session["cart"] = []
        session.modified = True
        
        flash(f"Payment successful! Order #{order_number} confirmed.", "success")
        return redirect(url_for("order_tracking", order_id=order_id))
        
    except Exception as e:
        conn.rollback()
        conn.close()
        flash(f"Error processing payment: {str(e)}", "danger")
        return redirect(url_for("payment"))

@app.route("/order_tracking/<int:order_id>")
@login_required
def order_tracking(order_id):
    conn = get_db_connection()
    
    # Get order
    order = conn.execute("SELECT * FROM orders WHERE id = ? AND user_id = ?", (order_id, session["user_id"])).fetchone()
    
    if not order:
        conn.close()
        flash("Order not found.", "danger")
        return redirect(url_for("listings"))
    
    # Get order items
    items = conn.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,)).fetchall()
    
    # Get tracking history
    tracking = conn.execute("SELECT * FROM tracking_history WHERE order_id = ? ORDER BY timestamp DESC", (order_id,)).fetchall()
    
    conn.close()
    
    # Convert to dict and attach items/tracking
    order_dict = dict(order)
    order_dict["items"] = [dict(item) for item in items]
    order_dict["tracking_history"] = [dict(t) for t in tracking]
    
    return render_template("order_tracking.html", order=order_dict, tracking_history=order_dict["tracking_history"])

# --- Offers/Deals Page ---
@app.route("/offers")
def offers():
    conn = get_db_connection()
    # Get products under ₹200 or high-value items on discount
    deals = conn.execute("SELECT p.*, u.name as seller FROM products p LEFT JOIN users u ON p.user_id = u.id WHERE p.price < 200 OR p.price > 500 ORDER BY p.price ASC LIMIT 5").fetchall()
    conn.close()
    return render_template("offers.html", deals=deals)

# --- CAR LISTINGS ROUTES ---
@app.route("/cars")
def cars():
    conn = get_db_connection()
    
    # Get filter parameters
    brand = request.args.get('brand', '')
    model = request.args.get('model', '')
    price_min = request.args.get('price_min', '0')
    price_max = request.args.get('price_max', '999999')
    fuel_type = request.args.get('fuel_type', '')
    year_min = request.args.get('year_min', '2000')
    year_max = request.args.get('year_max', '2024')
    search = request.args.get('search', '')
    
    # Convert to integers safely
    try:
        price_min = int(price_min) if price_min else 0
        price_max = int(price_max) if price_max else 999999
        year_min = int(year_min) if year_min else 2000
        year_max = int(year_max) if year_max else 2024
    except ValueError:
        price_min, price_max, year_min, year_max = 0, 999999, 2000, 2024
    
    # Build dynamic query
    query = "SELECT p.*, u.name as seller FROM products p LEFT JOIN users u ON p.user_id = u.id WHERE p.category = 'Cars'"
    params = []
    
    if search:
        query += " AND (p.title LIKE ? OR p.description LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")
    
    if brand:
        query += " AND p.title LIKE ?"
        params.append(f"%{brand}%")
    
    if model:
        query += " AND p.title LIKE ?"
        params.append(f"%{model}%")
    
    if price_min > 0:
        query += " AND p.price >= ?"
        params.append(price_min)
    
    if price_max < 999999:
        query += " AND p.price <= ?"
        params.append(price_max)
    
    if fuel_type:
        query += " AND p.description LIKE ?"
        params.append(f"%{fuel_type}%")
    
    if year_min > 2000 or year_max < 2024:
        query += " AND p.description LIKE ?"
        params.append(f"%{year_min}%") if year_min > 2000 else None
    
    query += " ORDER BY p.created_on DESC LIMIT 5"
    
    # Execute query
    cars_list = conn.execute(query, [p for p in params if p]).fetchall()
    
    # Get unique brands for filter dropdown
    brands = conn.execute("SELECT DISTINCT title FROM products WHERE category = 'Cars' ORDER BY title").fetchall()
    
    conn.close()
    
    return render_template("cars_list.html", 
                         cars=cars_list, 
                         brands=[b['title'].split()[0] for b in brands],
                         filters={
                             'brand': brand,
                             'model': model,
                             'price_min': price_min,
                             'price_max': price_max,
                             'fuel_type': fuel_type,
                             'year_min': year_min,
                             'year_max': year_max,
                             'search': search
                         })

@app.route("/api/cars/search")
def api_cars_search():
    """API endpoint for car search (returns JSON)"""
    query_str = request.args.get('q', '').strip()
    limit = int(request.args.get('limit', '5'))
    
    if not query_str or len(query_str) < 2:
        return {"results": []}
    
    conn = get_db_connection()
    results = conn.execute(
        "SELECT id, title, price, image_path FROM products WHERE category = 'Cars' AND (title LIKE ? OR description LIKE ?) LIMIT ?",
        (f"%{query_str}%", f"%{query_str}%", limit)
    ).fetchall()
    conn.close()
    
    return {"results": [dict(r) for r in results]}

@app.route("/api/cars/stats")
def api_cars_stats():
    """API endpoint for car marketplace statistics"""
    conn = get_db_connection()
    
    total_cars = conn.execute("SELECT COUNT(*) FROM products WHERE category = 'Cars'").fetchone()[0]
    avg_price = conn.execute("SELECT AVG(price) FROM products WHERE category = 'Cars'").fetchone()[0] or 0
    min_price = conn.execute("SELECT MIN(price) FROM products WHERE category = 'Cars'").fetchone()[0] or 0
    max_price = conn.execute("SELECT MAX(price) FROM products WHERE category = 'Cars'").fetchone()[0] or 0
    
    fuel_types = conn.execute(
        "SELECT DISTINCT description FROM products WHERE category = 'Cars' LIMIT 1"
    ).fetchall()
    
    conn.close()
    
    return {
        "total_cars": total_cars,
        "avg_price": int(avg_price),
        "min_price": int(min_price),
        "max_price": int(max_price)
    }

@app.route("/cars/featured")
def featured_cars():
    """Display featured cars (high-end vehicles)"""
    conn = get_db_connection()
    featured = conn.execute(
        "SELECT p.*, u.name as seller FROM products p LEFT JOIN users u ON p.user_id = u.id WHERE p.category = 'Cars' AND p.price > 1000000 ORDER BY p.price DESC LIMIT 5"
    ).fetchall()
    conn.close()
    return render_template("cars_featured.html", cars=featured)

@app.route("/api/cars/compare")
def api_cars_compare():
    """API endpoint to compare multiple cars"""
    ids = request.args.getlist('ids')
    if not ids or len(ids) < 2:
        return {"error": "At least 2 car IDs required"}, 400
    
    # Limit to 5 cars for comparison
    ids = ids[:5]
    placeholders = ','.join('?' * len(ids))
    
    conn = get_db_connection()
    cars = conn.execute(
        f"SELECT id, title, price, description FROM products WHERE id IN ({placeholders}) AND category = 'Cars'",
        ids
    ).fetchall()
    conn.close()
    
    return {"cars": [dict(c) for c in cars]}

@app.route("/cars/compare", methods=["GET", "POST"])
def cars_compare():
    """Compare cars side-by-side"""
    car_ids = request.args.getlist('ids') or request.form.getlist('ids')
    
    if not car_ids or len(car_ids) < 2:
        flash("Select at least 2 cars to compare", "warning")
        return redirect(url_for("cars"))
    
    conn = get_db_connection()
    placeholders = ','.join('?' * len(car_ids))
    cars = conn.execute(
        f"SELECT p.*, u.name as seller FROM products p LEFT JOIN users u ON p.user_id = u.id WHERE p.id IN ({placeholders}) AND p.category = 'Cars'",
        car_ids
    ).fetchall()
    conn.close()
    
    return render_template("cars_compare.html", cars=cars)

@app.route("/car/<int:pid>")
def car_detail(pid):
    conn = get_db_connection()
    car = conn.execute("SELECT p.*, u.name as seller, u.email FROM products p LEFT JOIN users u ON p.user_id = u.id WHERE p.id = ? AND p.category = 'Cars'", (pid,)).fetchone()
    
    if not car:
        conn.close()
        flash("Car not found!", "danger")
        return redirect(url_for("cars"))
    
    # Get reviews
    reviews = conn.execute("SELECT r.*, u.name FROM reviews r LEFT JOIN users u ON r.user_id = u.id WHERE r.product_id = ? ORDER BY r.created_on DESC", (pid,)).fetchall()
    
    # Check if favorited
    is_fav = False
    if "user_id" in session:
        fav = conn.execute("SELECT id FROM favorites WHERE user_id = ? AND product_id = ?", (session["user_id"], pid)).fetchone()
        is_fav = fav is not None
    
    # Get similar cars (same brand, price range)
    car_brand = car['title'].split()[0]
    similar = conn.execute(
        "SELECT * FROM products WHERE category = 'Cars' AND title LIKE ? AND id != ? AND price BETWEEN ? AND ? LIMIT 4",
        (f"{car_brand}%", pid, car['price'] - 100000, car['price'] + 100000)
    ).fetchall()
    
    conn.close()
    
    return render_template("car_detail.html", 
                         car=car, 
                         reviews=reviews, 
                         is_fav=is_fav,
                         similar_cars=similar)

# --- TODO MANAGEMENT ROUTES ---
@app.route("/todos")
@login_required
def todos_list():
    """Display user's todo list for bikes and cars"""
    conn = get_db_connection()
    # Show up to 20 todos to match requested content limit
    todos = conn.execute(
        "SELECT * FROM todos WHERE user_id = ? ORDER BY created_on DESC LIMIT 5",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    
    # Separate by category
    bikes = [t for t in todos if t['item_type'] == 'Bike']
    cars = [t for t in todos if t['item_type'] == 'Car']
    
    return render_template("todos.html", todos=todos, bikes=bikes, cars=cars)

@app.route("/todos/add", methods=["GET", "POST"])
@login_required
def add_todo():
    """Add a new todo for bike or car"""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        item_type = request.form.get("item_type", "").strip()  # "Car" or "Bike"
        category = request.form.get("category", "").strip()
        price = request.form.get("price", "0")
        description = request.form.get("description", "").strip()
        image_path = None
        
        if not title or not item_type:
            flash("Title and item type are required.", "warning")
            return redirect(url_for("add_todo"))
        
        # Handle image upload
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename and allowed_file(file.filename):
                # Create unique filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                filename = secure_filename(timestamp + file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                image_path = f"uploads/{filename}"
        
        now = datetime.utcnow().isoformat()
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO todos (user_id, title, category, item_type, price, description, image_path, status, created_on, updated_on) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (session["user_id"], title, category, item_type, float(price) if price else 0, description, image_path, "pending", now, now)
            )
            conn.commit()
            flash(f"Todo added: {title}", "success")
        except Exception as e:
            flash(f"Error adding todo: {str(e)}", "danger")
        finally:
            conn.close()
        
        return redirect(url_for("todos_list"))
    
    return render_template("add_todo.html")

@app.route("/todos/<int:todo_id>/edit", methods=["GET", "POST"])
@login_required
def edit_todo(todo_id):
    """Edit an existing todo"""
    conn = get_db_connection()
    todo = conn.execute("SELECT * FROM todos WHERE id = ? AND user_id = ?", (todo_id, session["user_id"])).fetchone()
    
    if not todo:
        flash("Todo not found.", "danger")
        conn.close()
        return redirect(url_for("todos_list"))
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        price = request.form.get("price", "0")
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "pending")
        image_path = todo["image_path"]
        
        # Handle new image upload
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename and allowed_file(file.filename):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                filename = secure_filename(timestamp + file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                image_path = f"uploads/{filename}"
        
        now = datetime.utcnow().isoformat()
        try:
            conn.execute(
                "UPDATE todos SET title = ?, category = ?, price = ?, description = ?, image_path = ?, status = ?, updated_on = ? WHERE id = ?",
                (title, category, float(price) if price else 0, description, image_path, status, now, todo_id)
            )
            conn.commit()
            flash(f"Todo updated: {title}", "success")
        except Exception as e:
            flash(f"Error updating todo: {str(e)}", "danger")
        finally:
            conn.close()
        
        return redirect(url_for("todos_list"))
    
    conn.close()
    return render_template("edit_todo.html", todo=todo)

@app.route("/todos/<int:todo_id>/delete", methods=["POST"])
@login_required
def delete_todo(todo_id):
    """Delete a todo"""
    conn = get_db_connection()
    todo = conn.execute("SELECT * FROM todos WHERE id = ? AND user_id = ?", (todo_id, session["user_id"])).fetchone()
    
    if todo:
        conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        flash("Todo deleted successfully.", "success")
    else:
        flash("Todo not found.", "danger")
    
    conn.close()
    return redirect(url_for("todos_list"))

@app.route("/todos/<int:todo_id>/status/<status>", methods=["POST"])
@login_required
def update_todo_status(todo_id, status):
    """Update todo status"""
    if status not in ["pending", "in-progress", "completed"]:
        flash("Invalid status.", "danger")
        return redirect(url_for("todos_list"))
    
    conn = get_db_connection()
    todo = conn.execute("SELECT * FROM todos WHERE id = ? AND user_id = ?", (todo_id, session["user_id"])).fetchone()
    
    if todo:
        now = datetime.utcnow().isoformat()
        conn.execute("UPDATE todos SET status = ?, updated_on = ? WHERE id = ?", (status, now, todo_id))
        conn.commit()
        flash(f"Todo status updated to: {status}", "success")
    else:
        flash("Todo not found.", "danger")
    
    conn.close()
    return redirect(url_for("todos_list"))

@app.route("/api/todos")
@login_required
def api_todos():
    """API endpoint for todos (for AJAX requests)"""
    import json
    conn = get_db_connection()
    todos = conn.execute(
        "SELECT id, title, item_type, category, price, status, image_path, created_on FROM todos WHERE user_id = ? ORDER BY created_on DESC",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    return json.dumps([dict(t) for t in todos])

if __name__ == "__main__":
    app.run(debug=True)
