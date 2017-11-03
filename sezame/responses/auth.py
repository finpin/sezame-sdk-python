import requests
from sezame.response import Response


class Auth(Response):
    """
    Auth response object
    """

    def __init__(self, r: requests.Response):
        super().__init__(r)
        if r.status_code == requests.codes.ok:
            self._data = r.json()

    def get_id(self):
        """
        return authentication id
        :return:
        """
        return self.data['id']

    def get_status(self):
        """
        return authentication status
        :return:
        """
        return self.data['status']

    def is_ok(self) -> bool:
        """
        checks whether request has succeeded
        :return:
        """
        if not super().is_ok():
            return False

        return self.get_status() == 'initiated'

    @property
    def data(self):
        return self._data


class AuthStatus(Response):
    """
    Auth status object
    """

    def __init__(self, r: requests.Response):
        super().__init__(r)
        self._data = r.json()

    def get_status(self):
        """
        return authentication status
        :return:
        """
        if 'status' not in self.data:
            return None
        else:
            return self.data['status']

    def is_authorized(self):
        """
        whether authentication request has been authorized or not
        :return:
        """
        return self.get_status() == 'authorized'

    def is_denied(self):
        """
        whether authentication request has been denied by user
        :return:
        """
        return self.get_status() == 'denied'

    def is_pending(self):
        """
        whether authentication request is still pending
        :return:
        """
        return self.get_status() == 'pending'

    @property
    def data(self):
        return self._data
