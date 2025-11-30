#!/usr/bin/env python
"""
Template Validation Script
Verifies that all required template tags are properly loaded.
"""

import os
import re

# Files to check
TEMPLATES_TO_CHECK = [
    'templates/ecommerce/login.html',
    'templates/ecommerce/signup.html',
]

# Required loads for these files
REQUIRED_LOADS = {
    'templates/ecommerce/login.html': ['socialaccount'],
    'templates/ecommerce/signup.html': ['socialaccount'],
}

# Required tags that should be present if loads are correct
REQUIRED_TAGS = {
    'templates/ecommerce/login.html': ['provider_login_url'],
    'templates/ecommerce/signup.html': ['provider_login_url'],
}

print("=" * 80)
print("TEMPLATE VALIDATION SCRIPT")
print("=" * 80)

all_passed = True

for template_file in TEMPLATES_TO_CHECK:
    if not os.path.exists(template_file):
        print(f"\n❌ {template_file} - FILE NOT FOUND")
        all_passed = False
        continue

    print(f"\n📄 Checking: {template_file}")

    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for required loads
    required = REQUIRED_LOADS.get(template_file, [])
    for load_name in required:
        load_pattern = rf'{{% load {load_name} %}}'
        if load_pattern in content or f'{{% load {load_name} %}}' in content:
            print(f"   ✅ Load tag found: {load_pattern}")
        else:
            print(f"   ❌ Missing load tag: {load_pattern}")
            all_passed = False

    # Check for required tags
    tags = REQUIRED_TAGS.get(template_file, [])
    for tag_name in tags:
        if f'{{% {tag_name}' in content:
            print(f"   ✅ Tag found: {tag_name}")
        else:
            print(f"   ❌ Tag not found: {tag_name}")
            all_passed = False

    # Check if file starts with extends
    if content.strip().startswith('{% extends'):
        print(f"   ✅ Extends base template properly")
    else:
        print(f"   ❌ Does not extend base template")
        all_passed = False

    # Show first few lines
    lines = content.split('\n')
    print(f"\n   First 5 lines:")
    for i, line in enumerate(lines[:5], 1):
        print(f"   Line {i}: {line.strip()}")

print("\n" + "=" * 80)

if all_passed:
    print("✅ ALL TEMPLATE CHECKS PASSED!")
    print("\nYour templates are properly configured.")
    print("The Google OAuth buttons should now display correctly.")
else:
    print("❌ SOME CHECKS FAILED!")
    print("\nPlease ensure:")
    print("1. {% load socialaccount %} is present in both templates")
    print("2. It appears after {% extends 'base.html' %}")
    print("3. Both login and signup templates are syntactically correct")

print("=" * 80)
print("\nTo test the fix:")
print("1. Run: python manage.py runserver 8000")
print("2. Visit: http://127.0.0.1:8000/login/")
print("3. Visit: http://127.0.0.1:8000/signup/")
print("4. Look for Google OAuth buttons")
print("=" * 80)

