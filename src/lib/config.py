#!/usr/bin/env python

import os
import random
import string
from configparser import ConfigParser

HOME_DIR = os.path.expanduser('~')
PROFILE_DIR = os.path.join(HOME_DIR, '.empr')
CONFIG_PATH = os.path.join(PROFILE_DIR, 'config.ini')
MEDIA = os.path.join(PROFILE_DIR, 'media')
JSON = os.path.join(PROFILE_DIR, 'json')

# Get scraper keys
if os.getenv('FLASK_DEBUG'):
    MG_API_KEY = os.getenv('MG_API_KEY')
    GB_API_KEY = os.getenv('GB_API_KEY')
    SS_PASSWD = os.getenv('SS_PASSWD')
    SS_DEBUG = os.getenv('SS_DEBUG')
else:
    MG_API_KEY = None
    GB_API_KEY = None
    SS_PASSWD = None
    SS_DEBUG = None

def init_config():
    # Create 'profiles' directory if missing
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
        os.makedirs(MEDIA)
        os.makedirs(JSON)

    # Create config.ini
    conf['APP'] = {
        'app_id': str(os.getenv('APP_ID')),
        'app_title': str(os.getenv('APP_TITLE')),
        'debug': os.getenv('FLASK_DEBUG'),
        'db': os.path.join(PROFILE_DIR, 'db.sqlite3'),
        'media': MEDIA,
        'json': JSON,
        'key': generate_key(),
        'server_name': 'http://127.0.0.10:8080'
    }

    conf['GAMES'] = {
        'games_dir': os.path.join(HOME_DIR, 'Games'),
        'roms_dir': os.path.join(HOME_DIR, 'Games/roms'),
    }

    conf['RETROARCH'] = {
        'exec': os.path.join(HOME_DIR, '.local/bin/retroarch'),
        'cores': os.path.join(HOME_DIR, '.config/retroarch/cores')
    }

    conf['ES'] = {
        'exec': '/usr/bin/emulationstation',
        'cores': os.path.join(HOME_DIR, '.emulationstation')
    }

    conf['FTP'] =  {
        'host': '192.168.0.100',
        'port': 21
    }

    conf['SCRAPERS'] = {
        'mg_api_key': MG_API_KEY,
        'gb_api_key': GB_API_KEY,
        'ss_passwd': SS_PASSWD,
        'ss_debug': SS_DEBUG
    }

    conf['SETTINGS'] = {
        'show_mc': 0
    }

    # Write to config.ini
    with open(CONFIG_PATH, 'w') as conf_data:
        conf.write(conf_data)

def generate_key():
  key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64))
  return key

conf = ConfigParser()
conf.read(CONFIG_PATH)

if not os.path.exists(CONFIG_PATH):
    init_config()

# Create Config class
class Config:
    APP_ID = conf['APP']['app_id']
    APP_TITLE = conf['APP']['app_title']
    CONFIG_PATH = CONFIG_PATH
    DB = conf['APP']['db']
    DEBUG = int(conf['APP']['debug'])
    KEY = conf['APP']['key']
    JSON = conf['APP']['json']
    MEDIA = conf['APP']['media']
    SERVER_NAME = conf['APP']['server_name']
    GAMES_DIR = conf['GAMES']['games_dir']
    ROMS_DIR = conf['GAMES']['roms_dir']
    FTP_HOST = conf['FTP']['host']
    FTP_PORT = conf['FTP']['port']
    GB_API_KEY = conf['SCRAPERS']['gb_api_key']
    MG_API_KEY = conf['SCRAPERS']['mg_api_key']
    SS_DEBUG = conf['SCRAPERS']['ss_debug']
    SS_PASSWD = conf['SCRAPERS']['ss_passwd']
    SHOW_MC = int(conf['SETTINGS']['show_mc'])
  
