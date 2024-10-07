# backend/ai_service/admin.py

from django.contrib import admin
from .models import RewritePrompt, RewrittenItem, CommentGenerationConfig

@admin.register(RewritePrompt)
class RewritePromptAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'created_by')

@admin.register(RewrittenItem)
class RewrittenItemAdmin(admin.ModelAdmin):
    list_display = ('rewritten_title', 'parsed_item', 'created_at', 'status')
    search_fields = ('rewritten_title',)
    list_filter = ('status', 'created_at')

@admin.register(CommentGenerationConfig)
class CommentGenerationConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_comments', 'created_by', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'created_by')
