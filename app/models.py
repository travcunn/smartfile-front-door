import os

from sqlalchemy.orm import deferred
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(96))
    last_name = db.Column(db.String(72))
    username = db.Column(db.String(80), unique=True)
    __password = deferred(db.Column(db.String(96)))
    api_key = db.Column(db.String(32), unique=True)

    def __init__(self, username):
        self.username = username
        self.api_key = os.urandom(32).encode('hex')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def set_password(self, password):
        """ Sets a new password. """
        self.__password = generate_password_hash(password)

    def check_password(self, password):
        """ Checks a password against the user's password """
        return check_password_hash(self.__password, password)

    def __repr__(self):
        return '<User %r>' % (self.username)
