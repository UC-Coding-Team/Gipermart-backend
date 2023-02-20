# Generated by Django 4.1.5 on 2023-02-20 08:58

import apps.products.utils.units
from django.db import migrations
import django_measurement.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_productinventory_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinventory',
            name='weight',
            field=django_measurement.models.MeasurementField(default=0.0, measurement=apps.products.utils.units.Mass),
        ),
    ]
