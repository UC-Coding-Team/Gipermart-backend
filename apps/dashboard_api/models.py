from django.db import models


class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='logos', null=True, blank=True)
    phonenumbers = models.CharField(max_length=20, blank=True, null=True)
    site_type = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.site_type
