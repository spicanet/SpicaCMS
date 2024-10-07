# backend/parsing_service/views.py

from rest_framework import viewsets, permissions
from .models import ParsingTemplate, ParsedItem
from .serializers import ParsingTemplateSerializer, ParsedItemSerializer

class ParsingTemplateViewSet(viewsets.ModelViewSet):
    queryset = ParsingTemplate.objects.all()
    serializer_class = ParsingTemplateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ParsedItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParsedItem.objects.all()
    serializer_class = ParsedItemSerializer
    permission_classes = [permissions.IsAuthenticated]
