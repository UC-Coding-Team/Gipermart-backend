# Generated by Django 4.1.5 on 2023-02-03 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_initial'),
        ('checkout', '0002_alter_order_cart'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='Checkout',
        ),
    ]