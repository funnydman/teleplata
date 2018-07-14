DEBUG = True
TESTING = False

SECRET_KEY = 'prod'

DATABASE_USER = 'postplata'
DATABASE_PASSWORD = 'FUNNYDMAN'
DATABASE_NAME = 'postplata'
DATABASE_HOST = 'localhost'
DATABASE_POST = 5432

DATABASE = {'drivername': 'postgres',
            'database': DATABASE_NAME,
            'username': DATABASE_USER,
            'password': DATABASE_PASSWORD,
            'host': DATABASE_HOST,
            'port': DATABASE_POST}
