"""Module Base for Resources of Belvo API."""

from typing import Dict, Generator

from src.belvo.http import APISession


class Resource:
    """Class `Resource` for manage the Belvo API resources."""

    endpoint: str

    def __init__(self, session: APISession) -> None:
        """Initialize the resource with the Belvo API."""
        self._session = session

    @property
    def session(self) -> APISession:
        """Obtain the session from the APISession."""
        return self._session

    def get(self, id: str, **kwargs) -> Dict:
        """Get the details for a specific object.

        Args:
            id (str): The ID of the item you want to get details for (UUID).

        Returns:
            Dict: The details of the object.
        """
        return self.session.get(self.endpoint, id, params=kwargs)

    def list(self, **kwargs) -> Generator:
        """List all items for the given resource.

        Allow to list all items for a given resource.
        Additionally, you can add filters to your method in order to only
        retrieve results matching your query. If you don't provide any filters,
        we return all items for that resource.

        Example:

        ```python
            # Retrieve all accounts (no filter given)
            accounts = client.Accounts.list()

            # Retrieve accounts for a specific bank
            accounts = client.Accounts.list(institution="erebor_mx_retail")
            # Retrieve all checking accounts with an available balance >= 100
            accounts = client.Accounts.\
                list(type__in="checking", balance_available__gte=100)
        ```

        All allowed filters are listed in our API reference documentation.
        Check for more in: https://developers.belvo.com/reference/listlinks.

        Returns:
            _type_: _description_

        Yields:
            Generator: _description_
        """
        endpoint = self.endpoint
        return self.session.list(endpoint, params=kwargs)
