from rest_framework import viewsets
from . import serializers
from apps.products.models import (
    Category, Product, Brand,
    ProductAttribute, ProductType,
    ProductAttributeValue, ProductInventory,
    Media, Stock, ProductAttributeValues, ProductTypeAttribute,
    Wishlist,
)
from rest_framework.permissions import IsAuthenticated
from apps.outside import models


class ProductStockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = serializers.StockProductSerializers
    permission_classes = [IsAuthenticated]


class ProductAttributeValuesViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValues.objects.all()
    serializer_class = serializers.ProductAttributeValuesSerializers
    permission_classes = [IsAuthenticated]


class ProductTypeAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductTypeAttribute.objects.all()
    serializer_class = serializers.ProductTypeAttributeSerializers
    permission_classes = [IsAuthenticated]


class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = serializers.ProductAttributeValueSerializers
    permission_classes = [IsAuthenticated]


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = serializers.WishlistSerializers
    permission_classes = [IsAuthenticated]


class ProductInventoryViewSet(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    serializer_class = serializers.ProductInventorySerializers
    permission_classes = [IsAuthenticated]


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = serializers.MediaSerializers
    permission_classes = [IsAuthenticated]


class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = serializers.ProductAttributeSerializers
    permission_classes = [IsAuthenticated]


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializers
    permission_classes = [IsAuthenticated]


class BrandProductViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = serializers.ProductBrandSerializers
    permission_classes = [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializers
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializers
    permission_classes = [IsAuthenticated]


class SliderViewSet(viewsets.ModelViewSet):
    queryset = models.Slider.objects.all()
    serializer_class = serializers.SliderSerializers
    permission_classes = [IsAuthenticated]


class StockViewSet(viewsets.ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializers
    permission_classes = [IsAuthenticated]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializers
    permission_classes = [IsAuthenticated]
