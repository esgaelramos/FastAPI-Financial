"""Tests for Main Module for the FastAPI-Financial application."""

from fastapi.testclient import TestClient
from src.main import app

# Create a test client for our FastAPI application
client = TestClient(app)


def test_hello_world():
    """Test for the hello world endpoint of the API."""
    expected_response = {
        "success": True,
        "data": {"from Hello World": "to FastAPI-Financial"},
        "message": "Successful Request",
    }

    response = client.get("/v1/hello-world/")

    assert response.status_code == 200
    assert response.json() == expected_response


def test_custom_error():
    """Test for the custom error endpoint of the API."""
    expected_response = {
        "success": False,
        "message": "Custom Unexpected Error",
    }

    response = client.get("/v1/custom-error/")

    assert response.status_code == 500
    assert response.json() == expected_response
