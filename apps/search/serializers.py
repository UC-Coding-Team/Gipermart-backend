from apps.products.models import Product
from rest_framework import serializers


class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price')