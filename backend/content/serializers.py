# backend/content/serializers.py

from rest_framework import serializers
from .models import (
    News,
    Article,
    Page,
    NewsCategory,
    NewsTag,
    ArticleCategory,
    ArticleTag
)
from media_service.models import Gallery, Audio, Video
from media_service.serializers import GallerySerializer, AudioSerializer, VideoSerializer
from comments.serializers import CommentSerializer
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name', 'slug']

class NewsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = ['id', 'name', 'slug']

class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ['id', 'name', 'slug']

class ArticleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = ['id', 'name', 'slug']

class NewsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    categories = NewsCategorySerializer(many=True, read_only=True)
    tags = NewsTagSerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=NewsCategory.objects.all(), many=True, write_only=True, source='categories'
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=NewsTag.objects.all(), many=True, write_only=True, source='tags'
    )
    featured_image = serializers.ImageField(required=False, allow_null=True)

    # Прикрепленные медиа
    galleries = GallerySerializer(many=True, read_only=True)
    gallery_ids = serializers.PrimaryKeyRelatedField(
        queryset=Gallery.objects.all(), many=True, write_only=True, source='galleries'
    )
    audio_files = AudioSerializer(many=True, read_only=True)
    audio_file_ids = serializers.PrimaryKeyRelatedField(
        queryset=Audio.objects.all(), many=True, write_only=True, source='audio_files'
    )
    video_files = VideoSerializer(many=True, read_only=True)
    video_file_ids = serializers.PrimaryKeyRelatedField(
        queryset=Video.objects.all(), many=True, write_only=True, source='video_files'
    )

    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'content', 'author',
            'categories', 'tags', 'category_ids', 'tag_ids',
            'published_at', 'updated_at',
            'meta_title', 'meta_description', 'meta_keywords',
            'featured_image',
            # Прикрепленные медиа
            'galleries', 'gallery_ids',
            'audio_files', 'audio_file_ids',
            'video_files', 'video_file_ids',
        ]
        read_only_fields = ['slug', 'published_at', 'updated_at']

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    categories = ArticleCategorySerializer(many=True, read_only=True)
    tags = ArticleTagSerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=ArticleCategory.objects.all(), many=True, write_only=True, source='categories'
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=ArticleTag.objects.all(), many=True, write_only=True, source='tags'
    )
    featured_image = serializers.ImageField(required=False, allow_null=True)

    # Прикрепленные медиа
    galleries = GallerySerializer(many=True, read_only=True)
    gallery_ids = serializers.PrimaryKeyRelatedField(
        queryset=Gallery.objects.all(), many=True, write_only=True, source='galleries'
    )
    audio_files = AudioSerializer(many=True, read_only=True)
    audio_file_ids = serializers.PrimaryKeyRelatedField(
        queryset=Audio.objects.all(), many=True, write_only=True, source='audio_files'
    )
    video_files = VideoSerializer(many=True, read_only=True)
    video_file_ids = serializers.PrimaryKeyRelatedField(
        queryset=Video.objects.all(), many=True, write_only=True, source='video_files'
    )

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'content', 'author',
            'categories', 'tags', 'category_ids', 'tag_ids',
            'published_at', 'updated_at',
            'meta_title', 'meta_description', 'meta_keywords',
            'featured_image',
            # Прикрепленные медиа
            'galleries', 'gallery_ids',
            'audio_files', 'audio_file_ids',
            'video_files', 'video_file_ids',
        ]
        read_only_fields = ['slug', 'published_at', 'updated_at']

class PageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Page
        fields = [
            'id', 'title', 'slug', 'content',
            'author', 'created_at', 'updated_at', 'is_published',
            'meta_title', 'meta_description', 'meta_keywords',
        ]
        read_only_fields = ['created_at', 'updated_at']
