#!/usr/bin/env python

import os
import subprocess
import sys
import threading
import webview

from flask import Flask
from flask import Blueprint

## DEBUG
from icecream import ic

from lib.extensions import db, Config
from routes.app import app_bp
from routes.library import library_bp

# DB_PATH = os.path.join(os.path.expanduser('~'), '.empr/db.sqlite3')

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+Config.DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = Config.KEY
    db.init_app(app)
    app.register_blueprint(library_bp)
    app.register_blueprint(app_bp)
    return app

app = create_app()

if not os.path.exists(Config.DB):
    print("Initializing database...")
    with app.app_context():
        db.create_all()

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

    def search_query(self, query):
        ic(query)

api = Api()
app_window = webview.create_window(
    os.getenv('APP_TITLE'),
    app, js_api=api,
    draggable=True,
    min_size=(1280,720),
    text_select=True)    

def main():
    # webview.start()

    # Debug
    app.run()

if __name__ == '__main__':
    main()
