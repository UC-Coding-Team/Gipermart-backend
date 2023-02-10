import django_filters

from .models import ProductInventory


class ProductInventoryFilter(django_filters.FilterSet):
    sku = django_filters.CharFilter(lookup_expr='icontains')
    upc = django_filters.CharFilter(lookup_expr='icontains')
    product_type = django_filters.NumberFilter()
    brand = django_filters.NumberFilter()

    class Meta:
        model = ProductInventory
        fields = ['sku', 'upc', 'product_type', 'brand']