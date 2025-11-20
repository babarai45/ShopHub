from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Original price before discount')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', default='products/default.png')
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_sold = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, help_text='Average rating out of 5')
    total_reviews = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name

    def get_discount_percentage(self):
        """Calculate discount percentage if original_price exists"""
        if self.original_price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return int(discount)
        return 0


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s profile"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total(self):
        return sum(item.get_total() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} in {self.cart.user.username}'s cart"

    def get_total(self):
        return self.product.price * self.quantity


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, related_name='wishlisted_by', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wishlist for {self.user.username}"


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    emoji = models.CharField(max_length=10, default='📝')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    short_description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='blog/', default='blog/default.png')
    emoji = models.CharField(max_length=10, default='📝')
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['is_published']),
        ]

    def __str__(self):
        return self.title

    def get_short_content(self):
        """Get first 150 characters of content"""
        return self.content[:150] + '...' if len(self.content) > 150 else self.content
