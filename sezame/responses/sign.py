import requests
from sezame.response import Response


class Sign(Response):
    """
    Sign reponse object
    """

    def __init__(self, r: requests.Response):
        super().__init__(r)
        self._data = r.json()

    def get_certificate(self):
        """
        reuturn PEM formatted certificate string
        :return:
        """
        return self.data['cert']

    @property
    def data(self):
        return self._data
