# Generated by Django 3.0.7 on 2021-05-17 16:20

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20210517_1914'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='order',
            managers=[
                ('delete', django.db.models.manager.Manager()),
            ],
        ),
    ]
