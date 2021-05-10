from django.contrib import admin

from .models import Game, Genre, Platform, Tag

class GameAdmin(admin.ModelAdmin):
	list_display = ('title', 'genre', 'developer', 'publisher', 'platform')
	search_fields = (
		'title',
		'path',
		'genre__name',
		'developer',
		'publisher',
		'platform__name',
	)

admin.site.register(Game, GameAdmin)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Tag)
