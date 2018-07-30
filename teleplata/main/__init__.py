import os

from flask import Flask, session, render_template
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from werkzeug.contrib.fixers import ProxyFix

from teleplata.admin.views import admin, MyModelView

try:
    from instance.local_settings import DSN

    sentry = Sentry(dsn=DSN)
except ImportError:
    pass

db = SQLAlchemy()
from teleplata.main.models import Samsung

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

PROJECT_DIR = os.path.dirname(BASE_DIR)

STATIC_FOLDER = os.path.join(PROJECT_DIR, 'static')

TEMPLATE_FOLDER = os.path.join(PROJECT_DIR, 'templates')


def init_views(app):
    from . import views
    app.register_blueprint(views.main)


def init_db(app):
    db.init_app(app)


def create_app():
    app = Flask(__name__, instance_relative_config=True,
                template_folder=TEMPLATE_FOLDER,
                static_folder=STATIC_FOLDER)
    app.config.from_pyfile('configs/dev.py')
    app.config.from_pyfile('configs/prod.py', silent=True)
    app.path_to_tests = os.path.join(BASE_DIR, 'tests')

    init_db(app)
    init_views(app)
    sentry.init_app(app)
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
    app.cli.add_command(cli.users)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('500.html'), 500

    admin.init_app(app)
    admin.add_view(MyModelView(Samsung, db.session))

    return app
