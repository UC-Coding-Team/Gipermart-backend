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
from ..checkout.models import Checkout
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _

User = get_user_model()


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


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ('id', 'created_at')


class SellingStatusSerializer(serializers.Serializer):
    checkout_count = serializers.IntegerField()
    total_sum = serializers.IntegerField()
    checkout_list = CheckoutSerializer(many=True)


class ProductTypeAttributeSerializers(serializers.ModelSerializer):
    product_attributes = ProductAttributeSerializers(source='product_attribute', many=False, read_only=True)
    product_types = ProductTypeSerializers(source='product_type', many=False, read_only=True)

    class Meta:
        model = ProductTypeAttribute
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=40)
    password = serializers.CharField(max_length=128, write_only=True)
    tokens = serializers.DictField(read_only=True)

    class Meta:
        ref_name = "user_profile_login"

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'),
                            phone_number=phone_number, password=password)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        if not user.is_staff or not user.is_superuser:
            raise serializers.ValidationError(_('You must be an admin or superuser to login.'))
        update_last_login(None, user)
        refresh = user.tokens()
        attrs['tokens'] = refresh
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')

        if not user.check_password(old_password):
            msg = _('Your old password was entered incorrectly. Please enter it again.')
            raise serializers.ValidationError(msg, code='authorization')

        validate_password(new_password, user)
        attrs['user'] = user
        attrs['new_password'] = new_password
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()


class ForgetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=40)
    mycode = serializers.IntegerField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        mycode = attrs.get('mycode')

        user = User.objects.get(phone_number=phone_number)

        if not user:
            msg = _('User with provided phone number does not exist.')
            raise serializers.ValidationError(msg, code='authorization')

        if user.mycode != mycode:
            msg = _('Invalid verification code.')
            raise serializers.ValidationError(msg, code='authorization')

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
