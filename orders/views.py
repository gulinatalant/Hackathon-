from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor


class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthor]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_context(self):
        return{
            'request': self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    

