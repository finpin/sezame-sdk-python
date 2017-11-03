import os
from sezame.store import Store
from sezame.client import Client
from sezame.stores import File as FileStore


class Manager:
    """
    This class helps to manage the sezame client configuration.
    By default the manager uses a Filestore to save configuration files, certificate and private key, this could
    be any other Store implementing the Store interface.
    """

    def __init__(self, store: Store = None):
        if store is None:
            store = FileStore()

        self._store = store
        self._config = None
        self._private_key = None
        self._certificate = None

    def startup(self):
        """
        read config, certificate and private key from store
        :return:
        """
        self.config = self.store.read_config()
        self.private_key = self.store.read_private_key()
        self.certificate = self.store.read_certificate()

    def state(self):
        """
        return functional state
        :return:
        """
        if isinstance(self.config, dict) and isinstance(self.private_key, str) and isinstance(self.certificate, str):
            return 'ready'

        if isinstance(self.config, dict) and not isinstance(self.private_key, str) and not isinstance(self.certificate,
                                                                                                      str):
            return 'setup'

        return 'new'

    def is_ready(self):
        """
        sezame client is fully functional
        """
        return self.state() == 'ready'

    def is_setup(self):
        """
        checks whether sezame client is in registration state, registration is not fully completed
        :return:
        """
        return self.state() == 'register'

    def is_new(self):
        """
        sezame client just has been installed or cleaned up, no config, no certificate
        :return:
        """
        return self.state() == 'new'

    def save(self):
        """
        save configuration, certificate and private key to store
        :return:
        """
        if isinstance(self.config, dict):
            self.store.write_config(self.config)

        if isinstance(self.certificate, str):
            self.store.write_certificate(self.certificate)

        if isinstance(self.private_key, str):
            self.store.write_private_key(self.private_key)

    def cleanup(self):
        """
        cleanup configuration data and certificate
        :return:
        """
        self.store.cleanup()

    def get_sharedsecret(self):
        """
        return sharedsecret from config
        :return:
        """
        return self.config['sharedsecret']

    def get_clientcode(self):
        """
        return clientcode from config
        :return:
        """
        return self.config['clientcode']

    def get_public_key(self):
        """
        libsodium public key hex encoded
        :return:
        """
        return self.config['public_key']

    def get_client(self, endpoint=None):
        """
        return new sezame client, configure certificate and private key if present
        :param endpoint:
        :return:
        """
        certfile = self.store.get_certificate_filename()
        if not os.path.isfile(certfile):
            certfile = None

        keyfile = self.store.get_private_key_filename()
        if not os.path.isfile(keyfile):
            keyfile = None

        return Client(endpoint=endpoint, cert_file=certfile, private_key_file=keyfile)

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
