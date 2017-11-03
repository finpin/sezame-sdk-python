from requests import Response as RequestsResponse
from abc import ABCMeta, abstractmethod
import requests


class Response(metaclass=ABCMeta):
    """
    abstract class for all sezame http responses
    """
    def __init__(self, r: RequestsResponse):
        self._response = r

    def is_ok(self) -> bool:
        """
        request was ok
        :return:
        """
        return self.response.ok

    def is_notfound(self) -> bool:
        """
        resource was not found (404)
        :return:
        """
        return self.response.status_code == requests.codes.not_found

    def raise_on_error(self):
        """
        raise exception on error (http status codes indicating an error)
        :return:
        """
        self.response.raise_for_status()

    def get_status_code(self):
        """
        return http status code
        :return:
        """
        return self.response.status_code

    def get_status_message(self):
        """
        return http status message
        :return:
        """
        return self.response.reason

    @property
    def response(self):
        return self._response
