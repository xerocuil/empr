#!/usr/bin/env python

import os
import sys
import manage
import sqlite3
from sqlite3 import Error

USER_DIR = os.path.expanduser('~')
APPFILES = USER_DIR + "/.empr"
DBDIR = "db"
DBPATH = os.path.join(APPFILES,DBDIR)
EMPRDB = APPFILES + "/db/empr.sqlite3"

# file_path = os.path.realpath(__file__)
# browser_dir = os.path.dirname(file_path)

## Create db connections
def create_connection(db):
  conn = None
  try:
    conn = sqlite3.connect(db)
    print("SQLite3 version " + sqlite3.version)
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()

def init():
    print("\n## Empr Init ##\n")
    print("USER_DIR: " + USER_DIR)
    if os.path.exists(APPFILES):
        print("Empr path found.")
    else:
        print("Empr path not found.")
        os.makedirs(DBPATH)
        os.mkdir(APPFILES + "/media")
        os.mkdir(APPFILES + "/static")
        print("'% s' directory created." % APPFILES)
        create_connection(EMPRDB)
        print("'% s' database created." % EMPRDB)
    print("\n---\n")


def main():
    if sys.argv[1] == 'init':
        init()
    else:
        manage.main()

if __name__ == '__main__':
    main()