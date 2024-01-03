"""Tests for Class Auth Core in Module."""

from datetime import datetime, timedelta

from src.core.auth import AuthHandler


def test_password_hashing():
    """Test to password hashing."""
    auth = AuthHandler()
    password = "password_to_hash"
    hashed_password = auth.get_password_hash(password)

    assert auth.verify_password(password, hashed_password)


def test_jwt_token_creation_and_decoding():
    """Test to JWT token creation and decoding."""
    auth = AuthHandler()
    data = {"user_data": "value_data"}
    token = auth.create_access_token(data)

    decoded_data = auth.decode_access_token(token)

    assert decoded_data["user_data"] == "value_data"
    assert datetime.fromtimestamp(decoded_data["exp"]) \
        - datetime.utcnow() <= timedelta(minutes=30)


def test_jwt_token_raise_jwt_error():
    """Test to JWT token raise JWTError."""
    auth = AuthHandler()
    data = {"user_data": "value_data"}
    token = auth.create_access_token(data)

    decoded_data = auth.decode_access_token(token + "invalid")

    assert decoded_data is None
