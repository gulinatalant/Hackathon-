from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('category', CategoryView)
router.register('events', EventsView)
router.register('favourite', FavouriteView)

urlpatterns = [
    path('', include(router.urls)),
]