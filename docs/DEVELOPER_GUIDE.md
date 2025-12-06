# Order2Wear Developer Guide 👨‍💻

## Technical Documentation for Developers

This guide covers architecture, setup, common issues, and deployment.

---

## Table of Contents

1. [Project Setup](#project-setup)
2. [Project Structure](#project-structure)
3. [Database Schema](#database-schema)
4. [API Endpoints](#api-endpoints)
5. [Custom Models](#custom-models)
6. [Views & Logic](#views--logic)
7. [Template System](#template-system)
8. [Common Issues & Fixes](#common-issues--fixes)
9. [Testing & Deployment](#testing--deployment)

---

## Project Setup

### 📋 Requirements

```
Python 3.14+
Django 5.2.8
SQLite (Development)
pip & virtualenv
Git
```

### 🚀 Installation

```bash
# 1. Clone repository
git clone <repo-url>
cd SepApp

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (optional)
# Add environment variables here

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Create static files
python manage.py collectstatic

# 8. Start development server
python manage.py runserver 8000
```

### 📁 Key Files to Know

```
SepApp/
├── manage.py                 # Django management
├── requirements.txt          # Dependencies
├── db.sqlite3               # Database
├── SepApp/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL config
│   └── wsgi.py              # WSGI app
├── ecommerce/               # Main app
│   ├── models.py            # Data models
│   ├── views.py             # View functions
│   ├── urls.py              # App URLs
│   ├── admin.py             # Admin config
│   ├── forms.py             # Forms
│   ├── signals.py           # Django signals
│   └── migrations/          # Database migrations
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
└── media/                   # User uploads
```

---

## Project Structure

### 📦 Directory Layout

```
ecommerce/
├── models.py         # 14 models
├── views.py          # 25+ views
├── urls.py           # URL routing
├── admin.py          # Admin interface
├── forms.py          # User forms
├── signals.py        # Signals
└── migrations/       # 10 migrations

templates/ecommerce/
├── base.html         # Base template
├── home.html         # Homepage
├── product_*.html    # Product pages
├── cart.html         # Shopping cart
├── checkout.html     # Checkout
├── order_*.html      # Order pages
├── profile.html      # User profile
└── auth/             # Auth templates

static/
├── css/              # Tailwind CSS
├── js/               # JavaScript
└── images/           # Static images
```

---

## Database Schema

### 📊 Models

```
User (Django built-in)
├── id (PK)
├── username
├── email
├── password
├── created_at

UserProfile
├── id (PK)
├── user (FK)
├── phone
├── address
├── city
├── created_at

Product
├── id (PK)
├── name
├── slug
├── description
├── price (Decimal)
├── stock (Integer)
├── image
├── category (FK)
├── is_active
├── is_featured

Category
├── id (PK)
├── name
├── slug
├── description

Cart
├── id (PK)
├── user (FK)
├── created_at
├── updated_at

CartItem
├── id (PK)
├── cart (FK)
├── product (FK)
├── quantity

Order
├── id (PK)
├── user (FK)
├── subtotal (Decimal)
├── shipping_cost (Decimal)
├── tax_amount (Decimal)
├── total_amount (Decimal)
├── status
├── shipping_method (FK)
├── tax_rate (FK)
├── created_at

OrderItem
├── id (PK)
├── order (FK)
├── product (FK)
├── quantity
├── price

Coupon
├── id (PK)
├── code
├── discount_type
├── discount_value
├── is_active
├── is_featured
├── valid_from
├── valid_until
├── max_uses
├── current_uses

ShippingMethod
├── id (PK)
├── name
├── price
├── estimated_days
├── is_active

TaxRate
├── id (PK)
├── name
├── rate_percentage
├── is_active
├── is_default

Wishlist
├── id (PK)
├── user (FK)
├── product (FK)

BlogPost
├── id (PK)
├── title
├── slug
├── content
├── author (FK)
├── is_published
└── created_at

TrendingImage
├── id (PK)
├── title
├── image
├── link
├── is_active
```

---

## API Endpoints

### 📍 URL Routes

```
Home & Products:
  /                          - Homepage
  /products/                 - All products
  /product/<slug>/           - Product detail
  /search/                   - Search (if implemented)

Authentication:
  /signup/                   - Register
  /login/                    - Login
  /logout/                   - Logout
  /password-reset/           - Password reset

Cart & Checkout:
  /cart/                     - View cart
  /add-to-cart/<id>/         - Add product
  /remove-from-cart/<id>/    - Remove product
  /checkout/                 - Checkout page
  /apply-coupon/             - Apply coupon (AJAX)

Orders:
  /orders/<id>/              - Order detail
  /orders/<id>/invoice/      - Download invoice
  /my-orders/                - Order history

User Profile:
  /profile/                  - View profile
  /settings/                 - Edit profile

Wishlist:
  /wishlist/                 - View wishlist
  /wishlist/add/<id>/        - Add to wishlist
  /wishlist/remove/<id>/     - Remove from wishlist

Blog:
  /blog/                     - Blog list
  /blog/<slug>/              - Blog detail

Other:
  /about/                    - About page
  /admin/                    - Admin panel
```

---

## Custom Models

### 📝 Model Methods

**Product Model:**
```python
def __str__(self):
    return self.name

def get_absolute_url(self):
    return reverse('product_detail', args=[self.slug])

def get_discount_percentage(self):
    if self.original_price > 0:
        return ((self.original_price - self.price) / 
                self.original_price) * 100
```

**Order Model:**
```python
def get_total_discount(self):
    return self.subtotal - (self.total_amount - 
           self.shipping_cost - self.tax_amount)

def is_pending(self):
    return self.status == 'pending'

def is_completed(self):
    return self.status == 'completed'
```

**Coupon Model:**
```python
def is_valid(self):
    from django.utils import timezone
    now = timezone.now()
    return (self.is_active and 
            self.current_uses < self.max_uses and
            self.valid_from <= now <= self.valid_until)

def get_discount_amount(self, order_total):
    if self.discount_type == 'fixed':
        return min(self.discount_value, order_total)
    else:
        return (order_total * self.discount_value) / 100
```

---

## Views & Logic

### 🔍 View Functions

**Cart Logic:**
```python
def cart_view(request):
    # Get user's cart
    # Calculate subtotal
    # Apply admin-configured shipping
    # Calculate tax
    # Return context
```

**Checkout Logic:**
```python
def checkout(request):
    # Validate cart
    # Apply coupon if provided
    # Calculate totals
    # Create order
    # Create order items
    # Clear cart
    # Redirect to success page
```

**Invoice Generation:**
```python
def download_invoice(request, order_id):
    # Get order
    # Generate PDF with reportlab
    # Return PDF response
```

### 📊 Business Logic

**Price Calculation:**
```
Subtotal = Sum of (product price × quantity)
Shipping = Admin-configured shipping_method.price
Tax = (Subtotal + Shipping) × tax_rate.rate_percentage / 100
Total = Subtotal + Shipping + Tax

If Coupon Applied:
Discount = Subtotal × coupon.discount_value / 100
Total = Subtotal - Discount + Shipping + Tax
```

---

## Template System

### 🎨 Base Template

```html
{% extends 'base.html' %}

{% block title %}Page Title{% endblock %}

{% block content %}
    <!-- Page content -->
{% endblock %}
```

### 📋 Template Tags Used

- `{{ variable }}` - Display variable
- `{% for item in items %}` - Loop
- `{% if condition %}` - Conditional
- `{% url 'name' %}` - Reverse URL
- `{% csrf_token %}` - CSRF protection
- `{% static 'path' %}` - Static files
- `|` - Filters (date, currency, etc)

### 🎯 Context Data

Common context variables:

```python
context = {
    'user': request.user,
    'cart': cart_object,
    'products': product_list,
    'total': calculated_total,
    'shipping': shipping_cost,
    'tax': tax_amount,
}
```

---

## Common Issues & Fixes

### ❌ Issue: Merge Conflicts in Git

**Error:** `<<<<<<< HEAD` markers in files

**Fix:**
```bash
# View conflicts
git diff

# Resolve manually
# Then stage and commit
git add .
git commit -m "Resolve conflicts"
```

---

### ❌ Issue: reportlab Not Installed

**Error:** `ModuleNotFoundError: No module named 'reportlab'`

**Fix:**
```bash
pip install reportlab==4.4.5
pip freeze > requirements.txt
```

---

### ❌ Issue: Deprecation Warnings

**Error:** `settings.ACCOUNT_AUTHENTICATION_METHOD is deprecated`

**Fix:**
```python
# In settings.py
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
```

---

### ❌ Issue: Hardcoded Values

**Error:** Cart showing hardcoded shipping (₨5.00)

**Fix:**
```python
# Use database values
shipping = ShippingMethod.objects.filter(is_active=True).first()
shipping_cost = shipping.price if shipping else 0
```

---

### ❌ Issue: Template Merge Conflicts

**Error:** `<<<<<<< HEAD` in HTML template

**Fix:**
```html
<!-- Remove conflict markers -->
<!-- Keep desired version -->
<!-- Remove unwanted sections -->
```

---

## Testing & Deployment

### ✅ Testing Checklist

```
□ User Registration
□ User Login/Logout
□ Product Browsing
□ Add to Cart
□ Remove from Cart
□ Apply Coupon
□ Checkout Process
□ Order Creation
□ Invoice Download
□ Profile Update
□ Wishlist Functions
□ Admin Create Product
□ Admin Manage Orders
□ Admin Create Coupon
```

### 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test ecommerce.tests.ProductTest

# Verbose output
python manage.py test -v 2

# With coverage
pip install coverage
coverage run --source='ecommerce' manage.py test
coverage report
```

### 🚀 Deployment Checklist

```
□ Set DEBUG = False
□ Set SECRET_KEY in environment
□ Update ALLOWED_HOSTS
□ Use PostgreSQL (not SQLite)
□ Configure email backend
□ Set up static files
□ Enable HTTPS
□ Configure database backups
□ Set up error logging
□ Use gunicorn/uWSGI
□ Set up CDN for static files
□ Configure web server (Nginx/Apache)
```

### 📦 Production Settings

```python
# settings.py

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'order2wear_db',
        'USER': 'db_user',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'db.example.com',
        'PORT': '5432',
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 🔧 Development Commands

### Useful Commands

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create test data
python manage.py shell
>>> from ecommerce.models import Product
>>> Product.objects.create(name="Test", price=100)

# Collect static files
python manage.py collectstatic

# Create app
python manage.py startapp appname

# Database backup
python manage.py dumpdata > backup.json

# Database restore
python manage.py loaddata backup.json

# Check for issues
python manage.py check

# Run server
python manage.py runserver 0.0.0.0:8000
```

---

## 📚 Useful Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [reportlab](https://www.reportlab.com/)
- [django-allauth](https://django-allauth.readthedocs.io/)

---

## 🤝 Contributing Guidelines

1. Fork repository
2. Create feature branch
3. Make changes
4. Write tests
5. Submit pull request

---

## 📞 Developer Support

For technical help:
- Check ADMIN_GUIDE.md for setup issues
- Review common issues above
- Check Django docs
- Search Stack Overflow
- Contact: dev@order2wear.com

---

**Happy Coding! 👨‍💻**

*Last Updated: November 30, 2025*

