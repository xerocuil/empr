# Generated by Django 3.1.14 on 2022-08-09 04:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0045_auto_20220328_2335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='banner',
        ),
    ]
