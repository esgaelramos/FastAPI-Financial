"""Test cases for the Functions: Get User in the Auth Core Module."""

from unittest.mock import MagicMock

import pytest
from jose import jwt
from fastapi import HTTPException
from src.models.user import User
from src.core.auth import SECRET_KEY, ALGORITHM, get_current_user


@pytest.fixture
def mock_db_session():
    """Mock DB Session."""
    session = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = None
    return session


@pytest.fixture
def mock_token():
    """Mock Valid Token."""
    payload = {"sub": "existing_user"}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


@pytest.fixture
def mock_user():
    """Mock User with username."""
    return User(username="existing_user")


def test_get_current_user_valid_token(mock_db_session, mock_token, mock_user):
    """Test to get current user with valid token."""
    mock_db_session.query.return_value.\
        filter.return_value.first.return_value = mock_user

    user = get_current_user(mock_token, mock_db_session)

    assert user.username == "existing_user"


def test_get_current_user_payload_not_sub(mock_db_session, mock_token):
    """Test to get current user with valid token but payload not sub."""
    payload = {"username": "existing_user"}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exc:
        get_current_user(token, mock_db_session)

    assert exc.value.status_code == 401
    assert str(exc.value.detail) == "Invalid token"


def test_get_current_user_invalid_token(mock_db_session):
    """Test to get current user with invalid token."""
    with pytest.raises(HTTPException) as exc:
        get_current_user("invalid_token", mock_db_session)

    assert exc.value.status_code == 401
    assert str(exc.value.detail) == "Invalid token"


def test_get_current_user_user_not_found(mock_db_session, mock_token):
    """Test to get current user with valid token but user not found."""
    mock_db_session.query.return_value.\
        filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        get_current_user(mock_token, mock_db_session)

    assert exc.value.status_code == 404
    assert str(exc.value.detail) == "User not found"
