from abc import ABCMeta, abstractmethod


class Store(metaclass=ABCMeta):
    """
    abstract class for implementing a Store for retrieving and saving configuration data, certificate and private key
    """

    @abstractmethod
    def read_config(self): pass

    """
    read config should return a config dict containing configuration the data as written by write_config
    """

    @abstractmethod
    def write_config(self, config: dict): pass

    """
    write config to the store, the given dict must be returned as is by the read_config method 
    """

    @abstractmethod
    def read_private_key(self): pass

    """
    read private key, private key must be returned pem formatted and not protected by a password.
    Protecting the key is part of your store implementation
    """

    @abstractmethod
    def write_private_key(self, private_key: str): pass

    """
    write private key to store, private key is pem formatted and must be returned as is by read_private_key.
    Private key protection must be done in your store implementation.
    """

    @abstractmethod
    def get_private_key_filename(self): pass

    """
    return a filename to a file containing the private key, python http requests requires that the private key
    is provided as file
    """

    @abstractmethod
    def read_certificate(self): pass

    """
    read certificate, the certificate must be returned pem formatted.
    """

    @abstractmethod
    def write_certificate(self, certificate: str): pass

    """
    write the pem formatted certificate to your store
    """

    @abstractmethod
    def get_certificate_filename(self): pass

    """
    return a filename to a file containing the certificate, python http requests requires that the certificate
    is provided as file
    """

    @abstractmethod
    def cleanup(self): pass

    """
    cleanup your store, purge configuration data, certificate and private key
    """