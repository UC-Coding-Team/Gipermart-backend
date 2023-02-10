import django_filters

from .models import ProductInventory


class ProductInventoryFilter(django_filters.FilterSet):
    sku = django_filters.CharFilter(lookup_expr='icontains')
    upc = django_filters.CharFilter(lookup_expr='icontains')
    product_type = django_filters.NumberFilter(name='product_type__id')
    product = django_filters.NumberFilter(name='product__id')
    brand = django_filters.NumberFilter(name='brand__id')
    is_active = django_filters.BooleanFilter()
    is_default = django_filters.BooleanFilter()
    is_on_sale = django_filters.BooleanFilter()
    class Meta:
        model = ProductInventory
        fields = ['sku', 'upc', 'product_type', 'product', 'brand', 'is_active', 'is_default', 'is_on_sale']