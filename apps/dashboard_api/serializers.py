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
from django.contrib.auth import authenticate


class ProductBrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductAttributeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = '__all__'


class ProductTypeSerializers(serializers.ModelSerializer):
    product_type_attribute = ProductAttributeSerializers(source='product_type_attributes', many=True, read_only=True)

    class Meta:
        model = ProductType
        fields = '__all__'


class WishlistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
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
    products = ProductSerializers(source='product', many=False, read_only=True)
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
        exclude = ('phonenumbers', 'site_type')


class PhoneSiteSettingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ('id', 'phonenumbers', 'site_type')


class ProductTypeAttributeSerializers(serializers.ModelSerializer):
    product_attributes = ProductAttributeSerializers(source='product_attribute', many=False, read_only=True)
    product_types = ProductTypeSerializers(source='product_type', many=False, read_only=True)

    class Meta:
        model = ProductTypeAttribute
        fields = '__all__'


from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            user = authenticate(username=phone_number, password=password)
            if user:
                if user.is_superuser:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("User is not a superuser or admin.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must provide phone_number and password.")

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("The old password is incorrect")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("The new password and confirmation do not match")
        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
