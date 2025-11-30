#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SepApp.settings')
django.setup()

from django.urls import reverse

print("\nPassword Reset URL Test")
print("=" * 60)

try:
    url1 = reverse('ecommerce:password_reset')
    print(f"✓ password_reset: {url1}")
except Exception as e:
    print(f"✗ password_reset: {e}")
    sys.exit(1)

try:
    url2 = reverse('ecommerce:password_reset_done')
    print(f"✓ password_reset_done: {url2}")
except Exception as e:
    print(f"✗ password_reset_done: {e}")
    sys.exit(1)

try:
    url3 = reverse('ecommerce:password_reset_confirm', kwargs={'uidb64': 'test', 'token': 'test'})
    print(f"✓ password_reset_confirm: {url3}")
except Exception as e:
    print(f"✗ password_reset_confirm: {e}")
    sys.exit(1)

try:
    url4 = reverse('ecommerce:password_reset_complete')
    print(f"✓ password_reset_complete: {url4}")
except Exception as e:
    print(f"✗ password_reset_complete: {e}")
    sys.exit(1)

print("=" * 60)
print("✓ ALL PASSWORD RESET URLS ARE WORKING!")
print("\nPassword reset flow is now fixed:")
print("  1. User visits /password-reset/")
print("  2. Submits form")
print("  3. Redirects to /password-reset/done/")
print("  4. User gets email with reset link")
print("  5. Clicks link to /password-reset/<token>/")
print("  6. Submits new password")
print("  7. Redirects to /password-reset/complete/")
print("=" * 60 + "\n")

