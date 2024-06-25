"""The IRCEL - CELINE: Air quality Belgium integration."""

from __future__ import annotations

from open_irceline import IrcelineForecastClient, IrcelineRioClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

PLATFORMS: list[Platform] = [Platform.SENSOR]

type IrcelineConfigEntry = ConfigEntry  # noqa: F821


async def async_setup_entry(hass: HomeAssistant, entry: IrcelineConfigEntry) -> bool:
    """Set up IRCEL - CELINE: Air quality Belgium from a config entry."""

    session = async_get_clientsession(hass)

    entry.runtime_data = {
        "rio_client": IrcelineRioClient(session),
        "forecast_client": IrcelineForecastClient(session),
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: IrcelineConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
