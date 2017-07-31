import json
from .tests import BaseTest


class BucketlistTestCase(BaseTest):

    def Setup(self):
        pass

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
        pass

    def test_get_bucketlists(self):
        """ test get all bucketlists of a user """
        pass

    def test_get_bucketlist(self):
        """ test get specific bucketlist """
        pass

    def test_update_bucketlist(self):
        """: test edit and update a specific bucketlist """
        pass

    def test_delete_bucketlists(self):
        """ test deletion of a specific bucketlist """
        pass
