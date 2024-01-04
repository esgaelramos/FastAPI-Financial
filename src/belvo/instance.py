"""Module to create a Belvo Client instance."""

from src.belvo.client import Client
from src.core.config import Settings


settings = Settings()

belvo_client = Client(
    settings.BELVO_SECRET_ID,
    settings.BELVO_SECRET_PASSWORD,
    settings.BELVO_URL
)


def get_belvo_client():
    """Get Belvo Client instance for Injection."""
    return belvo_client
