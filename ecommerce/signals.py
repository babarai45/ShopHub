from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Cart, Wishlist


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when User is created"""
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """Create Cart when User is created"""
    if created:
        Cart.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def create_user_wishlist(sender, instance, created, **kwargs):
    """Create Wishlist when User is created"""
    if created:
        Wishlist.objects.get_or_create(user=instance)
