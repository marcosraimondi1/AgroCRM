# Generated by Django 3.1.6 on 2021-02-24 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0002_auto_20210224_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientprofile',
            name='owner',
        ),
    ]
