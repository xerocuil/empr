from flask import Flask, redirect, render_template, request, url_for
from libs.config import App as a


from models import Game, Platform

import legacy

app = a.app

@a.app.route('/')
def index():
    title = "Library Home | Empr"
    ### List 10 lastest added Game
    recently_added_games = a.db.session.execute(a.db.select(Game).limit(10).order_by(Game.date_added.desc())).scalars()
    return render_template('library/home.html',
        title = title,
        recently_added_games = recently_added_games
        )

@a.app.route('/detail/<int:id>')
def detail(id):

    title = "Detail | Empr"
    game = a.db.get_or_404(Game, id)
    return render_template('library/detail.html',
        title = title,
        game = game,
        )

## Load legacy DB
@a.app.route('/run_batch')
def run_batch():
    with a.app.app_context():
        legacy.batch()
    return redirect('/')

with a.app.app_context():
    game_list = a.db.session.execute(a.db.select(Game).limit(10).order_by(Game.date_added.desc())).scalars()

    for i in game_list:
        print(i.title, i.genre.name)