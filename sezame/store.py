from abc import ABCMeta, abstractmethod


class Store(metaclass=ABCMeta):

    @abstractmethod
    def read_config(self): pass

    @abstractmethod
    def write_config(self, config: dict): pass

    @abstractmethod
    def read_private_key(self): pass

    @abstractmethod
    def write_private_key(self, private_key: str): pass

    @abstractmethod
    def get_private_key_filename(self): pass

    @abstractmethod
    def read_certificate(self): pass

    @abstractmethod
    def write_certificate(self, certificate: str): pass

    @abstractmethod
    def get_certificate_filename(self): pass

    @abstractmethod
    def cleanup(self): pass
