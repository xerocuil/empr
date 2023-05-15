import glob, json, html, markdown, os, sass, shutil, sqlite3, subprocess, sys, tarfile, yaml
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

from slugify import slugify

from libs.config import System

app_dir = os.path.dirname(os.path.realpath(__file__))

## Database Connection

### Connect to legacy db
class legacy_db:
    try:
        connection = sqlite3.connect(System.l_db_file)
        cursor = connection.cursor()
    except:
        notification_stdout('Database Connection error')

### Connect to development db
class new_db:
    try:
        connection = sqlite3.connect('instance/test.db')
        cursor = connection.cursor()
    except:
        notification_stdout('Database Connection error')

## V1 Functions

### Notification (stdout)
def notification_stdout(string):
    print('\n' + string + '\n')

### Check if game is installed
def check_installed():
    
    if os.path.exists(GameObj.exec):
        GameObj.installed = True
    else:
        GameObj.installed = False

### Create readme.html file
def create_readme():
    ### Set template environment
    sass_dir = os.path.join(System.assets, 'style/sass')
    sass_file = os.path.join(sass_dir, 'main.sass')
    css_dir = os.path.join(System.assets, 'style/css')
    css_output = sass.compile(filename=(sass_file), output_style='compressed')
    sass.compile(dirname=(sass_dir, css_dir), output_style='compressed')
    
    env = Environment(
      loader=FileSystemLoader(System.templates),
      autoescape=select_autoescape()
    )
    readme = env.get_template("readme.html")

    if GameObj.controller_support:
        controller_support = "Controller Support"
    else:
        controller_support = "Mouse/Keyboard Required"

    if GameObj.description:
        description = markdown.markdown(GameObj.description)

    # if GameObj.players == "1":
    #     players = 'Single-Player'
    # else:
    #     players = '1-' + GameObj.players + ' players'

    if os.path.exists(GameObj.gd_dir + '/Manual.pdf'):
        manual = True
    else:
        manual = False

    def smart_truncate(content, length=32):
        if len(content) <= length:
            return content
        else:
            return ','.join(content[:length+1].split(',')[0:-1])
    
    tags_trunc = smart_truncate(TagsObj.tags_string)

    ## Get ESRB
    if GameObj.esrb:
        esrb_file = os.path.join(System.app_dir, 'assets/esrb/' + GameObj.esrb + '.svg')
        shutil.copy(esrb_file, GameObj.gd_img + '/' + GameObj.esrb + '.svg' )

    ### Write data to file

    game_html = open(GameObj.game_html, 'w')
    game_html.write(readme.render(
        title = GameObj.title,
        alt_title = GameObj.alt_title,
        steam_id = GameObj.steam_id,
        description = description,
        genre_id = GameObj.genre_id,
        genre = GenreObj.name,
        tags_string = TagsObj.tags_string,
        collection_id = GameObj.collection_id,
        release_date = GameObj.release_date,
        platform_name = PlatformObj.name,
        platform_slug = PlatformObj.slug,
        publisher = GameObj.publisher,
        developer = GameObj.developer,
        players = GameObj.players_h,
        co_op = GameObj.co_op,
        online = GameObj.online,
        controller_support = controller_support,
        esrb = GameObj.esrb,
        region = GameObj.region,
        translation = GameObj.translation,
        store = GameObj.store,
        operating_system = GameObj.operating_system,
        processor = GameObj.processor,
        ram = GameObj.ram,
        hdd = GameObj.hdd,
        gpu = GameObj.gpu,
        notes = GameObj.notes,
        manual = manual,
        css_output = css_output,
        ))
    
### Create gunzipped archive
def make_pkg(src, dest):
    print('\nPacking...\n')
    with tarfile.open(dest, "w:gz") as tar:
        tar.add(src, arcname=os.path.basename(src))

## Extract gunzipped archive
def extract_pkg(pkg, dest):
    print('\nUnpacking...\n')
    make_pkg = subprocess.run(['tar', '-xvf', pkg, '-C', dest])

### Extract game package
def extract_game():
    if check_archive():
        if not os.path.exists(GameObj.gd_platform):
            os.makedirs(GameObj.gd_platform)

        shutil.copy(GameObj.archive_path, System.pkg_dir)
        extract_pkg(GameObj.pkg_path, System.pkg_dir)
        os.remove(GameObj.pkg_path)

        source=GameObj.pkg_dir
        destination=PlatformObj.path

        # for file in glob.glob(GameObj.pkg_dir + '/' + GameObj.slug + '*'):

        print('\nInstalling ' + GameObj.title + ' to ' + PlatformObj.path + '.')

        if PlatformObj.platform_type == 'APP':
            shutil.move(GameObj.pkg_dir, GameObj.game_path)
        elif PlatformObj.platform_type == 'EMU':
            for file in glob.glob(GameObj.pkg_dir + '/*'):
                shutil.copy(file, destination)

### Package game to tar file
def pkg_game():

    if not os.path.exists(System.pkg_dir):
        print('\nCreating package directory...\n')
        os.makedirs(System.pkg_dir)

    ### Check if game is installed
    check_installed()
    if GameObj.installed:

        ### Check if archive dir is attached
        # if not check_archive():
        #     exit()

        ### Check if game package exists
        if os.path.exists(GameObj.archive_path):
            print('\nPackage exists in archive. Overwrite?\n')
            ao_query = input("(y/n): ")

            if ao_query == 'y':
                print('\nOverwriting package.\n')
            else:
                print('\nKeeping package.\n')
                exit()

        print('\nGathering files...\n')
        if os.path.isdir(GameObj.game_path):

            print('\nChecking wine prefix...\n')
            if os.path.exists(GameObj.game_path + '/data/dosdevices'):
                for f in glob.glob(GameObj.game_path + '/data/dosdevices/*'):
                    if not f.endswith('c:'):
                        print('Removing dosdevice ' + os.path.basename(f))
                        os.remove(f)

            shutil.copytree(GameObj.game_path, GameObj.pkg_dir, symlinks=True)
        elif os.path.isfile(GameObj.game_path):
            if not os.path.exists(GameObj.pkg_dir):
                os.makedirs(GameObj.pkg_dir)

            for f in glob.glob(PlatformObj.path + '/' + GameObj.slug +'.*'):
                shutil.copy(f, GameObj.pkg_dir)
        else:
            print('\nThere was a error creating the package.')
            exit()

        if os.path.exists(GameObj.gd_dir):
            shutil.copytree(GameObj.gd_dir, GameObj.pkg_dir + '/files')


        #### Init GameObj.archive_dir
        if not os.path.exists(GameObj.archive_dir):
            os.makedirs(GameObj.archive_dir)

        ## Save game package
        # print('\nCreating package...\n')
        # make_pkg(GameObj.pkg_dir, GameObj.pkg_path)

        # print('\nMoving package to archive...' + GameObj.archive_path +'\n')
        # shutil.move(GameObj.pkg_path, GameObj.archive_path)

        ### Clear GameObj.pkg_dir
        # shutil.rmtree(System.pkg_dir)



        # else:
        #     print('\nArchive not mounted.')
        #     exit()


    else:
        print('\nGame is not installed.\n')
        exit()

### Package save file
def pkg_save():
    game_data_platform = os.path.join(System.game_data, PlatformObj.slug)
    game_data_dir = os.path.join(game_data_platform, GameObj.slug)

    if not os.path.exists(System.game_data):
        os.makedirs(System.game_data)

    if not os.path.exists(game_data_platform):
        os.makedirs(game_data_platform)

    if not os.path.exists(game_data_dir):
        os.makedirs(game_data_dir)

    save_pkg = os.path.join(game_data_dir, 'save.tar.gz')
    game_path = os.path.join(PlatformObj.path, GameObj.path)

    check_installed()

    if GameObj.installed:
        if GameObj.save_path:
            if GameObj.save_path.startswith('[GAMEPATH]'):
                print('\nGameObj.save_path: ' + GameObj.save_path +'\n')
                save_suffix = GameObj.save_path.split("]/",1)[1]
                save_src = os.path.join(game_path, save_suffix)
                save_file = os.path.basename(os.path.realpath(save_src))
                save_parent = os.path.dirname(os.path.realpath(save_src))
                c_save_pkg = subprocess.run(["tar", "cvzf", save_pkg, "-C", save_parent, save_file])

    print(
        '\ngame_path: ' + game_path +'\n'
        'save_pkg: ' + save_pkg +'\n'
        'save_src: ' + save_src +'\n'
        'save_file: ' + save_file +'\n'
        'save_parent: ' + save_parent +'\n'
        )

### Debug report (stdout)
def debug_report():
    print('\n\n'\
        '# DEBUG\n'\
        '-------\n'\

        '\n## GLOBAL\n'\
        'app_dir        : ' + app_dir + '\n'\

        '\n## CONFIG\n'\
        'app_title      : ' + System.app_title + '\n'\
        'files          : ' + System.files + '\n'\
        'l_db_file      : ' + System.l_db_file + '\n'\
        'games_dir      : ' + System.games_dir + '\n'\
        'games_archive  : ' + System.games_archive + '\n'\
        '\n')


## Legacy Game/DB Functions

### Get legacy media art
def game_art(path):
    legacy_media = os.path.join(System.l_files, 'media')
    media = os.path.join(System.game_data)

    if not os.path.exists(legacy_media):
        notification_stdout('Could not find legacy media directory.')
        exit()

    ## Collect game information
    notification_stdout('Collecting information for ' + path)
    for m in game_path_q(path):
        filename = m[33]
        title = m[1]



        slug = get_slug(title)
        
        platform_id = m[37],
        if m[21]:
            boxart = os.path.join(legacy_media, m[21])
        else:
            boxart = ''

        if m[22]:
            display = os.path.join(legacy_media, m[22])
        else:
            display = ''

        if m[23]:
            grid = os.path.join(legacy_media, m[23])
        else:
            grid = ''

        if m[24]:
            icon = os.path.join(legacy_media, m[24])
        else:
            icon = ''

        if m[25]:
            screenshot = os.path.join(legacy_media, m[25])
        else:
            screenshot = ''

        if m[26]:
            logo = os.path.join(legacy_media, m[26])
        else:
            logo = ''

        if m[27]:
            wallpaper = os.path.join(legacy_media, m[27])
        else:
            wallpaper = ''

        if m[20]:
            manual = os.path.join(legacy_media, m[20])
        else:
            manual = ''

        platform_q = []
        platform_q = [platform_id_q(str(platform_id[0]))]

        for p in platform_q:
            platform_slug = p[1]
            platform_name = p[2]
            platform_type = p[3]

        game_data_platform = os.path.join(media, platform_slug)
        game_data_dir = os.path.join(game_data_platform, slug)
        game_data_img = os.path.join(game_data_dir, 'img')
        game_data_docs = os.path.join(game_data_dir, 'docs')

        ## Copy Images
        notification_stdout('Copying images...')
        if not os.path.exists(game_data_img):
            notification_stdout('Creating game data img directory.')
            os.makedirs(game_data_img)

        if os.path.exists(boxart):
            shutil.copy(boxart, game_data_img + '/boxart.jpg')
        if os.path.exists(display):
            shutil.copy(display, game_data_img + '/display.png')
        if os.path.exists(grid):
            shutil.copy(grid, game_data_img + '/grid.jpg')
        if os.path.exists(icon):
            shutil.copy(icon, game_data_img + '/icon.png')
        if os.path.exists(screenshot):
            shutil.copy(screenshot, game_data_img + '/screenshot.jpg')
        if os.path.exists(logo):
            shutil.copy(logo, game_data_img + '/logo.png')
        if os.path.exists(wallpaper):
            shutil.copy(wallpaper, game_data_img + '/background.jpg')

        ## Copy Manual
        if os.path.exists(manual):
            notification_stdout('Copying manual ...')
            if not os.path.exists(game_data_docs):
                os.makedirs(game_data_docs)
            shutil.copy(manual, game_data_docs + '/Manual.pdf')

        notification_stdout('Media collection complete.')

### Query game by path
def game_path_q(path):
    try:
        legacy_db.cursor.execute('SELECT * FROM games_game WHERE path = "' + path + '"')
        result = legacy_db.cursor.fetchall()
    except sqlite3.DatabaseError as err:
        notification_stdout('Game query error.')
        notification_stdout(str(err))
        exit()
    return result

### Query platform by id
def platform_id_q(platform_id):
    try:
        legacy_db.cursor.execute('SELECT id, slug, name, platform_type FROM games_platform WHERE id = ' + platform_id)
        result = legacy_db.cursor.fetchone()
        print(str(result))
    except sqlite3.DatabaseError as err:
        notification_stdout('Platform query error.')
        notification_stdout(str(err))
        exit()
    return result

### Import data from yaml file into database
def import_yml(yml_file):
    ### Get data from file
    with open(yml_file, 'r') as f:
        try:
            yaml_data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            notification_stdout(exc)
    y = yaml_data[0]
    
    ### Get keys/values
    keys = []
    for k in y.keys():
        keys += [k]

    values = []
    for v in y.values():
        values += [v]

    # ## DEBUG
    # notification_stdout('values: ' + str(values))

    sql = ''' INSERT INTO games(
        id,
        filename,
        steam_id,
        title,
        alt_title,
        description,
        collection_id,
        archived,
        notes,
        platform_id,
        genre_id,
        developer,
        publisher,
        release_date,
        region,
        esrb,
        translation,
        store,
        players,
        controller_support,
        co_op,
        online,
        operating_system,
        processor,
        ram,
        hdd,
        gpu,
        save_path,
        engine,
        date_added,
        date_modified
        )VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

    try:
        new_db.cursor.execute(sql, values)
        new_db.connection.commit()
        notification_stdout(values[3] + ' successfully added to database.')
    except sqlite3.DatabaseError as err:
        notification_stdout('Error adding game.')
        notification_stdout(str(err))

### Get legacy game data by filename.
def game_data(path):
    ### Exit if query fails
    if not game_path_q(path):
        notification_stdout('File not found in legacy database.')
        exit()

    ### Assign game data to array
    games = []
    for row in game_path_q(path):

        ### Get year from release date
        rdate = row[9]
        year = datetime.strptime(rdate, '%Y-%m-%d').year

        ### Format `players` field as integer
        if row[17]:
            players = int(row[17])
        else:
            players = 1

        games.append({
            ### Game
            'id': row[0],
            'filename': row[33],
            'steam_id' : row[29],
            'title': row[1],
            'alt_title': row[38],
            'description': row[3],
            'collection_id' : row[35],
            'archived' : row[34],
            'notes' : row[32],
            ### Release
            'platform_id' : row[37],
            'genre_id' : row[36],
            'developer': row[4],
            'publisher': row[5],
            'release_date': year,
            'region': row[7],
            'esrb': row[6],
            'translation': row[8],
            'store': row[10],
            ### User Interface
            'players' : players,
            'controller_support': row[11],
            'co_op' : row[18],
            'online' : row[19],
            ### PC
            'operating_system': row[12],
            'processor' : row[13],
            'ram' : row[14],
            'hdd' : row[15],
            'gpu' : row[16],
            'save_path' : row[39],
            'engine' : row[40],
            ### DateTime
            'date_added' : row[30],
            'date_modified' : row[31],
            })
    
    platform_id_q(str(row[37]))
    platform_q = [platform_id_q(str(row[37]))]
    for p in platform_q:
        platform_slug = p[1]
        

    filename = row[33]
    title = row[1]
    slug = get_slug(title)

    game_data_dir = os.path.join(System.game_data)
    game_data_platform = os.path.join(game_data_dir, platform_slug)
    game_data_slug = os.path.join(game_data_platform, slug)
    # game_data_docs = os.path.join(game_data_slug, 'docs')
    yml_file = os.path.join(game_data_slug, 'info.yml')

    if not os.path.exists(game_data_slug):
        os.makedirs(game_data_slug)

    with open(yml_file, 'w', encoding='utf-8') as f:
        yaml.dump(games, f, sort_keys=False)

    print('game_data_dir: ' + game_data_dir)
    print('game_data_platform: ' + game_data_platform)
    print('game_data_slug: ' + game_data_slug)

    game_art(path)
    import_yml(yml_file)
    os.remove(yml_file)

### Get slug
def get_slug(title):
    if title.startswith("The ") or title.startswith("A "):
        title_split = title.split(" ", 1)
        title_prefix = title_split[0]
        title_string = title_split[1]
    else:
        title_string = title

    slug = slugify(title_string, max_length=64, word_boundary=True)
    return slug

### Fix Windows path names
def fix_paths():
    try:
        legacy_db.cursor.execute('SELECT path, steam_id FROM games_game WHERE steam_id')
        result = legacy_db.cursor.fetchall()
    except sqlite3.DatabaseError as err:
        notification_stdout('Game query error.')
        notification_stdout(str(err))
        exit()

    for r in result:
        path = r[0]
        steam_id = r[1]

        


        sql = 'UPDATE games_game \
        SET path = "' + str(steam_id) +'" \
        WHERE path = "' + path + '"'

        print('\n\
            path: ' + path + '\n\
            steam_id: ' + str(steam_id) + '\n\
            sql: ' + str(sql) + '\n\
            ')

        try:
            legacy_db.cursor.execute(sql)
            legacy_db.connection.commit()
        except sqlite3.DatabaseError as err:
            notification_stdout('Fix path error.')
            notification_stdout(str(err))
            exit()

### Batch
def batch():
    try:
        # legacy_db.cursor.execute('SELECT id, path FROM games_game WHERE 1 ORDER BY id')
        legacy_db.cursor.execute('SELECT id, path FROM games_game WHERE 1 ORDER BY id LIMIT 100')
        result = legacy_db.cursor.fetchall()
    except sqlite3.DatabaseError as err:
        notification_stdout('Game query error.')
        notification_stdout(str(err))
        exit()

    for r in result:
        path = r[1]
        print('path: ' + path)
        game_data(path)






# legacy_db.connection.commit()
# legacy_db.connection.close()