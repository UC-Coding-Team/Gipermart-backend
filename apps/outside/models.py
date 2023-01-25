from django.db import models
from django.utils.safestring import mark_safe
# from apps.user_profile.models import User
from apps.products.models import Category, Product


class Slider(models.Model):
    slug = models.SlugField(max_length=40)
    images = models.ImageField(upload_to='Slider_img/', default='image.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.created_at
    def image_tag(self):
        if self.images.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.images.url))
        else:
            return ""


class Stock(models.Model):
    slug = models.SlugField(max_length=40)
    images = models.ImageField(upload_to='Stock_img/', default='image.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.created_at
    def image_tag(self):
        if self.images.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.images.url))
        else:
            return ""


class Brand(models.Model):
    slug = models.SlugField(max_length=40)
    images = models.ImageField(upload_to='Brands_img/', default='image.png')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_tag(self):
        if self.images.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.images.url))
        else:
            return ""

# class Add_to_cart(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.user
