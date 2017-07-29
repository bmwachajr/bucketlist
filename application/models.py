from flask_sqlalchemy import SQLAlchemy
from application import app, db, SECRET_KEY
from sqlalchemy.sql import func
import bcrypt
import jwt
from datetime import datetime, timedelta



class User(db.Model):
    """ Creates users on the system """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String)
    bucketlists = db.relationship('Bucketlist', backref='author', lazy='dynamic')

    def set_password(self, password):
        """ hash and set the new users password """
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.password = hashed_password

    def check_password(self, password):
        """ Check user password at login """
        return True if bcrypt.checkpw(password.encode(), self.password) else False

    def generate_auth(self):
        """ generate authentication token """
        payload = {'id': self.id,
                   'exp': datetime.utcnow() + timedelta(seconds=600),
                   "iat": datetime.utcnow()
                   }

        # encode payload
        auth_token = jwt.encode(payload, SECRET_KEY).decode()
        return auth_token

    def save(self):
        """ Save a user into the database """
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


class Bucketlist(db.Model):
    """ creates bucket lists """

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    created_by = db.Column(db.Integer, db.ForeignKey('users.email'))
    date_created = db.Column(db.DateTime, server_default=func.now())
    date_modified = db.Column(db.DateTime, server_onupdate=func.now())
    items = db.relationship('Item', backref='bucketlist', lazy='dynamic')

    def __repr__(self):
        return '<Bucketlist %r>' % self.title


class Item(db.Model):
    """ Creates bucketlist items """

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    description = db.column(db.String(120))
    is_done = False
    date_created = db.Column(db.DateTime, server_default=func.now())
    date_modified = db.Column(db.DateTime, server_onupdate=func.now())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __repr__(self):
        return '<item %r>' % self.title
