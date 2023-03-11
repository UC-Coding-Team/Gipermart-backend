from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from rest_framework import serializers
from .models import Slider, Stock, Brand, Add_to_wishlist
from ..cart.serializers import UserSerializer
from ..products.models import NewProductModel
from ..products.serializers import NewProductSerializer

User = get_user_model()


class Slider_serializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id', 'images', 'created_at', 'updated_at']


class Stock_serializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'images', 'created_at', 'updated_at']


class Brand_serializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "url", "images", "category", "product", "created_at", "updated_at"]


class WishlistItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = NewProductSerializer(read_only=True)

    class Meta:
        model = Add_to_wishlist
        fields = ('id', 'user', 'product', 'created_at', 'updated_at')


class WishlistCreateSerializer(serializers.ModelSerializer):
    weight = serializers.SerializerMethodField()

    class Meta:
        model = Add_to_wishlist
        fields = ('id', 'user', 'product', 'created_at', 'updated_at', 'weight')

    def get_weight(self, instance):
        if instance.product.weight:
            return str(instance.product.weight)
        else:
            return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['weight'] = self.get_weight(instance)
        return data