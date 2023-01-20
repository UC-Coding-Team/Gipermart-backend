from django.contrib import admin
from .models import (
    User,
    ProfileFeedItem,
)


# admin.site.register(UserProfile) # modelni adminda ko'rinishi
# admin.site.register(ProfileFeedItem) # modelni adminda ko'rinishi

@admin.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    """UserProfile admin"""
    list_display = ("id", "email", "name", "is_active", "is_staff")
    list_display_links = ("email",)


@admin.register(ProfileFeedItem)
class ProfileFeedItemAdmin(admin.ModelAdmin):
    """ProfileFeedItem admin"""
    list_display = ("id", "user_profile", "status_text", "created_on")
    list_display_links = ("user_profile",)