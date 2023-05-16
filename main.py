import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from libs.config import App as a
from libs.config import System as sys

from models import Game

import views

app = a.app

if __name__ == '__main__':
    app.run(debug=True)

print('\n\
    ## DEBUG\n\n\
    app_title       : ' + sys.app_title + '\n\n\
    app_root        : ' + sys.app_root + '\n\
    data_dir        : ' + sys.data_dir + '\n\
    game_data       : ' + sys.game_data + '\n\
    user_dir        : ' + sys.user_dir + '\n\
    l_files         : ' + sys.l_files + '\n\
    l_db_file       : ' + sys.l_db_file + '\n\n\
    games_dir       : ' + sys.games_dir + '\n\
    roms_dir        : ' + sys.roms_dir + '\n\
    archive        : ' + sys.archive + '\n\
    ')