# Generated by Django 3.1.14 on 2022-10-23 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_game_alt_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='alt_title',
            field=models.CharField(blank=True, max_length=128, null=True, unique=True),
        ),
    ]
