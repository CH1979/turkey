# Generated by Django 3.2.13 on 2022-04-22 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_auto_20220422_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='создано'),
        ),
    ]
