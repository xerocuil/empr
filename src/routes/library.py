import os

from flask import Flask, Blueprint, render_template, request, redirect, send_from_directory, url_for
import markdown

from lib.extensions import db, Config
from forms.library import *
from models.library import *

library_bp = Blueprint('library', __name__)

# Routes
@library_bp.route('/')
def home():
    games = Game.query.all()
    return render_template('library/home/index.html', games=games)



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

    if platform.emulator:
        base_dir = Config.ROMS_DIR
    else:
        base_dir = Config.GAMES_DIR

    platform_dir = os.path.join(base_dir, game.platform.slug)

    game_path = os.path.join(platform_dir, game.slug)

    if os.path.exists(game_path):
        installed = True
    else:
        installed = False


    return render_template('library/game/detail.html', desc=desc, game=game, game_path=game_path, installed=installed, notes=notes)

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

@library_bp.route('/library/genres')
def genres():
    genres = Genre.query.all()
    return render_template('library/genre/index.html', genres=genres)

@library_bp.route('/library/platforms')
def platforms():
    platforms = Platform.query.all()
    return render_template('library/platform/index.html', platforms=platforms)



# @library_bp.route('/media/<path:path>')
# def media(path):
#     return send_from_directory(Config.MEDIA, path)