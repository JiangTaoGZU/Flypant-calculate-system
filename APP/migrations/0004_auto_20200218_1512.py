# Generated by Django 2.2 on 2020-02-18 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0003_auto_20200218_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendorder',
            name='s_o_beizhu',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sendorder',
            name='s_o_sunhao',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='sendorderitems',
            name='soi_is_sign',
            field=models.BooleanField(default=False),
        ),
    ]
