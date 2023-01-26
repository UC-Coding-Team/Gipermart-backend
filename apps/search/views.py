from django_filters import filters
from rest_framework import generics
from apps.products.models import Product
from apps.products.serializers import ProductSerializer


class ProductsSearchView(generics.ListAPIView):
    queryset = Product
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__name',)

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.query("match", category__name=query)
        return queryset
