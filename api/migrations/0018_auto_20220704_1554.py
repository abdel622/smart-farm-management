# Generated by Django 3.2.13 on 2022-07-04 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20220704_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='farm',
            name='longitude',
            field=models.FloatField(),
        ),
    ]
