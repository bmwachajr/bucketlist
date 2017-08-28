from flask_restful import Api
from application import app
from application.resources.v1.auth import Login, Register
from application.resources.v1.bucketlists import Bucketlists, BucketlistResource
from application.resources.v1.items import Items, ItemResource


def load_urls(api):
    api.add_resource(Login, "/auth/login")
    api.add_resource(Register, "/auth/register")
    api.add_resource(Bucketlists, "/bucketlists/")
    api.add_resource(BucketlistResource, "/bucketlists/<int:id>")
    api.add_resource(Items, "/bucketlists/<int:id>/items/")
    api.add_resource(ItemResource, "/bucketlists/<int:id>/items/<int:item_id>")

@app.errorhandler(404)
def page_not_found(e):
    return "Not found, Please check your request", 404
