from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from apps.products.models import ProductInventory

@registry.register_document
class ProductInventoryDocument(Document):
    product = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
            "slug": fields.TextField(),
            "description": fields.TextField(),
        #     "category": fields.ObjectField(
        # properties={
        #     "id": fields.IntegerField(),
        #     "name": fields.TextField(),
        #     "slug": fields.TextField(),
        #     "description": fields.TextField(),
        #     "background_image": fields.FileField(),
        # }
# )
}
)
    brand = fields.ObjectField(properties={"name": fields.TextField()})
    product_type = fields.ObjectField(properties={"name": fields.TextField(),"slug": fields.TextField(),"description": fields.TextField()})
    attribute_values = fields.ObjectField(
    properties={
        "name": fields.TextField(),
        "value": fields.TextField(),
        "slug": fields.TextField(),
        "description": fields.TextField(),
        "background_image": fields.FileField(),
}
)

    class Index:
        name = "productinventory"

    class Django:
        model = ProductInventory

        fields = [
            "id",
            "sku",
            "upc",
            "price",
            "is_default",
            "is_active",
            "is_on_sale",
            "sale_price",
            "weight",
            "created_at",
            "updated_at",
        ]