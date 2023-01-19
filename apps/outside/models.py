from django.db import models

class Slider(models.Model):
    images = models.ImageField(upload_to='Slider_img/',default='image.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.created_at

class Stock(models.Model):
    slug = models.SlugField(max_length=40)
    images = models.ImageField(upload_to='Stock_img/',default='image.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.created_at