from rest_framework import serializers
from apps.products.models import (
    Category, Product, Brand,
    ProductAttribute, ProductType,
    ProductAttributeValue, ProductInventory,
    Media, Stock, ProductAttributeValues, ProductTypeAttribute,
    Wishlist,
)
from apps.outside import models


class ProductBrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'


class ProductTypeAttributeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductTypeAttribute
        fields = '__all__'


class WishlistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


class ProductAttributeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = '__all__'


class ProductAttributeValueSerializers(serializers.ModelSerializer):
    product_attributes = ProductAttributeSerializers(source='product_attribute', many=False, read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = ('id', 'attribute_value', 'product_attributes')


class MediaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class StockProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class ProductAttributeValuesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValues
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
        model = models.Brand
        fields = ('id', 'slug', 'images', 'category', 'product', 'created_at', 'updated_at')


class ProductInventorySerializers(serializers.ModelSerializer):
    product = ProductSerializers(many=False, read_only=True)
    media = MediaSerializers(many=True, read_only=True)
    brand = ProductBrandSerializers(read_only=True)
    attributes = ProductAttributeValueSerializers(
        source="attribute_values", many=True, read_only=True
    )

    class Meta:
        model = ProductInventory
        fields = '__all__'
