# Generated by Django 4.1.5 on 2023-02-03 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='related_product',
            new_name='is_recommended',
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('process', 'Process'), ('success', 'Success'), ('failed', 'Failed'), ('deleted', 'Deleted')], default='process', max_length=50),
        ),
    ]