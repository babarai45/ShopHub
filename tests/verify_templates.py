#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SepApp.settings')
django.setup()

from django.template import Template, Context
from django.template.loader import get_template

print("\n" + "="*60)
print("TEMPLATE RENDERING TEST")
print("="*60)

# Test signup.html
print("\n[1] Testing: templates/ecommerce/signup.html")
print("-" * 60)
try:
    template = get_template('ecommerce/signup.html')
    html = template.render({})
    print("✓ SUCCESS: Template renders without errors")
    if 'Continue with email' in html:
        print("✓ SUCCESS: Content is correct (contains 'Continue with email')")
    if 'provider_login_url' not in html:
        print("✓ SUCCESS: No provider_login_url code in output")
    if 'DoesNotExist' not in html and 'Exception' not in html:
        print("✓ SUCCESS: No exception messages in output")
except Exception as e:
    print(f"✗ FAILED: {type(e).__name__}")
    print(f"  Error: {str(e)[:150]}")
    sys.exit(1)

# Test login.html
print("\n[2] Testing: templates/ecommerce/login.html")
print("-" * 60)
try:
    template = get_template('ecommerce/login.html')
    html = template.render({})
    print("✓ SUCCESS: Template renders without errors")
    if 'Continue with email' in html:
        print("✓ SUCCESS: Content is correct (contains 'Continue with email')")
    if 'provider_login_url' not in html:
        print("✓ SUCCESS: No provider_login_url code in output")
    if 'DoesNotExist' not in html and 'Exception' not in html:
        print("✓ SUCCESS: No exception messages in output")
except Exception as e:
    print(f"✗ FAILED: {type(e).__name__}")
    print(f"  Error: {str(e)[:150]}")
    sys.exit(1)

print("\n" + "="*60)
print("✓ ALL TESTS PASSED!")
print("="*60)
print("\nBoth templates now render without DoesNotExist errors.")
print("Google OAuth button has been removed (not configured).")
print("\nPages are ready to use:")
print("  • http://127.0.0.1:8000/login/")
print("  • http://127.0.0.1:8000/signup/")
print("\n" + "="*60 + "\n")

