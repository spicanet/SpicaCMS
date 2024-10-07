# backend/parsing_service/models.py

from django.db import models
from django.contrib.auth.models import User

class ParsingTemplate(models.Model):
    name = models.CharField(max_length=255)
    site_url = models.URLField()
    list_page_url = models.URLField()
    pagination_xpath = models.CharField(max_length=255, blank=True, null=True)
    article_links_xpath = models.CharField(max_length=255)
    title_xpath = models.CharField(max_length=255)
    content_xpath = models.CharField(max_length=255)
    author_xpath = models.CharField(max_length=255, blank=True, null=True)
    publish_date_xpath = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parsing_templates')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ParsedItem(models.Model):
    template = models.ForeignKey(ParsingTemplate, on_delete=models.CASCADE, related_name='parsed_items')
    url = models.URLField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255, blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ), default='pending')

    def __str__(self):
        return self.title
