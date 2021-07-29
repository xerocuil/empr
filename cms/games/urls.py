from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

from .views import SearchResultsView

app_name = 'games'
urlpatterns = [
	path('', views.home, name='home'),
	path('admin/', admin.site.urls),
	path('detail/<int:game_id>/', views.detail, name='detail'),
	path('genre/<int:genre_id>/', views.genre, name='genre'),
	path('platform/<int:platform_id>/', views.platform, name='platform'),
	path('launcher/<int:game_id>/', views.launcher, name='launcher'),
	path('launcher_remote/<int:game_id>/', views.launcher_remote, name='launcher_remote'),
	path('gamelist/<int:platform_id>/', views.gamelist, name='gamelist'),
	path('readme/<int:game_id>/', views.readme, name='readme'),
	path('search/', SearchResultsView.as_view(), name='search_results'),
	path('scrape_game/', views.scrape_game, name='scrape_game'),
	path('scrape_search/<str:file_name>', views.scrape_search, name='scrape_search'),
	path('tag/<int:tag_id>/', views.tag, name='tag'),
	path('test/', views.test, name='test'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
