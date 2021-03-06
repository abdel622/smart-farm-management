# Generated by Django 3.2.13 on 2022-06-29 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_prelevements'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='region',
            field=models.CharField(choices=[('TT', 'Tanger-Tétouan-Al Hoceima'), ('OR', "L'Oriental"), ('FM', 'Fès-Meknès'), ('BM', 'Beni Mellal-Khénifra'), ('RS', 'Rabat-Salé-Kénitra'), ('CS', 'Casablanca-Settat'), ('MS', 'Marrakech-Safi'), ('DF', 'Drâa-Tafilalet'), ('SM', 'Souss-Massa'), ('GO', 'Guelmim-Oued Noun'), ('LS', 'Laâyoune-Sakia El Hamra'), ('DO', 'Dakhla-Oued Ed Dahab')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
