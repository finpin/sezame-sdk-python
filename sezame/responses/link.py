import requests
import json
from sezame.response import Response


class Link(Response):
    """
    Link/pairing response object
    """

    def __init__(self, r: requests.Response, username):
        super().__init__(r)
        self._data = r.json()
        self._username = username

    def get_id(self):
        """
        get pairing id
        :return:
        """
        return self.data['id']

    def get_clientcode(self):
        """
        get clientcode
        :return:
        """
        return self.data['clientcode']

    def is_duplicate(self) -> bool:
        """
        whether username already has been paired
        :return:
        """
        return self.response.status_code == 409

    def get_qrcode_data(self):
        """
        return qrcode data, this must be used as qr code payload
        :return:
        """
        return json.dumps({
            'id': self.get_id(),
            'username': self._username,
            'client': self.get_clientcode()
        })

    @property
    def data(self):
        return self._data

    @property
    def username(self):
        return self._username


class LinkStatus(Response):
    """
    LinkStatus response object
    """

    def __init__(self, r: requests.Response):
        super().__init__(r)
        self._data = r.json()

    @property
    def data(self):
        return self._data

    def is_linked(self) -> bool:
        return self.data


class LinkDelete(Response):
    """
    LinkDelete response object
    """

    def __init__(self, r: requests.Response):
        super().__init__(r)
