# Generated by Django 4.1.5 on 2023-02-09 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_productallmodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productallmodel',
            options={'verbose_name': 'product_all', 'verbose_name_plural': 'product_alls'},
        ),
    ]