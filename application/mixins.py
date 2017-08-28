from flask import request
from flask_restful import Resource
from application import app, db, SECRET_KEY
from application.models import User
from functools import wraps
import jwt
from datetime import datetime

class ResourceMixins(Resource):

    def __init__(self):
        super().__init__()
        self.request = request

    @staticmethod
    def authenticate(ViewMethod):
        """ authenticate that token is valid """
        @wraps(ViewMethod)
        def check_token(self,  **kwargs):
            # check if it has an auth token
            if not self.request.headers.get('auth_token'):
                return "Forbidden Access", 401

            auth_token = self.request.headers.get('auth_token')

            # decode authtoken
            try:
             payload = jwt.decode(auth_token, SECRET_KEY, options={'verify_exp':True, 'verify':False})
            except jwt.ExpiredSignatureError:
                return "Please login again", 401
            except jwt.DecodeError:
                return "Request not authenticated", 401

            # rerieve user from database
            user_id = payload['id']
            user = User.query.filter_by(id=payload['id']).first()
            if user:
                return ViewMethod(self, user, **kwargs)
            else:
                return "Forbidden Access", 401
        return check_token
