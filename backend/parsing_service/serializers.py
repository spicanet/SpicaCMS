# backend/parsing_service/serializers.py

from rest_framework import serializers
from .models import ParsingTemplate, ParsedItem

class ParsingTemplateSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ParsingTemplate
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')

class ParsedItemSerializer(serializers.ModelSerializer):
    template = ParsingTemplateSerializer(read_only=True)

    class Meta:
        model = ParsedItem
        fields = '__all__'
        read_only_fields = ('created_at',)
