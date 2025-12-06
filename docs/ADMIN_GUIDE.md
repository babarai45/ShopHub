# Order2Wear Admin Guide 🎛️

## How to Manage Order2Wear as an Administrator

This guide explains how to manage all aspects of Order2Wear through the admin panel.

---

## Table of Contents

1. [Admin Access](#admin-access)
2. [Managing Products](#managing-products)
3. [Managing Orders](#managing-orders)
4. [Managing Shipping Methods](#managing-shipping-methods)
5. [Managing Tax Rates](#managing-tax-rates)
6. [Creating Coupons](#creating-coupons)
7. [Managing Users](#managing-users)
8. [Blog Management](#blog-management)
9. [Dashboard Overview](#dashboard-overview)

---

## Admin Access

### 🔑 Login to Admin Panel

1. Go to: **http://localhost:8000/admin/**
2. Enter **username/email** and **password**
3. Click **"Log in"**
4. See admin dashboard ✅

### 👤 Admin Account

Admin account created during setup:
```bash
python manage.py createsuperuser
```

You'll be prompted for:
- **Username:** admin
- **Email:** admin@order2wear.com
- **Password:** your-secure-password

---

## Managing Products

### ➕ Add New Product

1. Go to **Admin Dashboard**
2. Click **"Products"** under Ecommerce
3. Click **"Add Product"** button
4. Fill in:

| Field | Example | Required |
|-------|---------|----------|
| Name | "Wireless Headphones" | ✅ |
| Description | Product details | ✅ |
| Price (PKR) | 5000 | ✅ |
| Stock | 50 | ✅ |
| Category | Electronics | ✅ |
| Image | Upload file | ✓ |
| SKU | WH-001 | ✓ |
| Is Featured | ✓ (checkbox) | ✓ |

5. Click **"Save"** ✅

### ✏️ Edit Product

1. Go to **Products**
2. Click product name
3. Edit fields as needed
4. Click **"Save"** ✅

### 🗑️ Delete Product

1. Go to **Products**
2. Check product checkbox
3. Select **"Delete selected products"** from dropdown
4. Click **"Go"**
5. Confirm deletion ✅

### 📊 Product Filters

Filter by:
- Category
- Price range
- Stock status
- Featured status
- Creation date

### 🏷️ Manage Categories

1. Go to **Categories**
2. Add new category with:
   - Name
   - Description
   - Slug (auto-generated)
3. Edit or delete existing categories

---

## Managing Orders

### 👁️ View All Orders

1. Go to **Admin Dashboard**
2. Click **"Orders"**
3. See all customer orders with:
   - Order ID
   - Customer name
   - Order date
   - Total amount
   - Status

### 🔍 Order Details

1. Click order ID
2. View:
   - **Order Items:** Products ordered
   - **Customer Info:** Name, email, address
   - **Payment Details:** Method, amount
   - **Shipping:** Cost, method
   - **Tax:** Rate, amount
   - **Timeline:** Order creation date

### ✏️ Update Order Status

1. Open order
2. Edit **Status** field:
   - Pending (Initial)
   - Completed (Shipped)
   - Cancelled
3. Click **"Save"** ✅

### 🔍 Filter Orders

By:
- Status (Pending/Completed/Cancelled)
- Date range
- Customer
- Amount range

### 📋 Order Items

View items in each order:
- Product name
- Quantity
- Unit price
- Total per item

---

## Managing Shipping Methods

### ➕ Add Shipping Method

1. Go to **Admin Dashboard**
2. Click **"Shipping Methods"**
3. Click **"Add Shipping Method"**
4. Fill in:

| Field | Example | Required |
|-------|---------|----------|
| Name | "Standard Delivery" | ✅ |
| Description | Delivery details | ✓ |
| Price (PKR) | 250 | ✅ |
| Estimated Days | 3-5 | ✅ |
| Is Active | ✓ | ✅ |

5. Click **"Save"** ✅

### 📋 Shipping Options

Create multiple options:
- **Standard:** ₨250 - 3-5 days
- **Express:** ₨500 - 1-2 days
- **Overnight:** ₨1000 - Next day

### ✏️ Edit Method

1. Go to **Shipping Methods**
2. Click method name
3. Edit details (price, days, description)
4. Click **"Save"** ✅

### ✅ Activate/Deactivate

1. Open shipping method
2. Check/uncheck **"Is Active"**
3. Save ✅

**Note:** Only active methods shown to customers

---

## Managing Tax Rates

### ➕ Add Tax Rate

1. Go to **Admin Dashboard**
2. Click **"Tax Rates"**
3. Click **"Add Tax Rate"**
4. Fill in:

| Field | Example | Required |
|-------|---------|----------|
| Name | "GST 17%" | ✅ |
| Description | Tax details | ✓ |
| Rate (%) | 17 | ✅ |
| Is Active | ✓ | ✅ |
| Is Default | ✓ | ✓ |

5. Click **"Save"** ✅

### 💰 Tax Examples

- **GST:** 17%
- **Sales Tax:** 5%
- **VAT:** 10%
- **Provincial Tax:** 2%

### ✏️ Edit Tax Rate

1. Go to **Tax Rates**
2. Click tax name
3. Edit rate percentage
4. Click **"Save"** ✅

### 🎯 Set Default Tax

1. Check **"Is Default"** checkbox
2. This tax automatically applied
3. Click **"Save"** ✅

**Note:** Only one can be default

---

## Creating Coupons

### ➕ Add Coupon

1. Go to **Admin Dashboard**
2. Click **"Coupons"**
3. Click **"Add Coupon"**
4. Fill in:

| Field | Example | Details |
|-------|---------|---------|
| Code | SAVE30 | Unique code |
| Type | Percentage | Fixed or % |
| Value | 30 | Discount amount |
| Min Order | 500 | Minimum amount |
| Max Uses | 100 | Usage limit |
| Valid From | Nov 30 | Start date |
| Valid Until | Dec 31 | End date |
| Is Active | ✓ | Enable/disable |
| Is Featured | ✓ | Show on homepage |

5. Click **"Save"** ✅

### 🎟️ Feature Coupon

To show on homepage:
1. Open coupon
2. Check **"Is Featured"** ✅
3. Click **"Save"**
4. Appears on home page with countdown timer

### 📊 Coupon Types

- **Percentage:** Discount % (e.g., 30% off)
- **Fixed Amount:** Fixed rupees (e.g., ₨500 off)

### 💡 Coupon Strategy

**Holiday Sales:**
- BLACKFRIDAY50 - 50% off
- Valid Nov 24-27

**Seasonal:**
- SUMMER25 - 25% off
- Valid June-July

**Customer Appreciation:**
- WELCOME20 - 20% off first purchase
- For new customers

### 📈 Coupon Tracking

See for each coupon:
- Total uses
- Usage limit
- Remaining uses
- Active status
- Featured status

---

## Managing Users

### 👥 View All Users

1. Go to **Users** section
2. See all registered customers
3. View:
   - Username
   - Email
   - Join date
   - Last login

### 👤 View User Details

1. Click username
2. See:
   - Profile info
   - Email
   - Join date
   - Last login
   - Status

### 🔐 Reset Password

1. Click user
2. Find **Password** section
3. Click **"Change Password"**
4. Set new password
5. Save ✅

### ✏️ Edit User Info

1. Click user
2. Edit:
   - Email
   - First/Last name
   - Status
3. Save ✅

### 🗑️ Deactivate User

1. Click user
2. Uncheck **"Active"** checkbox
3. Save ✅

**Note:** User can't login when deactivated

---

## Blog Management

### 📝 Create Blog Post

1. Go to **Blog Posts**
2. Click **"Add Blog Post"**
3. Fill in:

| Field | Required |
|-------|----------|
| Title | ✅ |
| Slug | ✅ |
| Content | ✅ |
| Category | ✓ |
| Featured Image | ✓ |
| Is Published | ✅ |

4. Click **"Save"** ✅

### ✏️ Edit Post

1. Go to **Blog Posts**
2. Click post title
3. Edit content
4. Update image if needed
5. Save ✅

### 🗑️ Delete Post

1. Select post checkbox
2. Choose **"Delete selected"**
3. Confirm ✅

### 🏷️ Blog Categories

1. Go to **Blog Categories**
2. Create categories for posts
3. Organize content

### 🖼️ Trending Images

Manage homepage slider:
1. Go to **Trending Images**
2. Add image with:
   - Image file
   - Title
   - Subtitle
   - Link (optional)
3. Active images show on homepage

---

## Dashboard Overview

### 📊 Main Statistics

View on dashboard:
- **Total Orders:** All orders placed
- **Completed Orders:** Delivered orders
- **Pending Orders:** Awaiting delivery
- **Total Users:** Registered customers
- **Total Products:** In catalog
- **Total Sales:** Revenue

### 🎯 Quick Actions

Shortcuts to:
- Add product
- View orders
- Manage users
- Create coupon
- Manage shipping

### 📈 Recent Activity

See:
- Recent orders
- New users
- Latest reviews
- Recent sales

---

## 🔧 System Configuration

### Settings to Configure

**On First Setup:**

1. **Shipping Methods:**
   - Add at least 1 method
   - Set prices in PKR

2. **Tax Rates:**
   - Add default tax rate
   - Set percentage

3. **Products:**
   - Upload products
   - Set prices
   - Assign categories

4. **Coupons:**
   - Create promotional coupons
   - Set featured coupons

---

## 📋 Checklist: Admin Setup

- ✅ Create admin account
- ✅ Add shipping methods
- ✅ Add tax rates
- ✅ Add product categories
- ✅ Add products with prices
- ✅ Create coupons
- ✅ Create blog posts
- ✅ Upload trending images
- ✅ Test ordering process

---

## 🆘 Troubleshooting

### Issue: Can't login
**Solution:** 
- Verify username/password
- Check if account is active
- Reset password

### Issue: Price not showing
**Solution:**
- Ensure shipping method added
- Ensure tax rate added
- Refresh page

### Issue: Coupon not appearing
**Solution:**
- Check "Is Featured" is checked
- Check "Is Active" is checked
- Check dates are valid

### Issue: Order not showing
**Solution:**
- Refresh admin page
- Check database migration
- Verify order was created

---

## 🔒 Admin Best Practices

- ✅ Use strong password
- ✅ Log out when done
- ✅ Regularly backup database
- ✅ Keep prices updated
- ✅ Monitor orders regularly
- ✅ Respond to inquiries promptly
- ✅ Review sales data
- ✅ Test new features

---

## 📞 Support

For admin support:
- Email: support@order2wear.com
- Check developer guide for technical issues

---

**Happy Managing! 🎛️**

*Last Updated: November 30, 2025*

