from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from .filter import ProductFilter
from .filters import ProductInventoryFilter
from .serializers import (
    CategorySerializer,
    RatingSerializer, NewProductSerializer
)
from apps.products.models import Category, Rating, NewProductModel
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
        queryset = NewProductModel.objects.filter(category__slug=slug)
        serializer = NewProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetailBySlug(APIView):
    """
    Return Sub Product by Slug
    """

    def get(self, request, pk=None):
        product = NewProductModel.objects.get(pk=pk)
        serializer = NewProductSerializer(product)
        return Response(serializer.data)


class AllProductsView(mixins.ListModelMixin, GenericViewSet):
    """
    Return products
    """
    queryset = NewProductModel.objects.all()
    serializer_class = NewProductSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ProductFilter


class RatingCreate(generics.CreateAPIView):
    """
    Create Rating
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated,)


class ProductFilterView(generics.ListCreateAPIView):
    queryset = NewProductModel.objects.all()
    serializer_class = NewProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductInventoryFilter
    search_fields = ('category__slug',)
    ordering_fields = ('price',)
    ordering = ('price',)
# class ProductFilterView(mixins.ListModelMixin, GenericViewSet):
#     queryset = ProductInventory.objects.all()
#     serializer_class = ProductInventorySerializer
#     filter_backends = [DjangoFilterBackend]
#     filter_class = ProductFilter