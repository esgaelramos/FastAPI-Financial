"""PyTest configuration file for the Belvo Module."""

import pytest
from src.belvo.http import APISession


@pytest.fixture
def fake_url():
    """Fake URL for the Belvo API."""
    yield "http://fake.url"


@pytest.fixture
def api_session(fake_url, authorized_response):
    """Fake API Session for the Belvo API.

    Args:
        fake_url (str): Fake URL for the Belvo API.
        authorized_response (fixture): Fake Authorized Response for Belvo API.
    """
    session = APISession(fake_url)
    session.login(secret_key_id="monty", secret_key_password="python")
    yield session


@pytest.fixture
def authorized_response(responses, fake_url):
    """Fake Authorized Response for the Belvo API.

    Args:
        responses (fixture): PyTest responses fixture.
        fake_url (str): Fake URL for the Belvo API.
    """
    responses.add(
        responses.GET, "{}/api/".format(fake_url), json={}, status=200
    )
    yield


@pytest.fixture
def unauthorized_response(responses, fake_url):
    """Fake Unauthorized Response for the Belvo API.

    Args:
        responses (fixture): PyTest responses fixture.
        fake_url (str): Fake URL for the Belvo API.

    """
    responses.add(
        responses.GET, "{}/api/".format(fake_url),
        json={"detail": "Unauthorized."}, status=401
    )
    yield
