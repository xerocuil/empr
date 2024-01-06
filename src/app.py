#!/usr/bin/env python

import enum
import json
import markdown
import os
import random
import string
import subprocess
import sys
import threading
import time
import webview

from configparser import ConfigParser
from datetime import datetime
from flask import Flask, render_template, request, redirect, send_from_directory, url_for

from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import func

# Debug
from icecream import ic



from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange



PROFILE_DIR = os.path.join(os.path.expanduser('~'), '.config/empr')
CONFIG_PATH = os.path.join(PROFILE_DIR, 'config.ini')

if not os.path.exists(CONFIG_PATH):
    print("\nInitializing config file...\n")
    subprocess.run(['pipenv', 'run', 'config'])

conf = ConfigParser()
conf.read(CONFIG_PATH)

DB_PATH = conf['APP']['db']
MEDIA = conf['APP']['media']

app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+conf['APP']['db']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = conf['APP']['key']

db = SQLAlchemy(app)


# MODELS

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text(1024), nullable=True)
    games = db.relationship('Game', backref='collection')
    def __repr__(self):
        return f'{self.name}'

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    games = db.relationship('Game', backref='genre')
    def __repr__(self):
        return f'{self.name}'

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    emulator = db.Column(db.Boolean, default=0)
    games = db.relationship('Game', backref='platform')
    def __repr__(self):
        return f'{self.name}'

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alt_title = db.Column(db.String(128), nullable=True, unique=True)
    archived = db.Column(db.Boolean, default=0)
    co_op = db.Column(db.Boolean, default=0)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    controller_support = db.Column(db.Boolean, default=0)
    date_added = db.Column(db.Date, default=datetime.utcnow)
    date_modified = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.Text(8192), nullable=True)
    developer = db.Column(db.String(64), nullable=True)
    esrb = db.Column(db.String(4), nullable=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    gpu = db.Column(db.String(64), nullable=True)
    hdd = db.Column(db.String(64), nullable=True)
    mod = db.Column(db.String(64), nullable=True)
    notes = db.Column(db.Text(8192), nullable=True)
    online_multiplayer = db.Column(db.Boolean, default=0)
    operating_system = db.Column(db.String(64), nullable=True)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    players = db.Column(db.Integer, db.CheckConstraint('players >= 1 AND players < 8'), default=1, nullable=True)
    processor = db.Column(db.String(64), nullable=True)
    publisher = db.Column(db.String(64), nullable=True)
    ram = db.Column(db.String(64), nullable=True)
    region = db.Column(db.String(2))
    save_path = db.Column(db.String(256), nullable=True)
    slug = db.Column(db.String(128), nullable=False, unique=True)
    steam_id = db.Column(db.Integer, nullable=True)
    store = db.Column(db.String(64), nullable=True)
    title = db.Column(db.String(128), nullable=False, unique=True)
    # tags = models.ManyToManyField(Tag, blank=True)
    translation = db.Column(db.Boolean, default=0)
    year = db.Column(db.Integer, db.CheckConstraint('year >= 1948 AND players < 9999'), nullable=True)
    

    def __repr__(self):
        return f'{self.title}'


## FUNCTIONS

def create_folders():
    os.makedirs(MEDIA)

def init_db():
    print("Initializing database...")
    with app.app_context():
        db.create_all()


# Init APP
if not os.path.exists(DB_PATH):
    init_db()



# FORMS
class GameForm(FlaskForm):
    description = TextAreaField()
    esrb = StringField(validators=[Length(max=4)])
    title = StringField(validators=[DataRequired('Title required.'), Length(max=128)])
    year = IntegerField(validators=[NumberRange(min=1948, max=9999, message='Year entered is out of sanity range.')])
    submit = SubmitField("Save")



# Template Tags
# @app.context_processor
# def utility_processor():
#     def play_button(slug, platform_slug):
#         args = [slug, platform_slug]
#         return args
#     return dict(play_button=play_button)




# Routes
@app.route('/')
def home():
    games = Game.query.all()
    return render_template('library/home/index.html', games=games)

@app.route('/library/collections')
def collections():
    collections = Collection.query.all()
    return render_template('library/collection/index.html', collections=collections)

@app.route('/library/game/<int:game_id>')
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
        base_dir = conf['GAMES']['roms_dir']
    else:
        base_dir = conf['GAMES']['games_dir']

    platform_dir = os.path.join(base_dir, game.platform.slug)

    game_path = os.path.join(platform_dir, game.slug)

    if os.path.exists(game_path):
        installed = True
    else:
        installed = False


    return render_template('library/game/detail.html', desc=desc, game=game, game_path=game_path, installed=installed, notes=notes)


@app.route('/library/game/edit/<int:game_id>', methods=('GET', 'POST'))
def game_edit(game_id):
    game = Game.query.get_or_404(game_id)
    form = GameForm()


    if form.validate_on_submit():
        game.esrb = form.esrb.data
        game.description = form.description.data
        game.title = form.title.data
        game.year = form.year.data
        db.session.commit()
        print("form submitted")
    return render_template('library/game/edit.html', game=game, form=form)

@app.route('/library/genres')
def genres():
    genres = Genre.query.all()
    return render_template('library/genre/index.html', genres=genres)

@app.route('/library/platforms')
def platforms():
    platforms = Platform.query.all()
    return render_template('library/platform/index.html', platforms=platforms)


@app.route('/media/<path:path>')
def media(path):
    return send_from_directory(MEDIA, path)



# OPTION MENU TEST
@app.route('/test')
def test():
    # Get json data
    genres_json = json.load(open('/home/xerocuil/Documents/projects/empr/src/import/games_genre.json'))

    # Sort json data by name
    sorted_genres = dict(genres_json)
    genres = sorted(genres_json, key=lambda x : x['name'])

    return render_template("test.html", genres=genres)
# END TEST



class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def launch_game(self, platform, slug):
        print("HI!")
        ic(platform)
        ic(slug)
        subprocess.run(["game-launcher", platform, slug])


    def close_window(self):
        app_window.destroy()

    def toggle_fullscreen(self):
        app_window.toggle_fullscreen()
        

api = Api()
app_window = webview.create_window(os.getenv('APP_TITLE'), app, draggable=True, min_size=(1280,720), text_select=True, js_api=api)       


def main():
    # webview.start()

    # Debug
    app.run()

if __name__ == '__main__':
    main()