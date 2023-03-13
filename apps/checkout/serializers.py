from rest_framework import serializers
from .models import Checkout
from apps.cart.serializers import CartItemSerializer


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ['PAY_STATUS', 'order_id', 'amount', 'created_at']


class CheckoutAllSerializer(serializers.ModelSerializer):
    cart = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Checkout
        fields = ['PAY_STATUS', 'order_id', 'amount', 'created_at', 'generate_link']
