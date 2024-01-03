"""Tests for the Resources module."""

import pytest
from src.belvo.http import APISession
from src.belvo.resources.base import Resource


@pytest.fixture
def mock_session(fake_url):
    """Mock a session for API."""
    return APISession(fake_url)


@pytest.fixture
def resource(mock_session):
    """Mock a resource for API."""
    return Resource(mock_session)


def test_resource_get_method(responses, fake_url, resource):
    """Test the get method from the Resource class.

    Args:
        responses (fixture): PyTest responses fixture.
        fake_url (str): Fake URL for the Belvo API.
        resource (fixture): Fake Resource for the Belvo API.
    """
    resource_id = "123"
    resource.endpoint = "/api/resource/"
    resource_url = f"{fake_url}{resource.endpoint}{resource_id}/"
    expected_response = {"id": resource_id, "name": "Test Resource"}

    responses.add(
        responses.GET, resource_url, json=expected_response, status=200
    )

    response = resource.get(resource_id)

    assert response == expected_response


def test_resource_list_method(responses, fake_url, resource):
    """Test the list method from the Resource class.

    Args:
        responses (fixture): PyTest responses fixture.
        fake_url (str): Fake URL for the Belvo API.
        resource (fixture): Fake Resource for the Belvo API.
    """
    resource.endpoint = "/api/resources/"
    resource_url = f"{fake_url}{resource.endpoint}"
    expected_response = [
        {"id": "1", "name": "Resource 1"}, {"id": "2", "name": "Resource 2"}
    ]

    responses.add(
        responses.GET, resource_url, status=200,
        json={"results": expected_response, "next": None}
    )

    results = list(resource.list())

    assert len(results) == 2
    assert results == expected_response
