from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import  CartItem
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




class CartItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = CartProductSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'user', 'product', 'quantity','total', 'created_at', 'updated_at')


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'user', 'product', 'quantity','total', 'created_at', 'updated_at')
