# Generated by Django 4.1.5 on 2023-02-26 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_media_product_inventory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='img_url',
            field=models.ImageField(upload_to='product/images', verbose_name='image_url'),
        ),
        migrations.AlterField(
            model_name='media',
            name='product_inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='media', to='products.productinventory', verbose_name='product_inventory'),
        ),
    ]