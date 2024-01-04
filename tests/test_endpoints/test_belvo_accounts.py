"""Tests for Belvo Accounts EndPoints for the FastAPI-Financial application."""

from unittest.mock import Mock, patch

import pytest
from requests import HTTPError
from fastapi.testclient import TestClient
from src.main import app
from src.belvo.client import Client
from src.belvo.http import APISession
from src.core.database import Base, engine

client = TestClient(app)


@pytest.fixture
def mock_belvo_client():
    """Mock for Belvo Client in Tests.

    This mock is used to avoid making requests to the Belvo API.
    Need assign values for the APISession.login and APISession.get methods.
    And also simulate the Client instance, used for inject in EndPoints.
    """
    with patch.object(APISession, 'login', return_value=True), \
         patch.object(APISession, '_get') as mock_get, \
         patch.object(APISession, 'get') as mock_get_detail, \
         patch('src.belvo.instance.get_belvo_client') as mock_client:

        # Config mocks for APISession GET methods
        mock_get.return_value = {
            "results": [{"id": "123", "name": "Test Account"}], "next": None
        }
        mock_get_detail.return_value = {
            "id": "123", "name": "Test Account"
        }

        # Instance fake Client
        mock_client_instance = Client("fake_id", "fake_password", "fake_url")
        mock_client.return_value = mock_client_instance

        yield mock_client_instance


@pytest.fixture
def mock_belvo_client_with_error():
    """Mock for Belvo Client in Tests, raise HTTPError."""
    with patch.object(APISession, 'login', return_value=True), \
            patch.object(APISession, '_get', side_effect=HTTPError(
                response=Mock(status_code=404,
                              json=lambda: {"error": "Not found"})
            )), \
         patch('src.belvo.instance.get_belvo_client') as mock_client:

        mock_client_instance = Client("fake_id", "fake_password", "fake_url")
        mock_client.return_value = mock_client_instance

        yield mock_client_instance


@pytest.fixture(scope="function")
def setup_and_teardown_db():
    """Fixture to create and drop database tables."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables
    Base.metadata.drop_all(bind=engine)


def _create_test_user():
    """Create a test user."""
    client.post(
        "/v1/auth/register",
        json={
            "username": "testuser", "password": "password",
            "email": "testuser@example.com",
        }
    )


def _obtain_token_from_login():
    """Obtain a JWT token from login."""
    _create_test_user()
    response = client.post(
        "/v1/auth/login",
        json={
            "username": "testuser", "password": "password",
            "email": "testuser@example.com",
        }
    )
    return response.json().get("access_token")


# ### ### ### ###
# Start Tests for the `accounts` Module:
# ### ### ### ###


def test_endpoint_account_get_list(setup_and_teardown_db, mock_belvo_client):
    """Test for getting a list of Belvo Accounts."""
    response = client.get(
        "/v1/belvo/accounts",
        headers={"Authorization": f"Bearer {_obtain_token_from_login()}"}
    )

    assert response.status_code == 200
    assert "accounts" in response.json()["data"]
    assert response.json()["data"]["accounts"][0]["id"] == "123"
    assert response.json()["data"]["accounts"][0]["name"] == "Test Account"


def test_endpoint_account_get_specific(
        setup_and_teardown_db, mock_belvo_client):
    """Test for getting a specific Belvo Account by ID."""
    response = client.get(
        "/v1/belvo/accounts", params={"id": "123"},
        headers={"Authorization": f"Bearer {_obtain_token_from_login()}"}
    )

    assert response.status_code == 200
    assert "id" in response.json()["data"]
    assert response.json()["data"]["id"] == "123"
    assert "name" in response.json()["data"]
    assert response.json()["data"]["name"] == "Test Account"


def test_endpoint_account_get_http_error(
        setup_and_teardown_db, mock_belvo_client_with_error):
    """Test for handling HTTPError when getting Belvo Account by ID."""
    response = client.get(
        "/v1/belvo/accounts", params={"id": "noexistent_id"},
        headers={"Authorization": f"Bearer {_obtain_token_from_login()}"}
    )

    assert response.status_code == 500
    assert "success" in response.json()
    assert not response.json()["success"]
    assert "message" in response.json()
    assert response.json()["message"] == "404: {'error': 'Not found'}"


def test_endpoint_account_get_error(
        setup_and_teardown_db, mock_belvo_client_with_error):
    """Test for getting Belvo Account by ID with error."""
    response = client.get(
        "/v1/belvo/accounts", params={"id": "999"},
        headers={"Authorization": f"Bearer {_obtain_token_from_login()}"}
    )

    assert response.status_code == 500
    assert "success" in response.json()
    assert not response.json()["success"]
    assert "message" in response.json()
