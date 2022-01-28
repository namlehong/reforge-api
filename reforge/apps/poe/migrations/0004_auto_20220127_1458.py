# Generated by Django 3.1.5 on 2022-01-27 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poe', '0003_auto_20220127_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradinghallcategory',
            name='priority',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userservice',
            name='listing_type',
            field=models.CharField(choices=[('wts', 'wts'), ('wtb', 'wtb')], default='wts', max_length=20),
        ),
    ]