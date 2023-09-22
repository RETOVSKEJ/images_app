import os
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.response import Response
from rest_framework import permissions, serializers, generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .permissions import IsBasic, IsPremium, IsEnterprise, IsCustom, CanFetchExpiringLink
from .serializers import ImageSerializer
from .models import Image, UserProfile, Thumbnail
from .utils import generate_thumbnail, generate_expiring_url, get_expiring_url


# Create your views here.


class ServeProtectedMedia(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, file_path, format=None):
        media_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
         
        if file_path.startswith('thumbnails/'):
            thumbnail = Thumbnail.objects.filter(file=file_path).first()
            if not thumbnail or thumbnail.image.owner != request.user.userprofile:
                raise Http404
            
        else:
            image = Image.objects.filter(file=file_path, owner=request.user.userprofile).first()
            if not image:
                raise Http404
        
        if os.path.exists(media_file_path):
            f = open(media_file_path, 'rb')
            return FileResponse(f)
        else:
            raise Http404


class ImageGetFromURL(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, token, *args, **kwargs):
        try:
            image_id = get_expiring_url(token)
        except ValueError:
            return Response({"error": "Invalid or expired token"}, 400)
        
        image = Image.objects.get(pk=image_id)
        # if image.owner.user != request.user:
        #     raise PermissionDenied("You are not the owner of an image")
        return FileResponse(open(image.file.path, 'rb'))


class ImageGetURL(APIView):
    permission_classes = (IsAuthenticated, CanFetchExpiringLink)
    
    def get(self, request, id, *args, **kwargs):
        if not request.user.userprofile.images.filter(pk=id).exists():
            raise PermissionDenied("You are not the owner of an image")
        
        duration = int(request.query_params.get('duration', 3000))
        if duration < 300 or duration > 30000:
            return Response({"error":"Duration has to be between 300 or 30000 seconds"}, 400)
        
        token = generate_expiring_url(id, duration)
        return Response({"token": token}, 200)

        

class ImageGetAllCreate(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Image.objects.all()

    def get_queryset(self):
        profile = UserProfile.objects.get(user=self.request.user)
        return Image.objects.filter(owner=profile).all()

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user.userprofile)
        user_tier = instance.owner.tier

        # TODO async/celery
        for size in user_tier.thumbnail_sizes.all():
            thumbnail = generate_thumbnail(instance, size.height)
            Thumbnail.objects.create(file=thumbnail, size=size, image=instance)




    