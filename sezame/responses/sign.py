import requests
from sezame.response import Response


class Sign(Response):
    def __init__(self, r: requests.Response):
        super().__init__(r)
        self._data = r.json()

    @property
    def data(self):
        return self._data

    def get_certificate(self):
        return self.data['cert']
