from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Cart, CartItem
from ..products.models import Product

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'created_at', 'is_staff', 'is_active']


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'created_at', 'updated_at', 'total', 'active')


class CartItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = CartProductSerializer(many=True)

    class Meta:
        model = CartItem
        fields = ('id', 'user', 'product', 'quantity', 'created_at', 'updated_at')


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'user', 'product', 'quantity', 'created_at', 'updated_at')
