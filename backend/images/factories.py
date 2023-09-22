import factory
from images.models import UserProfile, Image, Tier
from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'tester123')

# class UserProfileFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = UserProfile

#     @factory.post_generation
#     def set_premium(self, create, extracted, **kwargs):
#         if extracted:
#             self.tier = Tier.objects.filter(name__iexact='Premium').first()
#             self.save()

#     @factory.post_generation
#     def set_enterprise(self, create, extracted, **kwargs):
#         if extracted:
#             self.tier = Tier.objects.filter(name__iexact='Enterprise').first()
#             self.save()


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    file = factory.django.ImageField(color='blue')