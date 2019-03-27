# Generated by Django 2.1.7 on 2019-03-24 13:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restocking', '0003_auto_20190324_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='request_quantity',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, 'There is a value that is less than 0')]),
        ),
    ]