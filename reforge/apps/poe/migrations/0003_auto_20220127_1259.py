# Generated by Django 3.1.5 on 2022-01-27 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poe', '0002_auto_20220127_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='league',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]