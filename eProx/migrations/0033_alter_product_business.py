# Generated by Django 5.0.2 on 2024-04-26 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProx', '0032_alter_profile_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='business',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='eProx.business'),
        ),
    ]
