import json
import os
from sezame.store import Store


class File(Store):
    """
    File based store, stores config data, csr and private key
    By default the current directory is used
    """

    def __init__(self, basedir: str = '.'):
        """
        constructor
        :param basedir: the directory for storing the configuration
        """
        self.basedir = basedir.rstrip('/') + '/'
        if not os.path.isdir(self.basedir):
            os.makedirs(self.basedir, 0o700, True)

    def write_config(self, config: dict):
        """
        write config as json string
        :param config:
        :return:
        """
        f = open(self.get_config_filename(), "w")
        json.dump(config, f)
        f.close()

    def read_config(self):
        """
        read config from file and json-decode
        :return: config dictionary
        :rtype: dict
        """
        try:
            f = open(self.get_config_filename(), "r")
            cfg = json.load(f)
            f.close()
            return cfg
        except FileNotFoundError:
            return None

    def write_certificate(self, certificate: str):
        """
        write PEM formatted certificate to file
        :param certificate:
        :return:
        """
        f = open(self.get_certificate_filename(), "w")
        f.write(certificate)
        f.close()

    def read_certificate(self):
        """
        read certificate from file
        :return: PEM formatted certificate string
        """
        try:
            f = open(self.get_certificate_filename(), "r")
            return f.read()
        except FileNotFoundError:
            return None

    def write_private_key(self, private_key: str):
        """
        write private key to file and set permissions accordingly
        :param private_key: PEM formatted private key string
        :return:
        """
        f = open(self.get_private_key_filename(), "w")
        f.write(private_key)
        f.close()
        os.chmod(self.get_private_key_filename(), 0o600)

    def read_private_key(self):
        """
        read private key from file
        :return: PEM formatted private key string
        """
        try:
            f = open(self.get_private_key_filename())
            return f.read()
        except FileNotFoundError:
            return None

    def get_config_filename(self):
        """
        get absolute path to config filename
        :return:
        """
        return self.basedir + 'sezame-cfg.json'

    def get_certificate_filename(self):
        """
        get absolute path to certificate filename
        :return:
        """
        return self.basedir + 'sezame-cert.pem'

    def get_private_key_filename(self):
        """
        get absolute path to private key filename
        :return:
        """
        return self.basedir + 'sezame-key.pem'

    def cleanup(self):
        """
        cleanup after service cancelation, purge all files
        :return:
        """
        super().cleanup()
        if os.path.isfile(self.get_certificate_filename()):
            os.unlink(self.get_certificate_filename())
        if os.path.isfile(self.get_private_key_filename()):
            os.unlink(self.get_private_key_filename())
        if os.path.isfile(self.get_config_filename()):
            os.unlink(self.get_config_filename())
