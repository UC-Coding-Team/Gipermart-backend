from rest_framework import serializers
from django.contrib.auth import password_validation

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Class responsible to serialize the order item data
    """
    class Meta:
        # The model related to this serializer
        model = OrderItem
        # Which fields are related to this serialization
        # Field names identical to the persisted fields in the model are persisted
        fields = (
            'order',
            'product',
            'quantity',
            'item_total'
        )


class OrderSerializer(serializers.ModelSerializer):
    """
    Class responsible to serialize the order data
    """
    # Let's consider a nested relationship.
    # The serializer will bring all the items for this order
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        # The model related to this serializer
        model = Order
        # Which fields are related to this serialization
        # Field names identical to the persisted fields in the model are persisted
        fields = (
            'id',
            'user',
            'items',
            'order_total',
        )