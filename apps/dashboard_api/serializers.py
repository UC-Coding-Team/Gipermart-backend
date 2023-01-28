from rest_framework import serializers
from apps.products.models import Category, Product
from apps.outside.models import Slider, Stock, Brand


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# class ColorSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Color
#         fields = ('id', 'name', 'code')
#
#
# class SizeSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Size
#         fields = ('id', 'name')
#
#
# class VariantSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Variants
#         fields = ('id', 'title', 'product', 'color', 'size', 'image', 'quantity', 'price')


class SliderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ('id', 'slug', 'images', 'created_at', 'updated_at')


class StockSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'slug', 'images', 'created_at', 'updated_at')


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'slug', 'images', 'category', 'product', 'created_at', 'updated_at')


