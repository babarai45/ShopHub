from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

app_name = 'ecommerce'

urlpatterns = [
    # Home and products
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password Reset
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='ecommerce/password_reset.html',
             form_class=CustomPasswordResetForm,
             email_template_name='ecommerce/password_reset_email.html',
             subject_template_name='ecommerce/password_reset_subject.txt',
             success_url=reverse_lazy('ecommerce:password_reset_done')
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='ecommerce/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='ecommerce/password_reset_confirm.html',
             form_class=CustomSetPasswordForm,
             success_url=reverse_lazy('ecommerce:password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='ecommerce/password_reset_complete.html'
         ),
         name='password_reset_complete'),


    # Social auth (Google OAuth)
    path('accounts/', include('allauth.urls')),

    # User profile
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/invoice/', views.download_invoice, name='download_invoice'),

    # Shopping cart
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    path('update-cart-ajax/<int:cart_item_id>/', views.update_cart_item_ajax, name='update_cart_item_ajax'),
    path('checkout/', views.checkout, name='checkout'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),

    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Product sharing
    path('share/<int:product_id>/', views.share_product, name='share_product'),

    # Pages
    path('about/', views.about_view, name='about'),
    path('blog/', views.blog_view, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
]

