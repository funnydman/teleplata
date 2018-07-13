import os

from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import URL
from werkzeug.contrib.fixers import ProxyFix

db = SQLAlchemy()

PROJECT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

STATIC_FOLDER = os.path.join(PROJECT_DIR, 'static')
TEMPLATE_FOLDER = os.path.join(PROJECT_DIR, 'templates')


def load_models():
    from . import models


load_models()


def init_views(app):
    from . import views
    app.register_blueprint(views.main)

    from admin import views
    app.register_blueprint(views.bp_admin)

    from auth import views
    app.register_blueprint(views.auth)


def create_app():
    app = Flask(__name__, instance_relative_config=True,
                template_folder=TEMPLATE_FOLDER,
                static_folder=STATIC_FOLDER)
    app.config.from_pyfile('config.py', silent=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = URL(**app.config['DATABASE'])

    db.init_app(app)

    init_views(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        # app.permanent_session_lifetime = timedelta(minutes=5)

    return app
