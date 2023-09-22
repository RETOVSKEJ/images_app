import uuid
from django.conf import settings
from datetime import datetime
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from io import BytesIO
from .models import Image

def generate_expiring_url(image_id, duration):
    if not (300 <= duration <= 30000):
        raise ValueError("Invalid Duration")

    image = Image.objects.filter(pk=image_id).exists()
    if not image:
        raise ValueError(f'No image found for ID: {image_id}')

    token = str(uuid.uuid4())

    settings.REDIS.setex(token, duration, value=image_id)
    return token

def get_expiring_url(token):
    image_id = settings.REDIS.get(token)
    if not image_id:
        raise ValueError("Invalid or expired url")
    return int(image_id)
    


def generate_thumbnail(image_instance, height):
    """Generate a thumbnail of the image."""
    image_field = image_instance.file

    with PilImage.open(image_field.open()) as img:
        hpercent = height / float(img.size[1])
        wsize = int(float(img.size[0]) * float(hpercent))
        img = img.resize((wsize, height), PilImage.LANCZOS)
        
        thumbnail_io = BytesIO()

        if str(image_field).lower().endswith(('.jpg', '.jpeg')):
            format = 'JPEG'
        elif str(image_field).lower().endswith('.png'):
            format = 'PNG'

        img.save(thumbnail_io, format=format, quality=85)
        
        filename = f"{height}px.{format.lower()}"
        return ContentFile(thumbnail_io.getvalue(), name=filename)