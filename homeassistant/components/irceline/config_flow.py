"""Config flow for IRCEL - CELINE: Air quality Belgium integration."""

from __future__ import annotations

import logging
from typing import Any

from open_irceline import IrcelineRioClient, RioFeature
import voluptuous as vol

from homeassistant.components.zone import DOMAIN as ZONE_DOMAIN
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import ATTR_LATITUDE, ATTR_LONGITUDE, CONF_ZONE
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig

from .const import DOMAIN
from .utils import get_config_value

_LOGGER = logging.getLogger(__name__)


def get_schema(config_entry: ConfigEntry | None) -> vol.Schema:
    """Get the form schema for the config and option flows."""
    return vol.Schema(
        {
            vol.Required(
                CONF_ZONE,
                default=None
                if config_entry is None
                else get_config_value(config_entry, CONF_ZONE),
            ): EntitySelector(EntitySelectorConfig(domain=ZONE_DOMAIN)),
        }
    )


async def validate_input(
    hass: HomeAssistant, data: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    errors: dict[str, Any] = {}
    info: dict[str, Any] = {}
    if (zone := hass.states.get(data[CONF_ZONE])) is None:
        errors[CONF_ZONE] = "zone_not_exist"
        return info, errors

    api_client = IrcelineRioClient(session=async_get_clientsession(hass))

    try:
        result = await api_client.get_data(
            [RioFeature.PM10_HMEAN, RioFeature.NO2_HMEAN, RioFeature.O3_HMEAN],
            (zone.attributes[ATTR_LATITUDE], zone.attributes[ATTR_LONGITUDE]),
        )
        if not result:
            errors["base"] = "cannot_connect"

    except Exception:
        _LOGGER.exception("Unexpected exception")
        errors["base"] = "unknown"

    info = {"title": zone.name if zone else "IRCEL - CELINE"}
    return info, errors


class IrcelineConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for IRCEL - CELINE: Air quality Belgium."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            info, errors = await validate_input(self.hass, user_input)
            if not errors:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=get_schema(None), errors=errors
        )


class IrcelineOptionFlow(OptionsFlow):
    """Handle an option flow for IRCEL - CELINE: Air quality Belgium."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> ConfigFlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}
        if user_input is not None:
            info, errors = await validate_input(self.hass, user_input)
            if not errors:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="init", errors=errors, data_schema=get_schema(self.config_entry)
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class UnknownZone(HomeAssistantError):
    """Error to the zone does not exist."""
