# Generated by Django 5.0.2 on 2024-03-20 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eProx', '0002_delete_business_alter_product_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('contacts', models.CharField(max_length=20)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='business_logos/')),
            ],
        ),
    ]
