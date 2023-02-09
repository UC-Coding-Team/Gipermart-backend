from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .serializers import (
    CategorySerializer,
    ProductInventorySerializer,
    ProductSerializer,
    RatingSerializer
)
from .models import Category, Product, ProductInventory, Rating
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
        product = ProductInventory.objects.filter(pk=pk)
        serializer = ProductInventorySerializer(product, many=True)
        return Response(serializer.data)


class AllProductsView(ListAPIView):
    """
    Return products
    """
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer


class RatingCreate(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated,)
