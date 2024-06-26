"""Sensors for pollutants from IRCEL - CELINE."""

from homeassistant.components import sensor
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ATTRIBUTION,
    POLLUTANT_TO_FEATURE,
    POLLUTANT_TO_SENSOR_DEVICE_CLASS,
    POLLUTANT_TO_UNIT,
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        [IrcelinePollutantRio(entry, pollutant) for pollutant in POLLUTANT_TO_FEATURE]
    )


class IrcelinePollutantRio(SensorEntity):
    """Representation of a pollutant sensor with value extracted from the RIO interpolation of IRCELINE."""

    _attr_has_entity_name = True
    _attr_attribution = ATTRIBUTION

    def __init__(self, entry: ConfigEntry, pollutant: str) -> None:
        """Set up the sensor."""
        # super().__init__(coordinator)
        SensorEntity.__init__(self)
        self._attr_device_class = POLLUTANT_TO_SENSOR_DEVICE_CLASS[pollutant]
        self._attr_native_unit_of_measurement = POLLUTANT_TO_UNIT[pollutant]
        self._attr_unique_id = f"{entry.entry_id}-{pollutant}"
        self.entity_id = sensor.ENTITY_ID_FORMAT.format(
            f"{str(entry.title).lower()}_{pollutant}"
        )
        # self._attr_device_info = coordinator.shared_device_info
        self._attr_translation_key = f"{pollutant}"
        # self._attr_icon = POLLEN_TO_ICON_MAP[pollen]

    @property
    def native_value(self) -> float | None:
        """Get value of the sensor."""
        return 42.1
