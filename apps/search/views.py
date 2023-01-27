from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from .document import ProductDocument
from apps.search.serializers import ProductSerializer

class ProductViewSet(BaseDocumentViewSet):
    document = ProductDocument
    serializer_class = ProductSerializer