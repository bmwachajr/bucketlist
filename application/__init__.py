from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import config
from . import resource_urls

# set application environment
environment = 'development'


# create the flask application
def create_application(environment):
    app = Flask(__name__)
    app.config.from_object(config.environment_configuration[environment])
    return app


app = create_application(environment)
db = SQLAlchemy(app)
api = Api(app=app)


from . import views, models,  resource_urls
resource_urls.load_urls(api)
