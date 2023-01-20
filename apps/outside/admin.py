from django.contrib import admin
from .models import Slider,Stock,Brand


@admin.register(Slider)
class Slideradmin(admin.ModelAdmin):
    """Slider admin"""
    list_display = ("id","slug", "images","created_at","updated_at","image_tag")
    list_display_links = ("id",)
    readonly_fields = ('image_tag',)

@admin.register(Stock)
class Stockadmin(admin.ModelAdmin):
    """Stock admin"""
    list_display = ("id","slug", "images","created_at","updated_at","image_tag")
    list_display_links = ("id",)
    readonly_fields = ('image_tag',)


@admin.register(Brand)
class Brandadmin(admin.ModelAdmin):
    """Brand admin"""
    list_display = ("id","slug","images","category","product","created_at","updated_at","image_tag")
    list_display_links = ("id",)
    readonly_fields = ('image_tag',)