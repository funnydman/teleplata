import os

import pytest
from alembic.command import upgrade
from alembic.config import Config

from teleplata.main import create_app, db as _db, PROJECT_DIR

ALEMBIC_CONFIG = os.path.join(PROJECT_DIR, 'alembic.ini')


def apply_migrations():
    """Applies all alembic migrations."""
    config = Config(ALEMBIC_CONFIG)
    upgrade(config, 'head')


@pytest.fixture(scope='session')
def app(request):
    app = create_app()
    app.config.from_pyfile('configs/test.py')
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(app.config["DATABASE_SOURCE"]):
        os.unlink(app.config["DATABASE_SOURCE"])

    def teardown():
        _db.drop_all()
        os.unlink(app.config["DATABASE_SOURCE"])

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(client):
    return client.post(
        '/login',
        data={'username': "TELEPLATA", 'password': "TELEPLATA"}
    )
