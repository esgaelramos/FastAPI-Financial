"""Module `client` for manage the Belvo API client."""

from src.belvo import resources
from src.belvo.http import APISession
from src.belvo.exceptions import BelvoException


class Client:
    """Class `Client` for connect to the BelvoAPI."""

    def __init__(self, secret_key_id: str,
                 secret_key_password: str, url: str) -> None:
        """Initialize the client with the Belvo API.

        You must provide your `secret_key_id` and `secret_key_password`.
        When creating a new instance of Client, it will automatically perform
        a login and create a `JWTSession` (if the credentials are valid).

        Args:
            secret_key_id (str): Secret key id.
            secret_key_password (str): Secret key password.
            url (str): URL of the environment you want to connect to.

        Raises:
            BelvoException: If the login fails.
        """
        self.session = APISession(url)

        if not self.session.login(secret_key_id, secret_key_password):
            raise BelvoException("Login failed.")

        self._accounts = resources.Accounts(self.session)
        self._links = resources.Links(self.session)
        self._owners = resources.Owners(self.session)
        self._transactions = resources.Transactions(self.session)

    @property
    def Accounts(self):
        """Get the Accounts resource."""
        return self._accounts

    @property
    def Links(self):
        """Get the Links resource."""
        return self._links

    @property
    def Owners(self):
        """Get the Owners resource."""
        return self._owners

    @property
    def Transactions(self):
        """Get the Transactions resource."""
        return self._transactions
