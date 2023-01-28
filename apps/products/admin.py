from django.contrib import admin
from . import models


class ProductInventoryInline(admin.TabularInline):
    model = models.ProductInventory
    raw_id_fields = ['product']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'is_active', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name', )}
    inlines = [ProductInventoryInline, ]
    list_filter = ['is_active', 'created_at', 'updated_at']
    list_editable = ['is_active']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'parent']
    prepopulated_fields = {'slug': ('name', )}
    list_editable = ['is_active']


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(models.Media)
