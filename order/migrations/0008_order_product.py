# Generated by Django 5.0.2 on 2024-05-08 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_remove_order_checkout_remove_order_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(null=True, related_name='orders', to='order.orderedproducts'),
        ),
    ]
