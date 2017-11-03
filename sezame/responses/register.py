import requests
from sezame.response import Response


class Register(Response):
    """
    Registration response object
    """

    def __init__(self, r: requests.Response):
        super().__init__(r)
        self._data = r.json()

    def get_clientcode(self):
        """
        get clientcode, a unique identifier of your application registration
        must be used in the csr
        :return:
        """
        return self.data['clientcode']

    def get_public_key(self):
        """
        return libsodium public key (hex encoded)
        :return:
        """
        return self.data['public_key']

    def get_sharedsecret(self):
        """
        return sharedsecret which must be used by the sign request
        :return:
        """
        return self.data['sharedsecret']

    @property
    def data(self):
        return self._data
