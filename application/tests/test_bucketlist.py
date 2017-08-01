import json, jwt
from datetime import datetime, timedelta
from application import SECRET_KEY
from .tests import BaseTest
from flask import flash


class BucketlistTestCase(BaseTest):

    def Setup(self):
        """ setup users to add bucketlists """
        self.user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        self.headers = {'auth_token': auth_token}

    def test_create_bucketlist(self):
        """ test create new bucketlist """
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        form = {'name': 'Trip to paris'}
        url = '/bucketlists/'

        # create bucket list
        response = self.client.post(url, data=form, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully created bucketlist', response.data.decode())

    def test_unathorized_bucketlist_creation(self):
        """ test creating a bucketlist without being logged in """
        form = {'name': 'bucketlist while not loggedin'}
        url = '/bucketlists/'

        response = self.client.post(url, data=form)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Forbidden Access', response.data.decode())

    def test_create_bucketlist_invalid_token(self):
        """ test create a bucketlist with an invalid token """
        form = {'name': 'Bucketlist invalid token'}
        headers = {'auth_token': ''}
        url = '/bucketlists/'

        # create bucket list
        response = self.client.post(url, data=form, headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Forbidden Access', response.data.decode())

    def test_create_invalid_bucketlist(self):
        """ test creating bucketlist with empty data """
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        form = {'name': ''}
        url = '/bucketlists/'

        # create bucket list
        response = self.client.post(url, data=form, headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Name cannot be empty', response.data.decode())

    def test_unregistered_user_add_bucketlist(self):
        """ test adding a bucketlist by an unregistered user """
        # create a valid token for an unregistered user
        payload = {'id': 50,
                   'exp': datetime.utcnow() + timedelta(seconds=600),
                   "iat": datetime.utcnow()
                   }

        # encode payload and return auth_token
        auth_token = jwt.encode(payload, SECRET_KEY).decode()

        # create forms and headers
        headers = {'auth_token': auth_token}
        form = {'name': ''}
        url = '/bucketlists/'

        # create bucket list
        response = self.client.post(url, data=form, headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Forbidden Access', response.data.decode())

    def test_expired_auth_add_bucketlist(self):
        """ test adding a bucketlist by an unregistered user """
        # create a valid token for an user1
        payload = {'id': 1,
                   'exp': datetime.utcnow() - timedelta(seconds=60),
                   "iat": datetime.utcnow()
                   }

        # encode payload and return auth_token
        auth_token = jwt.encode(payload, SECRET_KEY).decode()

        # create forms and headers
        headers = {'auth_token': auth_token}
        form = {'name': 'Dubai Sky dive'}
        url = '/bucketlists/'

        # create bucket list
        response = self.client.post(url, data=form, headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Please login again', response.data.decode())

    def test_get_bucketlists(self):
        """ test get all bucketlists of a user """
        # login default_user
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        url = '/bucketlists/'

        # get default_user's bucketlists
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Trip to Mombasa', response.data.decode())

    def test_get_bucketlist_successfully(self):
        """ test get specific bucketlist """
        # login default_user
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        url = '/bucketlists/2'

        # response data
        get_response = self.client.get(url, headers=headers)
        self.assertEqual(get_response.status_code, 200)
        self.assertIn('Charity Drive', get_response.data.decode())

    def test_get_unathorized_bucketlist(self):
        """ test get another user bucketlist """
        # login default_user
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        url = '/bucketlists/3'

        # response data
        get_response = self.client.get(url, headers=headers)
        self.assertEqual(get_response.status_code, 204)

    def test_get_invalid_bucketlist(self):
        """ test get invalid bucketlist id  """
        # login default_user
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        url = '/bucketlists/invalid_id'

        # response data
        get_response = self.client.get(url, headers=headers)
        self.assertEqual(get_response.status_code, 204)

    def test_get_nonexistent_bucketlist(self):
        """ test get a non existant bucketlist  """
        # login default_user
        user = {'username': 'default_user', 'password': 'password'}
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)

        # extract auth_token
        user_auth = json.loads(response.data)
        auth_token = user_auth['auth_token']
        headers = {'auth_token': auth_token}
        url = '/bucketlists/10'

        # response data
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 204)

    def test_update_bucketlist(self):
        """ test edit and update a specific bucketlist """
        pass

    def test_delete_bucketlists(self):
        """ test deletion of a specific bucketlist """
        pass
