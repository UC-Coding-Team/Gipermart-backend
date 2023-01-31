from rest_framework import viewsets
from . import serializers
from apps.products.models import Category, Product
from rest_framework.permissions import IsAuthenticated
from apps.outside.models import Slider, Stock, Brand


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializers
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializers
    permission_classes = [IsAuthenticated]


class SliderViewSet(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = serializers.SliderSerializers
    permission_classes = [IsAuthenticated]


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = serializers.StockSerializers
    permission_classes = [IsAuthenticated]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = serializers.BrandSerializers
    permission_classes = [IsAuthenticated]

