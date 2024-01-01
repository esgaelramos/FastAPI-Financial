"""Tests for Schemas Validating User Data."""

import pytest
from src.schemas.user_schema import UserRequest, UserResponse


def test_user_request_validation():
    """Test the UserRequest Class.

    It should validate the user data input.
    - Check for the valid data
    - Check for the invalid email
    """
    data = {
        "username": "user",
        "email": "user@example.com",
        "password": "secure_password",
    }
    user_request = UserRequest(**data)
    assert user_request.username == data["username"]
    assert user_request.email == data["email"]
    assert user_request.password == data["password"]

    # Check for the invalid email
    with pytest.raises(ValueError):
        UserRequest(
            username="user", email="invalid_email", password="secure_password"
        )


def test_user_response_validation():
    """Test the UserResponse Class.

    It should validate the user data output.
    - Check for the valid data
    """
    data = {
        "id": 1,
        "username": "user",
        "email": "user@example.com",
    }
    user_response = UserResponse(**data)
    assert user_response.id == data["id"]
    assert user_response.username == data["username"]
    assert user_response.email == data["email"]
