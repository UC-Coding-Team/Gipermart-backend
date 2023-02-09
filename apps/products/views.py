from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from django.db import models
from rest_framework.viewsets import GenericViewSet

from .filter import ProductFilter
from .serializers import (
    CategorySerializer,
    ProductInventorySerializer,
    ProductSerializer,
    RatingSerializer
)
from apps.products.models import Category, Product, ProductInventory, Rating
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


def calculate_rating(product_id):
    ratings = Rating.objects.filter(product=product_id)
    total_ratings = ratings.count()
    total_sum = ratings.aggregate(models.Sum('rating'))['rating__sum']
    return total_sum / total_ratings


class ProductDetailBySlug(APIView):
    """
    Return Sub Product by Slug
    """

    def get_object(self, pk):
        try:
            return ProductInventory.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        product.rating = calculate_rating(product.id)
        serializer = ProductInventorySerializer(product, many=True)
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
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated,)
