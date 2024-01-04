"""Tests for Belvo Transactions EndPoints for the FastAPI-Financial app."""

from unittest.mock import Mock, patch

import pytest
from requests import HTTPError
from fastapi.testclient import TestClient
from src.main import app
from src.belvo.client import Client
from src.belvo.http import APISession
from src.core.database import Base, engine
from src.api.v1.endpoints.belvo_transactions import group_mount_transactions

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
            "results": [{"id": "123", "name": "Test Transaction"}],
            "next": None
        }
        mock_get_detail.return_value = {
            "id": "123", "name": "Test Transaction"
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


def test_endpoint_transaction_get_list(mock_belvo_client):
    """Test for getting a list of Belvo Transactions."""
    response = client.get(
        "/v1/belvo/transactions",
        params={"page": 1, "account": "123", "link": "123"}
    )

    assert response.status_code == 200
    assert "transactions" in response.json()["data"]
    assert response.json()["data"]["transactions"][0]["id"] == "123"
    assert response.json()["data"]["transactions"][0]["name"] == \
        "Test Transaction"


def test_endpoint_transaction_get_http_error(mock_belvo_client_with_error):
    """Test for handling HTTPError when getting Belvo Transaction by ID."""
    response = client.get(
        "/v1/belvo/transactions", params={"id": "nonexistent_id"}
    )

    assert response.status_code == 500
    assert "success" in response.json()
    assert not response.json()["success"]
    assert "message" in response.json()
    assert response.json()["message"] == "404: {'error': 'Not found'}"


def test_endpoint_transaction_get_error(mock_belvo_client_with_error):
    """Test for getting Belvo Transaction by ID with error."""
    response = client.get("/v1/belvo/transactions", params={"id": "999"})

    assert response.status_code == 500
    assert "success" in response.json()
    assert not response.json()["success"]
    assert "message" in response.json()


# ### ### ### ###
# Start Tests for the EndPoints Belvo Transactions Group:
# ### ### ### ###


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


# TESTS FOR OUTCOMES ENDPOINT:
def test_endpoint_transactions_outcomes(setup_and_teardown_db, mock_belvo_client):  # noqa: E501
    """Test for getting grouped outcomes of Belvo Transactions Category."""
    response = client.get(
        "/v1/belvo/transactions-outcomes/",
        params={"page": 1, "account": "123", "link": "123"},
        headers={"Authorization": f"Bearer {_obtain_token_from_login()}"}
    )

    assert response.status_code == 200
    assert "transactions_by_category" in response.json()["data"]
    # TODO: Add more asserts!!!


def test_endpoint_incomes_get_http_error(
        setup_and_teardown_db, mock_belvo_client_with_error):
    """Test for handling HTTPError getting grouped outcomes by Category."""
    response = client.get(
        "/v1/belvo/transactions-outcomes/",
        params={"page": 1, "account": "123", "link": "123"},
        headers={"Authorization": f"Bearer {_obtain_token_from_login()}"}
    )

    assert response.status_code == 500
    assert "success" in response.json()
    assert not response.json()["success"]
    assert "message" in response.json()
    assert response.json()["message"] == "404: {'error': 'Not found'}"


# TESTS FOR INCOMES ENDPOINT:
def test_endpoint_transactions_incomes(setup_and_teardown_db, mock_belvo_client):  # noqa: E501
    """Test for getting grouped incomes of Belvo Transactions by category."""
    response = client.get(
        "/v1/belvo/transactions-incomes/",
        params={"page": 1, "account": "123", "link": "123"},
        headers={"Authorization": f"Bearer {_obtain_token_from_login()}"}
    )

    assert response.status_code == 200
    assert "transactions_by_category" in response.json()["data"]
    # TODO: Add more asserts!!!


def test_endpoint_outcomes_get_http_error(
        setup_and_teardown_db, mock_belvo_client_with_error):
    """Test for handling HTTPError when getting grouped incomes by Category."""
    response = client.get(
        "/v1/belvo/transactions-incomes/",
        params={"page": 1, "account": "123", "link": "123"},
        headers={"Authorization": f"Bearer {_obtain_token_from_login()}"}
    )

    assert response.status_code == 500
    assert "success" in response.json()
    assert not response.json()["success"]
    assert "message" in response.json()
    assert response.json()["message"] == "404: {'error': 'Not found'}"


# Test for aux function!
def test_group_mount_transactions():
    """Test for grouping transactions by category."""
    test_transactions = [
        {"type": "OUTFLOW", "category": "Groceries", "amount": 50},
        {"type": "OUTFLOW", "category": "Groceries", "amount": 100},
        {"type": "OUTFLOW", "category": "Utilities", "amount": 75},
        {"type": "INFLOW", "category": "Salary", "amount": 1000},
        {"type": "OUTFLOW", "category": "Entertainment", "amount": 50},
        {"type": "INFLOW", "category": "Investments", "amount": 200},
    ]

    result = group_mount_transactions(test_transactions, "OUTFLOW")

    assert result == {
        "Groceries": 150,
        "Utilities": 75,
        "Entertainment": 50
    }

    result = group_mount_transactions(test_transactions, "INFLOW")

    assert result == {
        "Salary": 1000,
        "Investments": 200
    }
