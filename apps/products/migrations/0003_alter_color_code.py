# Generated by Django 4.1.5 on 2023-01-21 07:19

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='code',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None),
        ),
    ]
