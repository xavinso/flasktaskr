import os

# grab the folder were the script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = '}\xfb\t\xb3b\xc1\xc1\x83\xa4\x81~\xd4\x02Jvh\xb4\x18D<\x9b\x93\xd5\x02'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

DEBUG = False
