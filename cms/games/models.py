import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from PIL import Image

class Tag(models.Model):
	name = models.CharField(max_length=64)
	class Meta:
		ordering = ['name']
	def __str__(self):
		return self.name

class App(models.Model):
	title = models.CharField(max_length=128, unique=True)
		
class Game(models.Model):
	## Classes
	class esrb_ratings(models.TextChoices):
		E = 'E', _('Everyone')
		E10 = 'E10+', _('Everyone 10+')
		T = 'T', _('Teen')
		M = 'M', _('Mature')
		AO = 'AO', _('Adults Only')

	class player_options(models.TextChoices):
		ONE = '1', _('1 Player')
		TWO = '2', _('2 Players')
		FOUR = '2-4', _('2-4 Players')
		FOURPLUS = '4+', _('4+ Players')

	class regions(models.TextChoices):
		EU = 'EU', _('Europe')
		NA = 'NA', _('North America')
		JP = 'JP', _('Japan')

	class store_options(models.TextChoices):
		BLIZZARD = 'BLIZZARD', _('Blizzard')
		EPIC = 'EPIC', _('Epic Games')
		GOG = 'GOG', _('GOG.com')
		HUMBLE = 'HUMBLE', _('Humble Bundle')
		ITCH = 'ITCH', _('itch.io')
		MS = 'MICROSOFT', _('Microsoft')
		NINTENDO = 'NINTENDO', _('Nintendo')
		PSN = 'PSN', _('PlayStation Network')
		STEAM = 'STEAM', _('Steam')

	## Release Info
	title = models.CharField(max_length=128, unique=True)
	sort_title = models.CharField(max_length=128, unique=True)
	description = models.TextField(blank=True, max_length=512)
	developer = models.CharField(blank=True, max_length=128)
	publisher = models.CharField(blank=True, max_length=128)
	esrb = models.CharField('ESRB', blank=True, choices=esrb_ratings.choices, max_length=4, null=True)
	genre = models.ForeignKey('Genre', blank=True, null=True, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, blank=True)
	region = models.CharField(choices=regions.choices, default="NA", max_length=2, blank=True, null=True)
	release_date = models.DateField('Release Date', blank=True, null=True)
	store = models.CharField(blank=True, choices=store_options.choices, max_length=10, null=True)

	## System Info
	controller_support = models.BooleanField(default=True)
	platform = models.ForeignKey('Platform', on_delete=models.CASCADE)

	## Player Support
	player = models.CharField(blank=True, choices=player_options.choices, max_length=10, null=True)
	co_op = models.BooleanField(default=False)
	online_multiplayer = models.BooleanField(default=False)

	## Images
	boxart = models.ImageField(blank=True, null=True, upload_to='games/boxart/')
	wallpaper = models.ImageField(blank=True, null=True, upload_to='games/wallpaper/')

	## Misc
	favorite = models.BooleanField(default=False)
	kid_friendly = models.BooleanField(default=False)
	required_files = models.TextField(blank=True, null=True)
	steam_id = models.IntegerField(blank=True, null=True)
	hidden = models.BooleanField(default=False)

	## DB Info
	date_added = models.DateTimeField('Date Added', auto_now_add=True)
	date_modified = models.DateTimeField('Date Modified', auto_now=True)
	notes = models.TextField(blank=True, null=True)
	path = models.CharField(blank=True, max_length=128, null=True)
	installed = models.BooleanField(default=False)
	
	def __str__(self):
		return self.title
	def was_added_recently(self):
		return self.date_added >= timezone.now() - datetime.timedelta(days=1)

	def get_game_tags(self):
		ret = ''
		
		print(self.tags.all())

		for tag in self.tags.all():
			ret = ret + tag.name + ', '

		return ret[:-2]

class Genre(models.Model):
	name = models.CharField(max_length=128, unique=True)
	class Meta:
		ordering = ['name']
	def __str__(self):
		return self.name

class Platform(models.Model):
	name = models.CharField(max_length=128, unique=True)
	slug = models.CharField(max_length=64, unique=True)
	path = models.CharField(max_length=128, unique=True, null=True)
	logo = models.ImageField(blank=True, null=True, upload_to='platform/logos/')
	icon = models.ImageField(blank=True, null=True, upload_to='platform/icons/')
	class Meta:
		ordering = ['name']
	def __str__(self):
		return self.name
