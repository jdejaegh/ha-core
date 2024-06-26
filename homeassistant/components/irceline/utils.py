"""Functions commonly used in the integration."""

from typing import Any

from homeassistant.config_entries import ConfigEntry


def get_config_value(config_entry: ConfigEntry, key: str) -> Any:
    """Get the value for the given key in the options if available, else get if from the config data."""
    if config_entry.options and key in config_entry.options:
        return config_entry.options[key]
    return config_entry.data[key]
