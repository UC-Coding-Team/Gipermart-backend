from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from .models import Category, Product, Wishlist, ProductInventory, Media, Brand, ProductAttributeValue, Rating, \
    ProductAttribute, ProductAllModel
from django.db import models


def calculate_rating(product_id):
    ratings = Rating.objects.filter(product=product_id)
    total_ratings = ratings.count()
    if total_ratings == 0:
        return 0
    total_sum = ratings.aggregate(models.Sum('rating'))['rating__sum']
    return int(total_sum) / int(total_ratings)


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id', 'user', 'product', 'date_added')


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        depth = 2
        fields = '__all__'
        read_only = True


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = '__all__'


class ProductAttributeValueSerializerFiler(serializers.ModelSerializer):
    product_attribute = ProductAttributeSerializer()

    class Meta:
        model = ProductAttributeValue
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]
        read_only = True


class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.StringRelatedField(source='parent.name')
    parent_id = serializers.StringRelatedField(source='parent.id')

    class Meta:
        model = Category
        fields = ['id', "name", "slug", "description", "background_image", "is_active", 'parent_name', 'parent_id']
        read_only = True


class ProductMediaSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ["img_url", "alt_text"]
        read_only = True
        editable = False

    def get_img_url(self, obj):
        # try:
        #     return self.context['request'].build_absolute_uri(obj.img_url.url)
        # except:
        return obj.img_url.url
        # pass


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = (
        #     'id', 'name', 'slug', 'description', 'category', 'is_active', 'is_recommended', 'USA_product', 'created_at')
        # exclude = ["id"]
        fields = '__all__'
        read_only = True
        # editable = False


class ProductInventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    media = ProductMediaSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    attributes = ProductAttributeValueSerializer(
        source="attribute_values", many=True, read_only=True
    )
    rating = serializers.SerializerMethodField()
    # category = StringRelatedField(source='product.category')

    def get_rating(self, obj):
        product_id = obj.id
        return calculate_rating(product_id)

    class Meta:
        model = ProductInventory

        fields = '__all__'


class ProductInventorySearchSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    # media = ProductMediaSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)

    attributes = ProductAttributeValueSerializer(
        source="attribute_values", many=True, read_only=True
    )

    class Meta:
        model = ProductInventory
        # fields = '__all__'
        fields = [
            "id",
            "sku",
            "price",
            "is_default",
            "product",
            "brand",
            'attributes',
        ]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class PrFilter(serializers.ModelSerializer):
    atributes_value = ProductAttributeValueSerializerFiler(many=True)

    class Meta:
        model = ProductAllModel
        fields = '__all__'
