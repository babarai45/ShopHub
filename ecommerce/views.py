from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, UserProfile
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm


def home(request):
    """Homepage with featured products"""
    featured_products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()
    context = {
        'featured_products': featured_products,
        'categories': categories,
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
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('ecommerce:profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
        'user_profile': user_profile,
        'page_title': 'My Profile'
    }
    return render(request, 'ecommerce/profile.html', context)


@login_required(login_url='ecommerce:login')
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, f'{product.name} added to cart!')
    return redirect('ecommerce:cart')


@login_required(login_url='ecommerce:login')
def cart_view(request):
    """View shopping cart"""
    from decimal import Decimal

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    subtotal = Decimal(str(cart.get_total()))
    shipping = Decimal('5.00')
    tax_amount = round((subtotal + shipping) * Decimal('0.1'), 2)
    total_amount = subtotal + shipping + tax_amount

    context = {
        'cart': cart,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax_amount': tax_amount,
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

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated!')

    return redirect('ecommerce:cart')

