from django.db import models
from apps.products.models import Product
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel
from django.db.models.signals import post_save

User = get_user_model()


class Cart(TimeStampedModel):
    user = models.OneToOneField(
        User, related_name="user_cart", on_delete=models.CASCADE
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True
    )


@receiver(post_save, sender=User)
def create_user_cart(sender, created, instance, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_user', null=True)
    product = models.ForeignKey(
        Product, related_name="cart_product", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)

