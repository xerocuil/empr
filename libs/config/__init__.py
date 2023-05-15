import os

config_root = os.path.dirname(os.path.realpath(__file__))
libs = os.path.dirname(config_root)


## Init Config class
class System:

    app_title = "Empr"
    
    app_root = os.path.dirname(libs)
    
    user_dir = os.path.expanduser('~')

    l_files = os.path.join(user_dir, '.empr')
    l_db_file =os.path.join(l_files, 'db/empr.sqlite3')

    data_dir = os.path.join(app_root, 'static/data')
    game_data = os.path.join(data_dir, 'games')
    platform_data = os.path.join(data_dir, 'platforms')
    
    games_dir =os.path.join(user_dir, 'Games')
    roms_dir = os.path.join(games_dir, 'roms')
    archive = os.path.join(user_dir, '.mnt/Archive/Games')
