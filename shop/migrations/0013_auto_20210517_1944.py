# Generated by Django 3.0.7 on 2021-05-17 16:44

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20210517_1930'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='order',
            managers=[
                ('delete', django.db.models.manager.Manager()),
            ],
        ),
    ]
