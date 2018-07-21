import os

from elasticsearch import Elasticsearch
from flask import Flask, session
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
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) or None
    app.path_to_tests = os.path.join(PROJECT_DIR, 'tests')
    init_db(app)
    init_views(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    @app.shell_context_processor
    def shell_context():
        return {'db': db}

    from . import cli
    app.cli.add_command(cli.create_user)
    app.cli.add_command(cli.get_pdf_report)
    app.cli.add_command(cli.drop_db)

    return app
