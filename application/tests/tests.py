from flask_testing import TestCase

from application import app, db
import config


class BaseTest(TestCase):
    def create_app(self):
        app.config.from_object(config.environment_configuration['testing'])
        return app

    def setUp(self):
        """ create test database and client """
        self.client = self.app.test_client()
        db.create_all()
        #manage.create()
        print('Created db')
        db.drop_all()
        print('droped bd')
