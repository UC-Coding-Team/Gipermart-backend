import json

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CartItem
from ..products.models import Product, ProductInventory
from django.forms.models import model_to_dict


from ..products.serializers import ProductSerializer, ProductMediaSerializer, BrandSerializer, \
    ProductAttributeValueSerializer, calculate_rating
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

class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    media = ProductMediaSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    attributes = ProductAttributeValueSerializer(
        source="attribute_values", many=True, read_only=True
    )
    rating = serializers.SerializerMethodField()
    # category = StringRelatedField(source='product.category')
    weight = serializers.SerializerMethodField()

    def get_rating(self, obj):
        product_id = obj.id
        return calculate_rating(product_id)

    def get_weight(self, obj):
        weight_obj = obj.weight
        if isinstance(weight_obj, Weight):
            return float(weight_obj.value)
        return 0.0  # or any default value you want

    class Meta:
        model = ProductInventory
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = CartProductSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'user', 'product', 'quantity', 'total', 'created_at', 'updated_at')


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'user', 'product', 'quantity', 'total', 'created_at', 'updated_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        pr = ProductInventory.objects.get(pk=data['product'])
        us = User.objects.get(id=data['user'])
        # serialized_obj = model_to_dict(pr, exclude=['created_at', 'updated_at'])
        serialized_obj2 = model_to_dict(us)
        # data['product'] = serialized_obj
        data['user'] = serialized_obj2
        return data
