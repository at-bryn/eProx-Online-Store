# Generated by Django 5.0.2 on 2024-03-20 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProx', '0004_customer_remove_business_logo_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
