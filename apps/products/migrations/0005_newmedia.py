# Generated by Django 4.1.5 on 2023-03-06 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_newproductmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_url', models.ImageField(upload_to='product/images', verbose_name='image_url')),
                ('alt_text', models.CharField(max_length=255, verbose_name='img_url')),
                ('is_feature', models.BooleanField(default=False, verbose_name='alt_text')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='is_feature')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='created_at')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_media', to='products.newproductmodel', verbose_name='product_inventory')),
            ],
            options={
                'verbose_name': 'Media',
                'verbose_name_plural': 'Media',
            },
        ),
    ]
