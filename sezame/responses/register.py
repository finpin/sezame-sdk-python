import requests
from sezame.response import Response


class Register(Response):
    def __init__(self, r: requests.Response):
        super().__init__(r)
        self._data = r.json()

    @property
    def data(self):
        return self._data

    def get_clientcode(self):
        return self.data['clientcode']

    def get_public_key(self):
        return self.data['public_key']

    def get_sharedsecret(self):
        return self.data['sharedsecret']
