# backend/content/views.py

from rest_framework import viewsets, permissions
from .models import (
    News,
    Article,
    Page,
    NewsCategory,
    NewsTag,
    ArticleCategory,
    ArticleTag
)
from .serializers import (
    NewsSerializer,
    ArticleSerializer,
    PageSerializer,
    NewsCategorySerializer,
    NewsTagSerializer,
    ArticleCategorySerializer,
    ArticleTagSerializer
)

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-published_at')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NewsSerializer
        return NewsSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-published_at')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleSerializer
        return ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all().order_by('-created_at')
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class NewsCategoryViewSet(viewsets.ModelViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class NewsTagViewSet(viewsets.ModelViewSet):
    queryset = NewsTag.objects.all()
    serializer_class = NewsTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ArticleCategoryViewSet(viewsets.ModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ArticleTagViewSet(viewsets.ModelViewSet):
    queryset = ArticleTag.objects.all()
    serializer_class = ArticleTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
