# Generated by Django 3.1.14 on 2022-01-07 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0041_auto_20220107_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='grid',
            field=models.ImageField(blank=True, null=True, upload_to='games/grid/', verbose_name='Header'),
        ),
    ]
