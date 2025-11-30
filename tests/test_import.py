#!/usr/bin/env python
import sys
print("Python version:", sys.version)
print("Python executable:", sys.executable)

try:
    import requests
    print("✓ requests imported successfully")
except ImportError as e:
    print("✗ Failed to import requests:", e)

try:
    import django
    print("✓ django imported successfully")
except ImportError as e:
    print("✗ Failed to import django:", e)

try:
    import allauth
    print("✓ allauth imported successfully")
except ImportError as e:
    print("✗ Failed to import allauth:", e)

try:
    import widget_tweaks
    print("✓ widget_tweaks imported successfully")
except ImportError as e:
    print("✗ Failed to import widget_tweaks:", e)

print("\nAll imports completed!")

