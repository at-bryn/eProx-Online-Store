# Generated by Django 5.0.4 on 2024-04-28 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProx', '0040_alter_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='digital',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
