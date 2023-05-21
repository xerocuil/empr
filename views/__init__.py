from flask import Flask, redirect, render_template, request, url_for
from libs.config import App as a

from models import Game, Platform
import legacy


# from forms import gameSearchForm
# from PIL import Image


app = a.app

@a.app.route('/', methods=['get', 'post'])
def index():
    title = "Library Home | Empr"
    ### List 10 lastest added Game
    recently_added_games = a.db.session.execute(a.db.select(Game).limit(100).order_by(Game.date_added.desc())).scalars()
    # search = gameSearchForm(request.form)
    if request.method == 'POST':
        # return search_results(search)
        return render_template('library/home.html',
            title = title,
            # form = search
            )
    else:
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

@a.app.route('/print/case/<int:id>')
def print_case(id):
    
    # title = "Print Case"
    game = a.db.get_or_404(Game, id)
    game.grayscale_logo()
    title = game.title
    return render_template('library/case.html',
        title = title,
        game = game,
        )

## Load legacy DB
@a.app.route('/run_batch')
def run_batch():
    with a.app.app_context():
        legacy.batch()
    return redirect('/')

@a.app.route('/test', methods=['POST', 'GET'])
def test():
    return render_template('library/test.html')

@a.app.route('/test2')
def test2(str):
    return f'<h1>(str)</h1>'


with a.app.app_context():
    game_list = a.db.session.execute(a.db.select(Game).limit(10).order_by(Game.date_added.desc())).scalars()

    for i in game_list:
        print(i.title, i.genre.name)

@app.route('/results', methods=['GET', 'POST'])
def search_results(search):
    results =[]
    search_string = search.data['search']
    if search.data['search'] == '':
        qry = a.db.select(Game)
        results = qry.all()

    if not results:
        flash('No results found.')
        return redirect('/')
    else:
        return render_template('library/search.html')


    return render_template('library/search.html',
        games = games,
        searchResult = searchResult)

        