from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.PaYme.methods.generate_link import GeneratePayLink
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
    cart = models.ManyToManyField(CartItem, blank=True, verbose_name=_('cart'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkout', null=True, verbose_name=_('user'))
    PAY_STATUS = models.BooleanField(
        default=False, verbose_name=_('PAY_STATUS'))
    NAXT_STATUS = models.BooleanField(
        default=False,  verbose_name=_('NAXT_STATUS'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    generate_link = models.CharField(max_length=300, blank=True)
    total_price = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.full_name


    def generate_pay_link(self):
        if self.PAY_STATUS:
            pay_link = GeneratePayLink(
                payment_id=self.pk,
                amount=self.total_price
            ).generate_link()
            self.generate_link = pay_link
            self.save()
        # print(total_price)

    class Meta:
        verbose_name = _('Checkout')
        verbose_name_plural = _('Checkout')


@receiver(post_save, sender=Checkout)
def checkout_post_save(sender, instance, **kwargs):
    if instance.PAY_STATUS and not instance.generate_link:
        instance.generate_pay_link()