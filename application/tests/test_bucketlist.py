import json
from .tests import BaseTest


class BucketlistTestCase(BaseTest):

    def Setup(self):
        pass

    def test_create_bucketlist(self):
        """ test create new bucketlist """
        pass

    def test_unathorized_bucketlist_creation(self):
        """ test creating a bucketlist without being logged in """
        pass

    def test_create_invalid_bucketlist(self):
        """ test creating bucketlist with empty data """
        pass

    def test_get_bucketlists(self):
        """ test get all bucketlists of a user """
        pass

    def test_get_bucketlist(self):
        """ test get specific bucketlist """
        pass

    def test_update_bucketlist(self):
        """: test edit and update a specific bucketlist """
        pass

    def test_delete_bucketlists(self):
        """ test deletion of a specific bucketlist """
        pass
