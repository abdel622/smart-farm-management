# Generated by Django 3.2.13 on 2022-07-01 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_sector_is_connected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='soilphsensorreadings',
            name='sensor',
        ),
        migrations.DeleteModel(
            name='SoilNPKSensorReadings',
        ),
        migrations.DeleteModel(
            name='SoilPhSensorReadings',
        ),
    ]
