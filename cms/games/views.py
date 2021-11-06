import csv
import subprocess
from django.contrib import messages

from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from .forms import ScrapeGameForm
from .models import Collection, Game, Genre, Platform, Tag
	
latest_games = Game.objects.order_by('-date_added')[:15]
collections = Collection.objects.order_by('name')
genres = Genre.objects.order_by('name')
platforms = Platform.objects.order_by('name')
tags = Tag.objects.order_by('name')

def home(request):
	return render(request, 'games/home.html', {
		'collections': collections,
		'genres': genres,
		'latest_games': latest_games,
		'platforms': platforms,
		'tags': tags
	})

def collection(request, collection_id):
	collection = get_object_or_404(Collection, pk=collection_id)
	games = Collection.objects.get(id=collection_id).game_set.order_by('release_date')
	return render(request, 'games/collection.html', {
		'games': games,
		'collection': collection,
		'collections': collections,
		'genres': genres,
		'latest_games': latest_games,
		'platforms': platforms,
		'tags': tags
	})

def detail(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	return render(request, 'games/detail.html', {
		'game': game,
		'collections': collections,
		'genres': genres,
		'platforms': platforms,
		'tags': tags
	})

# def gamelist(request, platform_id):
# 	from django.core import serializers
# 	games = serializers.serialize(
# 		"xml", Game.objects.filter(platform_id=platform_id),
# 		fields=(
# 			'title',
# 			'sort_title',
# 			'description',
# 			'release_date',
# 			'developer',
# 			'publisher',
# 			'genre',
# 			'player',
# 		)
# 	)
# 	from django.core.files import File
# 	f = open('gamelist.xml', 'w')
# 	myfile = File(f)
# 	myfile.write(games)
# 	myfile.close()
# 	return HttpResponse("All done!")

def genre(request, genre_id):
	genre = get_object_or_404(Genre, pk=genre_id)
	games = Genre.objects.get(id=genre_id).game_set.order_by('sort_title')
	return render(request, 'games/genre.html', {
		'games': games,
		'genre': genre,
		'collections': collections,
		'genres': genres,
		'latest_games': latest_games,
		'platforms': platforms,
		'tags': tags
	})

def launcher(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	name = game.title
	filename = game.path
	platform = game.platform.slug
	cmd = 'game-launcher ' + platform + ' ' + filename + ' &'
	subprocess.Popen(cmd, shell=True)
	return render(request, 'games/launcher.html', {
		'game': game,
	})

def launcher_remote(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	name = game.title
	filename = game.path
	platform = game.platform.slug
	cmd = 'ssh arcade "export DISPLAY=:0;game-launcher ' + platform + ' ' + filename + '"'
	subprocess.Popen(cmd, shell=True)
	return render(request, 'games/launcher.html', {
		'game': game,
	})

def platform(request, platform_id):
	platform = get_object_or_404(Platform, pk=platform_id)
	games = Platform.objects.get(id=platform_id).game_set.order_by('sort_title')
	return render(request, 'games/platform.html', {
		'games': games,
		'platform': platform,
		'collections': collections,
		'genres': genres,
		'platforms': platforms,
		'tags': tags
	})

class SearchResultsView(ListView):
	model = Game
	template_name = 'games/search_results.html'

	def get_queryset(self):
		query = self.request.GET.get('q')
		object_list = Game.objects.filter(
			Q(sort_title__icontains=query) |
			Q(developer__icontains=query) |
			Q(genre__name__icontains=query) |
			#Q(tags__name__icontains=query) |
			Q(platform__name__icontains=query) |
			Q(publisher__icontains=query)
			
		).order_by('sort_title')
		return object_list

def scrape_search(request,file_name):
	notification = 'You submitted: ' + file_name
	cmd = '/home/xerocuil/Projects/empr/utils/scrapers/tgdb/tgdb_scraper.sh ' + file_name
	subprocess.Popen(cmd, shell=True)
	return render(request, 'games/scrape_search.html', {
		'notification': notification
	})

def scrape_game(request):
	if request.method == 'POST':
		form = ScrapeGameForm(request.POST)
		if form.is_valid():
			file_name = form.cleaned_data['file_name']
			return HttpResponseRedirect('/scrape_search/' + file_name)
	else:
		form = ScrapeGameForm()

	return render(request, 'games/scrape_game.html', { 'form': form })

def tag(request, tag_id):
	tag = get_object_or_404(Tag, pk=tag_id)
	games = Tag.objects.get(id=tag_id).game_set.order_by('sort_title')
	return render(request, 'games/tag.html', {
		'games': games,
		'tag': tag,
		'collections': collections,
		'genres': genres,
		'latest_games': latest_games,
		'platforms': platforms,
		'tags': tags
	})

def readme(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	return render(request, 'games/readme.html', {
		'game': game,
	})

def gamelist(request, platform_id):
	platform = get_object_or_404(Platform, pk=platform_id)
	games = Platform.objects.get(id=platform_id).game_set.order_by('sort_title')
	return render(request, 'games/xml_list.html', {
		'games': games,
		'platform': platform
	})