from django.db import models
from apps.user_profil.models import User
from django.db.models import Sum, F, DecimalField
from apps.products.models import Product
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator



# Create your models here.
class Base(models.Model):
    """Base class to be inherited by all models of the API
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)  # Used for logical deletion

    class Meta:
        abstract = True


class Order(Base):
    """Class used to represent and persist the orders data.
        Order is related to a user. Order items are implemented in separate class.
        Fields persisted: 1 + Base
            user: The user related to this order
        Fields Computed: 1
            order_total: Decimal
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['id']

    def __str__(self):
        return f'Order placed at {self.created} by {self.user}'

    @property
    def order_total(self):
        total = self.items.aggregate(
            order_total=Sum(F('quantity') * F('product__price'),
                            output_field=DecimalField())).get('order_total')
        return total


class OrderItem(Base):
    """Class used to represent and to persist the item in an order
    Fields Persisted: 3 + Base
        order<Order>: The order related to this orderItem
        product<Product>: The product related to this orderItem
        quantity<int>: The quantity ordered
    Fields Computed: 1
        item_total<Decimal>: The price total (product.price * quantity)
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('order', 'product')

    @property
    def item_total(self):
        total = self.product.price * self.quantity
        return total


# This receiver will handle a token creation immediately a new user is created
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)