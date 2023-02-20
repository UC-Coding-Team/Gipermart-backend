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
