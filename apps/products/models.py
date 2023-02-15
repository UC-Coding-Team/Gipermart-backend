from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from ..user_profile.models import User


class Category(MPTTModel):
    name = models.CharField(
        max_length=100,
    )
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    background_image = models.ImageField(upload_to='category-backgrounds', blank=True, null=True)
    is_active = models.BooleanField(
        default=False,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Product(models.Model):
    PROCESS = "process"
    SUCCESS = "success"
    FAILED = "failed"
    DELETED = "deleted"

    CHOICES = [
        (PROCESS, "Process"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
        (DELETED, "Deleted"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True)
    name = models.CharField(
        max_length=255,
    )
    slug = models.SlugField(
        # null=True,
        # blank=True,
        max_length=255,
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        related_name="product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=False,
    )
    is_recommended = models.BooleanField(default=False)
    USA_product = models.BooleanField(
        default=False,
    )
    status = models.CharField(
        max_length=50, choices=CHOICES, default=PROCESS
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    product_type_attributes = models.ManyToManyField(
        ProductAttribute,
        related_name="product_type_attributes",
        through="ProductTypeAttribute",
    )

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="product_attribute",
        on_delete=models.PROTECT,
    )
    attribute_value = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return str(self.attribute_value)


class ProductInventory(models.Model):
    sku = models.CharField(
        max_length=20,
        unique=True,
    )
    upc = models.CharField(
        max_length=12,
        unique=True,
    )
    product_type = models.ForeignKey(ProductType, related_name="product_type", on_delete=models.PROTECT)
    product = models.ForeignKey(Product, related_name="product", on_delete=models.PROTECT)
    brand = models.ForeignKey(
        Brand,
        related_name="brand",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name="product_attribute_values",
        through="ProductAttributeValues",
    )
    is_active = models.BooleanField(
        default=False,
    )
    is_default = models.BooleanField(
        default=False,
    )
    price = models.PositiveIntegerField()
    sale_price = models.PositiveIntegerField()
    installment_plan = models.CharField(max_length=250)
    is_on_sale = models.BooleanField(default=False)
    weight = models.FloatField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.sku


class Media(models.Model):
    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.PROTECT,
        related_name="media",
    )
    img_url = models.ImageField()
    alt_text = models.CharField(
        max_length=255,
    )
    is_feature = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )


class Stock(models.Model):
    product_inventory = models.OneToOneField(
        ProductInventory,
        related_name="product_inventory",
        on_delete=models.PROTECT,
    )
    last_checked = models.DateTimeField(
        null=True,
        blank=True,
    )
    units = models.IntegerField(
        default=0,
    )
    units_sold = models.IntegerField(
        default=0,
    )


class ProductAttributeValues(models.Model):
    attributevalues = models.ForeignKey(
        "ProductAttributeValue",
        related_name="attributevaluess",
        on_delete=models.PROTECT,
    )
    productinventory = models.ForeignKey(
        ProductInventory,
        related_name="productattributevaluess",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = (("attributevalues", "productinventory"),)

    def __str__(self):
        return str(self.productinventory)


class ProductTypeAttribute(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="productattribute",
        on_delete=models.PROTECT,
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name="producttype",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = (("product_attribute", "product_type"),)

    def __str__(self):
        return str(self.product_attribute)


class Wishlist(models.Model):
    user = models.ForeignKey('user_profile.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product


class Rating(models.Model):
    product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.rating


class ProductAllModel(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    atributes_value = models.ManyToManyField(ProductAttributeValue)

    # def __str__(self):
    #     return self.pk

    class Meta:
        verbose_name = 'product_all'
        verbose_name_plural = 'product_alls'
