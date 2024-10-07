# backend/ai_service/models.py

from django.db import models
from django.contrib.auth.models import User
from parsing_service.models import ParsedItem

class RewritePrompt(models.Model):
    name = models.CharField(max_length=255)
    prompt_text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewrite_prompts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class RewrittenItem(models.Model):
    parsed_item = models.OneToOneField(ParsedItem, on_delete=models.CASCADE, related_name='rewritten_item')
    rewritten_title = models.CharField(max_length=255)
    rewritten_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ), default='pending')

    def __str__(self):
        return self.rewritten_title

class CommentGenerationConfig(models.Model):
    name = models.CharField(max_length=255)
    prompt_template = models.TextField(help_text="Шаблон промпта для генерации комментария. Используйте {content} для вставки содержания материала.")
    number_of_comments = models.PositiveIntegerField(default=5)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_generation_configs')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
