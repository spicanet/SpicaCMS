# backend/comments/admin.py

from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at',)
