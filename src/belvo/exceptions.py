"""Module `exceptions` for manage custom errors."""

from typing import Any


class BelvoException(Exception):
    """Class for manage Belvo exceptions."""

    ...


class RequestError(BelvoException):
    """Class for manage custom Request errors."""

    def __init__(self, status_code: int, detail: Any):
        """Initialize the RequestError class."""
        self.status_code = status_code
        self.detail = detail
