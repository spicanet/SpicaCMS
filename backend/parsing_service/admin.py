# backend/parsing_service/admin.py

from django.contrib import admin
from .models import ParsingTemplate, ParsedItem

@admin.register(ParsingTemplate)
class ParsingTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'site_url', 'is_active', 'created_by', 'created_at')
    search_fields = ('name', 'site_url')
    list_filter = ('is_active', 'created_at', 'created_by')

@admin.register(ParsedItem)
class ParsedItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'template', 'created_at', 'status')
    search_fields = ('title', 'url')
    list_filter = ('status', 'created_at', 'template')
