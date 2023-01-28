from django.contrib import admin
from . import models


class ProductInventoryAdmin(admin.TabularInline):
    model = models.ProductInventory
    raw_id_fields = ['product']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'is_active', 'created_at', 'updated_at']
    inlines = [ProductInventoryAdmin, ]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'parent']


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

