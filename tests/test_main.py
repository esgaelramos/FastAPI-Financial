"""Tests for Main Module for the FastAPI-Financial application."""

from fastapi.testclient import TestClient
from src.main import app

# Create a test client for our FastAPI application
client = TestClient(app)


def test_hello_world():
    """Test for the root endpoint of the API."""
    response = client.get("/v1/hello-world/")

    assert response.status_code == 200
    assert response.json() == {"from Hello World": "to FastAPI-Financial"}
