# Generated by Django 3.0.7 on 2021-05-24 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_auto_20210524_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='city',
            field=models.CharField(default='qena', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='country',
            field=models.CharField(default='qena', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default='qena', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='first_name',
            field=models.CharField(default='qena', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(default='qena', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='street',
            field=models.CharField(default='qena', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='tel',
            field=models.CharField(default='qena', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='zip',
            field=models.CharField(default='qena', max_length=10),
            preserve_default=False,
        ),
    ]