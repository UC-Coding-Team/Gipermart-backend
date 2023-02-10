# Generated by Django 4.1.5 on 2023-02-07 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_productinventory_installment_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productinventory')),
            ],
        ),
    ]