"""Module `config` for load the application configuration."""

from typing import Dict

import yaml
from decouple import config


class AppConfig:
    """Class `AppConfig` for load the application configuration."""

    _instance = None

    def __new__(cls):
        """Create a new instance of AppConfig.

        Verify if the instance is already created, if not, create a new one.
        If the instance is already created, return the instance.
        """
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Load the application configuration from a YAML file."""
        path_config_yaml = config(
            'PATH_CONFIG_YAML', default='src/core/config.yaml'
        )
        env = config('APP_ENV', default='sandbox')

        with open(path_config_yaml, "r") as file:
            config_data = yaml.safe_load(file)
            self.env_config = config_data.get(env, {})

            for key, value in self.env_config.items():
                self.env_config[key] = config(value, default=value)

    @property
    def config(self) -> Dict[str, str]:
        """Get the application configuration.

        Returns:
            Dict[str, str]: A dictionary with the application configuration.
        """
        return self.env_config


class Settings:
    """Class `Settings` for provide the application configuration."""

    def __init__(self):
        """Init the application configuration."""
        self.app_config = AppConfig().config

    def __getattr__(self, name):  # pragma: no cover
        """Get the application configuration attribute."""
        return self.app_config.get(name, None)

    def __getitem__(self, name):  # pragma: no cover
        """Get the application configuration item."""
        return self.app_config.get(name, None)
