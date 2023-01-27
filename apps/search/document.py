from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from apps.products.models import Product, Category


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Product

    fields = [
        'title',
        'description',
        'price',
        'amount',
        'variant',
        'slug',
        'status',
        'create_at',
        'update_at',
    ]