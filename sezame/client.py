import requests
import sezame.responses


class Client:
    """
    Sezame client
    """
    def __init__(self, endpoint=None, cert_file=None, private_key_file=None):
        if endpoint is None:
            endpoint = 'https://hqfrontend-finprin.finprin.com/'
        self._endpoint = endpoint
        self._cert_file = cert_file
        self._private_key_file = private_key_file
        self._session = requests.Session()

    def ping(self):
        """
        connectivity test
        :return:
        """
        return self._session.get(self._endpoint + 'ping')

    def get_session(self):
        """
        return the http session
        :return:
        """
        return self._session

    def register(self, email, name):
        """
        start self regoistratin process
        :param email: the recovery e-mail as provided during the mobile app installation
        :param name: the name of your applicatio, e.g. my nice shop
        :return: Register response object
        """
        payload = {'email': email, 'name': name}
        r = self._session.post(self._endpoint + 'client/register', json=payload)
        return sezame.responses.Register(r)

    def sign(self, sharedsecret, csr):
        """
        request a certificate from the hq sever
        :param sharedsecret: sharedsecret obtained by the registration process
        :param csr: PEM formated csr string
        :return: Sign response object
        """
        r = self._session.post(self._endpoint + 'client/sign', json={'sharedsecret': sharedsecret, 'csr': csr})
        return sezame.responses.Sign(r)

    def link(self, username):
        """
        pair user with your application
        :param username: application username
        :return: Link response Object
        """
        r = self._session.post(self._endpoint + 'client/link', cert=(self._cert_file, self._private_key_file),
                               json={'username': username})
        return sezame.responses.Link(r, username)

    def link_status(self, username):
        """
        check pairing status of the given application username
        :param username: application username
        :return: LinkStatus response Object
        """
        r = self._session.post(self._endpoint + 'client/link/status', cert=(self._cert_file, self._private_key_file),
                               json={'username': username})
        return sezame.responses.LinkStatus(r)

    def link_delete(self, username):
        """
        delete pairing
        :param username: application username to be removed
        :return: LinkDelete response Object
        """
        r = self._session.delete(self._endpoint + 'client/link', cert=(self._cert_file, self._private_key_file),
                                 json={'username': username})
        return sezame.responses.LinkDelete(r)

    def auth(self, username, authtype='auth', message=None, timeout=None):
        """
        start authentication request
        :param username: application username to be authenticated
        :param authtype: auth|fraud
        :param message: an optional message, will be displayed on the mobile app
        :param timeout: the timeout in secs
        :return: Auth response Object
        """
        data = {
            'username': username,
            'type': authtype
        }
        if message is not None:
            data['message'] = message

        if timeout is not None:
            data['timeout'] = timeout

        r = self._session.post(self._endpoint + 'auth/login', cert=(self._cert_file, self._private_key_file),
                               json=data)
        return sezame.responses.Auth(r)

    def auth_status(self, auth_id):
        """
        check authentication status of the given auth-id
        :param auth_id: authentication id as returned by the auth request
        :return: AuthStatus response Object
        """
        r = self._session.get(self._endpoint + 'auth/status/' + auth_id, cert=(self._cert_file, self._private_key_file))
        return sezame.responses.AuthStatus(r)

    def cancel(self):
        """
        cancel service, invalidates certificate
        :return: Cancel response Object
        """
        r = self._session.post(self._endpoint + 'client/cancel', cert=(self._cert_file, self._private_key_file))
        return sezame.responses.Cancel(r)

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = value

    @property
    def cert_file(self):
        return self.cert_file

    @cert_file.setter
    def cert_file(self, value):
        self._cert_file = value

    @property
    def private_key_file(self):
        return self._private_key_file

    @private_key_file.setter
    def private_key_file(self, value):
        self._private_key_file = value
