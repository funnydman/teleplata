import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import URL

db = SQLAlchemy()

PROJECT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

STATIC_FOLDER = os.path.join(PROJECT_DIR, 'static')
TEMPLATE_FOLDER = os.path.join(PROJECT_DIR, 'templates')


def create_app():
    app = Flask(__name__, instance_relative_config=True,
                template_folder=TEMPLATE_FOLDER,
                static_folder=STATIC_FOLDER)
    app.config.from_pyfile('config.py', silent=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = URL(**app.config['DATABASE'])

    print(URL(**app.config['DATABASE']))

    db.init_app(app)
    from .models import Samsung

    # from admin import views
    # app.register_blueprint(views.bp_admin)

    from . import views
    app.register_blueprint(views.main)

    return app
