import unittest
from sezame import client, certutil


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = client.Client()

    def tearDown(self):
        self.client.get_session().close()

    def test_ping(self):
        r = self.client.ping()
        self.assertEqual(r.text, "boing")

    def test_register(self):
        data = self.client.register('reg@bretterklieber.com', 'pytest')
        self.assertIn('id', data)
        self.assertIn('clientcode', data)
        self.assertIn('public_key', data)
        self.assertIn('sharedsecret', data)

    def test_sign(self):
        data = {
            'sharedsecret': '42f47b70b6da411ff995f9cadbc7889e28192a9d7594805022cad2bd63d2be3a',
            'id': 'bc160877c778ca58dd6715a9d270f195bbc3401614e6ce33eac056db8687ed49',
            'public_key': '3f996122f799e8a3c93ffb92dccc174f309d2cf63220094db1da2051024ac218',
            'clientcode': '59ea10e5348014.08787350'
        }

        private_key, csr = certutil.CertUtil.make_csr(data['clientcode'], 'reg@bretterklieber.com')
        data = self.client.sign(data['sharedsecret'], csr)
        self.assertIn('cert', data)
        print(data)
