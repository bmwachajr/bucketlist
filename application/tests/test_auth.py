import json
from .tests import BaseTest
from application.resources.v1.auth import Login


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

        self.assertIn(test_user['username'], response.data)
        json_output = json.loads(response.data)
        self.assertIn(json_output['message'], "successfully Registered User")

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

        json_output = json.loads(response.data)
        self.assertIn(json_output['message'], 'invalid username or email')

    def test_registration_invalid_keys(self):
        """ test registering a user using invalid keys """
        user = {'key1': "henry",
                'key2': 'password',
                'key3': 'henry@example.com'}

        url = '/auth/register'

        response = self.client.post(url, data=user)
        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        """ Test that a user can login successfully """
        user = {'username': 'test_user', 'password': 'password'}
        url = '/auth/login'

        response = self.client.post(url, data=user)

        # looged in user is redirected to dashboard
        self.assertEqual(response.status_code, 202)
        self.assertEqual(self.client.current_user.username, 'test_user')

    def test_invalid_username_login_attempt(self):
        """ Test user login with invalid username """
        invalid_username = {'username': 'test_user', 'password': 'invalid'}
        url = '/auth/login'

        response = self.client.post(url, data=invalid_username)
        self.assertEqual(response.status_code, 401)  # status code for invalid
        json_output = json.loads(response.data)
        self.assertIn(json_output['message'], 'Invalid username or password')
        self.assertEqual(self.client.current_user, None)

    def test_invalid_password_login_attempt(self):
        """ Test user login with invalid password """
        invalid_password = {'username': 'test_user', 'password': 'invalid'}
        url = '/auth/login'

        response = self.client.post(url, data=invalid_password)
        self.assertEqual(response.status_code, 401)  # status code for invalid
        json_output = json.loads(response.data)
        self.assertIn(json_output['message'], 'Invalid username or password')
        self.assertEqual(self.client.current_user, None)

    def test_user_logout(self):
        """ Test successfull user logout """
        # login user
        user = {'username': 'test_user', 'password': 'password'}
        url = '/auth/login'
        response = self.client.post(url, data=user)
        self.assertEqual(self.client.current_user.username, 'test_user')

        # logout user
        url = '/auth/logout'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.current_user, None)
