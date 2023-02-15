from django.db import models
from apps.products.models import ProductInventory
from django.contrib.auth import get_user_model

User = get_user_model()


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.product

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
