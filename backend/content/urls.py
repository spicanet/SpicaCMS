# backend/content/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NewsViewSet,
    ArticleViewSet,
    PageViewSet,
    NewsCategoryViewSet,
    NewsTagViewSet,
    ArticleCategoryViewSet,
    ArticleTagViewSet
)

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'articles', ArticleViewSet, basename='articles')
router.register(r'pages', PageViewSet, basename='pages')
router.register(r'news-categories', NewsCategoryViewSet, basename='news-categories')
router.register(r'news-tags', NewsTagViewSet, basename='news-tags')
router.register(r'article-categories', ArticleCategoryViewSet, basename='article-categories')
router.register(r'article-tags', ArticleTagViewSet, basename='article-tags')

urlpatterns = [
    path('', include(router.urls)),
]
