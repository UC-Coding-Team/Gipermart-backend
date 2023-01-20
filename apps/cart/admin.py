from django.contrib import admin
from .models import (
    Cart,
    CartItem,
)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Cart admin"""
    list_display = ("id", "user", "total")
    list_display_links = ("user",)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """CartItem admin"""
    list_display = ("id", "cart", "product","quantity")
    list_display_links = ("cart",)

# admin.site.register(Cart)
# admin.site.register(CartItem)
