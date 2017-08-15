from application.mixins import ResourceMixins
from application.models import Bucketlist
from datetime import datetime


class Bucketlists(ResourceMixins):
    @ResourceMixins.authenticate
    def post(self, user):
        """ API Endpoint to create a new Bucletlist 
        ---
        tags:
          - Bucketlists
        parameters:
          - name: name
            description: the name or short description of a new bucketlist
            in: formData
            type: string
            required: true

          - name: auth_token
            description: Authentication token
            in: header
            type: string
            required: true
        """
        # parse request data
        bucketlist_name = self.request.form['name']

        # validate bucketlist
        if not bucketlist_name:
            return "Name cannot be empty", 401

        # create bucketlist and save bucketlist
        bucketlist = Bucketlist(name=bucketlist_name, date_created=datetime.utcnow(
        ), created_by=user.username, author=user)
        bucketlist.save()

        return "Successfully created bucketlist", 201

    @ResourceMixins.authenticate
    def get(self, user):
        """ API Endpoint to get all Bucketlists 
        ---
        tags:
          - Bucketlists
        parameters:
          - name: auth_token
            description: Authentication token
            in: header
            type: string
            required: true

          - name: limit
            description: Pagination limit of return bucketlists
            in: query
            type: integer

          - name: page
            description: Page number
            in: query
            type: integer

          - name: q
            description: Search results using keyword
            in: query
            type: string
        """
        search = True if self.request.args.get('q') else False
        limit = int(self.request.args.get('limit')) if self.request.args.get('limit') else 20
        page = int(self.request.args.get('page')) if self.request.args.get('page') else 1
        bucketlists = user.bucketlists.paginate(page, limit, True).items
        bucketlists = user.bucketlists.filter(Bucketlist.name.contains(self.request.args.get('q'))) if self.request.args.get('q') else bucketlists

        bucketlists = [
            {'id': bucketlist.id,
             'name': bucketlist.name,
             'items': [
                 {'id': item.id,
                  'name': item.description,
                  'date_created': str(item.date_created),
                  'date_modified': str(item.date_modified),
                  'done': str(item.is_done)
                  } for item in bucketlist.items
             ],
             'date_created': str(bucketlist.date_created),
             'date_modified': str(bucketlist.date_modified),
             'created_by': bucketlist.created_by
             } for bucketlist in bucketlists
        ]

        # if empty retutn no bucketlists added
        if not bucketlists:
            return "You have no avialable bucketlists", 200

        return bucketlists, 200


class BucketlistResource(ResourceMixins):
    @ResourceMixins.authenticate
    def get(self, user, id):
        """ API Endpoint to get a specific bucketlist
        ---
        tags:
          - Bucketlists
        parameters:
          - name: auth_token
            description: Authentication token
            in: header
            type: string
            required: true

          - name: id
            in: path
            type: int
            required: true
        """
        # Search for bucketlist
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=user.email).first()

        # return 400 if bucketlist non exixtant or not belongs to this user
        if bucketlist is None:
            return 'Bucketlist not found', 202

        # serialize items if ann
        bucketlists_items = [
            {'id': item.id,
             'name': item.description,
             'date_created': str(item.date_created),
             'date_modified': str(item.date_modified),
             'done': str(item.is_done)
             } for item in bucketlist.items
        ]

        # serialize bucketlist
        response_bucketlist = [
            {'id': bucketlist.id,
             'name': bucketlist.name,
             'items': bucketlists_items,
             'date_created': str(bucketlist.date_created),
             'date_modified': str(bucketlist.date_modified),
             'created_by': bucketlist.created_by
             }
        ]

        return response_bucketlist, 200

    @ResourceMixins.authenticate
    def put(self, user, id):
        """ API Endpoint to uodate a bucketlist 
        ---
        tags:
          - Bucketlists
        parameters:
          - name: auth_token
            description: Authentication token
            in: header
            type: string
            required: true

          - name: id
            description: Bucketlist Id
            in: path
            type: integer

          - name: name
            in: formData
            type: string
            required: true
        """
        # parse request data
        if 'name' not in self.request.form:
            return "Bucketlist not Update", 202

        bucketlist_name = self.request.form['name']

        # validate bucketlist
        if not bucketlist_name:
            return "Name cannot be empty", 401

        # search for the bucketlist_id
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=user.email).first()

        # return 400 if bucketlist non exixtant or not belongs to this user
        if bucketlist is None:
            return 'Bucketlist not found', 202

        # Update bucketlist and save changes
        bucketlist.name = bucketlist_name
        bucketlist.save()

        return "Successfully updated bucketlist", 201

    @ResourceMixins.authenticate
    def delete(self, user, id):
        """ API Endpoint to delete a bucletlist
        ---
        tags:
          - Bucketlists
        parameters:
          - name: auth_token
            description: Authentication token
            in: header
            type: string
            required: true

          - name: id
            description: Bucketlist id
            in: path
            type: integer
        """
        # Search for bucketlist
        print (id)
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=user.email).first()

        # return 400 if bucketlist non exixtant or not belongs to this user
        if bucketlist is None:
            return 'Bucketlist not found', 202

        bucketlist.delete()

        return "Successfully deleted bucketlist", 200
