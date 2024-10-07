# backend/media_service/serializers.py

from rest_framework import serializers
from .models import Image, Audio, Video, Gallery

class ImageSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Image
        fields = ['id', 'title', 'image', 'uploaded_at', 'uploaded_by']

class AudioSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Audio
        fields = ['id', 'title', 'audio_file', 'uploaded_at', 'uploaded_by']

class VideoSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'video_file', 'uploaded_at', 'uploaded_by']

class GallerySerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    image_ids = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(), many=True, write_only=True, source='images'
    )

    class Meta:
        model = Gallery
        fields = ['id', 'title', 'images', 'image_ids', 'created_at', 'created_by']
