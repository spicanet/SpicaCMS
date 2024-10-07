# backend/ai_service/views.py

from rest_framework import viewsets, permissions
from .models import RewritePrompt, RewrittenItem, CommentGenerationConfig
from .serializers import RewritePromptSerializer, RewrittenItemSerializer, CommentGenerationConfigSerializer

class RewritePromptViewSet(viewsets.ModelViewSet):
    queryset = RewritePrompt.objects.all()
    serializer_class = RewritePromptSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class RewrittenItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RewrittenItem.objects.all()
    serializer_class = RewrittenItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentGenerationConfigViewSet(viewsets.ModelViewSet):
    queryset = CommentGenerationConfig.objects.all()
    serializer_class = CommentGenerationConfigSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

