# Generated by Django 4.1.5 on 2023-03-10 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_newmedia_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newproductmodel',
            old_name='title',
            new_name='title_en',
        ),
        migrations.AddField(
            model_name='newproductmodel',
            name='title_ru',
            field=models.CharField(default=3, max_length=300, verbose_name='title'),
            preserve_default=False,
        ),
    ]
