# Generated by Django 3.0.7 on 2021-05-26 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_remove_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='item',
            field=models.CharField(max_length=150),
        ),
    ]