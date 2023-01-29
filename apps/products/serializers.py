from rest_framework import serializers
from .models import Category, Product, Wishlist, ProductInventory, Media, Brand, ProductAttributeValue


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id', 'user', 'product', 'date_added')


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        depth = 2
        exclude = ["id"]
        read_only = True


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]
        read_only = True


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug", "description", "background_image", "is_active"]
        read_only = True


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ["id"]
        # read_only = True
        # editable = False


class ProductMediaSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ["img_url", "alt_text"]
        read_only = True
        editable = False

    def get_img_url(self, obj):
        return obj.img_url.url


class ProductInventorySerializer(serializers.ModelSerializer):

    product = ProductSerializer(many=False, read_only=True)
    media = ProductMediaSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    attributes = ProductAttributeValueSerializer(
        source="attribute_values", many=True, read_only=True
    )

    class Meta:
        model = ProductInventory
        fields = [
            "id",
            "sku",
            "price",
            "is_default",
            "brand",
            "product",
            "is_on_sale",
            "weight",
            "media",
            "attributes",
            "product_type",
        ]
        read_only = True


class ProductInventorySearchSerializer(serializers.ModelSerializer):

    product = ProductSerializer(many=False, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)

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
        ]
