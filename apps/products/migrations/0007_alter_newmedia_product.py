# Generated by Django 4.1.5 on 2023-03-09 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_product_category_remove_product_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newmedia',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_media', to='products.newproductmodel', verbose_name='media'),
        ),
    ]
