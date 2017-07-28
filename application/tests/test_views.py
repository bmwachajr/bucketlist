from .tests import BaseTest


class TestViews(BaseTest):

    def test_index(self):
        """ test the index view """
        url = '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
