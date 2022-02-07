# Generated by Django 3.1.6 on 2021-03-04 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0022_auto_20210304_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='land',
            name='embeded_map',
        ),
        migrations.AddField(
            model_name='land',
            name='map_src',
            field=models.URLField(default='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d27260.20150718884!2d-64.28966512218979!3d-31.344483531409676!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x94329c27aaf7ddad%3A0x7740f3267d47999b!2sBarrio%20La%20Salle%2C%20Pablo%20Buitrago%206100%2C%20X5147%20C%C3%B3rdoba!5e0!3m2!1ses!2sar!4v1614877393341!5m2!1ses!2sar', verbose_name='google maps embed source'),
            preserve_default=False,
        ),
    ]