# Generated by Django 3.1.12 on 2021-07-26 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0025_auto_20210716_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.TextField(blank=True, max_length=1024),
        ),
    ]