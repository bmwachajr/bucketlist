from flask_restful import Api
from application.resources.v1.auth import Login, Register
from application.resources.v1.bucketlists import Bucketlists, BucketlistResource
from application.resources.v1.items import Items, Item


def load_urls(api):
    api.add_resource(Login, "/auth/login")
    api.add_resource(Register, "/auth/register")
    api.add_resource(Bucketlists, "/bucketlists/")
    api.add_resource(BucketlistResource, "/bucketlists/<id>")
    api.add_resource(Items, "/bucketlists/<id>/item")
    api.add_resource(Item, "/bucketlists/<id>/item/<item_id>")
