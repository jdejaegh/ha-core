"""Config flow for IRCEL - CELINE: Air quality Belgium integration."""

from __future__ import annotations

from datetime import UTC, datetime
import logging
from typing import Any

from open_irceline import IrcelineRioClient, RioFeature
import voluptuous as vol

from homeassistant.components.zone import DOMAIN as ZONE_DOMAIN
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import ATTR_LATITUDE, ATTR_LONGITUDE, CONF_ZONE
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ZONE): EntitySelector(
            EntitySelectorConfig(domain=ZONE_DOMAIN)
        ),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    if (zone := hass.states.get(data[CONF_ZONE])) is None:
        raise UnknownZone

    api_client = IrcelineRioClient(session=async_get_clientsession(hass))

    result = await api_client.get_data(
        datetime.now(UTC),
        [RioFeature.PM10_HMEAN, RioFeature.NO2_HMEAN, RioFeature.O3_HMEAN],
        (zone.attributes[ATTR_LATITUDE], zone.attributes[ATTR_LONGITUDE]),
    )

    if not result:
        raise CannotConnect

    return {"title": zone.name if zone else "IRCEL - CELINE"}


class IrcelineConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for IRCEL - CELINE: Air quality Belgium."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except UnknownZone:
                errors[CONF_ZONE] = "zone_not_exist"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class UnknownZone(HomeAssistantError):
    """Error to the zone does not exist."""
