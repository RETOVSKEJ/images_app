from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', ImageGetAllCreate.as_view(), name='image-list-create'),
    path('<str:token>', ImageGetFromURL.as_view(), name='image-expiring'),
    path('<int:id>/link', ImageGetURL.as_view(), name='image-link'),
]