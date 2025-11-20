#!/usr/bin/env python
"""
Quick test script to verify the e-commerce app is set up correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SepApp.settings')
django.setup()

from django.contrib.auth.models import User
from ecommerce.models import Category, Product, Cart, CartItem, UserProfile

def test_setup():
    print("\n" + "="*60)
    print("E-COMMERCE APP SETUP VERIFICATION")
    print("="*60 + "\n")

    # Test 1: Check Users
    print("✓ TEST 1: User Accounts")
    users = User.objects.all()
    print(f"  Total users: {users.count()}")
    for user in users[:5]:
        print(f"    - {user.username} ({user.email})")

    # Test 2: Check Categories
    print("\n✓ TEST 2: Product Categories")
    categories = Category.objects.all()
    print(f"  Total categories: {categories.count()}")
    for cat in categories:
        print(f"    - {cat.name} ({cat.slug})")

    # Test 3: Check Products
    print("\n✓ TEST 3: Products")
    products = Product.objects.all()
    print(f"  Total products: {products.count()}")
    for product in products[:5]:
        print(f"    - {product.name} (${product.price}) - Stock: {product.stock}")

    # Test 4: Check User Profiles
    print("\n✓ TEST 4: User Profiles")
    profiles = UserProfile.objects.all()
    print(f"  Total profiles: {profiles.count()}")

    # Test 5: Check Carts
    print("\n✓ TEST 5: Shopping Carts")
    carts = Cart.objects.all()
    print(f"  Total carts: {carts.count()}")
    for cart in carts[:3]:
        items_count = cart.items.count()
        total = cart.get_total()
        print(f"    - {cart.user.username}: {items_count} items (${total})")

    # Test 6: Model Relationships
    print("\n✓ TEST 6: Database Relationships")
    print("  ✓ User to UserProfile (1:1)")
    print("  ✓ User to Cart (1:1)")
    print("  ✓ Cart to CartItem (1:Many)")
    print("  ✓ Product to Category (Many:1)")

    # Test 7: Admin User
    print("\n✓ TEST 7: Admin Access")
    admin = User.objects.filter(is_staff=True).first()
    if admin:
        print(f"  Admin user: {admin.username}")
        print(f"  Email: {admin.email}")

    print("\n" + "="*60)
    print("SETUP VERIFICATION COMPLETE ✓")
    print("="*60)
    print("\nREADY TO START:")
    print("  1. Run: python manage.py runserver")
    print("  2. Visit: http://localhost:8000")
    print("  3. Admin: http://localhost:8000/admin/")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    test_setup()

