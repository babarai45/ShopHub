import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SepApp.settings')
django.setup()

from django.template.loader import render_to_string

print("Testing templates...")
print("-" * 50)

try:
    html = render_to_string('ecommerce/signup.html')
    print("✓ signup.html: RENDERS OK")
except Exception as e:
    print(f"✗ signup.html: {type(e).__name__}: {str(e)[:100]}")

try:
    html = render_to_string('ecommerce/login.html')
    print("✓ login.html: RENDERS OK")
except Exception as e:
    print(f"✗ login.html: {type(e).__name__}: {str(e)[:100]}")

print("-" * 50)
print("Template test complete!")

