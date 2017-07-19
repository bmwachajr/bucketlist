from flask_sqlalchemy import SQLAlchemy
from application import app, db


class User(db.Model):
    """ Creates users on the system """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String)
    bucketlists = db.relationship('bucketlist', backref='author', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class bucketlist(db.Model):
    """ creates bucket lists """

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(120))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, description, user_id):
        self.title = title
        self.description - description
        self.created_by = user_id

    def __repr__(self):
        return '<bucketlist %r>' % self.title


class item(db.Model):
    """ Creates bucketlist items """

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.column(db.String(80))
    decsription = db.Column(db.String(120))
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    bucketlist = db.relationship('bucketlists')
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship('User')

    def __init__(self, title, description, bucket_id, user_id):
        self.title = title
        self.description = description
        self.bucket_id = bucket_id
        self.created_by = user_id

    def __repr__(self):
        return '<item %r>' % self.title
