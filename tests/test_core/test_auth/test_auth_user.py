"""Test cases for the Functions: Auth User in the Auth Core Module."""

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from src.models.user import User
from src.core.auth import AuthHandler, authenticate_user


@pytest.fixture
def mock_db_session():
    """Mock DB Session."""
    session = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = None
    return session


@pytest.fixture
def mock_user():
    """Mock User with username and password."""
    user = User(
        username="existing_user",
        hashed_password=AuthHandler().get_password_hash("password")
    )
    return user


def test_authenticate_user_success(mock_db_session, mock_user):
    """Test to authenticate user successfully."""
    mock_db_session.query.return_value.\
        filter.return_value.first.return_value = mock_user

    authenticated_user = authenticate_user(
        "existing_user", "password", mock_db_session
    )
    assert authenticated_user.username == "existing_user"


def test_authenticate_user_failure(mock_db_session):
    """Test to authenticate user failure."""
    mock_db_session.query.return_value.\
        filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        authenticate_user("non_existing_user", "password", mock_db_session)

    assert exc.value.status_code == 401
    assert str(exc.value.detail) == "Incorrect username or password"
