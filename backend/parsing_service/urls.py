# backend/parsing_service/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParsingTemplateViewSet, ParsedItemViewSet

router = DefaultRouter()
router.register(r'parsing-templates', ParsingTemplateViewSet, basename='parsing-templates')
router.register(r'parsed-items', ParsedItemViewSet, basename='parsed-items')

urlpatterns = [
    path('', include(router.urls)),
]
