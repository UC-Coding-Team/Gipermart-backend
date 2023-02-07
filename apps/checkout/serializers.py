from rest_framework import serializers
from .models import Checkout
from apps.cart.serializers import CartItemSerializer, UserSerializer


class CheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checkout
        fields = ['full_name','phone_number','region','town','address','comment','cart', 'user', 'PAY_STATUS','NAXT_STATUS','created_at']

class CheckoutAllSerializer(serializers.ModelSerializer):

    cart = CartItemSerializer(many=False, read_only=True)

    class Meta:
        model = Checkout
        fields = ['full_name','phone_number','region','town','address','comment','cart','PAY_STATUS','NAXT_STATUS','created_at']