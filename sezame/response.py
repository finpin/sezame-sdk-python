from requests import Response as RequestsResponse
from abc import ABCMeta, abstractmethod
import requests


class Response(metaclass=ABCMeta):
    def __init__(self, r: RequestsResponse):
        self._response = r

    @property
    def response(self):
        return self._response

    def is_ok(self) -> bool:
        return self.response.ok

    def is_notfound(self) -> bool:
        return self.response.status_code == requests.codes.not_found

    def raise_on_error(self):
        self.response.raise_for_status()

    def get_status_code(self):
        return self.response.status_code

    def get_status_message(self):
        return self.response.reason
