import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SepApp.settings')
django.setup()

from django.contrib.auth.models import User
from ecommerce.models import Category, Product

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@shophub.com', 'admin123')
    print("✓ Superuser 'admin' created successfully")
else:
    print("✓ Superuser 'admin' already exists")

# Create test categories
categories_data = [
    {'name': 'Electronics', 'slug': 'electronics', 'description': 'Electronic devices and gadgets'},
    {'name': 'Fashion', 'slug': 'fashion', 'description': 'Clothing, shoes, and accessories'},
    {'name': 'Home & Kitchen', 'slug': 'home-kitchen', 'description': 'Home and kitchen appliances'},
    {'name': 'Sports', 'slug': 'sports', 'description': 'Sports equipment and accessories'},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={
            'name': cat_data['name'],
            'description': cat_data['description']
        }
    )
    if created:
        print(f"✓ Category '{category.name}' created")
    else:
        print(f"✓ Category '{category.name}' already exists")

# Create test products
products_data = [
    {
        'name': 'Wireless Headphones',
        'slug': 'wireless-headphones',
        'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life.',
        'short_description': 'Premium wireless headphones with noise cancellation',
        'price': '99.99',
        'original_price': '149.99',
        'category': 'electronics',
        'stock': 50,
        'rating': '4.5',
        'total_reviews': 156,
        'total_sold': 342
    },
    {
        'name': 'Smart Watch',
        'slug': 'smart-watch',
        'description': 'Feature-rich smartwatch with fitness tracking, heart rate monitor, and GPS.',
        'short_description': 'Advanced smartwatch with health tracking features',
        'price': '199.99',
        'original_price': '249.99',
        'category': 'electronics',
        'stock': 30,
        'rating': '4.3',
        'total_reviews': 89,
        'total_sold': 245
    },
    {
        'name': '4K Webcam',
        'slug': '4k-webcam',
        'description': 'Professional 4K ultra HD webcam perfect for streaming and video conferencing.',
        'short_description': '4K ultra HD streaming webcam',
        'price': '89.99',
        'original_price': '119.99',
        'category': 'electronics',
        'stock': 25,
        'rating': '4.7',
        'total_reviews': 256,
        'total_sold': 578
    },
    {
        'name': 'Winter Jacket',
        'slug': 'winter-jacket',
        'description': 'Comfortable and stylish winter jacket with waterproof material and warm lining.',
        'short_description': 'Waterproof warm winter jacket',
        'price': '89.99',
        'original_price': '129.99',
        'category': 'fashion',
        'stock': 40,
        'rating': '4.2',
        'total_reviews': 142,
        'total_sold': 387
    },
    {
        'name': 'Running Shoes',
        'slug': 'running-shoes',
        'description': 'Professional running shoes with advanced cushioning technology for maximum comfort.',
        'short_description': 'Comfortable professional running shoes',
        'price': '79.99',
        'original_price': '109.99',
        'category': 'fashion',
        'stock': 60,
        'rating': '4.6',
        'total_reviews': 298,
        'total_sold': 651
    },
    {
        'name': 'Designer Sunglasses',
        'slug': 'designer-sunglasses',
        'description': 'Premium designer sunglasses with UV protection and stylish frames.',
        'short_description': 'UV-protected designer sunglasses',
        'price': '129.99',
        'original_price': '199.99',
        'category': 'fashion',
        'stock': 35,
        'rating': '4.4',
        'total_reviews': 178,
        'total_sold': 412
    },
    {
        'name': 'Coffee Maker',
        'slug': 'coffee-maker',
        'description': 'Automatic coffee maker with programmable timer and heat retention.',
        'short_description': 'Smart programmable coffee maker',
        'price': '59.99',
        'original_price': '79.99',
        'category': 'home-kitchen',
        'stock': 45,
        'rating': '4.1',
        'total_reviews': 127,
        'total_sold': 289
    },
    {
        'name': 'Air Fryer',
        'slug': 'air-fryer',
        'description': 'Healthier cooking with our advanced air fryer technology, 6L capacity.',
        'short_description': 'Healthy air fryer cooking appliance',
        'price': '109.99',
        'original_price': '159.99',
        'category': 'home-kitchen',
        'stock': 20,
        'rating': '4.8',
        'total_reviews': 312,
        'total_sold': 723
    },
    {
        'name': 'Yoga Mat',
        'slug': 'yoga-mat',
        'description': 'Non-slip yoga mat with extra cushioning for comfortable practice sessions.',
        'short_description': 'Cushioned non-slip yoga mat',
        'price': '29.99',
        'original_price': '49.99',
        'category': 'sports',
        'stock': 100,
        'rating': '4.5',
        'total_reviews': 487,
        'total_sold': 1245
    },
    {
        'name': 'Dumbbells Set',
        'slug': 'dumbbells-set',
        'description': 'Adjustable dumbbells set with weights from 5kg to 25kg.',
        'short_description': 'Adjustable dumbbell weight set',
        'price': '149.99',
        'original_price': '199.99',
        'category': 'sports',
        'stock': 15,
        'rating': '4.9',
        'total_reviews': 198,
        'total_sold': 567
    },
]

for prod_data in products_data:
    category = Category.objects.get(slug=prod_data.pop('category'))
    slug = prod_data['slug']
    product, created = Product.objects.get_or_create(
        slug=slug,
        defaults={
            **prod_data,
            'category': category,
            'is_active': True
        }
    )
    if created:
        print(f"✓ Product '{product.name}' created with {product.rating} rating")
    else:
        # Update existing product with new data
        for key, value in prod_data.items():
            if hasattr(product, key):
                setattr(product, key, value)
        product.category = category
        product.save()
        print(f"✓ Product '{product.name}' updated with {product.rating} rating")

# Create test users
test_users = [
    {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
    {'username': 'alex_wilson', 'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Wilson'},
]

for user_data in test_users:
    username = user_data['username']
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            email=user_data['email'],
            password='testpass123',
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        print(f"✓ Test user '{username}' created (password: testpass123)")
    else:
        print(f"✓ Test user '{username}' already exists")

print("\n" + "="*50)
print("✓ Database initialized successfully!")
print("="*50)
print("\nAdmin Credentials:")
print("  Username: admin")
print("  Password: admin123")
print("\nTest User Credentials:")
for user_data in test_users:
    print(f"  Username: {user_data['username']}")
    print(f"  Password: testpass123")
print("\n" + "="*50)

