# Generated by Django 3.1.8 on 2021-05-10 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0019_game_required_files'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platform',
            old_name='full_name',
            new_name='name',
        ),
    ]
