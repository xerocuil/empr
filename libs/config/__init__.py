import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

config_root = os.path.dirname(os.path.realpath(__file__))
libs = os.path.dirname(config_root)


## Init Config class
class System:

    app_title = "Empr"
    
    app_root = os.path.dirname(libs)
    
    user_dir = os.path.expanduser('~')

    l_files = os.path.join(user_dir, '.empr')
    l_db_file =os.path.join(l_files, 'db/empr.sqlite3')

    static = os.path.join(app_root, 'static')
    templates = os.path.join(app_root, 'templates')
    data_dir = os.path.join(app_root, 'static/data')
    game_data = os.path.join(static, 'games')
    # platform_data = os.path.join(data_dir, 'platforms')
    
    games_dir =os.path.join(user_dir, 'Games')
    roms_dir = os.path.join(games_dir, 'roms')
    archive = os.path.join(user_dir, '.mnt/Archive/Games')

class App:
    db = SQLAlchemy()

    app = Flask(__name__,
      static_url_path='/static', 
      static_folder = System.static,
      template_folder= System.templates
      )

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db.init_app(app)