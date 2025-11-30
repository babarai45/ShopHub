# 🎯 Quick Reference Guide

## Most Used Commands

### Start Development Server
```bash
# Windows - Double-click this file:
run_server.bat

# Or use command line:
python manage.py runserver 8000
```

### Run Migrations
```bash
python manage.py migrate
python manage.py migrate ecommerce
```

### Create Admin Account
```bash
python manage.py createsuperuser
```

### Access Admin Panel
Visit: http://127.0.0.1:8000/admin/

### View Database
```bash
python manage.py shell
```

Then in Python shell:
```python
from ecommerce.models import Product
products = Product.objects.all()
for p in products:
    print(p.name, p.price)
```

### Verify System
```bash
python verify_complete_setup.py
```

### Check System Health
```bash
python manage.py check
```

---

## Application URLs

| Feature | URL |
|---------|-----|
| Home | http://127.0.0.1:8000/ |
| Products | http://127.0.0.1:8000/products/ |
| Product Detail | http://127.0.0.1:8000/product/[slug]/ |
| Cart | http://127.0.0.1:8000/cart/ |
| Checkout | http://127.0.0.1:8000/checkout/ |
| Wishlist | http://127.0.0.1:8000/wishlist/ |
| Profile | http://127.0.0.1:8000/profile/ |
| My Orders | http://127.0.0.1:8000/my-orders/ |
| Blog | http://127.0.0.1:8000/blog/ |
| About | http://127.0.0.1:8000/about/ |
| Admin | http://127.0.0.1:8000/admin/ |
| Login | http://127.0.0.1:8000/login/ |
| Signup | http://127.0.0.1:8000/signup/ |

---

## Key Files Location

```
E:\Specialization\django_Sep\SepApp\
├── manage.py                 # Django command center
├── db.sqlite3               # Database
├── requirements.txt         # Dependencies
│
├── SepApp/                  # Main project folder
│   ├── settings.py         # Configuration
│   ├── urls.py             # URL routing
│   ├── wsgi.py             # WSGI config
│
├── ecommerce/              # Main app
│   ├── models.py           # Database models
│   ├── views.py            # Business logic
│   ├── urls.py             # App URLs
│   ├── forms.py            # Forms
│   ├── admin.py            # Admin config
│
├── templates/              # HTML templates
│   ├── base.html           # Main template
│   ├── ecommerce/          # App templates
│
├── static/                 # CSS, JS, images
│   └── ...
│
├── media/                  # User uploads
│   ├── products/
│   ├── profiles/
│   └── blog/
│
└── Documentation files:
    ├── FINAL_STATUS_REPORT.md
    ├── COMPLETE_SETUP_GUIDE.md
    ├── FIXES_SUMMARY.md
    └── run_server.bat
```

---

## Database Models

### Product
- Name, slug, description
- Price, original price, discount
- Category, stock level
- Images, ratings, reviews count
- Featured flag, active status

### User
- Username, email, password
- Profile (avatar, address, phone)
- Cart (items and quantities)
- Wishlist (saved products)
- Orders (purchase history)

### Order
- User reference
- Total amount, status
- Order items (products + quantities)
- Created/updated timestamps

### Coupon
- Code, discount value
- Discount type (fixed/percentage)
- Valid dates, usage limits
- Minimum order amount

### Blog
- Title, slug, content
- Category, author
- Featured image, emoji
- Published status, view count

---

## Common Tasks

### Add a New Product Category
1. Go to: http://127.0.0.1:8000/admin/
2. Click "Categories"
3. Click "Add Category"
4. Fill in name, slug, description
5. Click "Save"

### Add a New Product
1. Go to Admin panel
2. Click "Products"
3. Click "Add Product"
4. Fill in details:
   - Name, slug, description
   - Price, stock, image
   - Category, tags
5. Click "Save"

### Create a Discount Coupon
1. Admin > Coupons > Add Coupon
2. Fill in:
   - Code (e.g., SUMMER20)
   - Discount value and type
   - Valid dates
   - Usage limits
3. Save

### Add a Blog Post
1. Admin > Blog Posts > Add Post
2. Fill in:
   - Title, slug
   - Content (description)
   - Category, featured image
   - Published status
3. Save

### Add Trending Image (Slider)
1. Admin > Trending Images > Add
2. Fill in:
   - Title, subtitle
   - Image file
   - Link (optional)
   - Order in slider
3. Save

---

## User Account Setup

### Test Existing Account
Username: `babar001`
Password: (check with administrator)

### Create New User Account
1. Go to: http://127.0.0.1:8000/signup/
2. Fill in:
   - Username
   - Email
   - Password
   - Confirm password
3. Click "Sign Up"

### Create Admin Account
```bash
python manage.py createsuperuser
```

Then enter:
- Username
- Email
- Password
- Confirm password

---

## Troubleshooting

### Problem: "Server won't start"
```bash
python manage.py check
```
Then fix any errors shown.

### Problem: "Port 8000 already in use"
```bash
python manage.py runserver 8001
# Use port 8001 instead
```

### Problem: "No database tables"
```bash
python manage.py migrate
```

### Problem: "Static files not showing"
```bash
python manage.py collectstatic --noinput
```

### Problem: "Can't login"
1. Check if user exists: Admin > Users
2. Reset password: http://127.0.0.1:8000/password-reset/
3. Create new user: /signup/

### Problem: "404 errors"
- Check URL is correct
- Verify app is in INSTALLED_APPS
- Run: `python manage.py check`

---

## Performance Tips

### For Better Performance:
1. Use PostgreSQL instead of SQLite
2. Enable caching
3. Optimize database queries
4. Minify CSS/JS
5. Compress images
6. Use CDN for static files

### For Better Security:
1. Set DEBUG = False
2. Add ALLOWED_HOSTS
3. Use HTTPS
4. Set secure cookies
5. Add security headers
6. Enable HSTS

---

## Django Shell Commands

```bash
python manage.py shell
```

Then use Python:

```python
# Import models
from ecommerce.models import Product, Order, User

# View all products
products = Product.objects.all()
for p in products:
    print(f"{p.name}: ${p.price}")

# Find product by name
product = Product.objects.get(name="Product Name")

# Get all orders
orders = Order.objects.all()

# Get user's orders
user = User.objects.get(username='babar001')
user_orders = Order.objects.filter(user=user)

# Create a product
from django.utils.text import slugify
Product.objects.create(
    name="New Product",
    slug=slugify("New Product"),
    price=99.99,
    stock=10,
    category_id=1
)

# Update a product
product = Product.objects.get(id=1)
product.price = 79.99
product.save()

# Delete a product
product = Product.objects.get(id=1)
product.delete()

# Exit shell
exit()
```

---

## Environment Variables (Optional)

Create `.env` file:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

Then in `settings.py`:
```python
from decouple import config
DEBUG = config('DEBUG', default=True, cast=bool)
SECRET_KEY = config('SECRET_KEY')
```

---

## Useful Links

- **Django Docs**: https://docs.djangoproject.com/
- **allauth Docs**: https://django-allauth.readthedocs.io/
- **Tailwind CSS**: https://tailwindcss.com/
- **Font Awesome**: https://fontawesome.com/
- **SQLite Docs**: https://www.sqlite.org/

---

## Getting Help

1. Check system: `python manage.py check`
2. Run verification: `python verify_complete_setup.py`
3. Check logs for errors
4. Review documentation files
5. Search Django documentation

---

## Common Settings

### settings.py Important Settings

```python
DEBUG = True                    # Change to False for production
ALLOWED_HOSTS = []             # Add domains for production
SECRET_KEY = '...'             # Keep secure
DATABASES = {...}              # Database configuration
INSTALLED_APPS = [...]         # Registered apps
MIDDLEWARE = [...]             # Request/response processors
TEMPLATES = [...]              # Template configuration
STATIC_URL = '/static/'        # Static files URL
MEDIA_URL = '/media/'          # User uploads URL
```

---

## File Permissions (Linux/Mac)

```bash
# Make manage.py executable
chmod +x manage.py

# Make run script executable
chmod +x run_server.sh

# Fix directory permissions
chmod 755 media/
chmod 755 static/
```

---

## Next Steps

1. ✅ Run server: `python manage.py runserver 8000`
2. ✅ Visit: http://127.0.0.1:8000/
3. ✅ Add products via admin
4. ✅ Test shopping flow
5. ✅ Create user accounts
6. ✅ Test checkout process

---

**Happy coding! 🚀**

Last Updated: 2025-11-30

