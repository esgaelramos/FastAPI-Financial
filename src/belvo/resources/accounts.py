"""Resources for Accounts."""

from src.belvo.resources.base import Resource


class Accounts(Resource):
    """Class `Accounts` for manage the Belvo API resources."""

    endpoint = "/api/accounts/"
