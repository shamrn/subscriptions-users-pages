# Generated by Django 3.2 on 2021-05-15 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20210515_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pages',
            name='url',
        ),
        migrations.AddField(
            model_name='pages',
            name='slug',
            field=models.SlugField(default='url_url', help_text='Url можно изменить', verbose_name='URL страницы'),
            preserve_default=False,
        ),
    ]
