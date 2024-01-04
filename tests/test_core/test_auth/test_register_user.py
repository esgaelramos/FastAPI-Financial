"""Tests cases for the Functions: Register User in the Auth Core Module."""

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from src.schemas.user_schema import UserRequest
from src.core.auth import register_new_user


@pytest.fixture
def mock_db_session():
    """Mock DB Session."""
    session = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = None
    return session


def test_register_new_user_success(mock_db_session):
    """Test to register new user successfully."""
    user_data = UserRequest(
        username="new_user", email="new_user@example.com", password="password"
    )
    new_user = register_new_user(user_data, mock_db_session)

    assert new_user.username == user_data.username
    assert new_user.email == user_data.email
    assert mock_db_session.add.called
    assert mock_db_session.commit.called


def test_register_new_user_username_already_exists(mock_db_session):
    """Test to register new user with username already exists."""
    user_data = UserRequest(
        username="existing_user", password="password",
        email="existing_user@example.com"
    )
    mock_db_session.query.return_value.\
        filter.return_value.first.return_value = "existing_user"

    with pytest.raises(HTTPException) as exc:
        register_new_user(user_data, mock_db_session)

    assert exc.value.status_code == 400
    assert str(exc.value.detail) == "Username or email already in use"


def test_register_new_user_email_already_exists(mock_db_session):
    """Test to register new user with email already exists."""
    user_data = UserRequest(
        username="existing_user", password="password",
        email="existing_user@example.com"
    )
    mock_db_session.query.return_value.\
        filter.return_value.first.return_value = "existing_user"

    with pytest.raises(HTTPException) as exc:
        register_new_user(user_data, mock_db_session)

    assert exc.value.status_code == 400
    assert str(exc.value.detail) == "Username or email already in use"


def test_register_new_user_db_error(mock_db_session):
    """Test to handle database error while registering new user."""
    user_data = UserRequest(
        username="new_user", password="password",
        email="new_user@example.com"
    )
    mock_db_session.add.side_effect = Exception("Database error")

    with pytest.raises(HTTPException) as exc:
        register_new_user(user_data, mock_db_session)

    assert exc.value.status_code == 500
    assert str(exc.value.detail) == "Error registering new user"
    assert mock_db_session.rollback.called
