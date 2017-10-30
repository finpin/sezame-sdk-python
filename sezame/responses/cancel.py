import requests
from sezame.response import Response


class Cancel(Response):
    def __init__(self, r: requests.Response):
        super().__init__(r)
