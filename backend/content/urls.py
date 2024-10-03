# backend/content/urls.py

from django.urls import path
from .views import ArticleListCreateView, ArticleDetailView

urlpatterns = [
    path('articles/', ArticleListCreateView.as_view(), name='article_list_create'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
]
