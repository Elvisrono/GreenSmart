# Generated by Django 5.1.4 on 2025-01-09 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0004_rename_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='price',
        ),
    ]
