# Generated by Django 2.1.7 on 2019-03-06 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restocking', '0005_auto_20190306_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='restocking.Product'),
        ),
        migrations.AlterField(
            model_name='restockinglistitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restocking_item', to='restocking.Product'),
        ),
    ]