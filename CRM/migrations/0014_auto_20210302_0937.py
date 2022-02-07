# Generated by Django 3.1.6 on 2021-03-02 12:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0013_auto_20210302_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantprofile',
            name='landlords',
            field=models.ManyToManyField(blank=True, related_name='tenants', to=settings.AUTH_USER_MODEL),
        ),
    ]
