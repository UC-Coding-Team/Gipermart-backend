from rest_framework import serializers
from apps.products.models import Category, Product, Color, Size, Variants


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'parent', 'title', 'description', 'image', 'status', 'slug', 'create_at', 'update_at')


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'category', 'title', 'installment_plan', 'description', 'image', 'price', 'amount', 'variant', 'detail', 'slug', 'status', 'create_at', 'update_at')


class ColorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name', 'code')


class SizeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('id', 'name')


class VariantSerializers(serializers.ModelSerializer):
    class Meta:
        model = Variants
        fields = ('id', 'title', 'product', 'color', 'size', 'image', 'quantity', 'price')
