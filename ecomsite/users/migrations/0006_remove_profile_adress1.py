# Generated by Django 4.2.5 on 2023-09-21 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_adress1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='adress1',
        ),
    ]
