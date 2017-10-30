import requests
from sezame.response import Response


class Auth(Response):
    def __init__(self, r: requests.Response):
        super().__init__(r)
        if r.status_code == requests.codes.ok:
            self._data = r.json()

    @property
    def data(self):
        return self._data

    def get_id(self):
        return self.data['id']

    def get_status(self):
        return self.data['status']

    def is_ok(self) -> bool:
        if not super().is_ok():
            return False

        return self.get_status() == 'initiated'


class AuthStatus(Response):
    def __init__(self, r: requests.Response):
        super().__init__(r)
        self._data = r.json()

    @property
    def data(self):
        return self._data

    def get_status(self):
        if 'status' not in self.data:
            return None
        else:
            return self.data['status']

    def is_authorized(self):
        return self.get_status() == 'authorized'

    def is_denied(self):
        return self.get_status() == 'denied'

    def is_pending(self):
        return self.get_status() == 'pending'
