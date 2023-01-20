from django.contrib import admin
from .models import (
    Order,
    OrderItem,
)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin"""
    list_display = ("id", "user")
    list_display_links = ("user",)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """CartItem admin"""
    list_display = ("id", "order", "product","quantity")
    list_display_links = ("order",)