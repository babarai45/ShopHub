from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ecommerce.models import Wishlist

class Command(BaseCommand):
    help = 'Create wishlists for users who dont have one'

    def handle(self, *args, **options):
        users_without_wishlist = []
        created_count = 0

        for user in User.objects.all():
            wishlist, created = Wishlist.objects.get_or_create(user=user)
            if created:
                created_count += 1
                users_without_wishlist.append(user.username)

        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_count} wishlists'))
        if users_without_wishlist:
            self.stdout.write(self.style.SUCCESS(f'✓ Users: {", ".join(users_without_wishlist)}'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ All users already have wishlists'))

