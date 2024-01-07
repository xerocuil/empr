import os
import sys

# Add directories to sys path
LIB_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(LIB_DIR)
sys.path.append(os.path.dirname(LIB_DIR))
sys.path.append(os.path.dirname(APP_DIR))

from lib.config import Config

# Init DB
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
