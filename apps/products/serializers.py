from rest_framework import serializers
from .models import Category, Product, Wishlist, ProductInventory, Media, Brand, ProductAttributeValue, Rating


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

    class Meta:
        model = ProductInventory
        fields = [
            "id",
            "sku",
            "price",
            'installment_plan',
            'product_type',
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
