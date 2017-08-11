from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import config
from config import environment


# create the flask application
def create_application(environment):
    app = Flask(__name__)
    app.config.from_object(config.environment_configuration[environment])
    return app


app = create_application(environment)
db = SQLAlchemy(app)
api = Api(app=app)
SECRET_KEY = app.config.get('SECRET_KEY')

from . import resource_urls, views
resource_urls.load_urls(api)
