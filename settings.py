import os
import sqlite3
# The prefix that will be used to parse commands.
# It doesn't have to be a single character!
COMMAND_PREFIX = "!!"

# The bot token. Keep this secret!
#BOT_TOKEN = ""
BOT_TOKEN = ""
# The now playing game. Set this to anything false-y ("", None) to disable it
NOW_PLAYING = COMMAND_PREFIX + "ruda - lista komend"

# Base directory. Feel free to use it if you want.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


SETTINGS = {}


WEATHER = "1af25092acbe1e1651a58933ee7cc93b"

# google image
API_KEY = 'AIzaSyDWnpIhshDF3_b-x_rwiQMeqbVdlhh4yyg'  # put your API key here
API_KEY = 'AIzaSyASnIXiREDxjAcRQPlyfp03KJtxR0S8QWA'  # put your API key here
SEARCH_ENGINE_ID = 'fe3e471181dfd0331'  # you also have to generate a search engine token


conn = sqlite3.connect('db.db')
c = conn.cursor()


c.execute('PRAGMA auto_vacuum=1;')
c.execute('PRAGMA journal_mode = WAL;') #MEMORY
c.execute('PRAGMA page_size = '+str(16*1024)+';')
c.execute('PRAGMA synchronous = 1;')
c.execute('PRAGMA temp_store = 2;')
c.execute('PRAGMA locking_mode=NORMAL;')
c.execute('PRAGMA cache_size=10000;')
c.execute('PRAGMA count_changes=OFF;')

#c.execute('CREATE TABLE IF NOT EXISTS auto (x INTEGER PRIMARY KEY, komenda TEXT NOT NULL, czas TEXT, serwer TEXT, kanal TEXT);')

#c.execute('CREATE TABLE IF NOT EXISTS limi (x INTEGER PRIMARY KEY, komenda TEXT NOT NULL, czas TEXT, serwer TEXT, last TEXT DEFAULT 0);')

c.execute('CREATE TABLE IF NOT EXISTS config (x INTEGER PRIMARY KEY, id TEXT NOT NULL, conf TEXT, serwer TEXT);')

c.execute('CREATE TABLE IF NOT EXISTS licz (x INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, odp TEXT);')

c.execute("CREATE TABLE IF NOT EXISTS command ('x' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'cmd' TEXT, 'srv' TEXT, 'txt' TEXT, 'md5' TEXT);")

c.execute("CREATE TABLE IF NOT EXISTS  'msg' ('x' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'msg' TEXT, 'history' TEXT,'chan' TEXT,'autor' INTEGER,'idmsg' INTEGER,'srv' INTEGER,'time' DATETIME, 'edit' TEXT, 'attach' TEXT, 'embed' TEXT);")

c.execute("CREATE TABLE IF NOT EXISTS 'moon' ('x' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'time' TEXT, 'phase' TEXT, 'distance' TEXT);")

c.execute("CREATE TABLE IF NOT EXISTS 'calendar' ('x' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'month' INTEGER, 'day' INTEGER, 'swieto' TEXT, 'przyslowie' TEXT, 'imieniny' TEXT, 'cytat' TEXT);")

c.execute("CREATE TABLE IF NOT EXISTS 'calendar_local' ('x' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'day' INTEGER, 'month' INTEGER, 'server' INTEGER, 'swieto' TEXT);")

c.execute("CREATE TABLE IF NOT EXISTS 'newssub' ('x' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'news' TEXT NOT NULL, 'chan' INTEGER NOT NULL, 'srv' INTEGER NOT NULL);")



DOG_API_URL   = "https://api.thedogapi.com/"
CAT_API_URL   = "https://api.thecatapi.com/"
CAT_API_KEY   = "b99d30de-e4cc-4e5a-980a-370511ff8a8a"; 

SLOWA=[]
SLOW={}


JWST_API = "ae19dd33-d97e-4f0c-8389-3d62251fb918"
