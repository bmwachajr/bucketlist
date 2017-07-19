from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import environment_configuration

# set application environment
environment = 'development'

# create the flask application
app = Flask(__name__)
app.config.from_object(environment_configuration[environment])
db = SQLAlchemy(app)


from application import views, models
