# API & URL Endpoints Reference

## 🏠 Public Pages (No Login Required)

### Home Page
- **URL**: `/`
- **Method**: GET
- **Template**: `ecommerce/home.html`
- **Features**:
  - Hero section with CTA
  - Featured products (8 items)
  - Statistics showcase
  - Feature highlights
  - Newsletter signup
  - Responsive design

### Product List
- **URL**: `/products/`
- **Method**: GET
- **Query Parameters**:
  - `q=<search>` - Search by name/description
  - `category=<id>` - Filter by category
  - `sort=<field>` - Sort by: `-created_at`, `name`, `price`, `-price`
- **Template**: `ecommerce/product_list.html`
- **Features**:
  - Browse all products
  - Search functionality
  - Category filtering
  - Sorting options
  - Pagination ready

### Product Detail
- **URL**: `/product/<slug>/`
- **Method**: GET
- **Variables**:
  - `slug` - Product URL slug (e.g., "wireless-headphones")
- **Template**: `ecommerce/product_detail.html`
- **Features**:
  - Full product information
  - Image gallery
  - Detailed description
  - Stock status
  - Related products
  - Add to cart form

### Sign Up
- **URL**: `/signup/`
- **Method**: GET, POST
- **Template**: `ecommerce/signup.html`
- **Form Fields**:
  - `username` - Required, unique
  - `email` - Required, unique
  - `password1` - Required, validated
  - `password2` - Must match password1
  - `first_name` - Optional
  - `last_name` - Optional
- **Redirects**: 
  - Success: `/login/`
  - Already logged in: `/`
- **Auto Creates**: 
  - UserProfile
  - Shopping Cart

### Login
- **URL**: `/login/`
- **Method**: GET, POST
- **Template**: `ecommerce/login.html`
- **Form Fields**:
  - `username` - Username or email
  - `password` - User password
  - `remember` - Optional checkbox
- **Redirects**:
  - Success: `/`
  - Already logged in: `/`
- **Features**:
  - Email/username login
  - Validation
  - Error messages

---

## 🔒 Authenticated Pages (Login Required)

### User Logout
- **URL**: `/logout/`
- **Method**: GET
- **Auth Required**: YES
- **Redirects**: `/` (home)
- **Features**:
  - Clear session
  - Success message
  - Redirect home

### User Profile
- **URL**: `/profile/`
- **Method**: GET, POST
- **Auth Required**: YES
- **Template**: `ecommerce/profile.html`
- **GET Features**:
  - Display user information
  - Show current profile picture
  - Display address info
  - Show account statistics
  
- **POST Fields** (Update Profile):
  - `phone` - Phone number
  - `address` - Street address
  - `city` - City/Town
  - `state` - State/Province
  - `postal_code` - ZIP/Postal code
  - `country` - Country name
  - `profile_image` - Profile picture (JPG, PNG, GIF)
  
- **Redirects**: 
  - Success: `/profile/`
  - Not logged in: `/login/`

### Shopping Cart View
- **URL**: `/cart/`
- **Method**: GET
- **Auth Required**: YES
- **Template**: `ecommerce/cart.html`
- **Features**:
  - Display all cart items
  - Show quantities
  - Display item prices
  - Calculate subtotal
  - Calculate shipping ($5.00)
  - Calculate tax (10%)
  - Show total
  - Remove item buttons
  - Update quantity buttons
  - Checkout button (UI ready)

### Add to Cart
- **URL**: `/add-to-cart/<id>/`
- **Method**: POST
- **Auth Required**: YES
- **Form Fields**:
  - `quantity` - Integer (1+)
  
- **POST Parameters**:
  - `<id>` - Product ID (in URL)
  
- **Redirects**: `/cart/`
- **Features**:
  - Add new items
  - Update existing items
  - Success message
  - Stock validation ready

### Remove from Cart
- **URL**: `/remove-from-cart/<id>/`
- **Method**: POST
- **Auth Required**: YES
- **URL Parameters**:
  - `<id>` - CartItem ID
  
- **Redirects**: `/cart/`
- **Features**:
  - Remove single item
  - Success message

### Update Cart Item
- **URL**: `/update-cart-item/<id>/`
- **Method**: POST
- **Auth Required**: YES
- **Form Fields**:
  - `quantity` - New quantity (1+)
  
- **URL Parameters**:
  - `<id>` - CartItem ID
  
- **Redirects**: `/cart/`
- **Features**:
  - Update item quantity
  - Validate quantity
  - Recalculate total

---

## 🔐 Admin Panel

### Admin Dashboard
- **URL**: `/admin/`
- **Auth Required**: YES (staff user)
- **Access**: 
  - Username: `admin`
  - Password: `admin123`

### Admin Features

#### Categories
- **View/List**: Browse all categories
- **Add**: Create new category
- **Edit**: Modify category details
- **Delete**: Remove category
- **Search**: Search by name
- **Fields**: name, slug, description

#### Products
- **View/List**: Browse all products
- **Add**: Create new product
- **Edit**: Modify product details
- **Delete**: Remove product
- **Filter**: By category, active status
- **Search**: By name, description
- **Fields**: name, slug, description, price, category, image, stock, is_active

#### User Profiles
- **View/List**: Browse user profiles
- **View Details**: See full profile info
- **Filter**: By country, creation date
- **Search**: By username, email, phone
- **Fields**: user, phone, address, city, state, postal_code, country, profile_image

#### Shopping Carts
- **View/List**: Browse all carts
- **View Items**: See cart contents
- **View Details**: See cart totals

#### Cart Items
- **View/List**: Browse all cart items
- **Filter**: By creation date
- **Search**: By product name, username

---

## 📊 URL Patterns Summary

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/` | GET | No | Home page |
| `/products/` | GET | No | Product listing |
| `/product/<slug>/` | GET | No | Product details |
| `/signup/` | GET, POST | No | Registration |
| `/login/` | GET, POST | No | Login |
| `/logout/` | GET | Yes | Logout |
| `/profile/` | GET, POST | Yes | Profile management |
| `/cart/` | GET | Yes | View cart |
| `/add-to-cart/<id>/` | POST | Yes | Add product |
| `/remove-from-cart/<id>/` | POST | Yes | Remove product |
| `/update-cart-item/<id>/` | POST | Yes | Update quantity |
| `/admin/` | GET | Yes (staff) | Admin panel |

---

## 🔄 Request/Response Examples

### Sign Up Request
```
POST /signup/
Content-Type: application/x-www-form-urlencoded

username=newuser&email=user@example.com&password1=SecurePass123!&password2=SecurePass123!
```

### Login Request
```
POST /login/
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=testpass123
```

### Add to Cart Request
```
POST /add-to-cart/1/
Content-Type: application/x-www-form-urlencoded
Cookie: sessionid=abc123...

quantity=2
```

### Update Cart Item Request
```
POST /update-cart-item/5/
Content-Type: application/x-www-form-urlencoded
Cookie: sessionid=abc123...

quantity=3
```

---

## 🎯 Navigation Flow

### First-Time Visitor
1. Visit home `/`
2. Browse products `/products/`
3. View product details `/product/<slug>/`
4. Click "Login to Buy" 
5. Sign up at `/signup/`
6. Login at `/login/`
7. Add products to cart
8. View cart `/cart/`

### Registered User
1. Login `/login/`
2. Browse products `/products/`
3. Add to cart (direct)
4. Update profile `/profile/`
5. View cart `/cart/`
6. Logout `/logout/`

### Admin
1. Login `/login/`
2. Visit `/admin/`
3. Manage products, categories, users
4. View statistics

---

## 🚀 Query Parameters Reference

### Product List Filters
```
/products/?category=1              # Filter by category ID
/products/?q=headphones            # Search by name
/products/?sort=price              # Sort by price (low to high)
/products/?sort=-price             # Sort by price (high to low)
/products/?sort=name               # Sort by name (A-Z)
/products/?sort=-created_at        # Sort by newest

# Combined
/products/?category=1&q=wireless&sort=price
```

---

## 📝 Response Status Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 200 | OK | Successful request |
| 302 | Redirect | Login required, form submitted |
| 404 | Not Found | Product/page doesn't exist |
| 405 | Not Allowed | Wrong HTTP method |
| 500 | Server Error | Application error |

---

## 🔐 Session & Authentication

### Django Session
- **Cookie Name**: `sessionid`
- **Duration**: 2 weeks
- **Stored in**: Database

### Login Required
- Protected views redirect to: `/login/`
- Redirect back to original page after login
- Query parameter: `next=/cart/`

### Permissions
- Anonymous: Can view public pages
- Authenticated: Can add to cart, view profile
- Staff: Can access admin panel
- Superuser: Full admin access

---

## 📱 Mobile & Responsive

All endpoints are optimized for:
- ✓ Mobile (320px+)
- ✓ Tablet (768px+)
- ✓ Desktop (1024px+)
- ✓ Large Screens (1536px+)

---

## 🧪 Testing Endpoints

### With curl (Windows PowerShell)
```powershell
# Get home page
curl http://localhost:8000/

# Get products
curl "http://localhost:8000/products/?q=headphones"

# Get product details
curl http://localhost:8000/product/wireless-headphones/

# Login
curl -c cookies.txt -d "username=admin&password=admin123" http://localhost:8000/login/

# View cart (using saved cookies)
curl -b cookies.txt http://localhost:8000/cart/
```

### With Python requests
```python
import requests

session = requests.Session()

# Login
session.post('http://localhost:8000/login/', {
    'username': 'admin',
    'password': 'admin123'
})

# View cart
response = session.get('http://localhost:8000/cart/')
print(response.status_code)
```

---

## 🔍 URL Namespace

All URLs use the `ecommerce` namespace:

```html
<!-- In templates -->
{% url 'ecommerce:home' %}
{% url 'ecommerce:product_list' %}
{% url 'ecommerce:product_detail' slug=product.slug %}
{% url 'ecommerce:login' %}
{% url 'ecommerce:cart' %}
```

---

## 📞 Error Pages

### 404 Not Found
- Product doesn't exist
- Custom handling available

### 403 Forbidden
- Login required
- Auto-redirected to `/login/?next=...`

### 500 Server Error
- Application error
- Check Django logs

---

**For detailed information, see QUICKSTART.md and README.md**

