# Generated by Django 2.2 on 2020-02-18 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendorder',
            name='s_o_is_sign',
            field=models.BooleanField(default=False),
        ),
    ]
