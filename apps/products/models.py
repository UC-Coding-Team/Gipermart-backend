from django_measurement.models import MeasurementField
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from .utils.units import Weight, WeightUnits, zero_weight
from ..user_profile.models import User


class Category(MPTTModel):
    name = models.CharField(
        max_length=100, verbose_name=_('name')
    )
    slug = models.SlugField(max_length=150, unique=True, verbose_name=_('slug'))
    description = models.TextField(verbose_name=_('description'))
    background_image = models.ImageField(upload_to='category-backgrounds', blank=True, null=True, verbose_name=_('background_image'))
    test_image = models.CharField(max_length=700, null=True, blank=True, verbose_name=_('test_image'))
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('is_active')
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
        verbose_name=_('parent')
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, verbose_name=_('user'))
    name = models.CharField(
        max_length=255,
        verbose_name=_('name')
    )
    slug = models.SlugField(
        # null=True,
        # blank=True,
        max_length=255,
        verbose_name=_('slug'),
    )
    description = models.TextField(blank=True, verbose_name=_('description'))
    category = models.ForeignKey(
        Category,
        related_name="product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('category')
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('is_active')
    )
    is_recommended = models.BooleanField(default=False, verbose_name=_('is_recommended'))
    USA_product = models.BooleanField(
        default=False,
        verbose_name=_('USA_product')
    )
    status = models.CharField(
        max_length=50, choices=CHOICES, default=PROCESS, verbose_name=_('status')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('created_at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated_at')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

class Brand(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('name')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')


class ProductAttribute(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('name')
    )
    description = models.TextField(blank=True, verbose_name=_('description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('ProductAttribute')
        verbose_name_plural = _('ProductAttributes')


class ProductType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('name')
    )

    product_type_attributes = models.ManyToManyField(
        ProductAttribute,
        related_name="product_type_attributes",
        through="ProductTypeAttribute",
        verbose_name=_('product_type_attributes')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('ProductType')
        verbose_name_plural = _('ProductTypes')


class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="product_attribute",
        on_delete=models.PROTECT,
        verbose_name=_('product_attribute')
    )
    attribute_value = models.CharField(
        max_length=255,
        verbose_name=_('attribute_value')
    )

    def __str__(self):
        return str(self.attribute_value)

    class Meta:
        verbose_name = _('ProductAttributeValue')
        verbose_name_plural = _('ProductAttributeValue')


class ProductInventory(models.Model):
    sku = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('sku')
    )
    upc = models.CharField(
        max_length=12,
        unique=True,
        verbose_name=_('upc')
    )
    product_type = models.ForeignKey(ProductType, related_name="product_type", on_delete=models.CASCADE,
                                     verbose_name=_('product_type'))
    product = models.ForeignKey(Product, related_name="product", on_delete=models.CASCADE,
                                verbose_name=_('product'))
    brand = models.ForeignKey(
        Brand,
        related_name="brand",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('brand')
    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name="product_attribute_values",
        through="ProductAttributeValues",
        verbose_name=_('attribute_values')
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('is_active')
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_('is_default')
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('price')
    )
    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('sale_price')
    )
    installment_plan = models.CharField(max_length=250,verbose_name=_('installment_plan'))
    is_on_sale = models.BooleanField(default=False, verbose_name=_('is_on_sale'))
    weight = MeasurementField(
        measurement=Weight,
        unit_choices=WeightUnits.CHOICES,  # type: ignore
        blank=True,
        null=True,
        verbose_name=_('weight')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('created_at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated_at')
    )

    def __str__(self):
        return self.sku

    class Meta:
        verbose_name = _('ProductInventory')
        verbose_name_plural = _('ProductInventory')


class Media(models.Model):
    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.CASCADE,
        related_name="media",
        verbose_name=_('product_inventory')
    )
    img_url = models.ImageField(upload_to='product/images', verbose_name=_('image_url'))
    alt_text = models.CharField(
        max_length=255,
        verbose_name=_('img_url')
    )
    is_feature = models.BooleanField(
        default=False,
        verbose_name=_('alt_text')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('is_feature')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('created_at')
    )

    class Meta:
        verbose_name = _('Media')
        verbose_name_plural = _('Media')


class Stock(models.Model):
    product_inventory = models.OneToOneField(
        ProductInventory,
        related_name="product_inventory",
        on_delete=models.PROTECT,
        verbose_name=_('product_inventory')
    )
    last_checked = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('last_checked')
    )
    units = models.IntegerField(
        default=0,
        verbose_name=_('units')
    )
    units_sold = models.IntegerField(
        default=0,
        verbose_name=_('units_sold')
    )

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stock')


class ProductAttributeValues(models.Model):
    attributevalues = models.ForeignKey(
        "ProductAttributeValue",
        related_name="attributevaluess",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('attributevalues')
    )
    productinventory = models.ForeignKey(
        ProductInventory,
        related_name="productattributevaluess",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('productinventory')
    )

    class Meta:
        unique_together = (("attributevalues", "productinventory"),)
        verbose_name = _('ProductAttributeValues')
        verbose_name_plural = _('ProductAttributeValues')

    def __str__(self):
        return str(self.productinventory)


class ProductTypeAttribute(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="productattribute",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('attributevalues')
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name="producttype",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('productinventory')
    )

    class Meta:
        unique_together = (("product_attribute", "product_type"),)
        verbose_name = _('ProductTypeAttribute')
        verbose_name_plural = _('ProductTypeAttribute')

    def __str__(self):
        return str(self.product_attribute)


class Wishlist(models.Model):
    user = models.ForeignKey('user_profile.User', on_delete=models.CASCADE, verbose_name=_('user'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('date_added'))

    def __str__(self):
        return self.product


class Rating(models.Model):
    product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE, verbose_name=_('product'))
    rating = models.PositiveSmallIntegerField(verbose_name=_('rating'))

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
