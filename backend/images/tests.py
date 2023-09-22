from rest_framework.test import APITestCase
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .factories import *
from .models import Tier
from seed import create_standard_tiers





# Create your tests here.

class TestSetUp(APITestCase):
    def setUp(self):
        create_standard_tiers()
        self.list_create_url = reverse('image-list-create')  
        self.token_url = reverse('image-expiring', kwargs={"token": "dummy"})
        self.link_url = reverse('image-link', kwargs={"id": 1})  
        self.media_url = reverse('media', kwargs={"file_path": "dummy.jpg"})

        self.basic_tier = Tier.objects.filter(name__iexact="Basic").first()
        self.premium_tier = Tier.objects.filter(name__iexact="Premium").first()
        self.enterprise_tier = Tier.objects.filter(name__iexact="Enterprise", expiring_urls=True).first()

        self.user = UserFactory()
 
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
class TestViews(TestSetUp):
    @staticmethod
    def generate_image(self):
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
        
        response = self.client.post(self.list_create_url, data, format='multipart')
        return response
 

    def test_can_login(self):
        bool = self.client.login(username=self.user.username, password='tester123')
        self.assertTrue(bool)

    def test_can_view_as_anon(self):
        response = self.client.get(self.token_url) 
        self.assertIn(response.status_code, [200, 400])

    def test_cannot_view_as_anon(self):
        response = self.client.get(self.link_url) 
        self.assertEqual(response.status_code, 403)
        response = self.client.get(self.list_create_url) 
        self.assertEqual(response.status_code, 403)
        response = self.client.post(self.list_create_url) 
        self.assertEqual(response.status_code, 403)
        response = self.client.get(self.media_url) 
        self.assertEqual(response.status_code, 403)

    def test_user_have_tier(self):
        self.assertIsNotNone(self.user.userprofile, "User does not have a profile")
        self.assertIsNotNone(self.user.userprofile.tier, "User's profile does not have a tier")


    def test_can_view_as_user(self):
        self.client.login(username=self.user.username, password='tester123')
        response = self.client.get(self.list_create_url) 
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.media_url) 
        self.assertIn(response.status_code, [200,404])
   

    def test_all_tiers_can_upload(self):
        self.client.login(username=self.user.username, password='tester123')
        response = TestViews.generate_image(self)
        self.assertEqual(response.status_code, 201)

    def test_cannot_view_expiringURL_as_basic(self):
        self.client.login(username=self.user.username, password='tester123')
        response = self.client.get(self.link_url) 
        self.assertEqual(response.status_code, 403)

    def test_cannot_view_expiringURL_as_premium(self):
        self.client.login(username=self.user.username, password='tester123')
        self.user.userprofile.tier = self.premium_tier
        response = self.client.get(self.link_url) 
        self.assertEqual(response.status_code, 403)
        
    def test_can_view_own_expiringURL_as_enterprise(self):
        self.client.login(username=self.user.username, password='tester123')
        self.user.userprofile.tier = self.enterprise_tier
        self.user.userprofile.save()
        image = ImageFactory(owner=self.user.userprofile)
        link_url = reverse('image-link', kwargs={'id': image.id})
        response = self.client.get(link_url) 
        self.assertEqual(response.status_code, 200)

    def test_all_tiers_has_200px_thumbnail(self):
        self.client.login(username=self.user.username, password='tester123')

        response = TestViews.generate_image(self)
        image = Image.objects.get(id=response.data['id'])
        thumbnail = image.thumbnails.filter(size__height=200).first()
        self.assertIsNotNone(thumbnail, "200px thumbnail does not exist")

    def test_basic_doesnt_have_400px_thumbnail(self):
        self.client.login(username=self.user.username, password='tester123')

        response = TestViews.generate_image(self)
        image = Image.objects.get(id=response.data['id'])
        thumbnail = image.thumbnails.filter(size__height=400).first()
        self.assertIsNone(thumbnail, "200px thumbnail does not exist")