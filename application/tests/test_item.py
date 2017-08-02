import json
import jwt
from datetime import datetime, timedelta
from application import SECRET_KEY
from .tests import BaseTest


class ItemsTestCase(BaseTest):

    def test_create_item_successfully(self):
        """ test create an item succesfully """
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}

        form = {'description': 'A skinny deep into the ice waters'}
        url = '/bucketlists/2/items/'

        # create an item
        post_response = self.client.post(url, data=form, headers=headers)
        self.assertEqual(post_response.status_code, 201)
        self.assertIn('Successfully created item', post_response.data.decode())
