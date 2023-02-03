from django.contrib import admin
from . import models


class ProductInventoryInline(admin.TabularInline):
    model = models.ProductInventory
    raw_id_fields = ['product']


class ProductAttributeValuesInline(admin.TabularInline):
    model = models.ProductAttributeValues
    raw_id_fields = ['productinventory']


class ProductMediaInline(admin.TabularInline):
    model = models.Media
    raw_id_fields = ['product_inventory']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'is_active', 'is_recommended', 'USA_product', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductInventoryInline, ]
    list_filter = ['is_active', 'created_at', 'updated_at']
    list_editable = ['is_active', 'is_recommended', 'USA_product']
    fields = ('name', 'slug', 'description', 'category', 'is_active', 'is_recommended', 'USA_product')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'parent']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['product_inventory', 'img_url', 'alt_text', 'is_feature', 'created_at', 'updated_at']
    list_editable = ['is_feature']
    list_filter = ['is_feature', 'created_at', 'updated_at']


@admin.register(models.ProductInventory)
class ProductInventory(admin.ModelAdmin):
    list_display = ['sku', 'upc', 'product_type', 'product', 'brand', 'is_active', 'is_default', 'sale_price',
                    'price', 'weight', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    list_editable = ['is_active', 'is_default', 'sale_price', 'price']
    inlines = [ProductAttributeValuesInline, ProductMediaInline]


@admin.register(models.ProductAttributeValues)
class ProductAttributeValuesAdmin(admin.ModelAdmin):
    list_display = ['attributevalues', 'productinventory']


@admin.register(models.ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['product_attribute', 'attribute_value']


@admin.register(models.ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    

@admin.register(models.ProductTypeAttribute)
class ProductTypeAttributeAdmin(admin.ModelAdmin):
    list_display = ['product_attribute', 'product_type']