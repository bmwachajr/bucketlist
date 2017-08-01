from flask_restful import Resource
from application.mixins import ResourceMixins
from application.models import Bucketlist
from datetime import datetime


class Bucketlists(ResourceMixins):
    @ResourceMixins.authenticate
    def post(self, user):
        """ create a new a bucletlist """
        # parse request data
        bucketlist_name = self.request.form['name']

        # validate bucketlist
        if not bucketlist_name:
            return "Name cannot be empty", 401

        # create bucketlist and save bucketlist
        bucketlist = Bucketlist(name=bucketlist_name, date_created=datetime.utcnow(), created_by=user.username, author=user)
        bucketlist.save()

        return "Successfully created bucketlist", 201

    @ResourceMixins.authenticate
    def get(self, user):
        """ Getall created bucketlists """
        bucketlists = [
                        {'id': bucketlist.id,
                         'name': bucketlist.name,
                         'date_created': str(bucketlist.date_created),
                         'date_modified': str(bucketlist.date_modified),
                         'created_by': bucketlist.created_by
                         } for bucketlist in user.bucketlists
        ]

        # if empty retutn no bucketlists added
        if not bucketlists:
            return "You have no avialable bucketlists", 200

        return bucketlists, 200

class BucketlistResource(Resource):
    pass
