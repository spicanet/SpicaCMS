# backend/ai_service/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RewritePromptViewSet, RewrittenItemViewSet, CommentGenerationConfigViewSet

router = DefaultRouter()
router.register(r'rewrite-prompts', RewritePromptViewSet, basename='rewrite-prompts')
router.register(r'rewritten-items', RewrittenItemViewSet, basename='rewritten-items')
router.register(r'comment-generation-configs', CommentGenerationConfigViewSet, basename='comment-generation-configs')

urlpatterns = [
    path('', include(router.urls)),
]
