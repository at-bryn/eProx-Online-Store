# Generated by Django 5.0.4 on 2024-05-08 15:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProx', '0044_remove_shippingaddress_order_remove_orderitem_order_and_more'),
        ('order', '0014_rename_customer_checkout_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eProx.product'),
        ),
    ]
