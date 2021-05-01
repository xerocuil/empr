from django.contrib import admin

from .models import Game, Genre, Platform, Tag

admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Tag)
