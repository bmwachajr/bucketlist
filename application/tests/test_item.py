import json
import jwt
from datetime import datetime, timedelta
from application import SECRET_KEY
from .tests_setup import BaseTest


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

    def test_update_item_successfully(self):
        """ test update an item successfully """
        # login defualt user
        user = {'username': 'default_user', 'password': 'password'}
        login_response = self.client.post('/auth/login', data=user)
        self.assertEqual(login_response.status_code, 200)

        # extract auth token
        user_auth = json.loads(login_response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        update_data = {'description': 'Test item no 2 - completed', 'is_done': True}
        url = '/bucketlists/2/items/2'

        # update an item
        update_response = self.client.put(url, data=update_data, headers=headers)
        self.assertEqual(update_response.status_code, 201)
        self.assertIn('Successfully updated item', update_response.data.decode())

    def test_invalid_item_description_update(self):
        """ test update an item with empty data """
        # login defualt user
        user = {'username': 'default_user', 'password': 'password'}
        login_response = self.client.post('/auth/login', data=user)
        self.assertEqual(login_response.status_code, 200)

        # extract auth token
        user_auth = json.loads(login_response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        update_data = {'description': ''}
        url = '/bucketlists/2/items/2'

        # update an item
        update_response = self.client.put(url, data=update_data, headers=headers)
        self.assertEqual(update_response.status_code, 401)
        self.assertIn('Item decription cannot be empty', update_response.data.decode())

    def test_invalid_item_status_update(self):
        """ test update an item with empty data """
        # login defualt user
        user = {'username': 'default_user', 'password': 'password'}
        login_response = self.client.post('/auth/login', data=user)
        self.assertEqual(login_response.status_code, 200)

        # extract auth token
        user_auth = json.loads(login_response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        update_data = {'is_done': ''}
        url = '/bucketlists/2/items/2'

        # update an item
        update_response = self.client.put(url, data=update_data, headers=headers)
        self.assertEqual(update_response.status_code, 401)
        self.assertIn('is_done cannot be empty', update_response.data.decode())

    def test_update_nonexistent_item(self):
        """ test update a non existent item """
        # login default_user
        user = {'username': 'default_user', 'password': 'password'}
        login_response = self.client.post('/auth/login', data=user)
        self.assertEqual(login_response.status_code, 200)

        # extract auth token
        user_auth = json.loads(login_response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        update_data = {'is_done': 'Non existent item'}
        url = '/bucketlists/2/items/1'

        # update an item
        update_response = self.client.put(url, data=update_data, headers=headers)
        self.assertEqual(update_response.status_code, 202)
        self.assertIn('Item not found', update_response.data.decode())

    def test_update_unauthorized_item(self):
        """ test update another users item """
        # login default_user
        user = {'username': 'default_user', 'password': 'password'}
        login_response = self.client.post('/auth/login', data=user)
        self.assertEqual(login_response.status_code, 200)

        # extract auth token
        user_auth = json.loads(login_response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        update_data = {'is_done': 'Non existent item'}
        url = '/bucketlists/3/items/2'

        # update an item
        update_response = self.client.put(url, data=update_data, headers=headers)
        self.assertEqual(update_response.status_code, 202)
        self.assertIn('Bucketlist not found', update_response.data.decode())

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
        self.assertIn('Bucketlist not found', delete_response.data.decode())