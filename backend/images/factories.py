import factory
from images.models import UserProfile, Image, Tier
from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'tester123')


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    file = factory.django.ImageField(color='blue')