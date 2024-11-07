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
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = News.objects.all().order_by('-published_at')
        slug = self.request.query_params.get('slug', None)
        tag = self.request.query_params.get('tag', None)
        category = self.request.query_params.get('category', None)
        author = self.request.query_params.get('author', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        limit = self.request.query_params.get('limit', None)

        if slug:
            queryset = queryset.filter(slug=slug)
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        if category:
            queryset = queryset.filter(categories__slug=category)
        if author:
            queryset = queryset.filter(author__username=author)
        if start_date and end_date:
            queryset = queryset.filter(published_at__date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(published_at__date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(published_at__date__lte=end_date)
        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                pass  # Игнорировать некорректное значение limit

        return queryset

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
