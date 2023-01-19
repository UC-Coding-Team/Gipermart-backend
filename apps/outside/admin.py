from django.contrib import admin
from .models import Slider,Stock


@admin.register(Slider)
class Slideradmin(admin.ModelAdmin):
    """Slider admin"""
    list_display = ("id", "images","created_at","updated_at")
    list_display_links = ("id",)

@admin.register(Stock)
class Stockadmin(admin.ModelAdmin):
    """Stock admin"""
    list_display = ("id","slug", "images","created_at","updated_at")
    list_display_links = ("id",)