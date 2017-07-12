from flas import Flask
from flask_sqlalchemy import SQLAlchemy
from application import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.interger, primary_key=True)
    username = db.column(db.String(80), unique=True)
    email = db.column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
