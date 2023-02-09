import django_filters

from apps.products.models import ProductInventory


class ProductFilter(django_filters.FilterSet):
    name__not = django_filters.CharFilter(field_name='attribute_values', exclude=True)
    name__not__in = django_filters.CharFilter(field_name='attribute_values', method='filter_name_not_in')

    class Meta:
        model = ProductInventory
        fields = ['attribute_values']

    @staticmethod
    def filter_name_not_in(queryset, _, value):
        return queryset.exclude(attribute_values__in=value.split(','))
