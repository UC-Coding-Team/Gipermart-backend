from rest_framework import viewsets
from .serializers import CategorySerializers, ProductSerializers, ColorSerializers, SizeSerializers, VariantSerializers
from apps.products.models import Category, Product, Color, Size, Variants
from rest_framework.permissions import IsAuthenticated


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [IsAuthenticated]


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializers
    permission_classes = [IsAuthenticated]


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = ColorSerializers
    permission_classes = [IsAuthenticated]


class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variants.objects.all()
    serializer_class = VariantSerializers
    permission_classes = [IsAuthenticated]