import json
import os
import markdown
import requests

from flask import Flask, Blueprint, render_template, request, redirect, send_from_directory, url_for
# from flask_sqlalchemy import SQLAlchemy

from lib.extensions import db, Config
from forms.library import *
from models.library import *

# Debug
from icecream import ic

library_bp = Blueprint('library', __name__)


# Routes
@library_bp.route('/')
def home():
    # page = request.args.get('page', 1, type=int)
    pagination = Game.query.order_by(Game.date_added.desc()).paginate(per_page=50, max_per_page=100)
    return render_template('library/home/index.html', pagination=pagination)

@library_bp.route('/library/game/<int:game_id>')
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)

    try:
        desc = markdown.markdown(game.description)
    except AttributeError:
        desc = "No description."

    try:
        notes = markdown.markdown(game.notes)
    except AttributeError:
        notes = None
        # notes = "No description."

    platform = Platform.query.get_or_404(game.platform_id)


    # Get paths
    if platform.emulator:
        base_dir = Config.ROMS_DIR
    else:
        base_dir = Config.GAMES_DIR

    platform_dir = os.path.join(base_dir, game.platform.slug)
    game_path = os.path.join(platform_dir, game.filename)

    boxart_url = os.path.join(os.path.join(Config.MEDIA, 'games/'+game.platform.slug+'/boxart/'+game.slug()+'.jpg'))
    if os.path.exists(boxart_url):
        boxart = boxart_url
    else:
        boxart = None

    logo_url = os.path.join(os.path.join(Config.MEDIA, 'games/'+game.platform.slug+'/logo/'+game.filename+'.png'))
    if os.path.exists(logo_url):
        logo = logo_url
    else:
        logo = None

    if os.path.exists(game_path):
        installed = True
    else:
        installed = False

    return render_template('library/game/detail.html', boxart=boxart, boxart_url=boxart_url, logo=logo, desc=desc, game=game, game_path=game_path, installed=installed, notes=notes)

@library_bp.route('/library/game/edit/<int:game_id>', methods=('GET', 'POST'))
def game_edit(game_id):
    game = Game.query.get_or_404(game_id)
    genres = [(g.name,g.id) for g in Genre.query.all()]
    genres_sorted = sorted(genres)

    form = GameForm()

    if form.validate_on_submit():
        game.esrb = form.esrb.data
        game.description = form.description.data
        game.genre_id = form.genre_id.data
        game.title = form.title.data
        game.year = form.year.data
        db.session.commit()
        print("form submitted")
    return render_template('library/game/edit.html', game=game, genres=genres_sorted, form=form)

@library_bp.route('/library/collections')
def collections():
    collections = Collection.query.all()
    return render_template('library/collection/index.html', collections=collections)

@library_bp.route('/library/favorites')
def favorites():
    pagination = Game.query.filter(
        Game.favorite == True
    ).paginate(
        per_page=25,
        max_per_page=100)
    return render_template('/library/favorites.html', pagination=pagination)

@library_bp.route('/library/genres')
def genres():
    genres = Genre.query.all()
    return render_template('library/genre/index.html', genres=genres)

@library_bp.route('/library/platforms')
def platforms():
    platforms = Platform.query.all()
    return render_template('library/platform/index.html', platforms=platforms)

@library_bp.route('/library/search', methods =['GET'])
def search():
    query = request.args.get('query')

    if query:
        ic('query found: ',query)
        pagination = Game.query.filter(
            (Game.title.like('%' + query + '%')) |
            (Game.alt_title.like('%' + query + '%')) |
            (Game.developer.like('%' + query + '%')) |
            (Game.publisher.like('%' + query + '%')) |
            (Game.tags.like('%' + query + '%'))
        ).paginate(per_page=25, max_per_page=100)
    else:
        pagination = None
    return render_template('library/search.html',
        query=query,
        pagination=pagination,
    )

## TAGS
@library_bp.route('/library/tags')
def tags():
    DEBUG = []
    tags_api = 'http://127.0.0.1:5000'+url_for('library.tags_api')
    tags = requests.get(tags_api).json()
    return render_template('library/tags/index.html', tags=tags)

@library_bp.route('/library/tags/detail', methods =['GET'])
def tag_detail():
    query = request.args.get('query')

    if query:
        pagination = Game.query.filter(Game.tags.like('%' + query + '%')).paginate(per_page=25, max_per_page=100)
    else:
        pagination = None
    return render_template('library/tags/detail.html',
        query=query,
        pagination=pagination,
    )



## API
@library_bp.route('/library/api/tags')
def tags_api():
    tags_all = [(g.tags) for g in Game.query.all()]
    tag_list = []
    tags_unique = []

    for t in tags_all:
        if t:
            tag_string = t.split(', ')
            for ts in tag_string:
                tag_list.append(ts)

    for tag in tag_list:
        if tag not in tags_unique:
            tags_unique.append(tag)

    sorted_tags = sorted(tags_unique)
    return (sorted_tags)