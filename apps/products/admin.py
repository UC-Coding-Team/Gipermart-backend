import pandas as pd
from django.contrib import admin
from . import models
from .forms import ProductForm
from .models import Category, ProductType


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
    list_display = ['id', 'title_en', 'title_ru', 'created_at']
    exclude = ['user']
    form = ProductForm
    inlines = [NewProductMediaInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if 'excel_file' in request.FILES:
            # load the Excel file into a pandas dataframe
            df = pd.read_excel(request.FILES['excel_file'])

            # select only the 'name' and 'price' columns
            df = df[['sku', 'title_en', 'title_ru', 'price', 'sale_price', 'descriptions', 'weight', 'category', 'product_type']]

            # save each row as a new Product object
            for _, row in df.iterrows():
                category_name = row['category']
                category = Category.objects.get(name=category_name)
                product_type_name = row['product_type']
                product_type = ProductType.objects.get(name=product_type_name)

                product = models.NewProductModel(
                    sku=row['sku'],
                    title_en=row['title_en'],
                    title_ru=row['title_ru'],
                    price=row['price'],
                    sale_price=row['sale_price'],
                    descriptions=row['descriptions'],
                    weight=row['weight'],
                    category=category,
                    product_type=product_type,
                )
                product.save()
