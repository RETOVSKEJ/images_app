from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('all', ImageGetAll.as_view()),
    path('add', ImagePost.as_view()),
    path('<str:token>', ImageGetFromURL.as_view()),
    path('<int:id>/link', ImageGetURL.as_view()),
]