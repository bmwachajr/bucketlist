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
        item = Item(description=item_description, date_created=datetime.utcnow(), bucketlist_id=bucketlist.id, bucketlist=bucketlist)
        item.save()

        return "Successfully created item", 201




class ItemResource(ResourceMixins):
    
    @ResourceMixins.authenticate
    def put(self, user, id, item_id):
        """ update an new item """
        # search for bucketlist
        bucketlist = Bucketlist.query.filter_by(id=id, created_by=user.email).first()

        # return 400 if bucketlist non exixtant or not belongs to this user
        if bucketlist is None:
            return 'Bucketlist not found', 202

        # search for item
        item = Item.query.filter_by(id=item_id, bucketlist=bucketlist).first()

        if not item:
            return "Item not found", 202

        # parse and validate form data
        if 'description' in self.request.form:
            item_description = self.request.form['description']
            if not item_description:
                return "Item decription cannot be empty", 401
            else:
                item.description = item_description

        if 'is_done' in self.request.form:
            item_is_done = self.request.form['is_done']
            if not item_is_done:
                return "is_done cannot be empty", 401
            else:
                item.is_done = item_is_done

        # Save updates in database
        item.save()

        return "Successfully updated item", 201

    @ResourceMixins.authenticate
    def delete(self, user, id, item_id):
        """ delete an item """
        # Search for bucketlist
        bucketlist = Bucketlist.query.filter_by(id=id, created_by=user.email).first()

        # return 202 if bucketlist non exixtant or not belongs to this user
        if bucketlist is None:
            return "Bucketlist not found", 202

        # find the item and return 202 if not found
        item = Item.query.filter_by(id=item_id, bucketlist=bucketlist).first()

        if item is None:
            return "Item not found", 202

        item.delete()

        return "Successfully deleted item", 200
