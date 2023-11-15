from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register('comment', CommentViewSet)
router.register('rating', RatingViewSet)
router.register('likes', LikeViewSet)

urlpatterns = [
    path('', include(router.urls))
]