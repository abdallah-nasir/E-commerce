# Generated by Django 3.0.7 on 2021-05-15 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20210512_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
