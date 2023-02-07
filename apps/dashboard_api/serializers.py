from rest_framework import serializers
from apps.products.models import (
    Category, Product, Brand,
    ProductAttribute, ProductType,
    ProductAttributeValue, ProductInventory,
    Media, Stock, ProductAttributeValues, ProductTypeAttribute,
    Wishlist,
)
from apps.outside import models


class ProductTypeSerializers(serializers.ModelSerializer):
    class Meta:
        models = ProductType
        fields = '__all__'


class ProductTypeAttributeSerializers(serializers.ModelSerializer):
    class Meta:
        models = ProductTypeAttribute
        fields = '__all__'


class WishlistSerializers(serializers.ModelSerializer):
    class Meta:
        models = Wishlist
        fields = '__all__'


class ProductAttributeValueSerializers(serializers.ModelSerializer):
    class Meta:
        models = ProductAttributeValue
        fields = '__all__'


class ProductInventorySerializers(serializers.ModelSerializer):
    class Meta:
        models = ProductInventory
        fields = '__all__'


class MediaSerializers(serializers.ModelSerializer):
    class Meta:
        models = Media
        fields = '__all__'


class ProductAttributeSerializers(serializers.ModelSerializer):
    class Meta:
        models = ProductAttribute
        fields = '__all__'


class StockProductSerializers(serializers.ModelSerializer):
    class Meta:
        models = Stock
        fields = '__all__'


class ProductAttributeValuesSerializers(serializers.ModelSerializer):
    class Meta:
        models = ProductAttributeValues
        fields = '__all__'


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
        model = models.Slider
        fields = ('id', 'slug', 'images', 'created_at', 'updated_at')


class StockSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        fields = ('id', 'slug', 'images', 'created_at', 'updated_at')


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'slug', 'images', 'category', 'product', 'created_at', 'updated_at')
