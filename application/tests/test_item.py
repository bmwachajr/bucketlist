import json
import jwt
from datetime import datetime, timedelta
from application import SECRET_KEY
from .tests import BaseTest


class BucketlistTestCase(BaseTest):

    def Setup(self):
        """ setup users to add bucketlists """
        self.user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=self.user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        self.headers = {'auth_token': auth_token}

        self.post_url = '/bucketlists/2/items/'
        self.get_url = '/bucketlists/2/items/1'
        self.delete_url = '/bucketlists/2/items/1'

    def test_create_bucketlist(self):
        """ test create new item """
        form = {'description': 'A skinny deep into the ice waters'}

        # create an item
        response = self.client.post(self.post_url, data=form, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully created item', response.data.decode())
