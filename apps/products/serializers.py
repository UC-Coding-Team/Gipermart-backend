from rest_framework import serializers
from .models import Category, Product
from ..user_profil.models import User
from drf_extra_fields.fields import Base64ImageField


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.title

    class Meta:
        model = Product
        fields = '__all__'


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # read_only_fields = ('id', 'seller', 'category', 'title', 'price', 'image', 'description', 'quantity', 'views',)


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_category(self, obj):
        return obj.category.title

    class Meta:
        model = Product
        fields = '__all__'
