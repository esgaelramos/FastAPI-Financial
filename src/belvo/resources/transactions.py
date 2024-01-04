"""Resources for Transactions."""

from typing import Generator

from src.belvo.resources.base import Resource


class Transactions(Resource):
    """Class `Transactions` for manage the Belvo API resources."""

    endpoint = "/api/transactions/"

    def list(self, link, **kwargs) -> Generator:
        """List all Transactions for the given Link.

        Args:
            link (str): The ID of the Link to get Transactions for (UUID).

        Returns:
            Generator: A generator object that will yield each Transaction.
        """
        return super().list(link=link, **kwargs)
