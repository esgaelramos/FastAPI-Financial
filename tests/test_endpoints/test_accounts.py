"""Tests for Accounts EndPoints for the FastAPI-Financial application."""

import uuid

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import Base, engine


client = TestClient(app)


@pytest.fixture(scope="function")
def setup_and_teardown_db():
    """Fixture to create and drop database tables."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables
    Base.metadata.drop_all(bind=engine)


def create_test_user():
    """Create a test user."""
    client.post(
        "/v1/auth/register",
        json={
            "username": "testuser", "password": "password",
            "email": "testuser@example.com",
        }
    )


def test_register_user(setup_and_teardown_db):
    """Test to EndPoint `register` for user registration."""
    unique_username = f"user_{uuid.uuid4()}"
    response = client.post(
        "/v1/auth/register",
        json={
            "username": unique_username, "password": "password",
            "email": f"{unique_username}@example.com",
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_user(setup_and_teardown_db):
    """Test to EndPoint `login` for user login."""
    create_test_user()
    response = client.post(
        "/v1/auth/login",
        json={
            "username": "testuser", "password": "password",
            "email": "testuser@example.com"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_token_user(setup_and_teardown_db):
    """Test to EndPoint `token` for user token."""
    create_test_user()
    response = client.post(
        "/v1/auth/token",
        data={"username": "testuser", "password": "password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_and_read_current_user(setup_and_teardown_db):
    """Test to EndPoint `users/me` for read current user."""
    create_test_user()
    login_response = client.post(
        "/v1/auth/login",
        json={
            "username": "testuser", "password": "password",
            "email": "testuser@example.com"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")

    response = client.get(
        "/v1/auth/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "username" in response.json()


def test_need_auth_with_login(setup_and_teardown_db):
    """Test to EndPoint `need-auth` Auth for access to need auth."""
    create_test_user()
    login_response = client.post(
        "/v1/auth/login",
        json={
            "username": "testuser", "password": "password",
            "email": "testuser@example.com"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")

    response = client.get(
        "/v1/auth/need-auth",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "success" in response.json()


def test_need_auth_without_login(setup_and_teardown_db):
    """Test to EndPoint `need-auth` NoAuth for access to need auth."""
    response = client.get("/v1/auth/need-auth")
    expected_json = {'message': 'Not authenticated', 'success': False}

    assert response.status_code == 401
    assert response.json() == expected_json
