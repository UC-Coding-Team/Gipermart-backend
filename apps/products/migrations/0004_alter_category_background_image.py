# Generated by Django 3.2.16 on 2023-01-28 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20230128_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='category-backgrounds'),
        ),
    ]
