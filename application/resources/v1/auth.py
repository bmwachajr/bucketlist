from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from application.models import User

parser = reqparse.RequestParser()


class Register(Resource):
    def post(self):
        """ Register a new user """
        # Parse form data if any
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # validate data
        if not username or not email or not password:
            return "invalid username or email", 400

        # Check for username, email duplicates
        duplicate_user = User.query.filter_by(username=username, email=email).first()

        if duplicate_user:
            return "A user with those details already exists", 409

        # create new user
        new_user = User(username=username, email=email)

        # set new users password
        User.set_password(new_user, password=password)

        # Save user and return success 201
        User.save(new_user)

        # Redirect them to success page
        return "Successfully Registered User", 201


class Login(Resource):
    def post(self):
        """ Loging a registered user """
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # validate form data
        if not username or not password:
            return "Provide both username and password", 401

        # Check that the user is Registered
        user = User.query.filter_by(username=username).first()
        if not user:
            return "Invalid username or password", 401

        #  Check password
        if not user.check_password(password):
            return "Invalid Password", 401
        # generate auth token
        auth_token = user.generate_auth()
        response_dict = {'message': 'Successfully logged in',
                         'user': user.username,
                         'auth_token': auth_token
                         }

        # Return response dict
        return response_dict, 200
