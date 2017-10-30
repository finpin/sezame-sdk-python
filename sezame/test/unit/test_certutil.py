import unittest
from sezame import certutil


class CertUtilTestCase(unittest.TestCase):
    def test_ping(self):
        private_key, csr = certutil.CertUtil.make_csr('foo', 'foo@bar.com')
        self.assertTrue(private_key.startswith(b'-----BEGIN PRIVATE KEY'))
        self.assertTrue(csr.startswith(b'-----BEGIN CERTIFICATE REQUEST'))
