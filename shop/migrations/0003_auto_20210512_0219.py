# Generated by Django 3.0.7 on 2021-05-11 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_wishlist_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='device',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='device',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
