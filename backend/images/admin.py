from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Tier)
admin.site.register(ThumbnailSize)
admin.site.register(Thumbnail)
admin.site.register(UserProfile)
admin.site.register(Image)