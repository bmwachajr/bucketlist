from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from application import models

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
        duplicate_user = 2#User.query.filter_by(username=username, email=email).first()

        if duplicate_user:
            return "A user with those details already exists", 409

        # create new user
        new_user = User(username=username,
                        email=email,
                        password=password)

        # Save user and return success 201
        #User.save(new_user)

        # Redirect them to success page
        return "successfully added user", 201


class Login(Resource):
    pass
