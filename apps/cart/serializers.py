import json

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CartItem
from ..products.models import Product, ProductInventory, Media
from django.forms.models import model_to_dict

from ..products.serializers import ProductSerializer, ProductMediaSerializer, BrandSerializer, \
    ProductAttributeValueSerializer, calculate_rating, ProductInventorySerializer
from ..products.utils.units import Weight

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'created_at', 'is_staff', 'is_active']


class DashUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'created_at', 'is_staff', 'is_active']


class CartItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductInventorySerializer(many=True)

    class Meta:
        model = CartItem
        fields = ('id', 'user', 'product', 'quantity', 'total', 'created_at', 'updated_at')


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'user', 'product', 'quantity', 'total', 'created_at', 'updated_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        us = User.objects.get(id=data['user'])
        pr = ProductInventory.objects.get(id=data['product'])
        media = Media.objects.filter(product_inventory=data['product']).values_list('img_url', flat=True) or 'не найден'
        serialized_obj = model_to_dict(pr, exclude=['created_at', 'updated_at', 'weight'])
        serialized_obj2 = model_to_dict(us)
        data['media'] = media
        data['product'] = serialized_obj
        data['user'] = serialized_obj2
        return data
