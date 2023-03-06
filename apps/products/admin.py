from django.contrib import admin
from . import models


class ProductAttributeValuesInline(admin.TabularInline):
    model = models.ProductAttributeValues
    raw_id_fields = ['product']


class NewProductMediaInline(admin.TabularInline):
    model = models.NewMedia
    raw_id_fields = ['product']


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


@admin.register(models.ProductAttributeValues)
class ProductAttributeValuesAdmin(admin.ModelAdmin):
    list_display = ['id', 'attributevalues', 'product']


@admin.register(models.ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_attribute', 'attribute_value']


@admin.register(models.ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']


@admin.register(models.ProductTypeAttribute)
class ProductTypeAttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_attribute', 'product_type']


@admin.register(models.NewProductModel)
class NewProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    inlines = [NewProductMediaInline]
