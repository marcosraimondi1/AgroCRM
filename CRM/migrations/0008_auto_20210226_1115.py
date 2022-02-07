# Generated by Django 3.1.6 on 2021-02-26 14:15

import CRM.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0007_auto_20210226_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_tenant',
        ),
        migrations.AlterField(
            model_name='business',
            name='landlord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lands', to=settings.AUTH_USER_MODEL, validators=[CRM.validators.validate_landlord_user]),
        ),
        migrations.AlterField(
            model_name='tenantprofile',
            name='landlords',
            field=models.ManyToManyField(related_name='tenants', to=settings.AUTH_USER_MODEL, validators=[CRM.validators.validate_landlord_user]),
        ),
        migrations.AlterField(
            model_name='tenantprofile',
            name='tenant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, validators=[CRM.validators.validate_tenant_user]),
        ),
    ]
