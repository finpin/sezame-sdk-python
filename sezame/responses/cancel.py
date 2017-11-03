import requests
from sezame.response import Response


class Cancel(Response):
    """
    Cancel response object
    """
    def __init__(self, r: requests.Response):
        super().__init__(r)
