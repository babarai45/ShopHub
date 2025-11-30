#!/usr/bin/env python
"""Debug script to check coupon status"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SepApp.settings')
sys.path.insert(0, '/')
django.setup()

from ecommerce.models import Coupon
from django.utils import timezone

print("\n" + "="*60)
print("COUPON DEBUGGING SCRIPT")
print("="*60)

# Check all coupons
coupons = Coupon.objects.all()
print(f"\n✅ Total Coupons Found: {coupons.count()}")

if coupons.count() == 0:
    print("❌ No coupons found in database!")
else:
    for i, coupon in enumerate(coupons, 1):
        print(f"\n--- Coupon {i} ---")
        print(f"Code: {coupon.code}")
        print(f"Discount Type: {coupon.get_discount_type_display()}")
        print(f"Discount Value: {coupon.discount_value}")
        print(f"Min Order Amount: ${coupon.min_order_amount}")
        print(f"Max Uses: {coupon.max_uses}")
        print(f"Current Uses: {coupon.current_uses}")
        print(f"Is Active: {coupon.is_active}")
        print(f"Valid From: {coupon.valid_from}")
        print(f"Valid Until: {coupon.valid_until}")
        print(f"Description: {coupon.description}")

        # Check validity
        now = timezone.now()
        print(f"\nValidation Checks:")
        print(f"  ✓ Is Active: {coupon.is_active}")
        print(f"  ✓ Current Date: {now}")
        print(f"  ✓ Date Range Valid: {coupon.valid_from <= now <= coupon.valid_until}")
        print(f"  ✓ Usage Available: {coupon.current_uses} < {coupon.max_uses}")
        print(f"  ✓ Can Use: {coupon.is_valid()}")

print("\n" + "="*60)

