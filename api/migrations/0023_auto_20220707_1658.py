# Generated by Django 3.2.13 on 2022-07-07 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20220707_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fertilizer',
            name='type',
            field=models.CharField(choices=[('EC', 'Engrais Chimique'), ('EO', 'Engrais Organique')], max_length=2),
        ),
        migrations.AlterField(
            model_name='materielvegetal',
            name='type',
            field=models.CharField(choices=[('SS', 'Semences'), ('PL', 'Plants')], max_length=2),
        ),
        migrations.AlterField(
            model_name='productphyto',
            name='type',
            field=models.CharField(choices=[('PS', 'Pesticide-Acaricide'), ('HB', 'Herbicide'), ('FG', 'Fongicide')], max_length=2),
        ),
    ]
