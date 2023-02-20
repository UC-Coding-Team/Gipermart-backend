from django.contrib.auth import get_user_model
from django.db import models
from apps.cart.models import CartItem
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Checkout(models.Model):
    full_name = models.CharField(max_length=250, verbose_name=_('full_name'))
    phone_number = models.CharField(max_length=100, verbose_name=_('phone_number'))
    region = models.CharField(max_length=100, verbose_name=_('region'))
    town = models.CharField(max_length=100, verbose_name=_('town'))
    address = models.CharField(max_length=200, verbose_name=_('address'))
    comment = models.TextField(verbose_name=_('comment'))
    cart = models.ManyToManyField(CartItem, null=True, verbose_name=_('cart'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkout', null=True, verbose_name=_('user'))
    PAY_STATUS = models.BooleanField(
        default=False, verbose_name=_('PAY_STATUS'))
    NAXT_STATUS = models.BooleanField(
        default=False,  verbose_name=_('NAXT_STATUS'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('Checkout')
        verbose_name_plural = _('Checkout')
