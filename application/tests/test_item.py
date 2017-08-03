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

    def test_invalid_item_creation(self):
            """ test create an item in unauthorized bucketlist """
            user = {'username': 'default_user', 'password': 'password'}
            response = self.client.post('/auth/login', data=user)
            self.assertEqual(response.status_code, 200)

            # extract auth_token
            user_auth = json.loads(response.data)
            auth_token = user_auth['auth_token']
            headers = {'auth_token': auth_token}

            form = {'description': 'A skinny deep into the ice waters'}
            url = '/bucketlists/3/items/'

            # create an item
            post_response = self.client.post(url, data=form, headers=headers)
            self.assertEqual(post_response.status_code, 202)
            self.assertIn('Bucketlist not found', post_response.data.decode())

    def test_invalid_item_data(self):
        """ test creating an item with empty data """
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}

        form = {'description': ''}
        url = '/bucketlists/2/items/'

        # create an item
        post_response = self.client.post(url, data=form, headers=headers)
        self.assertEqual(post_response.status_code, 401)
        self.assertIn('Item decription cannot be empty', post_response.data.decode())

    def test_create_item_with_invalid_form_keys(self):
        """ test creating an item with invalid form keys """
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}

        form = {'invalid_key': 'This ket is invalid. use only description as a valid key'}
        url = '/bucketlists/2/items/'

        # create an item
        post_response = self.client.post(url, data=form, headers=headers)
        self.assertEqual(post_response.status_code, 202)
        self.assertIn('Item not created', post_response.data.decode())

    def test_delete_item_successfully(self):
        """ test delete an item sucessfully"""
        # login default_user
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        url = '/bucketlists/2/items/2'

        # response data
        delete_response = self.client.delete(url, headers=headers)
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn('Successfully deleted item', delete_response.data.decode())

        # Try to redelete the item to check it still exists
        try_response = self.client.delete(url, headers=headers)
        self.assertEqual(try_response.status_code, 202)
        self.assertIn('Item not found', try_response.data.decode())

    def test_delete_nonexistent_item(self):
        """ test delete a non existent item """
        # login default_user
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        url = '/bucketlists/2/items/1'

        # response data
        delete_response = self.client.delete(url, headers=headers)
        self.assertEqual(delete_response.status_code, 202)
        self.assertIn('Item not found', delete_response.data.decode())

    def test_delete_unathorized_item(self):
        """ test delete another users item """
        # login default_user
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        url = '/bucketlists/3/items/3'

        # response data
        delete_response = self.client.delete(url, headers=headers)
        self.assertEqual(delete_response.status_code, 202)
        self.assertIn('Bucketlist', delete_response.data.decode())