#!/usr/bin/env python

import json
import os
import random
import shutil
import sqlite3
import string
import subprocess
import tarfile

## FUNCTIONS

def create_readme(file):
  # Local variables
  user_file_dir = os.path.dirname(file)
  readme_path = os.path.join(user_file_dir, 'readme.md')
  logo_path = os.path.join(user_file_dir, 'logo.png')
  manual_path = os.path.join(user_file_dir, 'manual.pdf')
  extras_path = os.path.join(os.path.dirname(user_file_dir), 'extras')

  # Open json file
  with open(file) as user_file:
    json_data = json.load(user_file)

  # Init data array
  l = []

  # Add logo as header
  # Use title if logo does not exist
  if os.path.exists(logo_path):
    l.append("![logo](logo.png)\n")
  else:
    l.append("# "+json_data['title']+"\n")
    try:
      if json_data['alt_title']:
        l.append("  \nAlt Title: "+json_data['title'])
    except:
      pass

  # General data
  l.append("\n## Description\n\n"+json_data['description']+"\n")
  l.append("\n**Genre:** "+json_data['genre'])

  try:
    if json_data['tags']:
      tags = ", ".join(json_data['tags'])
      l.append("  \n**Tags:** "+tags)
  except:
    pass

  l.append("  \n**Released:** "+str(json_data['year']))
  l.append("  \n**Developer:** "+str(json_data['developer']))
  l.append("  \n**Publisher:** "+str(json_data['publisher']))

  try:
    if json_data['esrb']:
      l.append("  \n**ESRB Rating:** "+json_data['esrb'])
  except:
    pass

  l.append("  \n**Player(s):** ")

  if json_data['players'] == 1:
    l.append("Single-player")
  else:
    l.append(str(json_data['players'])+" players")

  try:
    if json_data['co_op']:
      l.append(", Co-op")
  except:
    pass

  try:
    if json_data['online_multiplayer']:
      l.append(", Online Multiplayer")
  except:
    pass

  try:
    if json_data['controller_support']:
      l.append("  \n**Controller Support:** Yes  ")
  except:
    pass

  try:
    if json_data['operating_system']:
      l.append("\n\n## System Requirements")
      l.append("\n\nSpec     | Min. Requirement",)
      l.append("\n:----    | :----------------")
      l.append("\n**OS**   | "+json_data['operating_system'])
      l.append("\n**CPU**  | "+json_data['processor'])
      l.append("\n**HDD**  | "+json_data['hdd'])
      l.append("\n**RAM**  | "+json_data['ram'])
      l.append("\n**GPU**  | "+json_data['gpu'])
  except:
    pass

  # Media files
  l.append("\n\n## Docs\n")

  if os.path.exists(manual_path):
    l.append("\n- [Manual](manual.pdf)")

  if os.path.exists(os.path.join(user_file_dir, 'boxart.jpg')):
    l.append("\n- [Boxart](boxart.jpg)")

  if os.path.exists(os.path.join(user_file_dir, 'grid.jpg')):
    l.append("\n- [Grid](grid.jpg)")

  if os.path.exists(os.path.join(user_file_dir, 'hero.jpg')):
    l.append("\n- [Hero](hero.jpg)")

  if os.path.exists(os.path.join(user_file_dir, 'icon.png')):
    l.append("\n- [Icon](icon.png)")

  if os.path.exists(os.path.join(user_file_dir, 'screenshot.jpg')):
    l.append("\n- [Screenshot](screenshot.jpg)")

  if os.path.exists(extras_path):
    l.append("\n\n## Extras")

    for f in sorted(os.listdir(extras_path)):
      l.append("\n- ["+f.split('.')[0].title()+"](../extras/"+f+")")

  # Write data to file
  readme = open(readme_path, 'w')
  readme.writelines(l)
  readme.close()

def create_tarfile(filename):
  clean_pfx(filename)
  with tarfile.open(filename+'.tar.gz', "w:gz") as tar:
    notification_stdout('Creating tarball...')
    tar.add(filename, arcname=os.path.basename(filename))

def info_template():
  print('{\n\
  "name": "",\n\
  "title": "",\n\
  "alt_title": "",\n\
  "description": "",\n\
  "developer": "",\n\
  "publisher": "",\n\
  "esrb": "",\n\
  "genre": "",\n\
  "tags": [""],\n\
  "players": 1,\n\
  "region": "",\n\
  "system": "",\n\
  "year": 1999,\n\
  "co_op": false,\n\
  "collection": "",\n\
  "controller_support": false,\n\
  "engine": "",\n\
  "notes": "",\n\
  "online_multiplayer": false,\n\
  "save_path": "",\n\
  "store": "",\n\
  "translation": false,\n\
  "operating_system": "",\n\
  "gpu": "",\n\
  "hdd": "",\n\
  "processor": "",\n\
  "ram": ""\n\
}')

def init_config():
  config = ConfigParser()

  # Create 'profiles' directory if missing
  if not os.path.exists(PROFILE):
    os.makedirs(PROFILE)

  # Create config.ini
  config["GLOBAL"] = {
    "APPDIR" : APPDIR,
    "APPTITLE": 'Empr',
    "BIOS": os.path.join(USERDIR, 'Games/bios'),
    "GAMES": os.path.join(USERDIR, 'Games'),
    "PROFILE": PROFILE,
    "ROMS": os.path.join(USERDIR, 'Games/roms')
  }

  config["APP"] = {
    "DEBUG": True,
    "SECRET_KEY": gen_secretkey(),
    "SQLALCHEMY_DATABASE_URI": 'sqlite:///'+os.path.join(PROFILE, 'db.sqlite3'),
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
  }

  config["RETROARCH"] = {
    "CONFIGDIR": os.path.join(USERDIR,'.config/retroarch'),
    "CORESDIR": os.path.join(USERDIR,'.config/retroarch/cores')
  }

  # Write to config.ini
  with open(CONFIG_PATH, 'w') as conf_data:
    config.write(conf_data)

  os.system('init_db.py')


def notification_stdout(string):
    print('\n' + string + '\n')

# GAME FUNCTIONS

def install_arcade_rom(tarball):
  tarball_name = os.path.basename(tarball)
  slug = tarball_name.split('.')[0]
  rom_name = slug+'.zip'
  cached_tarball_url = os.path.join(CACHE, tarball_name)
  
  arcade_roms = os.path.join(ROMS, 'arcade')
  arcade_bios = os.path.join(USERDIR, '.config/retroarch/system/mame/bios')

  if not os.path.exists(CACHE):
    os.mkdir(CACHE)
  
  shutil.copyfile(tarball, cached_tarball_url)

  cached_tarball = tarfile.open(cached_tarball_url)

  temp_dir = os.path.join(CACHE, slug)
  if not temp_dir:
    os.mkdir(temp_dir)

  cached_tarball.extractall(temp_dir)
  cached_tarball.close()

  os.remove(cached_tarball_url)

  shutil.move(os.path.join(temp_dir, rom_name), os.path.join(arcade_roms, rom_name))

  temp_files = os.listdir(temp_dir)

  for file in temp_files:
    shutil.move(os.path.join(temp_dir, file), arcade_bios)

  shutil.rmtree(temp_dir)

  print('tarball_name: '+tarball_name)
  print('rom_name: '+rom_name)
  print('slug: '+slug)
  print('ROMS: '+ROMS)


# WINE PFX FUNCTIONS

def clean_pfx(filename):
  pfx=get_pfx(filename)

  # Ask user to remove dotnet files
  dotnet_check=input('Would you like to remove .NET files? (y/n): ')
  if dotnet_check.lower() == 'y':
    notification_stdout('Removing .NET files')
    remove_dotnet(filename)
  else:
    notification_stdout('Keeping .NET files')

  # Remove all dosdevices except c:
  dosdevices=os.path.join(pfx, 'dosdevices')
  for file in os.listdir(dosdevices):
    if file != 'c:':
      os.remove(os.path.join(dosdevices, file))

def get_pfx(filename):
  if os.path.isdir(os.path.join(filename, 'drive_c')):
    pfx=filename
  elif os.path.isdir(os.path.join(filename, 'data/drive_c')):
    pfx=os.path.join(filename, 'data')
  else:
    notification_stdout('Could not find prefix.')
    exit()
  return pfx

def remove_dotnet(filename):
  pfx=get_pfx(filename)
  win=os.path.join(pfx, 'drive_c/windows')

  # Dotnet file array
  dotnet_files=[]
  dotnet_files.append(os.path.join(win, 'Installer'))
  dotnet_files.append(os.path.join(win, 'Microsoft.NET'))
  dotnet_files.append(os.path.join(win, 'mono'))
  dotnet_files.append(os.path.join(win, 'system32/gecko'))
  dotnet_files.append(os.path.join(win, 'system32/mono)'))
  dotnet_files.append(os.path.join(win, 'syswow64/)gecko'))

  # Remove dotnet files if present
  for d in dotnet_files:
    if os.path.isdir(d):
      shutil.rmtree(d)
