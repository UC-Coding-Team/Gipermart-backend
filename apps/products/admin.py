from django.contrib import admin

from . import models


admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.ProductAttribute)
admin.site.register(models.ProductAttributeValue)
admin.site.register(models.ProductAttributeValues)


# class ProductAttributeAdmin(admin.TabularInline):
#     model = models.ProductAttribute
#     raw_id_fields = ['product']
#
#
# class ProductAttributeValueAdmin(admin.TabularInline):
#     model = models.ProductAttributeValue
#     raw_id_fields = ['product']
#
#
# class ProductAttributeValuesAdmin(admin.TabularInline):
#     model = models.ProductAttributeValues
#     raw_id_fields = ['product']


@admin.register(models.ProductInventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "store_price")
    # inlines = [ProductAttributeAdmin, ProductAttributeValueAdmin, ProductAttributeValuesAdmin]

# admin.site.register(models.ProductInventory, InventoryAdmin)
