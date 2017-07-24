from flask_testing import TestCase
from flask import current_app
import nose
from application import app, db
import config


class BaseTest(TestCase):
    def create_app(self):
        app.config.from_object(config.environment_configuration['testing'])
        return app

    def setUp(self):
        """ create test database and client """
        self.client = current_app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()


if __name__ == "__main__":
    nose.run()
