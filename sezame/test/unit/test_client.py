import unittest
import sezame.client
import requests
import requests_mock


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.adapter = requests_mock.Adapter()
        self.client = sezame.client.Client(endpoint='mock://hqfrontend-dev.seza.me/')
        self.session = self.client.get_session()
        self.session.mount('mock', self.adapter)

    def test_ping(self):
        self.adapter.register_uri('GET', '/ping', text='boing')
        r = self.client.ping()
        self.assertEqual(r.text, "boing")
