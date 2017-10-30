import requests
import json
from sezame.response import Response


class Link(Response):
    def __init__(self, r: requests.Response, username):
        super().__init__(r)
        self._data = r.json()
        self._username = username

    @property
    def data(self):
        return self._data

    @property
    def username(self):
        return self._username

    def get_id(self):
        return self.data['id']

    def get_clientcode(self):
        return self.data['clientcode']

    def is_duplicate(self) -> bool:
        return self.response.status_code == 409

    def get_qrcode_data(self):
        return json.dumps({
            'id': self.get_id(),
            'username': self._username,
            'client': self.get_clientcode()
        })


class LinkStatus(Response):
    def __init__(self, r: requests.Response):
        super().__init__(r)
        self._data = r.json()

    @property
    def data(self):
        return self._data

    def is_linked(self) -> bool:
        return self.data


class LinkDelete(Response):
    def __init__(self, r: requests.Response):
        super().__init__(r)
