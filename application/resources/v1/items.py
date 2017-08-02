from application.mixins import ResourceMixins
from application.models import Item, Bucketlist
from datetime import datetime


class Items(ResourceMixins):
    @ResourceMixins.authenticate
    def post(self, user, id):
        """ create a new item in bucketlist.id """
        # search for bucketlist
        bucketlist = Bucketlist.query.filter_by(id=id, created_by=user.email).first()

        # return 400 if bucketlist non exixtant or not belongs to this user
        if bucketlist is None:
            return 'Bucketlist not found', 202

        if 'description' not in self.request.form:
            return "Item not created", 202

        # parse and validate form data
        item_description = self.request.form['description']

        if not item_description:
            return "Item decription cannot be empty", 401

        # Create item and save in database
        item = Item(description=item_description, date_created=datetime.utcnow(), bucketlist=bucketlist)
        item.save()

        return "Successfully created item", 201




class ItemResource(ResourceMixins):
    pass
