from rest_framework import serializers
from .models import Order, OrderItem
from rest_framework.response import Response
from events.models import Events
from django.shortcuts import get_object_or_404

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['event', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields =  ['id', 'created_at', 'total_amount','items', 'order_number']

    def create(self, validated_data):
        items = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        order = super().create(validated_data)
        total_amount = 0
        order_items = []
        for item in items:
            event_id = item['event'].id
            quantity=item['quantity']
            event = Events.objects.get(id=event_id) 
            order_items.append(OrderItem(order=order, event_id=event_id, quantity=quantity))
            total_amount += event.ticket_price * quantity
        OrderItem.objects.bulk_create(order_items)
        order.total_amount = total_amount
        order.save()
        return order

