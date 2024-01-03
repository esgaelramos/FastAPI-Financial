"""Test exceptions Module."""

from src.belvo.exceptions import BelvoException, RequestError


def test_belvo_exception_initialization():
    """Test BelvoException initialization."""
    message = "Some error occurred"
    error = BelvoException(message)

    assert str(error) == message


def test_request_error_initialization():
    """Test RequestError initialization."""
    status_code = 400
    detail = "Some error occurred"
    error = RequestError(status_code, detail)

    assert error.status_code == status_code
    assert error.detail == detail
    assert str(error) == "(400, 'Some error occurred')"
