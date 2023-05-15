import os
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from libs.config import System

db = SQLAlchemy()

app = Flask(__name__,
  static_url_path='/static', 
  static_folder='static',
  template_folder='templates'
  )

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

class Games(db.Model):
    ### Game
    id = db.Column(db.Integer, primary_key=True)
    #### REQUIRED
    filename = db.Column(db.String(128), nullable=False) 
    steam_id = db.Column(db.Integer(), nullable=True)
    #### REQUIRED
    title = db.Column(db.String(128), nullable=False) 
    alt_title = db.Column(db.String(128), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    collection_id = db.Column(db.Integer(), nullable=True)
    archived = db.Column(db.Boolean(), default=0)
    notes = db.Column(db.Text(), nullable=True)

    ### Release
    #### REQUIRED
    platform_id = db.Column(db.Integer(), nullable=False)
    genre_id = db.Column(db.Integer(), nullable=True)
    developer = db.Column(db.String(128), nullable=True)
    publisher = db.Column(db.String(128), nullable=True)

    #### !!Re-define these constraints later!!
    release_date = db.Column(db.Integer(), db.CheckConstraint('release_date > 1900 AND release_date < 2123'), nullable=True)

    region = db.Column(db.String(2), nullable=True)
    esrb = db.Column(db.String(4), nullable=True)
    translation = db.Column(db.Boolean(), default=0)
    store = db.Column(db.String(64), nullable=True)

    ### User Interface
    players = db.Column(db.Integer(), nullable=True)
    controller_support = db.Column(db.Integer())
    co_op = db.Column(db.Boolean(), default=0)
    online = db.Column(db.Boolean(), default=0)

    ### PC
    operating_system = db.Column(db.String(128), nullable=True)
    processor = db.Column(db.String(128), nullable=True)
    ram = db.Column(db.String(128), nullable=True)
    hdd = db.Column(db.String(128), nullable=True)
    gpu = db.Column(db.String(128), nullable=True)
    save_path = db.Column(db.String(200), nullable=True)
    engine = db.Column(db.String(200), nullable=True)
    
    ### DateTime
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)

    def controller_support_h(self):
        if self.controller_support:
            s = 'Controller Supported'
        return s

    def players_h(self):
        if self.players == 1:
            s = 'Single Player'
        else:
            s = '1-' + str(self.players) + 'Players'
        return s

    def online_h(self):
        if self.online:
            s = 'Online Multiplayer'
        return s

    def __repr__(self):
        return '<Title %r>' % self.id

class Platforms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    slug = db.Column(db.String(8), nullable=False)
    type = db.Column(db.String(3), nullable=False)
    launcher = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    title = "Library Home | Empr"
    games = db.session.execute(db.select(Games).order_by(Games.date_added)).scalars()
    return render_template('library/home.html', title = title, games = games)

@app.route('/detail/<int:id>')
def detail(id):

    title = "Detail | Empr"
    game = db.get_or_404(Games, id)
    return render_template('library/detail.html',
        title = title,
        game = game,
        )

print('\n\
    app_title       : ' + System.app_title + '\n\n\
    app_root        : ' + System.app_root + '\n\
    data_dir        : ' + System.data_dir + '\n\
    game_data       : ' + System.game_data + '\n\
    platform_data   : ' + System.platform_data + '\n\n\
    user_dir        : ' + System.user_dir + '\n\
    l_files         : ' + System.l_files + '\n\
    l_db_file       : ' + System.l_db_file + '\n\n\
    games_dir       : ' + System.games_dir + '\n\
    roms_dir        : ' + System.roms_dir + '\n\
    archive        : ' + System.archive + '\n\
    ')