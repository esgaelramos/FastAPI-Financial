"""Tests for Belvo Owners EndPoints for the FastAPI-Financial application."""

from unittest.mock import Mock, patch

import pytest
from requests import HTTPError
from fastapi.testclient import TestClient
from src.main import app
from src.belvo.client import Client
from src.belvo.http import APISession
from src.belvo.instance import get_belvo_client

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
            "results": [{"id": "123", "name": "Test Owner"}], "next": None
        }
        mock_get_detail.return_value = {
            "id": "123", "name": "Test Owner"
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


def test_endpoint_owner_get_list(mock_belvo_client):
    """Test for getting a list of Belvo Owners."""
    response = client.get("/v1/belvo/owners")

    assert response.status_code == 200
    assert "owners" in response.json()["data"]
    assert response.json()["data"]["owners"][0]["id"] == "123"
    assert response.json()["data"]["owners"][0]["name"] == "Test Owner"


def test_endpoint_owner_get_specific(mock_belvo_client):
    """Test for getting a specific Belvo Owner by ID."""
    response = client.get("/v1/belvo/owners", params={"id": "123"})

    assert response.status_code == 200
    assert "id" in response.json()["data"]
    assert response.json()["data"]["id"] == "123"
    assert "name" in response.json()["data"]
    assert response.json()["data"]["name"] == "Test Owner"


def test_endpoint_owner_get_http_error(mock_belvo_client_with_error):
    """Test for handling HTTPError when getting Belvo Owner by ID."""
    response = client.get("/v1/belvo/owners", params={"id": "nonexistent_id"})

    assert response.status_code == 500
    assert "success" in response.json()
    assert not response.json()["success"]
    assert "message" in response.json()
    assert response.json()["message"] == "404: {'error': 'Not found'}"


def test_endpoint_owner_get_error(mock_belvo_client_with_error):
    """Test for getting Belvo Owner by ID with error."""
    response = client.get("/v1/belvo/owners", params={"id": "999"})

    assert response.status_code == 500
    assert "success" in response.json()
    assert not response.json()["success"]
    assert "message" in response.json()


# Tests for the `instance` Module for Injects:
def test_belvo_client_instance_creation(mock_belvo_client):
    """Test Belvo Client instance creation."""
    try:
        client = get_belvo_client()
        assert isinstance(client, Client)
    except Exception as e:
        pytest.fail(f"Unexpected error occurred: {e}")
