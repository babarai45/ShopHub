from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ecommerce.models import Category, Product, Cart, CartItem, UserProfile


class AuthenticationTests(TestCase):
    """Test user authentication (signup, login, logout)"""

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('ecommerce:signup')
        self.login_url = reverse('ecommerce:login')
        self.logout_url = reverse('ecommerce:logout')
        self.home_url = reverse('ecommerce:home')
        self.profile_url = reverse('ecommerce:profile')

    def test_signup_page_loads(self):
        """Test that signup page loads successfully"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/signup.html')

    def test_signup_creates_user(self):
        """Test user registration"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.signup_url, data)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertRedirects(response, self.login_url)

    def test_signup_creates_profile(self):
        """Test that UserProfile is created on signup"""
        data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }
        self.client.post(self.signup_url, data)
        user = User.objects.get(username='testuser2')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_signup_creates_cart(self):
        """Test that Cart is created on signup"""
        data = {
            'username': 'testuser3',
            'email': 'test3@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }
        self.client.post(self.signup_url, data)
        user = User.objects.get(username='testuser3')
        self.assertTrue(Cart.objects.filter(user=user).exists())

    def test_duplicate_email_signup_fails(self):
        """Test that duplicate email signup fails"""
        # Create first user
        User.objects.create_user('user1', 'same@example.com', 'pass123')

        # Try to create second user with same email
        data = {
            'username': 'user2',
            'email': 'same@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='user2').exists())

    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/login.html')

    def test_user_login(self):
        """Test user login"""
        User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, self.home_url)

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        """Test user logout"""
        user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)

    def test_profile_requires_login(self):
        """Test that profile page requires login"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.login_url, response.url)

    def test_authenticated_user_profile_access(self):
        """Test authenticated user can access profile"""
        user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/profile.html')


class HomePageTests(TestCase):
    """Test home page and product display"""

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('ecommerce:home')

        # Create test category and products
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.products = [
            Product.objects.create(
                name=f'Product {i}',
                slug=f'product-{i}',
                description=f'Description {i}',
                price=f'{50 + i}.00',
                category=self.category,
                stock=10,
                is_active=True
            ) for i in range(10)
        ]

    def test_home_page_loads(self):
        """Test home page loads successfully"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/home.html')

    def test_featured_products_displayed(self):
        """Test featured products are displayed on home page"""
        response = self.client.get(self.home_url)
        self.assertIn('featured_products', response.context)
        self.assertEqual(len(response.context['featured_products']), 8)

    def test_categories_displayed(self):
        """Test categories are displayed on home page"""
        response = self.client.get(self.home_url)
        self.assertIn('categories', response.context)
        self.assertIn(self.category, response.context['categories'])


class ProductTests(TestCase):
    """Test product listing and details"""

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test Description',
            price='99.99',
            category=self.category,
            stock=50,
            is_active=True
        )
        self.product_list_url = reverse('ecommerce:product_list')
        self.product_detail_url = reverse('ecommerce:product_detail', args=[self.product.slug])

    def test_product_list_page_loads(self):
        """Test product list page loads"""
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/product_list.html')

    def test_products_displayed(self):
        """Test products are displayed in list"""
        response = self.client.get(self.product_list_url)
        self.assertIn(self.product, response.context['products'])

    def test_product_detail_page_loads(self):
        """Test product detail page loads"""
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/product_detail.html')

    def test_product_detail_content(self):
        """Test product detail contains correct information"""
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.context['product'], self.product)
        self.assertContains(response, self.product.name)
        self.assertContains(response, str(self.product.price))

    def test_product_search(self):
        """Test product search functionality"""
        response = self.client.get(self.product_list_url, {'q': 'Test Product'})
        self.assertIn(self.product, response.context['products'])

    def test_product_filter_by_category(self):
        """Test filtering products by category"""
        response = self.client.get(self.product_list_url, {'category': self.category.id})
        self.assertIn(self.product, response.context['products'])


class CartTests(TestCase):
    """Test shopping cart functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        self.client.login(username='testuser', password='testpass123')

        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test',
            price='99.99',
            category=self.category,
            stock=50,
            is_active=True
        )

        self.cart_url = reverse('ecommerce:cart')
        self.add_to_cart_url = reverse('ecommerce:add_to_cart', args=[self.product.id])

    def test_cart_page_loads(self):
        """Test cart page loads for authenticated user"""
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/cart.html')

    def test_add_to_cart(self):
        """Test adding product to cart"""
        data = {'quantity': 1}
        response = self.client.post(self.add_to_cart_url, data)
        self.assertTrue(CartItem.objects.filter(cart__user=self.user, product=self.product).exists())

    def test_cart_item_quantity(self):
        """Test cart item quantity is set correctly"""
        data = {'quantity': 3}
        self.client.post(self.add_to_cart_url, data)
        cart_item = CartItem.objects.get(cart__user=self.user, product=self.product)
        self.assertEqual(cart_item.quantity, 3)

    def test_add_duplicate_to_cart(self):
        """Test adding same product again increases quantity"""
        self.client.post(self.add_to_cart_url, {'quantity': 1})
        self.client.post(self.add_to_cart_url, {'quantity': 2})
        cart_item = CartItem.objects.get(cart__user=self.user, product=self.product)
        self.assertEqual(cart_item.quantity, 3)

    def test_cart_requires_login(self):
        """Test cart page requires login"""
        self.client.logout()
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 302)

    def test_remove_from_cart(self):
        """Test removing item from cart"""
        self.client.post(self.add_to_cart_url, {'quantity': 1})
        cart_item = CartItem.objects.get(cart__user=self.user, product=self.product)
        remove_url = reverse('ecommerce:remove_from_cart', args=[cart_item.id])
        self.client.post(remove_url, {})
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())


class NavigationTests(TestCase):
    """Test navigation and page access"""

    def setUp(self):
        self.client = Client()

    def test_navbar_links_accessible(self):
        """Test all navbar links are accessible"""
        urls = [
            reverse('ecommerce:home'),
            reverse('ecommerce:product_list'),
            reverse('ecommerce:signup'),
            reverse('ecommerce:login'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"URL {url} failed")

    def test_redirect_to_home_after_login(self):
        """Test user is redirected to home after login"""
        User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('ecommerce:login'), data)
        self.assertRedirects(response, reverse('ecommerce:home'))

