"""Sensors for pollutants from IRCEL - CELINE."""

from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
from datetime import date, timedelta
from itertools import product
import logging
from typing import Any

from homeassistant.components import sensor
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTRIBUTION,
    DOMAIN,
    FORECAST_POLLUTANT,
    POLLUTANT_TO_FEATURE,
    POLLUTANT_TO_SENSOR_DEVICE_CLASS,
    POLLUTANT_TO_UNIT,
    RIO_HOURLY_POLLUTANT,
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
            for pollutant in RIO_HOURLY_POLLUTANT
        ]
    )

    async_add_entities(
        [
            IrcelinePollutantForecast(coordinator, entry, pollutant, timedelta(days=d))
            for pollutant, d in product(FORECAST_POLLUTANT, range(4))
        ]
    )


class IrcelinePollutantSensor(CoordinatorEntity, SensorEntity, metaclass=ABCMeta):
    """Abstract base class for other pollutant sensors from IRCELINE."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(self, coordinator: IrcelineCoordinator, pollutant: str) -> None:
        """Set up the sensor."""
        super().__init__(coordinator)
        SensorEntity.__init__(self)
        self._attr_device_class = POLLUTANT_TO_SENSOR_DEVICE_CLASS[pollutant]
        self._attr_native_unit_of_measurement = POLLUTANT_TO_UNIT[pollutant]
        self._attr_device_info = coordinator.shared_device_info
        self._attr_translation_key = pollutant
        self._pollutant = pollutant

    @abstractmethod
    def _get_pollutant_data(self):
        pass

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Return the timestamp of the data as additional attribute."""
        return {"timestamp": self._get_pollutant_data().get("timestamp")}

    @property
    def native_value(self) -> float | None:
        """Get value of the sensor."""
        return self._get_pollutant_data().get("value")


class IrcelinePollutantRio(IrcelinePollutantSensor):
    """Representation of a pollutant sensor with value extracted from the RIO interpolation of IRCELINE."""

    def __init__(
        self, coordinator: IrcelineCoordinator, entry: ConfigEntry, pollutant: str
    ) -> None:
        """Set up the sensor."""
        super().__init__(coordinator, pollutant)
        self._attr_unique_id = f"{entry.entry_id}-{pollutant}"
        self.entity_id = sensor.ENTITY_ID_FORMAT.format(
            f"{str(entry.title).lower()}_{pollutant}"
        )

    def _get_pollutant_data(self) -> dict:
        return self.coordinator.data.get("rio", {}).get(
            POLLUTANT_TO_FEATURE[self._pollutant], {}
        )


class IrcelinePollutantForecast(IrcelinePollutantSensor):
    """Representation of a pollutant sensor with value extracted from the daily forecast of IRCELINE."""

    _attr_has_entity_name = True
    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: IrcelineCoordinator,
        entry: ConfigEntry,
        pollutant: str,
        time_delta: timedelta,
    ) -> None:
        """Set up the sensor."""
        super().__init__(coordinator, pollutant)
        self._attr_unique_id = f"{entry.entry_id}-{pollutant}_d{time_delta.days}"
        self.entity_id = sensor.ENTITY_ID_FORMAT.format(
            f"{str(entry.title).lower()}_{pollutant}_d{time_delta.days}"
        )
        self._time_delta = time_delta

    def _get_pollutant_data(self) -> dict:
        day = date.today() + self._time_delta
        return self.coordinator.data.get("forecast", {}).get(
            (POLLUTANT_TO_FEATURE[self._pollutant], day), {}
        )
