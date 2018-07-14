import os

import pytest

from main import create_app, db as _db

TEST_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

TESTDB = 'teleplata_test.db'

TESTDB_PATH = os.path.join(TEST_FOLDER_PATH, TESTDB)

TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH


@pytest.fixture(scope='session')
def app(request):
    app = create_app()
    app.config.from_pyfile('test_config.py')
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=TEST_DATABASE_URI,
        DEBUG=True,
        TESTING=True

    )
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TESTDB_PATH)

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
