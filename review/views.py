from django.shortcuts import render
from rest_framework.response import Response
from .serializers import CommentSerializer, RatingSerializer, LikeSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Comment, Rating, Like
from rest_framework.permissions import *
from .permissions import IsAuthorPermission
from review.models import Like

class PermissionMixin:
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()

class CommentViewSet(ModelViewSet, PermissionMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RatingViewSet(ModelViewSet, PermissionMixin):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    
class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
