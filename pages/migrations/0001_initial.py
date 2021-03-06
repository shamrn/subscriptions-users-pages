# Generated by Django 3.2 on 2021-05-15 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(max_length=100)),
                ('main_title', models.CharField(max_length=200, verbose_name='Главный заголовок')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('second_title', models.CharField(blank=True, help_text='Необязательное поле', max_length=200, null=True, verbose_name='Второстепенный заголовок')),
                ('pages', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.pages')),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list', models.CharField(blank=True, help_text='Необязательное поле', max_length=150, null=True, verbose_name='Список')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.section')),
            ],
        ),
        migrations.CreateModel(
            name='Body',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, help_text='Необязательное поле', null=True, verbose_name='Текст')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.section')),
            ],
        ),
    ]
