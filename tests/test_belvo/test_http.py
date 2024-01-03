"""Tests for the HTTP module."""

import pytest
from src.belvo.http import APISession


@pytest.mark.parametrize("wrong_http_code", [400, 401, 403, 500])
def test_login_false_whit_bad_response(wrong_http_code, responses, fake_url):
    """Test that login returns False when the response is not 200.

    Args:
        wrong_http_code (int): Wrong HTTP code to test.
        responses (fixture): PyTest responses fixture.
        fake_url (str): Fake URL for the Belvo API.
    """
    responses.add(
        responses.GET, "{}/api/".format(fake_url),
        json={}, status=wrong_http_code
    )
    session = APISession(fake_url)
    result = session.login(secret_key_id="monty", secret_key_password="python")

    assert not result


def test_get_method(responses, fake_url, api_session):
    """Test the get method of the APISession.

    Args:
        responses (fixture): PyTest responses fixture.
        fake_url (str): Fake URL for the Belvo API.
        api_session (fixture): Fake API Session for the Belvo API.
    """
    endpoint = "/api/resource/"
    resource_id = "123"
    resource_url = f"{fake_url}{endpoint}{resource_id}/"
    expected_response = {"id": resource_id, "name": "Test Resource"}

    responses.add(
        responses.GET, resource_url, json=expected_response, status=200
    )
    response = api_session.get(endpoint, resource_id)

    assert response == expected_response


def test_get_yields_results_whit_next_page(responses, fake_url, api_session):
    """Test the get yields results with next page.

    Args:
        responses (fixture): PyTest responses fixture.
        fake_url (str): Fake URL for the Belvo API.
        api_session (fixture): Fake API Session for the Belvo API.
    """
    resource_url = "{}/api/resources/".format(fake_url)
    data = {
        "next": "{}?page=2".format(resource_url),
        "count": 10,
        "results": ["one", "two", "three", "four", "five"],
    }

    resource_url_page_2 = "{}/api/resources/?page=2".format(fake_url)
    data_page_2 = {
        "next": None, "count": 10,
        "results": ["six", "seven", "eight", "nine", "ten"]
    }

    responses.add(
        responses.GET, resource_url, json=data, status=200
    )
    responses.add(
        responses.GET, resource_url_page_2, json=data_page_2, status=200
    )

    results = list(api_session.list("/api/resources/"))

    assert len(results) == 10
    assert results == [
        "one", "two", "three", "four", "five",
        "six", "seven", "eight", "nine", "ten",
    ]


def test_login_sets_correct_user_agent(responses, fake_url):
    """Test that login sets the correct user agent.

    Args:
        responses (fixture): PyTest responses fixture.
        fake_url (str): Fake URL for the Belvo API.
    """
    responses.add(
        responses.GET, "{}/api/".format(fake_url), json={}, status=200
    )
    session = APISession(fake_url)
    session.login(secret_key_id="monty", secret_key_password="python")

    assert session.headers["User-Agent"] == "fapi-financial (2024)"


def test_login_sets_key_id(responses, fake_url):
    """Test that login sets the correct key id.

    Args:
        responses (fixture): PyTest responses fixture.
        fake_url (str): Fake URL for the Belvo API.
    """
    responses.add(
        responses.GET, "{}/api/".format(fake_url), json={}, status=200
    )
    session = APISession(fake_url)
    session.login(secret_key_id="monty", secret_key_password="python")

    assert session.key_id == "monty"
