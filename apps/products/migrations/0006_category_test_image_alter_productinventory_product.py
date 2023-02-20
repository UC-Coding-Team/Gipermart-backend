# Generated by Django 4.1.5 on 2023-02-19 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_productinventory_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='test_image',
            field=models.CharField(blank=True, max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='productinventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product', to='products.product'),
        ),
    ]