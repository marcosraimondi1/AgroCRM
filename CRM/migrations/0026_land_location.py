# Generated by Django 3.1.6 on 2021-03-06 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0025_remove_land_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='land',
            name='location',
            field=models.CharField(default='Argentina, Cordoba, Cordoba', max_length=100, verbose_name='location'),
            preserve_default=False,
        ),
    ]
