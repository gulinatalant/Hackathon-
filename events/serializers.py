from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Events, Category, Favourite

class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class EventsSerializer(ModelSerializer):

    class Meta:
        model = Events
        fields = '__all__'

    def validate_price(self, price):
            if price <= 0:
                raise ValidationError('Price must be > 0')
            return price


class EventsListSerializer(ModelSerializer):

    class Meta:
        model = Events
        fields = ('id', 'title', 'date', 'ticket_price', 'image', 'location')


class FavouriteProductSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Favourite
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        favourite = self.Meta.model.objects.create(user=user, **validated_data)
        return favourite
    
    def validate(self, attrs):
        event = attrs.get('event')
        user = self.context.get('request').user
        if self.Meta.model.objects.filter(event=event, user=user).exists():
            raise serializers.ValidationError('В избранном')
        return attrs
