# Generated by Django 3.0.7 on 2021-05-26 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_remove_orderproduct_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
    ]
