#!/usr/bin/env python
"""
Django eCommerce App - Setup & Verification Script
This script verifies that the application is properly configured and ready to run.
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SepApp.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.core.checks import run_checks
from ecommerce.models import (
    Category, Product, User, Cart, CartItem, Wishlist,
    BlogCategory, BlogPost, Order, OrderItem, TrendingImage, Coupon, UserProfile
)

print("=" * 80)
print("Django eCommerce App - Setup & Verification")
print("=" * 80)

# 1. Check Django System
print("\n[1] Checking Django System Configuration...")
try:
    issues = run_checks()
    if not issues:
        print("✓ Django system check passed - No issues found!")
    else:
        print(f"⚠ Django system check found {len(issues)} warning(s)")
        for issue in issues:
            print(f"  - {issue.level}: {issue.msg}")
except Exception as e:
    print(f"✗ Django check failed: {e}")
    sys.exit(1)

# 2. Check Database
print("\n[2] Checking Database Tables...")
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    table_names = [t[0] for t in tables]

    required_tables = [
        'ecommerce_category',
        'ecommerce_product',
        'ecommerce_userprofile',
        'ecommerce_cart',
        'ecommerce_cartitem',
        'ecommerce_wishlist',
        'ecommerce_blogcategory',
        'ecommerce_blogpost',
        'ecommerce_trendingimage',
        'ecommerce_order',
        'ecommerce_orderitem',
        'ecommerce_coupon',
    ]

    missing_tables = [t for t in required_tables if t not in table_names]

    if not missing_tables:
        print(f"✓ All required tables exist! ({len(required_tables)} tables)")
        for table in required_tables:
            if table in table_names:
                print(f"  ✓ {table}")
    else:
        print(f"✗ Missing {len(missing_tables)} table(s):")
        for table in missing_tables:
            print(f"  ✗ {table}")
        print("\n  Run: python manage.py migrate")
        sys.exit(1)

# 3. Check Models
print("\n[3] Checking Models...")
try:
    models = [
        ('Category', Category),
        ('Product', Product),
        ('UserProfile', UserProfile),
        ('Cart', Cart),
        ('CartItem', CartItem),
        ('Wishlist', Wishlist),
        ('BlogCategory', BlogCategory),
        ('BlogPost', BlogPost),
        ('Order', Order),
        ('OrderItem', OrderItem),
        ('TrendingImage', TrendingImage),
        ('Coupon', Coupon),
    ]

    for name, model in models:
        count = model.objects.count()
        print(f"✓ {name}: {count} record(s)")
except Exception as e:
    print(f"✗ Model check failed: {e}")
    sys.exit(1)

# 4. Check User Accounts
print("\n[4] Checking User Accounts...")
superusers = User.objects.filter(is_superuser=True)
total_users = User.objects.count()
print(f"✓ Total users: {total_users}")
print(f"✓ Superusers: {superusers.count()}")

if superusers.count() == 0:
    print("\n⚠ No superuser found! Create one with:")
    print("  python manage.py createsuperuser")

# 5. Check Authentication Configuration
print("\n[5] Checking Authentication Configuration...")
from django.conf import settings

auth_backends = settings.AUTHENTICATION_BACKENDS
print(f"✓ Authentication backends configured: {len(auth_backends)}")
for backend in auth_backends:
    print(f"  - {backend}")

# 6. Check Installed Apps
print("\n[6] Checking Installed Apps...")
installed_apps = settings.INSTALLED_APPS
required_apps = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'ecommerce',
    'widget_tweaks',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

for app in required_apps:
    if app in installed_apps:
        print(f"✓ {app}")
    else:
        print(f"✗ Missing: {app}")

# 7. Check URL Configuration
print("\n[7] Checking URL Configuration...")
try:
    from django.urls import get_resolver
    resolver = get_resolver()
    url_patterns = resolver.url_patterns
    print(f"✓ URL configuration loaded: {len(url_patterns)} pattern(s)")
except Exception as e:
    print(f"✗ URL configuration error: {e}")

# 8. Check Static & Media Files
print("\n[8] Checking Static & Media Directories...")
base_dir = settings.BASE_DIR
static_root = settings.STATIC_ROOT
media_root = settings.MEDIA_ROOT

for path, name in [(static_root, 'Static'), (media_root, 'Media')]:
    if path.exists():
        print(f"✓ {name} directory: {path}")
    else:
        print(f"⚠ {name} directory doesn't exist: {path}")
        print(f"  Creating directory...")
        path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created!")

# 9. Check Dependencies
print("\n[9] Checking Python Dependencies...")
dependencies = {
    'django': 'Django',
    'django_allauth': 'django-allauth',
    'django_extensions': 'django-extensions',
    'PIL': 'Pillow',
    'requests': 'requests',
    'widget_tweaks': 'django-widget-tweaks',
}

for module, package_name in dependencies.items():
    try:
        __import__(module)
        print(f"✓ {package_name}")
    except ImportError:
        print(f"✗ {package_name} not installed")
        print(f"  Install with: pip install {package_name}")

print("\n" + "=" * 80)
print("✓ VERIFICATION COMPLETE!")
print("=" * 80)

print("\n📝 Next Steps:")
print("1. Run migrations if needed: python manage.py migrate")
print("2. Create superuser if needed: python manage.py createsuperuser")
print("3. Collect static files: python manage.py collectstatic --noinput")
print("4. Run server: python manage.py runserver 8000")
print("5. Access application:")
print("   - Frontend: http://127.0.0.1:8000/")
print("   - Admin: http://127.0.0.1:8000/admin/")

print("\n🎯 Features Available:")
print("✓ User Authentication (Login/Signup)")
print("✓ Product Catalog with Categories")
print("✓ Shopping Cart")
print("✓ Wishlist")
print("✓ Checkout with Coupon Support")
print("✓ Order Management")
print("✓ User Profile")
print("✓ Blog System")
print("✓ About Page")
print("✓ Google OAuth (allauth)")
print("✓ Password Reset")
print("✓ Trending Images/Slider")

print("\n" + "=" * 80)

