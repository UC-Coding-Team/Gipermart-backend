from django.contrib.auth import get_user_model
from django.db import models
from apps.cart.models import CartItem

User = get_user_model()


class Checkout(models.Model):
    full_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    comment = models.TextField()
    cart = models.ManyToManyField(CartItem, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkout', null=True)
    PAY_STATUS = models.BooleanField(
        default=False, )
    NAXT_STATUS = models.BooleanField(
        default=False, )
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return str(self.full_name)
