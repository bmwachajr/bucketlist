from datetime import datetime
from flask_testing import TestCase
import logging
import json
import nose
from application import app, db
import config
from application.models import User, Bucketlist, Item


class BaseTest(TestCase):
    """ This module setsup test udsers, bucketlistsand items used for testing the system """
    def create_app(self):
        """ create the flask application with testing configurations """
        app.config.from_object(config.environment_configuration['testing'])
        return app

    def setUp(self):
        """ create test database and client """
        self.client = app.test_client()
        SECRET_KEY = app.config.get("SECRET_KEY")
        db.create_all()

        default_user = User(username="default_user", email="Default@example.com")
        default_user.set_password(password="password")

        default_user2 = User(username="default_user2", email="Default2@example.com")
        default_user2.set_password(password="password")

        default_user3 = User(username="default_user3", email="Default3@example.com")
        default_user3.set_password(password="password")

        # add test bucketlists
        bucketlist1 = Bucketlist(name="Trip to Mombasa", date_created=datetime.utcnow(), created_by=default_user.username, author=default_user)
        bucketlist2 = Bucketlist(name="Charity Drive", date_created=datetime.utcnow(), created_by=default_user.username, author=default_user)
        bucketlist3 = Bucketlist(name="Dubai sky dive", date_created=datetime.utcnow(), created_by=default_user2.username, author=default_user2)

        # add test items
        item1 = Item(description="Test item no 1", bucketlist_id=bucketlist1.id, bucketlist=bucketlist1)
        item2 = Item(description="Test item no 2", bucketlist_id=bucketlist2.id, bucketlist=bucketlist2)
        item3 = Item(description="Test item no 3", bucketlist_id=bucketlist3.id, bucketlist=bucketlist3)

        db.session.add(default_user)
        db.session.add(default_user2)
        db.session.add(default_user3)
        db.session.add(bucketlist1)
        db.session.add(bucketlist2)
        db.session.add(bucketlist3)
        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.commit()

        # User login
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        self.headers = {'auth_token': auth_token}

    def tearDown(self):
        """ Drop the database after every test """
        db.drop_all()


if __name__ == "__main__":
    nose.run()
