from lib.extensions import db
from datetime import datetime

# MODELS

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text(1024), nullable=True)
    games = db.relationship('Game', backref='collection')
    def __repr__(self):
        return f'{self.name}'

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    games = db.relationship('Game', backref='genre')
    legacy_id = db.Column(db.Integer, unique=True)
    def __repr__(self):
        return f'{self.name}'

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emulator = db.Column(db.Boolean, default=0)
    launcher = db.Column(db.String(128), nullable=True)
    name = db.Column(db.String(128), unique=True)
    ra_core = db.Column(db.String(128))
    slug = db.Column(db.String(128), unique=True)
    legacy_id = db.Column(db.Integer, unique=True)
    games = db.relationship('Game', backref='platform')
    def __repr__(self):
        return f'{self.name}'

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # tags = models.ManyToManyField(Tag, blank=True)
    alt_title = db.Column(db.String(128), nullable=True, unique=True)
    archived = db.Column(db.Boolean, default=0)
    co_op = db.Column(db.Boolean, default=0)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    controller_support = db.Column(db.Boolean, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text(8192), nullable=True)
    developer = db.Column(db.String(64), nullable=True)
    esrb = db.Column(db.String(4), nullable=True)
    favorite = db.Column(db.Boolean, default=0)
    filename = db.Column(db.String(128), nullable=False, unique=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    gpu = db.Column(db.String(64), nullable=True)
    hdd = db.Column(db.String(64), nullable=True)
    last_played = db.Column(db.DateTime, nullable=True)
    mod = db.Column(db.String(64), nullable=True)
    notes = db.Column(db.Text(8192), nullable=True)
    online_multiplayer = db.Column(db.Boolean, default=0)
    operating_system = db.Column(db.String(64), nullable=True)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    play_count = db.Column(db.Integer, default=0)
    players = db.Column(db.Integer, db.CheckConstraint('players >= 1 AND players <= 64'), default=1, nullable=True)
    processor = db.Column(db.String(64), nullable=True)
    publisher = db.Column(db.String(64), nullable=True)
    ram = db.Column(db.String(64), nullable=True)
    region = db.Column(db.String(2))
    save_path = db.Column(db.String(256), nullable=True)
    steam_id = db.Column(db.Integer, nullable=True)
    store = db.Column(db.String(64), nullable=True)
    title = db.Column(db.String(128), nullable=False, unique=True)
    translation = db.Column(db.Boolean, default=0)
    year = db.Column(db.Integer, db.CheckConstraint('year >= 1948 AND players < 9999'), nullable=True)

    def __repr__(self):
        return f'{self.title}'

    def slug(self):
        slug = self.filename.split('.')[0]
        return slug