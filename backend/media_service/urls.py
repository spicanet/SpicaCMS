# backend/media_service/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet, AudioViewSet, VideoViewSet, GalleryViewSet

router = DefaultRouter()
router.register(r'images', ImageViewSet, basename='images')
router.register(r'audio', AudioViewSet, basename='audio')
router.register(r'videos', VideoViewSet, basename='videos')
router.register(r'galleries', GalleryViewSet, basename='galleries')

urlpatterns = [
    path('', include(router.urls)),
]
