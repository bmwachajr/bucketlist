from flask_testing import TestCase
import nose
from application import app, db
import config
from application.models import User


class BaseTest(TestCase):
    def create_app(self):
        app.config.from_object(config.environment_configuration['testing'])
        return app

    def setUp(self):
        """ create test database and client """
        self.client = app.test_client()
        SECRET_KEY = app.config.get("SECRET_KEY")
        db.create_all()

        default_user = User(username="default_user", email="Default@example.com")
        default_user.set_password(password="password")
        db.session.add(default_user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()


if __name__ == "__main__":
    nose.run()
