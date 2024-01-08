from lib.extensions import db
from datetime import datetime

# MODELS

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text(1024))
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
    launcher = db.Column(db.String(128))
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
    alt_title = db.Column(db.String(128), unique=True)
    archived = db.Column(db.Boolean, default=0)
    co_op = db.Column(db.Boolean, default=0)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    controller_support = db.Column(db.Boolean, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text(8192))
    developer = db.Column(db.String(64))
    esrb = db.Column(db.String(4))
    favorite = db.Column(db.Boolean, default=0)
    filename = db.Column(db.String(128), nullable=False, unique=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    gpu = db.Column(db.String(64))
    hdd = db.Column(db.String(64))
    last_played = db.Column(db.DateTime)
    mod = db.Column(db.String(64))
    notes = db.Column(db.Text(8192))
    online_multiplayer = db.Column(db.Boolean, default=0)
    operating_system = db.Column(db.String(64))
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    play_count = db.Column(db.Integer, default=0)
    players = db.Column(db.Integer, db.CheckConstraint('players >= 1 AND players <= 64'), default=1)
    processor = db.Column(db.String(64))
    publisher = db.Column(db.String(64))
    ram = db.Column(db.String(64))
    region = db.Column(db.String(2))
    save_path = db.Column(db.String(256))
    steam_id = db.Column(db.Integer)
    store = db.Column(db.String(64))
    tags = db.Column(db.String(128))
    title = db.Column(db.String(128), nullable=False, unique=True)
    translation = db.Column(db.Boolean, default=0)
    year = db.Column(db.Integer, db.CheckConstraint('year >= 1948 AND players < 9999'))

    def __repr__(self):
        return f'{self.title}'

    def slug(self):
        slug = self.filename.split('.')[0]
        return slug

    def tag_array(self):
        tag_array = []
        tag_string = self.tags.split(',')
        for t in tag_string:
            tag_array.append(t)
        return tag_array
