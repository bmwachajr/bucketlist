from flask_restful import Resource
from application.mixins import ResourceMixins
from application.models import Bucketlist


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
        bucketlist = Bucketlist(name=bucketlist_name, created_by=user.username, author=user)
        bucketlist.save()

        return "Successfully created bucketlist", 201

class BucketlistResource(Resource):
    pass
