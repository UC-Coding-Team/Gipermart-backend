from django.contrib.postgres.fields import ArrayField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.user_profile.models import User
# from saleor.order.services import send_telegram_notification


class Buyer(models.Model):
    STATUS_CHOICES = (
        (0, "не найден"),
        (1, "нужно добавить карту"),
        (2, "ожидание верификации"),
        (4, "верифицирован"),
        (5, "нужно фото паспорта"),
        (8, "отказано в верификации"),
        (10, "нужно фото селфи с паспортом"),
        (11, "нужно фото паспорта со страницей прописки"),
        (12, "добавить доверителя"),
    )
    phone_number = PhoneNumberField(unique=True)
    buyer_id = models.CharField(max_length=50)
    user_status = models.PositiveIntegerField(
        choices=STATUS_CHOICES, default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Contract(models.Model):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    CANCELED = 'CANCELED'
    FULFILLED = 'FULFILLED'
    UNFULFILLED = 'UNFULFILLED'

    STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (APPROVED, 'APPROVED'),
        (CANCELED, 'CANCELED'),
        (FULFILLED, 'FULFILLED'),
        (UNFULFILLED, 'UNFULFILLED'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product_variant = models.ForeignKey('products.Variants', on_delete=models.SET_NULL, null=True, blank=True)

    total_price = models.FloatField(default=0)
    total_count = models.IntegerField(default=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=PENDING)
    contract_id = models.PositiveBigIntegerField(unique=True, null=True, blank=True)
    products = ArrayField(models.JSONField())
    limit = models.PositiveSmallIntegerField()
    payment_date = models.PositiveSmallIntegerField(null=True, blank=True)
    buyer_phone = models.CharField(max_length=13)
    address = models.CharField(max_length=155)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.status


# @receiver(post_save, sender=Contract)
# def send_notification(sender, instance, created, **kwargs):
#     if created:
#         send_telegram_notification(instance, 'contract')
