from rest_framework.generics import ListAPIView

from .serializers import (
    CategorySerializer,
    ProductInventorySerializer,
    ProductSerializer,
)
from apps.products.models import Category, Product, ProductInventory
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
        queryset = ProductInventory.objects.filter(product__id=pk)
        serializer = ProductInventorySerializer(queryset, many=True)
        return Response(serializer.data)


class AllProductsView(ListAPIView):
    """
    Return products
    """
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer


