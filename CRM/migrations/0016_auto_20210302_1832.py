# Generated by Django 3.1.6 on 2021-03-02 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0015_auto_20210302_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lands', to='CRM.tenantprofile', verbose_name='tenant'),
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='amount')),
                ('method', models.CharField(max_length=100, verbose_name='mehtod')),
                ('period', models.DateField(verbose_name='period')),
                ('payed', models.FloatField(default=0, verbose_name='payed')),
                ('land', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='CRM.land', verbose_name='land')),
            ],
        ),
    ]
