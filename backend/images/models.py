from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

UserModel = get_user_model()

### USER MODEL ###

class UserProfile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, primary_key=True)
    tier = models.ForeignKey('Tier', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'{self.user.username}({self.tier})'

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        if instance.is_staff:
            profile.tier = Tier.objects.filter(name__iexact='Enterprise').first()
        else:    
            profile.tier = Tier.objects.filter(name__iexact='Basic').first()

@receiver(post_save, sender=UserModel)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

### OTHER MODELS ###

class ThumbnailSize(models.Model):
    height = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.height}px'

class Tier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    thumbnail_sizes = models.ManyToManyField(ThumbnailSize)
    original_urls = models.BooleanField(default=False)
    expiring_urls = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

class Image(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to=f'images/')
    
    # @property
    # def expiring_url(self):
    # TODO
    #     return uuid4     

    def __str__(self):
        return f'{self.owner} -> {self.file}'

class Thumbnail(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='thumbnails')
    size = models.ForeignKey(ThumbnailSize, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=f'thumbnails/')


    def __str__(self):
        return f'{self.size} {self.file}'
        
        



