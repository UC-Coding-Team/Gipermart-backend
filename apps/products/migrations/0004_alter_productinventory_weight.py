<<<<<<< HEAD
# Generated by Django 4.1.5 on 2023-02-17 11:29
=======
# Generated by Django 4.1.5 on 2023-02-19 17:56
>>>>>>> aa0c4478c6229a78121e39f70a97233ba6e719ff

import apps.products.utils.units
from django.db import migrations
import django_measurement.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_productinventory_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinventory',
            name='weight',
            field=django_measurement.models.MeasurementField(blank=True, measurement=apps.products.utils.units.Mass, null=True),
        ),
    ]
