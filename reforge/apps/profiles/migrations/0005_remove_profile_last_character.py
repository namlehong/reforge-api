# Generated by Django 3.1.5 on 2022-01-28 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_profile_characters'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='last_character',
        ),
    ]