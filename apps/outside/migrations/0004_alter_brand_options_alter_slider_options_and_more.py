# Generated by Django 4.1.5 on 2023-02-20 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outside', '0003_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name': 'Brand', 'verbose_name_plural': 'Brands'},
        ),
        migrations.AlterModelOptions(
            name='slider',
            options={'verbose_name': 'Slider', 'verbose_name_plural': 'Sliders'},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'verbose_name': 'Stock', 'verbose_name_plural': 'Stocks'},
        ),
    ]
