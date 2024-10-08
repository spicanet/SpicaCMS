# backend/media_service/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Image(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_images')

    def __str__(self):
        return self.title or self.image.name

class Audio(models.Model):
    title = models.CharField(max_length=255, blank=True)
    audio_file = models.FileField(upload_to='audio/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_audio')

    def __str__(self):
        return self.title or self.audio_file.name

class Video(models.Model):
    title = models.CharField(max_length=255, blank=True)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_videos')

    def __str__(self):
        return self.title or self.video_file.name

class Gallery(models.Model):
    title = models.CharField(max_length=255)
    images = models.ManyToManyField(Image, related_name='galleries')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_galleries')

    def __str__(self):
        return self.title
