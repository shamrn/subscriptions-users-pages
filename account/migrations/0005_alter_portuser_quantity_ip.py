# Generated by Django 3.2 on 2021-05-14 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_portuser_quantity_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portuser',
            name='quantity_ip',
            field=models.IntegerField(blank=True, null=True, verbose_name='Колличество ip адресов'),
        ),
    ]
