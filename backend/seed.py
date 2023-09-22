import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from images.models import Tier, ThumbnailSize


print(Tier.objects.all())
print(ThumbnailSize.objects.all())

def create_standard_tiers():
    # Check if the tiers already exist, if they do, don't recreate them
    if not Tier.objects.exists():
        t_200 = ThumbnailSize.objects.create(height=200)
        t_400 = ThumbnailSize.objects.create(height=400)

        basic = Tier.objects.create(name="Basic")
        basic.thumbnail_sizes.add(t_200)

        premium = Tier.objects.create(name="Premium", original_urls=True)
        premium.thumbnail_sizes.add(t_200, t_400)

        enterprise = Tier.objects.create(name="Enterprise", original_urls=True, expiring_urls=True)
        enterprise.thumbnail_sizes.add(t_200, t_400)

# if __name__ == "__main__":
#     create_standard_tiers()