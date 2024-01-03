"""Module `http` for manage the HTTP requests."""

from typing import Dict, Generator

from requests import HTTPError, Session


class APISession:
    """Class `APISession` for manage the HTTP requests."""

    _secret_key_id: str
    _secret_key_password: str
    _url: str

    def __init__(self, url: str) -> None:
        """Initialize the session with the Belvo API."""
        self._url = url
        self._session = Session()
        self._session.headers.update({"User-Agent": "fapi-financial (2024)"})

    @property
    def url(self) -> str:
        """Obtain the Belvo API URL."""
        return self._url

    @property
    def key_id(self) -> str:
        """Obtain the secret key id."""
        return self._secret_key_id

    @property
    def session(self) -> Session:
        """Obtain the session."""
        return self._session

    @property
    def headers(self) -> Dict:
        """Obtain the headers of the session."""
        return self.session.headers

    def login(self, secret_key_id: str, secret_key_password: str,
              timeout: int = 5) -> bool:
        """Login into the Belvo API.

        Args:
            secret_key_id (str): Secret key id.
            secret_key_password (str): Secret key password.
            timeout (int, optional): Timeout for the request. Defaults to 5.

        Return:
            bool: True if the login was successful, False otherwise.
        """
        self._secret_key_id = secret_key_id
        self._secret_key_password = secret_key_password
        base_api_url = "{}/api/".format(self.url)
        self._session.auth = (secret_key_id, secret_key_password)

        try:
            request = self.session.get(base_api_url, timeout=timeout)
            request.raise_for_status()
        except HTTPError:
            return False
        return True

    def _get(self, url: str, params: Dict = None) -> Dict:
        """Manage a GET request.

        Internal method for HTTP GET requests.
        Include a timeout and raise an exception if the request fails.

        Args:
            url (str): URL for the request.
            params (Dict, optional): Parameters for the request. Why???

        Returns:
            Dict: Response data.
        """
        if params is None:
            params = {}
        timeout = params.pop("timeout", 5)

        request = self.session.get(url=url, params=params, timeout=timeout)
        request.raise_for_status()

        return request.json()

    def get(self, endpoint: str, id: str, params: Dict = None) -> Dict:
        """Make a GET request to the Belvo API.

        Args:
            endpoint (str): Endpoint for the request.
            id (str): Id for the request.
            params (Dict, optional): Parameters for the request.

        Returns:
            Dict: Response data.
        """
        url = "{}{}{}/".format(self.url, endpoint, id)

        return self._get(url=url, params=params)

    def list(self, endpoint: str, params: Dict = None) -> Generator:
        """Make a GET request to List in the Belvo API.

        Create a generator for the response data.
        While the response has a `next` field, make a new request.
        Util for list all the resources.

        Args:
            endpoint (str): Endpoint for the request.
            params (Dict, optional): Parameters for the request.

        Yields:
            Generator: Response data.
        """
        url = "{}{}".format(self.url, endpoint)
        while True:
            data = self._get(url, params=params)
            for result in data["results"]:
                yield result

            if not data["next"]:
                break

            url = data["next"]
            params = None
