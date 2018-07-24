from werkzeug.security import generate_password_hash, \
    check_password_hash

from teleplata.main import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = self._set_password(password)

    def _set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username
