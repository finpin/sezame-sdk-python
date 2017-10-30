import json
import os
from sezame.store import Store


class File(Store):
    def __init__(self, basedir: str = '.'):
        self.basedir = basedir.rstrip('/') + '/'

    def write_config(self, config: dict):
        f = open(self.get_config_filename(), "w")
        json.dump(config, f)
        f.close()

    def read_config(self):
        try:
            f = open(self.get_config_filename(), "r")
            cfg = json.load(f)
            f.close()
            return cfg
        except FileNotFoundError:
            return None

    def write_certificate(self, certificate: str):
        f = open(self.get_certificate_filename(), "w")
        f.write(certificate)
        f.close()

    def read_certificate(self):
        try:
            f = open(self.get_certificate_filename(), "r")
            return f.read()
        except FileNotFoundError:
            return None

    def write_private_key(self, private_key: str):
        f = open(self.get_private_key_filename(), "w")
        f.write(private_key)
        f.close()
        os.chmod(self.get_private_key_filename(), 0o600)

    def read_private_key(self):
        try:
            f = open(self.get_private_key_filename())
            return f.read()
        except FileNotFoundError:
            return None

    def get_config_filename(self):
        return self.basedir + 'sezame-cfg.json'

    def get_certificate_filename(self):
        return self.basedir + 'sezame-cert.pem'

    def get_private_key_filename(self):
        return self.basedir + 'sezame-key.pem'

    def cleanup(self):
        super().cleanup()
        if os.path.isfile(self.get_certificate_filename()):
            os.unlink(self.get_certificate_filename())
        if os.path.isfile(self.get_private_key_filename()):
            os.unlink(self.get_private_key_filename())
        if os.path.isfile(self.get_config_filename()):
            os.unlink(self.get_config_filename())
