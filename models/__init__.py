import os

from datetime import datetime
from slugify import slugify

from libs.config import App as a
from libs.config import System as s


from PIL import Image

static = s.static

class Genre(a.db.Model):
    id = a.db.Column(a.db.Integer, primary_key=True)
    name = a.db.Column(a.db.String(64), nullable=False)
    games = a.db.relationship('Game', backref='genre')

class Platform(a.db.Model):
    id = a.db.Column(a.db.Integer, primary_key=True)
    name = a.db.Column(a.db.String(64), nullable=False)
    slug = a.db.Column(a.db.String(8), nullable=False)
    emulator = a.db.Column(a.db.Boolean, default=False)
    launcher = a.db.Column(a.db.String(200), nullable=False)
    games = a.db.relationship('Game', backref='platform')

game_tags = a.db.Table('game_tags',
    a.db.Column('game_id', a.db.Integer, a.db.ForeignKey('game.id')),
    a.db.Column('tag_id', a.db.Integer, a.db.ForeignKey('tag.id'))
    )

class Game(a.db.Model):
    ### Game
    id = a.db.Column(a.db.Integer, primary_key=True)
    #### REQUIRED
    filename = a.db.Column(a.db.String(128), nullable=False) 
    steam_id = a.db.Column(a.db.Integer(), nullable=True)
    #### REQUIRED
    title = a.db.Column(a.db.String(128), nullable=False) 
    alt_title = a.db.Column(a.db.String(128), nullable=True)
    edition = a.db.Column(a.db.String(128), nullable=True)
    description = a.db.Column(a.db.Text(), nullable=True)
    collection_id = a.db.Column(a.db.Integer(), nullable=True)
    archived = a.db.Column(a.db.Boolean(), default=0)
    notes = a.db.Column(a.db.Text(), nullable=True)

    ### Release
    #### REQUIRED
    platform_id = a.db.Column(a.db.ForeignKey('platform.id'))
    genre_id = a.db.Column(a.db.ForeignKey('genre.id'))
    tags = a.db.relationship('Tag', secondary=game_tags, backref='tags')
    developer = a.db.Column(a.db.String(128), nullable=True)
    publisher = a.db.Column(a.db.String(128), nullable=True)

    #### !!Re-define these constraints later!!
    release_date = a.db.Column(a.db.Integer(), a.db.CheckConstraint('release_date > 1900 AND release_date < 2123'), nullable=True)

    region = a.db.Column(a.db.String(2), nullable=True)
    esrb = a.db.Column(a.db.String(4), nullable=True)
    content_descriptors = a.db.Column(a.db.String(200), nullable=True)
    translation = a.db.Column(a.db.Boolean(), default=0)
    store = a.db.Column(a.db.String(64), nullable=True)

    ### User Interface
    players = a.db.Column(a.db.Integer(), nullable=True)
    controller_support = a.db.Column(a.db.Integer())
    co_op = a.db.Column(a.db.Boolean(), default=0)
    online = a.db.Column(a.db.Boolean(), default=0)

    ### PC
    operating_system = a.db.Column(a.db.String(128), nullable=True)
    processor = a.db.Column(a.db.String(128), nullable=True)
    ram = a.db.Column(a.db.String(128), nullable=True)
    hdd = a.db.Column(a.db.String(128), nullable=True)
    gpu = a.db.Column(a.db.String(128), nullable=True)
    save_path = a.db.Column(a.db.String(200), nullable=True)
    engine = a.db.Column(a.db.String(200), nullable=True)
    
    ### DateTime
    date_added = a.db.Column(a.db.DateTime, default=datetime.utcnow)
    date_modified = a.db.Column(a.db.DateTime, default=datetime.utcnow)


    ### Get slug
    def get_slug(self, title):
        if self.title.startswith("The ") or title.startswith("A "):
            title_split = title.split(" ", 1)
            title_prefix = title_split[0]
            title_string = title_split[1]
        else:
            title_string = title

        slug = slugify(title_string, max_length=64, word_boundary=True)
        return slug


    ### Get sort title
    def get_sort_title(self, title):
        if self.title.startswith("The ") or self.title.startswith("A "):
            title_split = self.title.split(" ", 1)
            title_prefix = title_split[0]
            title_suffix = title_split[1]
            sort_title = title_suffix + ', ' + title_prefix
        else:
            sort_title = self.title
        return sort_title

    ### !!!Get Default Images!!!!

    def get_game_image(self, filename):
        url_suffix = 'games/' + self.platform.slug + '/' + self.get_slug(self.title) + '/img/' + filename

        if os.path.exists(os.path.join(static, url_suffix)):
            url_path = '/static/' + url_suffix
        else:
            ### !!!Get Default Images!!!!
            url_path = '/static/blerg.png'

        return url_path

    def get_platform_image(self, filename):
        url_suffix = 'img/platform/' + self.platform.slug + '/' + filename

        if os.path.exists(os.path.join(static, url_suffix)):
            url_path = '/static/' + url_suffix
        else:
            ### !!!Get Default Images!!!!
            url_path = '/static/blerg.png'

        return url_path

    def get_esrb_image(self):
        url_suffix = 'img/esrb/' + self.esrb + '.svg'

        if os.path.exists(os.path.join(static, url_suffix)):
            url_path = '/static/' + url_suffix
        else:
            ### !!!Get Default Images!!!!
            url_path = '/static/blerg.png'

        return url_path

    def get_store_image(self, filename):
        url_suffix = 'img/store/' + self.store + '/' + filename

        if os.path.exists(os.path.join(static, url_suffix)):
            url_path = '/static/' + url_suffix
        else:
            ### !!!Get Default Images!!!!
            url_path = ''

        return url_path




    def grayscale_logo(self):
        logo = self.get_game_image('logo.png')
        
        app_root = s.app_root
        l_path = os.path.join(app_root + logo)
        
        if os.path.exists(l_path):
            print(l_path)

            l_name = os.path.basename(l_path)
            l_dir = os.path.dirname(l_path)
            l_slug = l_name.split('.')[0]
            l_print = os.path.join(l_dir, l_slug + '-print.png')

            if os.path.exists(l_print):
                print('\nPrint image exists.')
            else:
                try:
                    img = Image.open(l_path).convert('LA')
                    img.save(l_print)
                    print('\nImage created successfully\n')
                except:
                    print('\nThere was an error creating the image.\n') 
        else:
            print('no l_path')


    def content_descriptor_array(self):
        if self.content_descriptors:
            cda = self.content_descriptors.split(',')
            return cda



    def controller_support_h(self):
        if self.controller_support:
            s = 'Controller Supported'
        else:
            s = 'Mouse/Keyboard Required'
        return s

    def players_h(self):
        if self.players == 1:
            s = 'Single Player'
        else:
            s = '1-' + str(self.players) + ' Players'
        return s

    def online_h(self):
        if self.online:
            s = 'Online Multiplayer'
        return s

    def __repr__(self):
        return '<Title %r>' % self.id

class Tag(a.db.Model):
    id = a.db.Column(a.db.Integer, primary_key=True)
    name = a.db.Column(a.db.String(64), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id

with a.app.app_context():
    a.db.create_all()