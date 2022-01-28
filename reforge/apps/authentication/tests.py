from django.test import TestCase
from .ggg_api import GggApi
# Create your tests here.


class ApiTestCase(TestCase):

    def test_api(self):
        api = GggApi()
        api.get_token('8c81ffbc38befb5628fc142d6fefff21bc98651d')
        # api.profile()
