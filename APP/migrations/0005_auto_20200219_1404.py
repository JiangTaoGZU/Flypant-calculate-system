# Generated by Django 2.2 on 2020-02-19 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0004_auto_20200218_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='o_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sendorder',
            name='s_o_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
