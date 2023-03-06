import django_filters
from django_filters import rest_framework as filters
from .models import NewProductModel, ProductAttributeValue




class ProductInventoryFilter(django_filters.FilterSet):
    # sku = django_filters.CharFilter(lookup_expr='icontains')
    # upc = django_filters.CharFilter(lookup_expr='icontains')
    # product_type = django_filters.NumberFilter()
    # attributes = django_filters.NumberFilter()
    #
    # class Meta:
    #     model = ProductInventory
    #     fields = ['sku', 'upc', 'product_type', 'attributes']
    # brand = filters.NumberFilter(field_name='brand__id', lookup_expr='exact')
    attribute_values = filters.ModelMultipleChoiceFilter(
        queryset=ProductAttributeValue.objects.all(),
        field_name='attribute_values',
        to_field_name='id',
    )
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = NewProductModel
        fields = ['attribute_values', 'price']
