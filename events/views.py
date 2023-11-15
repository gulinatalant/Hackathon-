from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

class PermissionMixin:
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class CategoryView(PermissionMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class EventsView(PermissionMixin, ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title', 'ticket_price', 'category']
    search_fields = ['title', 'date', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return EventsListSerializer
        return self.serializer_class
    

class FavouriteView(ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteProductSerializer

    # @action(['POST'], detail=True)
    # def favourite(self, request, pk=None):
    #     event= self.get_object()
        # user = request.user
    #     try:
    #         favourite = Favourite.objects.get(event=event, user=user)
    #         favourite.favourite = not favourite.favourite
    #         if favourite.favourite:
    #             favourite.save()
    #         else:
    #             favourite.delete()
    #         message = 'в избранном' if favourite.favourite else 'не в избранном'
    #     except Favourite.DoesNotExist:
    #         Favourite.objects.create(event=event, user=user, favourite=True)
    #         message = 'в избранном'
    #     return Response(message, status=200)


class FavouritesListView(ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteProductSerializer
    permission_classes = [IsAuthenticated]


    