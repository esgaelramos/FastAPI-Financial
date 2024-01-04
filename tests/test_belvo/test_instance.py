"""Tests for the `instance` Module for Injects."""

from unittest.mock import patch

import pytest
from src.belvo.client import Client
from src.belvo.http import APISession
from src.belvo.instance import get_belvo_client


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


def test_belvo_client_instance_creation(mock_belvo_client):
    """Test Belvo Client instance creation."""
    try:
        client = get_belvo_client()
        assert isinstance(client, Client)
    except Exception as e:
        pytest.fail(f"Unexpected error occurred: {e}")
