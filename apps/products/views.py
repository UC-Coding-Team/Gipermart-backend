from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .filter import ProductFilter
from .filters import ProductInventoryFilter
from .serializers import (
    CategorySerializer,
    ProductInventorySerializer,
    ProductSerializer,
    RatingSerializer, ProductAttributeValueSerializerFiler, PrFilter
)
from apps.products.models import Category, Product, ProductInventory, Rating, ProductAttributeValue, ProductAllModel
from rest_framework.response import Response
from rest_framework.views import APIView


class CategoryList(APIView):
    """
    Return list of all categories
    """

    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class ProductByCategory(APIView):
    """
    Return product by category
    """

    def get(self, request, slug=None):
        queryset = Product.objects.filter(category__slug=slug)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetailBySlug(APIView):
    """
    Return Sub Product by Slug
    """

    def get(self, request, pk=None):
        product = ProductInventory.objects.get(pk=pk)
        serializer = ProductInventorySerializer(product)
        return Response(serializer.data)


class AllProductsView(mixins.ListModelMixin, GenericViewSet):
    """
    Return products
    """
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ProductFilter


class RatingCreate(generics.CreateAPIView):
    """
    Create Rating
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated,)


class ProductInventoryView(mixins.ListModelMixin, GenericViewSet):
    queryset = ProductAllModel.objects.all()
    serializer_class = PrFilter


class ProductInventoryAPIView(APIView):

    def get(self, request, pk):
        houses = ProductAllModel.objects.get(category__id=pk)
        serializer = PrFilter(houses, context={'request': request}, )
        return Response(serializer.data)

class ProductFilterView(generics.ListCreateAPIView):
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductInventoryFilter

# class ProductFilterView(mixins.ListModelMixin, GenericViewSet):
#     queryset = ProductInventory.objects.all()
#     serializer_class = ProductInventorySerializer
#     filter_backends = [DjangoFilterBackend]
#     filter_class = ProductFilter