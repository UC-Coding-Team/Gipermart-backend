from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .document import ProductDocument

class ProductSerializer(DocumentSerializer):
    class Meta:
        document = ProductDocument
        fields = (
            'title',
            'description',
            'price',
            'amount',
            'variant',
            'slug',
            'status',
            'create_at',
            'update_at',
        )