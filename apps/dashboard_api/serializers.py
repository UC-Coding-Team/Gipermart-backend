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


