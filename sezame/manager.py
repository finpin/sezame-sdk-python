import os
from sezame.store import Store
from sezame.client import Client
from sezame.stores import File as FileStore


class Manager:
    def __init__(self, store: Store = None):
        if store is None:
            store = FileStore()

        self._store = store
        self._config = None
        self._private_key = None
        self._certificate = None

    @property
    def store(self):
        return self._store

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def private_key(self):
        return self._private_key

    @private_key.setter
    def private_key(self, value):
        self._private_key = value

    @property
    def certificate(self):
        return self._certificate

    @certificate.setter
    def certificate(self, value):
        self._certificate = value

    def startup(self):
        self.config = self.store.read_config()
        self.private_key = self.store.read_private_key()
        self.certificate = self.store.read_certificate()

    def is_registered(self):
        return isinstance(self.config, dict) and not isinstance(self.private_key, str) and not isinstance(
            self.certificate, str)

    def is_ready(self):
        return isinstance(self.config, dict) and isinstance(self.private_key, str) and isinstance(self.certificate, str)

    def save(self):
        if isinstance(self.config, dict):
            self.store.write_config(self.config)

        if isinstance(self.certificate, str):
            self.store.write_certificate(self.certificate)

        if isinstance(self.private_key, str):
            self.store.write_private_key(self.private_key)

    def cleanup(self):
        self.store.cleanup()

    def get_sharedsecret(self):
        return self.config['sharedsecret']

    def get_clientcode(self):
        return self.config['clientcode']

    # this is the libsodium HQ public key
    def get_public_key(self):
        return self.config['public_key']

    def get_client(self, endpoint=None):
        certfile = self.store.get_certificate_filename()
        if not os.path.isfile(certfile):
            certfile = None

        keyfile = self.store.get_private_key_filename()
        if not os.path.isfile(keyfile):
            keyfile = None

        return Client(endpoint=endpoint, cert_file=certfile, private_key_file=keyfile)
