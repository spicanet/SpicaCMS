# backend/comments/views.py

from rest_framework import viewsets, permissions
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all()
        content_type = self.request.query_params.get('content_type', None)
        object_id = self.request.query_params.get('object_id', None)
        if content_type and object_id:
            try:
                model = ContentType.objects.get(model=content_type).model_class()
                queryset = queryset.filter(content_type__model=content_type, object_id=object_id, parent__isnull=True)
            except ContentType.DoesNotExist:
                queryset = Comment.objects.none()
        else:
            queryset = Comment.objects.none()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
