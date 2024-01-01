"""Tests for the Config Module."""

import unittest
from unittest.mock import patch

from src.core.config import AppConfig


class TestAppConfig(unittest.TestCase):
    """Test the AppConfig class."""

    def setUp(self):
        """Set up the test case."""
        self.app_config = AppConfig()
        self.dictionary_config = {
            'sandbox': {
                'DOMAIN': 'domain.sandbox'
            },
            'dev': {
                'DOMAIN': 'domain.dev'
            },
            'prod': {
                'DOMAIN': 'domain.prod'
            }
        }

    def test_app_config_singleton(self):
        """Test that AppConfig is a singleton."""
        config1 = AppConfig()
        config2 = AppConfig()
        self.assertIs(config1, config2)

    @patch('builtins.open')
    @patch('yaml.safe_load')
    @patch('src.core.config.config')
    def test_app_config_loads_data(self, mock_config, mock_yaml, mock_open):
        """Test that AppConfig loads the configuration data.

        We will check if the config is loaded from the correct
        environment variable. For this test, we will mock the:
        - open function to return a file object
        - yaml.safe_load to return a dictionary
        - config function to return the environment variable
        """
        mock_yaml.return_value = self.dictionary_config

        for environment in ['sandbox', 'dev', 'prod']:
            # Mocking environment variables
            mock_config.side_effect = lambda key, default=None: {
                'APP_ENV': environment,
            }.get(key, default)

            # Reload AppConfig to apply mocks
            AppConfig._instance = None
            app_config = AppConfig()

            # Checking if the config is loaded the environment variable
            self.assertEqual(
                app_config.config.get("DOMAIN"), f'domain.{environment}'
            )
