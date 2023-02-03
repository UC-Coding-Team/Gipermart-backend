from django.db import models
from apps.cart.models import CartItem

class Order(models.Model):
    full_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    comment = models.TextField()
    cart = models.ForeignKey(CartItem, on_delete=models.CASCADE, null=True)
    PAY_STATUS = models.BooleanField(
        default=False,)
    NAXT_STATUS = models.BooleanField(
        default=False,)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return str(self.full_name)