"""Sensors for pollutants from IRCEL - CELINE."""

import logging

from homeassistant.components import sensor
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTRIBUTION,
    DOMAIN,
    POLLUTANT_TO_FEATURE,
    POLLUTANT_TO_SENSOR_DEVICE_CLASS,
    POLLUTANT_TO_UNIT,
)
from .coordinator import IrcelineCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            IrcelinePollutantRio(coordinator, entry, pollutant)
            for pollutant in POLLUTANT_TO_FEATURE
        ]
    )


class IrcelinePollutantRio(CoordinatorEntity, SensorEntity):
    """Representation of a pollutant sensor with value extracted from the RIO interpolation of IRCELINE."""

    _attr_has_entity_name = True
    _attr_attribution = ATTRIBUTION

    def __init__(
        self, coordinator: IrcelineCoordinator, entry: ConfigEntry, pollutant: str
    ) -> None:
        """Set up the sensor."""
        super().__init__(coordinator)
        SensorEntity.__init__(self)
        self._attr_device_class = POLLUTANT_TO_SENSOR_DEVICE_CLASS[pollutant]
        self._attr_native_unit_of_measurement = POLLUTANT_TO_UNIT[pollutant]
        self._attr_unique_id = f"{entry.entry_id}-{pollutant}"
        self.entity_id = sensor.ENTITY_ID_FORMAT.format(
            f"{str(entry.title).lower()}_{pollutant}"
        )
        self._attr_device_info = coordinator.shared_device_info
        self._attr_translation_key = f"{pollutant}"

    @property
    def native_value(self) -> float | None:
        """Get value of the sensor."""
        return 42.1
