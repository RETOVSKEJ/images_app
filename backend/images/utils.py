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
    

def helper_generate_image(self):
        self.client.login(username=self.user.username, password='tester123')
        is_authenticated = self.client.session['_auth_user_id'] is not None
        self.assertTrue(is_authenticated, "User is not authenticated")
        
        self.assertIsNotNone(self.user.userprofile, "User does not have a profile")
        self.assertIsNotNone(self.user.userprofile.tier, "User's profile does not have a tier")

        self.client.request()
        image = ImageFactory(owner=self.user.userprofile)

        image_file = SimpleUploadedFile(
            image.file.name, 
            image.file.read(), 
            content_type="image/jpeg"
        )

        data = {
            'file': image_file,
            "owner": image.owner.pk
        }

        return  self.client.post(self.list_create_url, data, format='multipart')
 