# backend/ai_service/serializers.py

from rest_framework import serializers
from .models import RewritePrompt, RewrittenItem, CommentGenerationConfig


class RewritePromptSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RewritePrompt
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')

class RewrittenItemSerializer(serializers.ModelSerializer):
    parsed_item = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RewrittenItem
        fields = '__all__'
        read_only_fields = ('created_at',)

class CommentGenerationConfigSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CommentGenerationConfig
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')