from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from . import serializers
from apps.products.models import (
    Category, Product, Brand,
    ProductAttribute, ProductType,
    ProductAttributeValue, ProductInventory,
    Media, Stock, ProductAttributeValues, ProductTypeAttribute,
    Wishlist,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.outside import models
from ..cart.serializers import UserSerializer, DashUserSerializer
from ..checkout.models import Checkout
from ..checkout.serializers import CheckoutSerializer, CheckoutAllSerializer


class ProductStockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = serializers.StockProductSerializers
    permission_classes = [AllowAny]


class ProductAttributeValuesViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValues.objects.all()
    serializer_class = serializers.ProductAttributeValuesSerializers
    permission_classes = [AllowAny]


class ProductTypeAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductTypeAttribute.objects.all()
    serializer_class = serializers.ProductTypeAttributeSerializers
    permission_classes = [AllowAny]


class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = serializers.ProductAttributeValueSerializers
    permission_classes = [AllowAny]


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = serializers.WishlistSerializers
    permission_classes = [AllowAny]


class ProductInventoryViewSet(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    serializer_class = serializers.ProductInventorySerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['sku', ]


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = serializers.MediaSerializers
    permission_classes = [AllowAny]


class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = serializers.ProductAttributeSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class BrandProductViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = serializers.ProductBrandSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class SliderViewSet(viewsets.ModelViewSet):
    queryset = models.Slider.objects.all()
    serializer_class = serializers.SliderSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class StockViewSet(viewsets.ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class BrandViewSet(viewsets.ModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializers
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = DashUserSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']


class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'slug']
