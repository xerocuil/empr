import csv
import subprocess
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from .forms import ScrapeGameForm
from .models import Collection, Game, Genre, Platform, Tag

collections = Collection.objects.order_by('name')
games = Game.objects.order_by('sort_title')
genres = Genre.objects.order_by('name')
latest_games = Game.objects.order_by('-date_added')[:10]
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

def games_index(request):
	order_by = request.GET.get('order_by', '-date_added')
	object_list = Game.objects.order_by(order_by)
	paginator = Paginator(object_list, 50)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'games/games_index.html', {
		'collections': collections,
		'genres': genres,
		'games': games,
		'object_list': object_list,
		'order_by': order_by,
		'page_obj': page_obj,
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
	order_by = request.GET.get('order_by', 'sort_title')
	games = Genre.objects.get(id=genre_id).game_set.order_by(order_by)
	return render(request, 'games/genre.html', {
		'games': games,
		'genre': genre,
		'collections': collections,
		'genres': genres,
		'latest_games': latest_games,
		'order_by': order_by,
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
	order_by = request.GET.get('order_by', 'sort_title')
	games = Platform.objects.get(id=platform_id).game_set.order_by(order_by)
	return render(request, 'games/platform.html', {
		'games': games,
		'platform': platform,
		'collections': collections,
		'genres': genres,
		'order_by': order_by,
		'platforms': platforms,
		'tags': tags
	})

class SearchResultsView(ListView):
	model = Game
	template_name = 'games/search_results.html'

	def get_queryset(self):
		query = self.request.GET.get('q', '')
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

## CSV Export
def export_csv(request):
	games = Game.objects.all()
	fieldnames = [
		'sort_title',
		'description',
		'developer',
		'publisher',
		'esrb',
		'genre',
		# 'tags',
		'region',
		'translation',
		'release_date',
		'store',
		'collection',
		'controller_support',
		'platform',
		'player',
		'co_op',
		'online_multiplayer',
		'display',
	]

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="empr_games.csv"'
	writer = csv.DictWriter(response, fieldnames=fieldnames, restval='')
	writer.writeheader()

	for g in games:
		writer.writerow({
			'sort_title': g.sort_title,
			'description': g.description,
			'developer': g.developer,
			'publisher': g.publisher,
			'esrb': g.esrb,
			'genre': g.genre,
			# 'tags': g.tags,
			'region': g.region,
			'translation': g.translation,
			'release_date': g.release_date,
			'store': g.store,
			'collection': g.collection,
			'controller_support': g.controller_support,
			'platform': g.platform,
			'player': g.player,
			'co_op': g.co_op,
			'online_multiplayer': g.online_multiplayer,
			'display': g.display,
		})

	return response
