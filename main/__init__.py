import os

import click
from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
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


def init_db(app):
    db.init_app(app)


def create_app():
    app = Flask(__name__, instance_relative_config=True,
                template_folder=TEMPLATE_FOLDER,
                static_folder=STATIC_FOLDER)
    app.config.from_pyfile('configs/dev.py')
    app.config.from_pyfile('configs/prod.py', silent=True)

    init_db(app)

    init_views(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        # app.permanent_session_lifetime = timedelta(minutes=5)

    @app.cli.command()
    @click.option('--username', prompt=True, help='username')
    @click.password_option()
    def create_user(username, password):
        if username and password:
            from auth.models import User
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            click.echo(f"User {username} created")
        else:
            click.echo("Enter username and password")

    return app
