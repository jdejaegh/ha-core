"""The IRCEL - CELINE: Air quality Belgium integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed

from .const import DOMAIN
from .coordinator import IrcelineCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

type IrcelineConfigEntry = ConfigEntry  # noqa: F821


async def async_setup_entry(hass: HomeAssistant, entry: IrcelineConfigEntry) -> bool:
    """Set up IRCEL - CELINE: Air quality Belgium from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = irceline_coordinator = IrcelineCoordinator(
        hass, entry
    )

    try:
        await irceline_coordinator.async_config_entry_first_refresh()
    except UpdateFailed:
        # This should be caught by the config flow anyway
        return False

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: IrcelineConfigEntry) -> bool:
    """Unload a config entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
