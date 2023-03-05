# Generated by Django 4.1.5 on 2023-03-05 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinventory',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=12, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='productinventory',
            name='sale_price',
            field=models.DecimalField(decimal_places=0, max_digits=12, verbose_name='sale_price'),
        ),
    ]
