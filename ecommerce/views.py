from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, UserProfile, Order, ShippingMethod, TaxRate
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
import json
from django.http import JsonResponse


def home(request):
    """Homepage with featured products"""
    from .models import TrendingImage, Coupon
    from django.utils import timezone

    featured_products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()
    trending_images = TrendingImage.objects.filter(is_active=True)

    # Get featured coupon if available and valid
    now = timezone.now()
    featured_coupon = Coupon.objects.filter(
        is_featured=True,
        is_active=True,
        valid_from__lte=now,
        valid_until__gte=now
    ).first()

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'trending_images': trending_images,
        'featured_coupon': featured_coupon,
        'page_title': 'Home'
    }
    return render(request, 'ecommerce/home.html', context)


def product_list(request):
    """Display all products with filtering"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Search
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Sorting
    sort = request.GET.get('sort', '-created_at')
    products = products.order_by(sort)

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'page_title': 'Products'
    }
    return render(request, 'ecommerce/product_list.html', context)


def product_detail(request, slug):
    """Display product details"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
        'page_title': product.name
    }
    return render(request, 'ecommerce/product_detail.html', context)


def signup(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('ecommerce:home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create cart for new user (signal should handle this)
            Cart.objects.get_or_create(user=user)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('ecommerce:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'page_title': 'Sign Up'
    }
    return render(request, 'ecommerce/signup.html', context)


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('ecommerce:home')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('ecommerce:home')
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
        'page_title': 'Login'
    }
    return render(request, 'ecommerce/login.html', context)


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('ecommerce:home')


@login_required(login_url='ecommerce:login')
def profile(request):
    """User profile"""
    from .models import Order, Wishlist

    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('ecommerce:profile')
    else:
        form = UserProfileForm(instance=user_profile)

    # Calculate statistics
    total_orders = Order.objects.filter(user=request.user).count()
    completed_orders = Order.objects.filter(user=request.user, status='completed').count()
    pending_orders = Order.objects.filter(user=request.user, status='pending').count()

    # Get wishlist count
    wishlist_count = 0
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_count = wishlist.products.count()
    except Wishlist.DoesNotExist:
        wishlist_count = 0

    context = {
        'form': form,
        'user_profile': user_profile,
        'page_title': 'My Profile',
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'wishlist_count': wishlist_count,
    }
    return render(request, 'ecommerce/profile.html', context)


@login_required(login_url='ecommerce:login')
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    quantity = int(request.POST.get('quantity', 1))

    # Validate stock
    if quantity > product.stock:
        messages.error(request, f'Only {product.stock} items available in stock!')
        return redirect(request.META.get('HTTP_REFERER', 'ecommerce:home'))

    if quantity <= 0:
        messages.error(request, 'Quantity must be greater than 0!')
        return redirect(request.META.get('HTTP_REFERER', 'ecommerce:home'))

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        # Check if total quantity exceeds stock
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            messages.error(request, f'Only {product.stock - cart_item.quantity} more items can be added!')
            return redirect('ecommerce:cart')
        cart_item.quantity = new_quantity
        cart_item.save()

    messages.success(request, f'{product.name} added to cart!')
    return redirect('ecommerce:cart')


@login_required(login_url='ecommerce:login')
def cart_view(request):
    """View shopping cart"""
    from decimal import Decimal
    from .models import ShippingMethod, TaxRate

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    # Get admin-configured shipping and tax
    # First try to get default tax rate, if not available get any active tax rate
    tax_rate = TaxRate.objects.filter(is_active=True, is_default=True).first()
    if not tax_rate:
        tax_rate = TaxRate.objects.filter(is_active=True).first()

    shipping_method = ShippingMethod.objects.filter(is_active=True).first()

    subtotal = Decimal(str(cart.get_total()))
    shipping = Decimal(str(shipping_method.price)) if shipping_method else Decimal('0.00')

    if tax_rate:
        tax_amount = Decimal(str(tax_rate.calculate_tax(subtotal + shipping)))
    else:
        tax_amount = Decimal('0.00')

    total_amount = subtotal + shipping + tax_amount

    context = {
        'cart': cart,
        'subtotal': subtotal,
        'shipping': shipping,
        'shipping_method': shipping_method,
        'tax_amount': tax_amount,
        'tax_rate': tax_rate,
        'total_amount': total_amount,
        'page_title': 'Shopping Cart'
    }
    return render(request, 'ecommerce/cart.html', context)


@login_required(login_url='ecommerce:login')
def remove_from_cart(request, cart_item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('ecommerce:cart')


@login_required(login_url='ecommerce:login')
def update_cart_item(request, cart_item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    # Validate stock
    if quantity > cart_item.product.stock:
        messages.error(request, f'Only {cart_item.product.stock} items available in stock!')
        return redirect('ecommerce:cart')

    if quantity <= 0:
        messages.error(request, 'Quantity must be greater than 0!')
        return redirect('ecommerce:cart')

    cart_item.quantity = quantity
    cart_item.save()
    messages.success(request, 'Cart updated!')

    return redirect('ecommerce:cart')


@login_required(login_url='ecommerce:login')
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    from .models import Wishlist

    product = get_object_or_404(Product, id=product_id)

    # Get or create wishlist for user
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.info(request, f'{product.name} removed from wishlist!')
    else:
        wishlist.products.add(product)
        messages.success(request, f'{product.name} added to wishlist!')

    return redirect(request.META.get('HTTP_REFERER', 'ecommerce:home'))


@login_required(login_url='ecommerce:login')
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    from .models import Wishlist

    product = get_object_or_404(Product, id=product_id)

    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist.products.remove(product)
        messages.success(request, f'{product.name} removed from wishlist!')
    except Wishlist.DoesNotExist:
        messages.error(request, 'Wishlist not found!')

    return redirect(request.META.get('HTTP_REFERER', 'ecommerce:home'))


@login_required(login_url='ecommerce:login')
def share_product(request, product_id):
    """Generate shareable link for product"""
    product = get_object_or_404(Product, id=product_id)
    from django.urls import reverse
    product_url = request.build_absolute_uri(reverse('ecommerce:product_detail', kwargs={'slug': product.slug}))

    context = {
        'product': product,
        'share_url': product_url,
        'share_text': f'Check out {product.name} on Order2Wear!',
    }
    return render(request, 'ecommerce/share_product.html', context)


@login_required(login_url='ecommerce:login')
def update_cart_item_ajax(request, cart_item_id):
    """Update cart item quantity via AJAX and return updated totals"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from decimal import Decimal

        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))

        # Validate quantity against stock
        if quantity > cart_item.product.stock:
            return JsonResponse({
                'success': False,
                'message': f'Only {cart_item.product.stock} items available in stock!'
            })

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            return JsonResponse({'success': False, 'message': 'Quantity must be at least 1'})

        # Calculate new totals
        from .models import ShippingMethod, TaxRate

        cart = cart_item.cart
        shipping_method = ShippingMethod.objects.filter(is_active=True).first()
        # First try to get default tax rate, if not available get any active tax rate
        tax_rate = TaxRate.objects.filter(is_active=True, is_default=True).first()
        if not tax_rate:
            tax_rate = TaxRate.objects.filter(is_active=True).first()

        subtotal = Decimal(str(cart.get_total()))
        shipping = Decimal(str(shipping_method.price)) if shipping_method else Decimal('0.00')

        if tax_rate:
            tax_amount = Decimal(str(tax_rate.calculate_tax(subtotal + shipping)))
        else:
            tax_amount = Decimal('0.00')

        total_amount = subtotal + shipping + tax_amount

        return JsonResponse({
            'success': True,
            'item_total': float(cart_item.get_total()),
            'subtotal': float(subtotal),
            'tax': float(tax_amount),
            'total': float(total_amount),
            'message': 'Cart updated successfully!'
        })

    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required(login_url='ecommerce:login')
def wishlist_view(request):
    """Display user's wishlist"""
    from .models import Wishlist

    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlisted_products = wishlist.products.all()
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(user=request.user)
        wishlisted_products = wishlist.products.all()

    context = {
        'wishlisted_products': wishlisted_products,
        'page_title': 'My Wishlist'
    }
    return render(request, 'ecommerce/wishlist.html', context)


def about_view(request):
    """About page view"""
    context = {
        'page_title': 'About Us'
    }
    return render(request, 'ecommerce/about.html', context)


def blog_view(request):
    """Blog page view with published posts"""
    from .models import BlogPost, BlogCategory

    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    featured_post = BlogPost.objects.filter(is_published=True, is_featured=True).first()
    categories = BlogCategory.objects.all()

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)

    # Search
    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    context = {
        'posts': posts,
        'featured_post': featured_post,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'page_title': 'Blog'
    }
    return render(request, 'ecommerce/blog.html', context)


def blog_detail(request, slug):
    """Blog post detail view"""
    from .models import BlogPost

    post = get_object_or_404(BlogPost, slug=slug, is_published=True)

    # Increment views
    post.views += 1
    post.save(update_fields=['views'])

    # Get related posts
    related_posts = BlogPost.objects.filter(
        is_published=True,
        category=post.category
    ).exclude(id=post.id)[:3]

    context = {
        'post': post,
        'related_posts': related_posts,
        'page_title': post.title
    }
    return render(request, 'ecommerce/blog_detail.html', context)


@login_required(login_url='ecommerce:login')
def my_orders(request):
    """Display user's orders"""
    from .models import Order

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
        'page_title': 'My Orders'
    }
    return render(request, 'ecommerce/my_orders.html', context)


@login_required(login_url='ecommerce:login')
def order_detail(request, order_id):
    """Display order details"""
    from .models import Order

    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        'order': order,
        'page_title': f'Order #{order.id}'
    }
    return render(request, 'ecommerce/order_detail.html', context)


@login_required(login_url='ecommerce:login')
def settings_view(request):
    """User settings page"""
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('ecommerce:settings')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
        'user_profile': user_profile,
        'page_title': 'Settings'
    }
    return render(request, 'ecommerce/settings.html', context)


@login_required(login_url='ecommerce:login')
def checkout(request):
    """Checkout page with payment processing"""
    from decimal import Decimal
    from .models import Order, OrderItem, Cart, Coupon

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty!')
        return redirect('ecommerce:cart')

    if not cart.items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('ecommerce:cart')

    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Get applied coupon from session
    applied_coupon = None
    coupon_discount = Decimal('0.00')

    if 'applied_coupon' in request.session:
        try:
            applied_coupon = Coupon.objects.get(code__iexact=request.session['applied_coupon'])
            if applied_coupon.is_valid():
                subtotal = Decimal(str(cart.get_total()))
                coupon_discount = Decimal(str(applied_coupon.get_discount_amount(subtotal)))
        except Coupon.DoesNotExist:
            del request.session['applied_coupon']

    if request.method == 'POST':
        # Get form data for shipping information
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        shipping_address = request.POST.get('shipping_address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        country = request.POST.get('country', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')

        # Validate required fields
        if not all([first_name, last_name, email, phone, shipping_address, city, state, postal_code, country]):
            messages.error(request, 'Please fill in all required shipping information fields.')
            return redirect('ecommerce:checkout')

        # Get admin-configured shipping and tax
        from .models import ShippingMethod, TaxRate
        shipping_method = ShippingMethod.objects.filter(is_active=True).first()
        # First try to get default tax rate, if not available get any active tax rate
        tax_rate = TaxRate.objects.filter(is_active=True, is_default=True).first()
        if not tax_rate:
            tax_rate = TaxRate.objects.filter(is_active=True).first()

        # Calculate totals
        subtotal = Decimal(str(cart.get_total()))
        shipping = Decimal(str(shipping_method.price)) if shipping_method else Decimal('0.00')
        subtotal_with_coupon = subtotal - coupon_discount

        if tax_rate:
            tax_amount = Decimal(str(tax_rate.calculate_tax(subtotal_with_coupon + shipping)))
        else:
            tax_amount = Decimal('0.00')

        total_amount = subtotal_with_coupon + shipping + tax_amount

        # Create order with shipping information and references to shipping and tax
        order = Order.objects.create(
            user=request.user,
            shipping_method=shipping_method,
            tax_rate=tax_rate,
            subtotal=subtotal,
            shipping_cost=shipping,
            tax_amount=tax_amount,
            total_amount=total_amount,
            status='pending'
        )

        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            # Update product sold count
            cart_item.product.total_sold += cart_item.quantity
            cart_item.product.save(update_fields=['total_sold'])

        # Apply coupon if exists
        if applied_coupon:
            applied_coupon.apply()
            del request.session['applied_coupon']

        # Process payment
        if payment_method == 'card':
            # Credit card (currently disabled in frontend)
            order.status = 'completed'
            order.save(update_fields=['status'])
            cart.items.all().delete()
            messages.success(request, f'Order #{order.id} placed successfully! Payment processed.')
            return redirect('ecommerce:order_detail', order_id=order.id)
        elif payment_method == 'cod':
            # Cash on Delivery (Only enabled payment method)
            order.status = 'pending'
            order.save(update_fields=['status'])
            cart.items.all().delete()
            messages.success(request, f'Order #{order.id} placed! We will contact you for payment confirmation.')
            return redirect('ecommerce:order_detail', order_id=order.id)
        else:
            # Any other payment method (currently disabled)
            order.status = 'pending'
            order.save(update_fields=['status'])
            cart.items.all().delete()
            messages.success(request, f'Order #{order.id} placed! Awaiting payment verification.')
            return redirect('ecommerce:order_detail', order_id=order.id)

    # Get admin-configured shipping and tax
    from .models import ShippingMethod, TaxRate
    shipping_method = ShippingMethod.objects.filter(is_active=True).first()
    # First try to get default tax rate, if not available get any active tax rate
    tax_rate = TaxRate.objects.filter(is_active=True, is_default=True).first()
    if not tax_rate:
        tax_rate = TaxRate.objects.filter(is_active=True).first()

    # Calculate totals
    subtotal = Decimal(str(cart.get_total()))
    shipping = Decimal(str(shipping_method.price)) if shipping_method else Decimal('0.00')
    subtotal_with_coupon = subtotal - coupon_discount

    if tax_rate:
        tax_amount = Decimal(str(tax_rate.calculate_tax(subtotal_with_coupon + shipping)))
    else:
        tax_amount = Decimal('0.00')

    total_amount = subtotal_with_coupon + shipping + tax_amount

    context = {
        'cart': cart,
        'user_profile': user_profile,
        'subtotal': subtotal,
        'coupon_discount': coupon_discount,
        'shipping': shipping,
        'shipping_method': shipping_method,
        'tax_amount': tax_amount,
        'tax_rate': tax_rate,
        'total_amount': total_amount,
        'applied_coupon': applied_coupon,
        'page_title': 'Checkout'
    }
    return render(request, 'ecommerce/checkout.html', context)


@login_required(login_url='ecommerce:login')
def apply_coupon(request):
    """Apply coupon code to cart via AJAX"""
    from decimal import Decimal
    from .models import Cart, Coupon

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        coupon_code = request.POST.get('coupon_code', '').strip().upper()

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Cart is empty!'
            })

        try:
            # Use case-insensitive lookup
            coupon = Coupon.objects.get(code__iexact=coupon_code)
        except Coupon.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': f'Coupon code "{coupon_code}" not found!'
            })

        # Check if coupon is valid
        if not coupon.is_valid():
            if coupon.current_uses >= coupon.max_uses:
                return JsonResponse({
                    'success': False,
                    'message': 'This coupon has reached its usage limit!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'This coupon is no longer valid!'
                })

        # Check minimum order amount
        subtotal = Decimal(str(cart.get_total()))
        if subtotal < coupon.min_order_amount:
            return JsonResponse({
                'success': False,
                'message': f'Minimum order amount ${coupon.min_order_amount} required for this coupon!'
            })

        # Apply coupon - store the actual code from database
        request.session['applied_coupon'] = coupon.code
        coupon_discount = Decimal(str(coupon.get_discount_amount(subtotal)))

        # Get admin-configured shipping and tax
        from .models import ShippingMethod, TaxRate
        shipping_method = ShippingMethod.objects.filter(is_active=True).first()
        # First try to get default tax rate, if not available get any active tax rate
        tax_rate = TaxRate.objects.filter(is_active=True, is_default=True).first()
        if not tax_rate:
            tax_rate = TaxRate.objects.filter(is_active=True).first()

        # Recalculate totals
        subtotal_with_coupon = subtotal - coupon_discount
        shipping = Decimal(str(shipping_method.price)) if shipping_method else Decimal('0.00')

        if tax_rate:
            tax_amount = Decimal(str(tax_rate.calculate_tax(subtotal_with_coupon + shipping)))
        else:
            tax_amount = Decimal('0.00')

        total_amount = subtotal_with_coupon + shipping + tax_amount

        return JsonResponse({
            'success': True,
            'message': f'Coupon "{coupon_code}" applied successfully!',
            'coupon_code': coupon_code,
            'coupon_discount': float(coupon_discount),
            'subtotal': float(subtotal),
            'subtotal_with_coupon': float(subtotal_with_coupon),
            'tax': float(tax_amount),
            'total': float(total_amount)
        })

    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required(login_url='ecommerce:login')
def remove_coupon(request):
    """Remove applied coupon code"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from decimal import Decimal
        from .models import Cart

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Cart is empty!'
            })

        if 'applied_coupon' in request.session:
            del request.session['applied_coupon']

        # Get admin-configured shipping and tax
        from .models import ShippingMethod, TaxRate
        shipping_method = ShippingMethod.objects.filter(is_active=True).first()
        # First try to get default tax rate, if not available get any active tax rate
        tax_rate = TaxRate.objects.filter(is_active=True, is_default=True).first()
        if not tax_rate:
            tax_rate = TaxRate.objects.filter(is_active=True).first()

        # Recalculate totals without coupon using admin config
        subtotal = Decimal(str(cart.get_total()))
        shipping = Decimal(str(shipping_method.price)) if shipping_method else Decimal('0.00')

        if tax_rate:
            tax_amount = Decimal(str(tax_rate.calculate_tax(subtotal + shipping)))
        else:
            tax_amount = Decimal('0.00')

        total_amount = subtotal + shipping + tax_amount

        return JsonResponse({
            'success': True,
            'message': 'Coupon removed successfully!',
            'subtotal': float(subtotal),
            'tax': float(tax_amount),
            'total': float(total_amount),
            'coupon_discount': 0.0
        })

    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required(login_url='ecommerce:login')
def download_invoice(request, order_id):
    """Download order invoice as PDF with professional formatting"""
    from django.http import HttpResponse
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from io import BytesIO

    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.5*inch, leftMargin=0.5*inch,
                          topMargin=0.5*inch, bottomMargin=0.5*inch)

    elements = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=6,
        alignment=1
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        spaceBefore=12
    )

    # Title
    elements.append(Paragraph("🛍️ Order2Wear Invoice", title_style))
    elements.append(Spacer(1, 0.2*inch))

    # Invoice header info
    header_data = [
        ['Invoice #', f'{order.id}', 'Date', order.created_at.strftime('%B %d, %Y')],
        ['Status', order.get_status_display(), 'Order Time', order.created_at.strftime('%I:%M %p')],
    ]

    header_table = Table(header_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.2*inch))

    # Customer info
    elements.append(Paragraph("Customer Information", heading_style))
    customer_data = [
        ['Name', order.user.get_full_name() or order.user.username],
        ['Email', order.user.email],
    ]

    customer_table = Table(customer_data, colWidths=[1.5*inch, 5*inch])
    customer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(customer_table)
    elements.append(Spacer(1, 0.2*inch))

    # Order items
    elements.append(Paragraph("Order Items", heading_style))

    items_data = [['Product', 'Quantity', 'Unit Price', 'Total']]

    for item in order.items.all():
        items_data.append([
            item.product.name[:40],
            str(item.quantity),
            f'₨{item.price:.2f}',
            f'₨{item.price * item.quantity:.2f}'
        ])

    items_table = Table(items_data, colWidths=[2.5*inch, 1*inch, 1.5*inch, 1.5*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 0.2*inch))

    # Order summary
    elements.append(Paragraph("Order Summary", heading_style))

    summary_data = [
        ['Subtotal', '', f'₨{order.subtotal:.2f}'],
        ['Shipping', f'({order.shipping_method.name if order.shipping_method else "N/A"})', f'₨{order.shipping_cost:.2f}'],
        ['Tax', f'({order.tax_rate.name if order.tax_rate else "N/A"})', f'₨{order.tax_amount:.2f}'],
        ['', '', ''],
        ['TOTAL', '', f'₨{order.total_amount:.2f}'],
    ]

    summary_table = Table(summary_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 3), 'Helvetica'),
        ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 4), (-1, 4), 12),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 4), (-1, 4), colors.white),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))

    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph("Thank you for your purchase!", footer_style))
    elements.append(Paragraph("For any queries, contact: support@order2wear.com", footer_style))
    elements.append(Paragraph("Visit us: www.order2wear.com", footer_style))

    # Build PDF
    doc.build(elements)

    # Return PDF
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice-{order.id}.pdf"'
    return response
