from rest_framework import serializers
from apps.products.models import (
    Category, Product, Brand,
    ProductAttribute, ProductType,
    ProductAttributeValue, ProductInventory,
    Media, Stock, ProductAttributeValues, ProductTypeAttribute,
    Wishlist,
)
from apps.outside import models
from apps.products.utils.units import Weight
from .models import SiteSettings


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
        fields = ('id', 'url', 'images', 'created_at', 'updated_at')


class StockSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        fields = ('id', 'url', 'images', 'created_at', 'updated_at')


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ('id', 'url', 'images', 'category', 'product', 'created_at', 'updated_at')


class ProductInventorySerializers(serializers.ModelSerializer):
    product = ProductSerializers(many=False, read_only=True)
    media = MediaSerializers(many=True, read_only=True)
    brand = ProductBrandSerializers(read_only=True)
    attributes = ProductAttributeValueSerializers(
        source="attribute_values", many=True, read_only=True
    )
    weight = serializers.SerializerMethodField()

    def get_weight(self, obj):
        weight_obj = obj.weight
        if isinstance(weight_obj, Weight):
            return float(weight_obj.value)
        return 0.0  # or any default value you want

    class Meta:
        model = ProductInventory
        fields = '__all__'


class ProductAttributeValuesSerializers(serializers.ModelSerializer):
    attribute_values = ProductAttributeValueSerializers(source='attributevalues', many=False, read_only=True)
    product_inventory = ProductInventorySerializers(source='productinventory', many=False, read_only=True)

    class Meta:
        model = ProductAttributeValues
        fields = '__all__'


class SiteSettingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        exclude = ('phonenumbers',)


class PhoneSiteSettingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ('id', 'phonenumbers',)
