# Generated by Django 3.1.7 on 2021-02-28 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genre',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='platform',
            old_name='name',
            new_name='slug',
        ),
        migrations.AddField(
            model_name='game',
            name='boxart',
            field=models.ImageField(blank=True, null=True, upload_to='games/boxart/'),
        ),
        migrations.AddField(
            model_name='game',
            name='icons',
            field=models.ImageField(blank=True, null=True, upload_to='games/icons/'),
        ),
        migrations.AddField(
            model_name='game',
            name='wallpaper',
            field=models.ImageField(blank=True, null=True, upload_to='games/wallpaper/'),
        ),
        migrations.AddField(
            model_name='platform',
            name='description',
            field=models.TextField(blank=True, max_length=4096),
        ),
        migrations.AddField(
            model_name='platform',
            name='full_name',
            field=models.CharField(default='Platform', max_length=128, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='platform',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='platform/icons/'),
        ),
        migrations.AddField(
            model_name='platform',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='platform/images/'),
        ),
        migrations.AddField(
            model_name='platform',
            name='launcher',
            field=models.CharField(default='echo "$1"', max_length=192),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='platform',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='platform/logos/'),
        ),
        migrations.AddField(
            model_name='platform',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
