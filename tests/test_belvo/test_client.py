"""Tests for the Client class for Belvo."""

import pytest
from src.belvo.client import Client
from src.belvo.exceptions import BelvoException


@pytest.fixture
def mock_login_success(responses, fake_url):
    """Mock a successful login for API."""
    responses.add(responses.GET, f"{fake_url}/api/", json={}, status=200)
    yield


@pytest.mark.usefixtures("mock_login_success")
def test_client_instance_creation():
    """Test Client instance creation."""
    try:
        client = Client(
            secret_key_id="y", secret_key_password="z", url="http://fake.url"
        )
        assert isinstance(client, Client)
    except Exception as e:
        pytest.fail(f"Unexpected error occurred: {e}")


@pytest.mark.usefixtures("unauthorized_response")
def test_client_will_raise_exception_when_login_has_failed():
    """Test Client raises exception when login has failed."""
    with pytest.raises(BelvoException) as exc:
        Client(
            secret_key_id="a", secret_key_password="b", url="http://fake.url"
        )

    assert str(exc.value) == "Login failed."


@pytest.mark.usefixtures("authorized_response")
@pytest.mark.parametrize(
    "resource_name",
    [
        "Links",
        "Owners",
    ],
)
def test_client_resources_uses_same_session_as_client(resource_name):
    """Test Client resources uses same session as Client."""
    client = Client(
        secret_key_id="y", secret_key_password="z", url="http://fake.url"
    )

    assert client.session is getattr(client, resource_name).session
