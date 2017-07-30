import json
from .tests import BaseTest


class AuthTestCase(BaseTest):

    def Setup(self):
        pass

    def test_user_registers_succesfully(self):
        """ Test that a user can register successfully """
        test_user = {
                'username': 'test_user',
                'password': 'password',
                'email': 'test@example.com'}
        url = '/auth/register'

        response = self.client.post(url, data=test_user)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Successfully Registered User", response.data.decode())

    def test_duplicate_user_registration(self):
        """ Test cannot register a duplicate email or useername """
        duplicate_user = {
                'username': 'test_user',
                'password': 'password',
                'email': 'duplicate@example.com'}
        url = '/auth/register'

        response = self.client.post(url, data=duplicate_user)
        self.assertEqual(response.status_code, 201)

        response = self.client.post(url, data=duplicate_user)
        self.assertEqual(response.status_code, 409)



    def test_invalid_user_registration(self):
        """ Test that a user cannot register with invalid email or username """
        # new user with invalid username or email
        invalid_user = {
                'username': '',
                'password': 'password',
                'email': ''}
        url = '/auth/register'

        response = self.client.post(url, data=invalid_user)
        self.assertEqual(response.status_code, 400)
        #self.assertIn(json_output['message'], 'invalid username or email')

    def test_registration_invalid_keys(self):
        """ test registering a user using invalid keys  """
        user = {'key1': "henry",
                'key2': 'password',
                'key3': 'henry@example.com'}

        url = '/auth/register'

        response = self.client.post(url, data=user)
        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        """ Test that a user can login successfully """
        user = {'username': 'default_user', 'password': 'password'}
        url = '/auth/login'

        response = self.client.post(url, data=user)

        # looged in user is redirected to dashboard
        self.assertEqual(response.status_code, 200)
        self.assertTrue('auth_token', response.data.decode())

    def test_login_empty_data(self):
        """ test submitting empty data """
        user = {'username': '', 'password': ''}
        url = '/auth/login'

        response = self.client.post(url, data=user)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Provide both username and password', response.data.decode())

    def test_invalid_username_login_attempt(self):
        """ Test user login with invalid username """
        invalid_username = {'username': 'test_user', 'password': 'invalid'}
        url = '/auth/login'

        response = self.client.post(url, data=invalid_username)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid username or password', response.data.decode())

    def test_invalid_password_login_attempt(self):
        """ Test user login with invalid password """

        invalid_password = {'username': 'default_user', 'password': 'invalid'}
        url = '/auth/login'

        response = self.client.post(url, data=invalid_password)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid Password', response.data.decode())

    def test_user_logout(self):
        """ Test successfull user logout
        # login user
        user = {'username': 'test_user', 'password': 'password'}
        url = '/auth/login'

        response = self.client.post(url, data=user)
        self.assertEqual(self.client.auth_token, None)

        # logout user
        url = '/logout'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.auth_token, None) """

    def test_login_unregistered_user(self):
        """ Test login an unregistered user """
        user = {'username': 'unregistered', 'password': 'password'}
        url = '/auth/login'

        response = self.client.post(url, data=user)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid username or password", response.data.decode())
