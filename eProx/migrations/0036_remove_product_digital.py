# Generated by Django 5.0.4 on 2024-04-27 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eProx', '0035_product_upload_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
    ]
