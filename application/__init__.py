from flask import Flask
from sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config')
db = SQLAlchemy(app)

from application import views, models
