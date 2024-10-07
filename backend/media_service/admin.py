# backend/media_service/admin.py

from django.contrib import admin
from .models import Image, Audio, Video, Gallery

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'uploaded_by', 'uploaded_at')
    search_fields = ('title', 'uploaded_by__username')
    list_filter = ('uploaded_at', 'uploaded_by')

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'audio_file', 'uploaded_by', 'uploaded_at')
    search_fields = ('title', 'uploaded_by__username')
    list_filter = ('uploaded_at', 'uploaded_by')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_file', 'uploaded_by', 'uploaded_at')
    search_fields = ('title', 'uploaded_by__username')
    list_filter = ('uploaded_at', 'uploaded_by')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'created_by__username')
    list_filter = ('created_at', 'created_by')
