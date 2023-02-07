from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from rest_framework import serializers
from .models import Slider, Stock, Brand, Add_to_wishlist
from ..cart.serializers import UserSerializer, CartProductSerializer
from ..products.models import Product

User = get_user_model()

class Slider_serializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id', 'images', 'created_at', 'updated_at']


class Stock_serializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'slug', 'images', 'created_at', 'updated_at']


class Brand_serializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "slug", "images", "category", "product", "created_at", "updated_at"]


class WishlistItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = CartProductSerializer()

    class Meta:
        model = Add_to_wishlist
        fields = ('id', 'user', 'product', 'created_at', 'updated_at')


class WishlistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add_to_wishlist
        fields = ('id', 'user', 'product', 'created_at', 'updated_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        pr = Product.objects.get(id=data['product'])
        us = User.objects.get(id=data['user'])
        serialized_obj = model_to_dict(pr)
        serialized_obj2 = model_to_dict(us)
        data['product'] = serialized_obj
        data['user'] = serialized_obj2
        return data
