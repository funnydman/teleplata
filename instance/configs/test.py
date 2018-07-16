import os

from sqlalchemy.engine.url import URL

DEBUG = True
TESTING = True

SECRET_KEY = 'test'

PROJECT_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
))
TEST_FOLDER_PATH = os.path.join(PROJECT_DIR, 'tests')

TEST_USERNAME = "TELEPLATA"
TEST_PASSWORD = "TELEPLATA"

DATABASE_NAME = 'postplata.db'

DATABASE_SOURCE = os.path.join(TEST_FOLDER_PATH, DATABASE_NAME)

DATABASE = {'drivername': 'sqlite',
            'database': DATABASE_SOURCE
            }
SQLALCHEMY_DATABASE_URI = URL(**DATABASE)
