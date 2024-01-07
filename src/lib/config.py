#!/usr/bin/env python

import os
import random
import string
from configparser import ConfigParser

HOME_DIR = os.path.expanduser('~')
PROFILE_DIR = os.path.join(HOME_DIR, '.config/empr')
CONFIG_PATH = os.path.join(PROFILE_DIR, 'config.ini')

if not os.path.exists(CONFIG_PATH):
    init_config()

conf = ConfigParser()
conf.read(CONFIG_PATH)

def generate_key():
  key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64))
  return key

def init_config():

    # Create 'profiles' directory if missing
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)

    # Create config.ini
    config['APP'] = {
        'app_id': str(os.getenv('APP_ID')),
        'app_title': str(os.getenv('APP_TITLE')),
        'debug': True,
        'db': os.path.join(PROFILE_DIR, 'db.sqlite3'),
        'media': os.path.join(PROFILE_DIR, 'media'),
        'key': generate_key()
    }

    config['GAMES'] = {
        'games_dir': os.path.join(HOME_DIR, 'Games'),
        'roms_dir': os.path.join(HOME_DIR, 'Games/roms'),
    }

    config['RETROARCH'] = {
        'exec': os.path.join(HOME_DIR, '.local/bin/retroarch'),
        'cores': os.path.join(HOME_DIR, '.config/retroarch/cores')
    }

    config['ES'] = {
        'exec': '/usr/bin/emulationstation',
        'cores': os.path.join(HOME_DIR, '.emulationstation')
    }

    # Write to config.ini
    with open(CONFIG_PATH, 'w') as conf_data:
        config.write(conf_data)


# Create Config class
class Config:
  APP_ID = conf['APP']['app_id']
  APP_TITLE = conf['APP']['app_title']
  CONFIG_PATH = CONFIG_PATH
  DB = conf['APP']['db']
  KEY = conf['APP']['key']
  MEDIA = conf['APP']['media']
  GAMES_DIR = conf['GAMES']['games_dir']
  ROMS_DIR = conf['GAMES']['roms_dir']
